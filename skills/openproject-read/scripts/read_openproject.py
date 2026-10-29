"""Read OpenProject using a local token, without third-party dependencies."""
import argparse
import base64
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urljoin, urlsplit, urlunsplit
from urllib.request import build_opener, HTTPRedirectHandler, Request

DEFAULT_URL = "https://iproj.my.id:5443"


class ReadError(Exception):
    pass


def repo_root():
    for parent in Path(__file__).resolve().parents:
        if (parent / ".agents/instructions/project.md").is_file():
            return parent
    raise ReadError("Root repository tidak ditemukan; gunakan skill dari repository proyek.")


def read_env(path):
    """Parse literal single-line dotenv values; never execute or interpolate."""
    if not path.is_file():
        return {}
    result = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        match = re.match(r"\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)", line)
        if not match:
            continue
        key, value = match.groups()
        value = value.strip()
        if value.startswith(("'", '"')):
            end = value.find(value[0], 1)
            if end < 0:
                raise ReadError("Nilai .env harus satu baris dengan quote berpasangan.")
            value = value[1:end]
        else:
            value = re.split(r"\s+#", value, maxsplit=1)[0].rstrip()
        result[key] = value
    return result


def origin(url):
    parsed = urlsplit(url)
    return parsed.scheme.lower(), parsed.hostname, parsed.port or 443


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ReadError("Redirect ditolak; token OP tidak diteruskan. Periksa URL server/download.")


class Client:
    def __init__(self, base_url, token):
        parsed = urlsplit(base_url)
        if (parsed.scheme != "https" or not parsed.hostname or parsed.username
                or parsed.password or parsed.query or parsed.fragment
                or parsed.path not in ("", "/")):
            raise ReadError("OPENPROJECT_URL harus origin HTTPS tanpa kredensial/path/query.")
        self.base_url = base_url.rstrip("/")
        self.authorization = "Basic " + base64.b64encode(f"apikey:{token}".encode()).decode()
        self.opener = build_opener(NoRedirect())

    def url(self, href):
        target = urljoin(self.base_url + "/", href)
        parsed = urlsplit(target)
        if (origin(target) != origin(self.base_url) or parsed.username
                or parsed.password or parsed.fragment):
            raise ReadError("Tautan di luar origin OpenProject ditolak.")
        return target

    def fetch(self, href, params=None, binary=False):
        target = self.url(href)
        if params:
            parts = urlsplit(target)
            query = parts.query + ("&" if parts.query else "") + urlencode(params)
            target = urlunsplit(parts._replace(query=query))
        req = Request(target, method="GET", headers={
            "Authorization": self.authorization,
            "Accept": "*/*" if binary else "application/hal+json",
        })
        try:
            with self.opener.open(req, timeout=45) as response:
                content = response.read()
        except HTTPError as error:
            hints = {401: "Token tidak diterima.", 403: "Akses ditolak.", 404: "Resource tidak ditemukan."}
            raise ReadError(f"OpenProject HTTP {error.code}. " + hints.get(error.code, "Permintaan gagal.")) from None
        except (URLError, TimeoutError, OSError):
            raise ReadError("Koneksi OpenProject gagal. Periksa jaringan, sandbox, URL, dan sertifikat TLS.") from None
        if binary:
            return content
        try:
            data = json.loads(content)
        except (ValueError, UnicodeError):
            raise ReadError("Respons OpenProject bukan JSON valid.") from None
        if not isinstance(data, dict) or data.get("_type") == "Error":
            raise ReadError("Respons API tidak valid atau berisi error.")
        return data

    def collection(self, href, params=None):
        params = {**(params or {}), "pageSize": 100, "offset": 1}
        rows, seen = [], set()
        while True:
            marker = json.dumps([href, params], sort_keys=True)
            if marker in seen:
                raise ReadError("Pagination OpenProject berulang; hasil tidak lengkap.")
            seen.add(marker)
            page = self.fetch(href, params)
            elements = page.get("_embedded", {}).get("elements")
            if not isinstance(elements, list):
                raise ReadError("Respons bukan collection OpenProject.")
            rows.extend(elements)
            next_href = page.get("_links", {}).get("nextByOffset", {}).get("href")
            if next_href:
                href, params = next_href, {}
                continue
            total = page.get("total")
            if total is None or len(rows) >= total:
                return rows
            if not elements:
                raise ReadError("Pagination berhenti sebelum seluruh hasil diambil.")
            # offset is a page number, not the number of skipped rows.
            parts = urlsplit(href)
            query = parse_qs(parts.query)
            current = int(params.get("offset", query.get("offset", [1])[0]))
            query.update({key: [str(value)] for key, value in params.items()})
            query["offset"] = [str(current + 1)]
            query.setdefault("pageSize", ["100"])
            href = urlunsplit(parts._replace(query=urlencode(query, doseq=True)))
            params = {}


def summary(row):
    return {key: row[key] for key in ("id", "name", "identifier", "isClosed", "isDefault", "active") if key in row}


def task_summary(row, base_url):
    result = {key: row.get(key) for key in ("id", "subject", "percentageDone", "startDate", "dueDate", "updatedAt", "estimatedTime")}
    for key in ("project", "status", "assignee", "type", "priority"):
        result[key] = row.get("_links", {}).get(key)
    result["url"] = f"{base_url}/work_packages/{row['id']}"
    return result


