// Power Query (M) - Top 5 Unused Capacity per Month
// Source: table in this workbook named "testData" (change name below if your table has another name)
// Result: one table with top 5 rows by Unused FTE (then Unused Headcount) for each Fiscal Year + Period

let
    // 1) Get data from the table named "testData" in the current workbook
    Source = Excel.CurrentWorkbook(){[Name = "testData"]}[Content],

    // 2) Keep only Capacity scenario rows
    FilterCapacity = Table.SelectRows(Source, each [Scenario] = "Capacity"),

    // 3) Sort by month then by Unused FTE (desc), then Unused Headcount (desc)
    Sorted = Table.Sort(FilterCapacity, {
        {"Fiscal Year", Order.Ascending},
        {"Period", Order.Ascending},
        {"Unused FTE", Order.Descending},
        {"Unused Headcount", Order.Descending}
    }),

    // 4) Group by Fiscal Year + Period, take first 5 rows in each group
    Grouped = Table.Group(Sorted, {"Fiscal Year", "Period"}, {
        {"Top5", each Table.FirstN(_, 5), type table}
    }, GroupKind.Local),

    // 5) Expand the Top5 table back into rows (include all columns you need in the report)
    Expanded = Table.ExpandTableColumn(Grouped, "Top5", {
        "Entity",
        "Region",
        "Department",
        "Product Line",
        "Account Type",
        "Scenario",
        "Period End Date",
        "Unused Headcount",
        "Unused FTE",
        "Comment"
    }, {
        "Entity",
        "Region",
        "Department",
        "Product Line",
        "Account Type",
        "Scenario",
        "Period End Date",
        "Unused Headcount",
        "Unused FTE",
        "Comment"
    })
in
    Expanded
