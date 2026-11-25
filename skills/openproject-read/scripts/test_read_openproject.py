"""Offline behavior checks; synthetic credentials and responses only."""
import io
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

import read_openproject as op


class ReaderTests(unittest.TestCase):
    def test_literal_env_quotes_comments_and_no_execution(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / ".env"
            path.write_text("\ufeffexport OPENPROJECT_API_TOKEN='a#b' # note\nOTHER=$(example) # note\n", encoding="utf-8")
            self.assertEqual(op.read_env(path), {"OPENPROJECT_API_TOKEN": "a#b", "OTHER": "$(example)"})

    def test_auth_is_get_with_basic_apikey(self):
        client = op.Client("https://op.example", "test-secret")
        with patch.object(client.opener, "open") as opened:
            opened.return_value.__enter__.return_value.read.return_value = b'{"id":14}'
            self.assertEqual(client.fetch("/api/v3/users/me")["id"], 14)
            req = opened.call_args.args[0]
            self.assertEqual(req.get_method(), "GET")
            self.assertEqual(req.get_header("Authorization"), "Basic YXBpa2V5OnRlc3Qtc2VjcmV0")

    def test_external_origins_rejected_before_request(self):
        client = op.Client("https://op.example", "test-secret")
        with patch.object(client.opener, "open") as opened:
            for href in ("https://other.example/file", "//other.example/file", "http://op.example/file", "https://op.example:444/file"):
                with self.subTest(href=href), self.assertRaises(op.ReadError):
                    client.fetch(href)
            opened.assert_not_called()

    def test_redirect_never_carries_auth(self):
        with self.assertRaises(op.ReadError):
            op.NoRedirect().redirect_request(None, None, 302, "Found", {}, "https://other.example")

    def test_http_error_hides_response_and_credentials(self):
        client = op.Client("https://op.example", "test-secret")
        error = HTTPError("https://op.example/?secret=test-secret", 401, "test-secret", {}, None)
        with patch.object(client.opener, "open", side_effect=error):
            with self.assertRaises(op.ReadError) as caught:
                client.fetch("/api/v3/users/me")
            self.assertIn("401", str(caught.exception))
            self.assertNotIn("test-secret", str(caught.exception))

    def test_pagination_follows_hal_next_link(self):
        client = op.Client("https://op.example", "test-secret")
        pages = [
            {"total": 2, "_embedded": {"elements": [{"id": 1}]}, "_links": {"nextByOffset": {"href": "/api/v3/projects?offset=2&pageSize=1"}}},
            {"total": 2, "_embedded": {"elements": [{"id": 2}]}},
        ]
        with patch.object(client, "fetch", side_effect=pages) as fetch:
            self.assertEqual(client.collection("/api/v3/projects"), [{"id": 1}, {"id": 2}])
            self.assertEqual(fetch.call_args.args, ("/api/v3/projects?offset=2&pageSize=1", {}))

    def test_incomplete_collection_is_error(self):
        client = op.Client("https://op.example", "test-secret")
        with patch.object(client, "fetch", return_value={"total": 2, "_embedded": {"elements": []}}):
            with self.assertRaises(op.ReadError):
                client.collection("/api/v3/projects")

    def test_task_filters_use_current_user_and_resolved_status(self):
        client = op.Client("https://op.example", "test-secret")
        args = SimpleNamespace(project="Endo Medica", assignee="me", status="In progress")
        with patch.object(client, "fetch", return_value={"id": 14}), patch.object(client, "collection") as collection:
            collection.side_effect = [[{"id": 31, "name": "Endo Medica"}], [{"id": 7, "name": "In progress"}], []]
            self.assertEqual(op.tasks(client, args)["count"], 0)
            filters = json.loads(collection.call_args.args[1]["filters"])
            self.assertIn({"project": {"operator": "=", "values": ["31"]}}, filters)
            self.assertIn({"status": {"operator": "=", "values": ["7"]}}, filters)
            self.assertIn({"assignee": {"operator": "=", "values": ["14"]}}, filters)

    def test_output_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "result.json"
            op.write_new(path, "original")
            with self.assertRaises(FileExistsError):
                op.write_new(path, "replacement")
            self.assertEqual(path.read_text(), "original")

    def test_stdout_redacts_token_and_auth(self):
        args = SimpleNamespace(env_file=Path("missing.env"), output=None)
        auth = op.Client("https://op.example", "test-secret").authorization
        with patch.object(op, "parser") as parser, patch.dict(op.os.environ, {"OPENPROJECT_API_TOKEN": "test-secret"}), patch.object(op, "run", return_value={"echo": "test-secret " + auth}), patch("sys.stdout", new_callable=io.StringIO) as output:
            parser.return_value.parse_args.return_value = args
            self.assertEqual(op.main(), 0)
            self.assertNotIn("test-secret", output.getvalue())
            self.assertNotIn(auth, output.getvalue())


if __name__ == "__main__":
    unittest.main()
