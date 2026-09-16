# Biz-A Query Join Depth Problem

Use this reference when a Biz-A `queryData` call fails with `token unknown`, especially when a form/list collects rows through a long relation path such as BO Maintain collecting BO Sourcing rows by `doc_no` or customer.

## Problem Signal

- Error contains `token unknown` while running a `queryData` collect/search.
- `columns[].data` or `filter[].column` contains a deep path across more than 3 related tables.
- A query path tries to walk through BO Sourcing -> BO Sourcing Detail -> Workshop Sales Detail -> Workshop Sales -> SPR -> JOA Sub Job -> JOA.
- A fix introduces a query against a table that is planned but not actually created yet.

## Root Cause

Biz-A query path strings only support short joins reliably. Deep relation paths can break the SQL builder and surface as `token unknown`.

Another common mistake is replacing the deep join with a query to a table that does not exist yet. This may pass code review visually, but it fails at runtime because the schema is not deployed.

## Corrected Approach

- Keep every `columns[].data` and `filter[].column` path short, preferably at most 3 table hops.
- Split a complex collect into multiple short queries.
- Merge/hydrate the rows in JavaScript after each query returns.
- For far-table filters, filter the near foreign key with a subquery instead of putting the entire relation chain in `filter[].column`.
- Only query tables that already exist in the deployed schema.
- If a denormalized field exists on a nearer table, use it. Example: if `workshop_sales.job_number` exists, load `job_number` from `workshop_sales`, not through `spr` or `joa_sub_job`.

## BO Maintain Pattern

For BO Maintain collect rows:

1. Query `bo_sourcing` and `bo_sourcing_detail` only for base fields.
2. Hydrate `workshop_sales_detail` by `source_ws_detail_id`.
3. Load `doc_no`, `doc_date`, `warehouse_id`, and `job_number` through `workshop_sales_detail.workshop_sales_id.id.workshop_sales`.
4. Hydrate SPR/JOA data only for fields that still require it, such as customer, serial number, and model.
5. Merge rows by stable ids such as `source_ws_detail_id` and `spr_id`.

Short example:

```javascript
const sourceWsDetailIds = baseRows.map((row) => row.source_ws_detail_id);
return this.f().getBoMaintainWorkshopRowsByDetailIds(sourceWsDetailIds).pipe(
    this.switchMap((workshopRows) => {
        const sprIds = workshopRows.map((row) => row.spr_id);
        return this.f().getBoMaintainSprRowsByIds(sprIds).pipe(
            this.map((sprRows) => this.f().mergeBoMaintainCollectRows(baseRows, workshopRows, sprRows))
        );
    })
);
```

## What To Avoid

Do not put this kind of full chain in `columns[].data` or `filter[].column`:

```javascript
bo_sourcing.id.bo_sourcing_id.bo_sourcing_detail.source_ws_detail_id.id.workshop_sales_detail.workshop_sales_id.id.workshop_sales.spr_id.id.spr.joa_sub_job_id.id.joa_sub_job.joa_id.id.joa.customer_name
```

Do not query a non-existing planned table to calculate display values:

```javascript
part_purchase_order_detail.source_ws_detail_id
```

If the table does not exist yet, keep the display value defaulted or derive it from existing rows only.