def resolve_id(rows, value, label):
    matches = [row for row in rows if str(row.get("id")) == value
               or str(row.get("name", "")).casefold() == value.casefold()
               or str(row.get("identifier", "")).casefold() == value.casefold()]
    if len(matches) != 1:
        raise ReadError(f"{label} tidak ditemukan atau ambigu; gunakan discovery dan ID.")
    return str(matches[0]["id"])


def tasks(client, args):
    filters = []
    if args.project:
        project_id = resolve_id(client.collection("/api/v3/projects"), args.project, "Proyek")
        filters.append({"project": {"operator": "=", "values": [project_id]}})
    if args.assignee != "all":
        assignee = args.assignee
        if assignee == "me":
            assignee = str(client.fetch("/api/v3/users/me")["id"])
        if not assignee.isdecimal():
            raise ReadError("--assignee harus me, all, atau ID user.")
        filters.append({"assignee": {"operator": "=", "values": [assignee]}})
    if args.status in ("open", "all"):
        filters.append({"status": {"operator": "o" if args.status == "open" else "*", "values": []}})
    else:
        status_id = resolve_id(client.collection("/api/v3/statuses"), args.status, "Status")
        filters.append({"status": {"operator": "=", "values": [status_id]}})
    rows = client.collection("/api/v3/work_packages", {
        "filters": json.dumps(filters), "sortBy": json.dumps([["id", "asc"]]),
    })
    return {"count": len(rows), "tasks": [task_summary(row, client.base_url) for row in rows]}


def positive_id(value):
    if not value.isdecimal() or int(value) <= 0:
        raise argparse.ArgumentTypeError("ID harus integer positif.")
    return int(value)


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--env-file", type=Path, default=repo_root() / ".env")
    result.add_argument("--output", type=Path, help="Simpan JSON ke file baru.")
    commands = result.add_subparsers(dest="command", required=True)
    commands.add_parser("me")
    projects = commands.add_parser("projects")
    projects.add_argument("--search", default="")
    commands.add_parser("statuses")
    listing = commands.add_parser("tasks")
    listing.add_argument("--project")
    listing.add_argument("--assignee", default="me")
    listing.add_argument("--status", default="open")
    detail = commands.add_parser("task")
    detail.add_argument("id", type=positive_id)
    attachment = commands.add_parser("attachment")
    attachment.add_argument("id", type=positive_id)
    attachment.add_argument("--output", dest="download_output", type=Path, required=True)
    return result


def write_new(path, content, binary=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb" if binary else "x", **({} if binary else {"encoding": "utf-8"})) as handle:
        handle.write(content)


def run(client, args):
    if args.command == "me":
        row = client.fetch("/api/v3/users/me")
        return {"id": row["id"], "name": row.get("name")}
    if args.command in ("projects", "statuses"):
        rows = client.collection(f"/api/v3/{args.command}")
        if args.command == "projects":
            rows = [row for row in rows if args.search.casefold() in row.get("name", "").casefold()]
        return {args.command: [summary(row) for row in rows]}
    if args.command == "tasks":
        return tasks(client, args)
    if args.command == "task":
        prefix = f"/api/v3/work_packages/{args.id}"
        return {
            "task": client.fetch(prefix), "url": f"{client.base_url}/work_packages/{args.id}",
            "activities": client.collection(prefix + "/activities"),
            "attachments": client.collection(prefix + "/attachments"),
        }
    row = client.fetch(f"/api/v3/attachments/{args.id}")
    href = row.get("_links", {}).get("downloadLocation", {}).get("href")
    if not href:
        raise ReadError("Lampiran tidak memiliki downloadLocation.")
    content = client.fetch(href, binary=True)
    write_new(args.download_output, content, binary=True)
    return {"attachmentId": args.id, "savedTo": str(args.download_output), "bytes": len(content)}


def main():
    args = parser().parse_args()
    try:
        env = read_env(args.env_file)
        token = os.environ.get("OPENPROJECT_API_TOKEN") or env.get("OPENPROJECT_API_TOKEN")
        if not token or "\r" in token or "\n" in token:
            raise ReadError("OPENPROJECT_API_TOKEN belum tersedia atau tidak valid di .env/environment.")
        base_url = os.environ.get("OPENPROJECT_URL") or env.get("OPENPROJECT_URL") or DEFAULT_URL
        client = Client(base_url, token)
        result = {"fetchedAt": datetime.now(timezone.utc).isoformat(), **run(client, args)}
        output = json.dumps(result, ensure_ascii=False, indent=2)
        output = output.replace(token, "[REDACTED]").replace(client.authorization, "[REDACTED]") + "\n"
        if args.output:
            write_new(args.output, output)
        else:
            sys.stdout.write(output)
        return 0
    except ReadError as error:
        print(f"Error: {error}", file=sys.stderr)
    except (OSError, ValueError, KeyError, TypeError):
        print("Error: Konfigurasi, respons, atau file output tidak valid/tidak dapat diakses; file tidak ditimpa.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
