# How to run the "Top 5 Unused Capacity per Month" query

Your colleague can run this **Power Query** on their copy of `testData.xlsx` to get the same top-5-unused-capacity-per-month result.

## One-time setup in their file

1. **Open** their copy of `testData.xlsx` in Excel.
2. **Turn the data into a table** (if it isn’t already):
   - Click any cell in the data (e.g. in the `testData` sheet).
   - Press **Ctrl+T** (Windows) or **Cmd+T** (Mac), or use **Insert → Table**.
   - If asked, tick “My table has headers”.
   - In **Table Design**, set **Table name** to **`testData`** (must match the name in the query).

## Run the query

1. **Data** tab → **Get Data** → **From Other Sources** → **Blank Query**.
2. In the Power Query Editor, click **Home** → **Advanced Editor**.
3. **Delete** any code that’s already there.
4. **Open** the file `Top5UnusedCapacityPerMonth.pq` (in Notepad or any editor), **copy** all its contents, and **paste** into the Advanced Editor.
5. Click **Done**.
6. **Home** → **Close & Load** (or **Close & Load To…** and choose where to put the result).

The new sheet/table will show **top 5 unused capacity rows per month** (by Unused FTE, then Unused Headcount), with Entity, Region, Department, Product Line, Period End Date, Unused Headcount, Unused FTE, and Comment.

## If their table has a different name

In the Advanced Editor, change this line:

```pq
Source = Excel.CurrentWorkbook(){[Name = "testData"]}[Content],
```

Replace `"testData"` with their table name (e.g. `"Table1"`).

## Refreshing

To refresh the result after changing the source data: right‑click the result table/sheet → **Refresh**, or use **Data** → **Refresh All**.
