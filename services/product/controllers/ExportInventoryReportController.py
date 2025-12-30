from fastapi.responses import StreamingResponse
from queries.ExportInventoryReportQuery import ExportInventoryReportQuery
from shared_config.custom_exception import BadRequestException
import io
import pandas as pd


class ExportInventoryReportController:
    def __init__(self):
        self.query = ExportInventoryReportQuery()

    def execute(self, min_stock: int, max_stock: int, user_info: dict):
        role_name = user_info.get("role_name", "").lower().strip()
        if role_name not in ["admin", "manager"]:
            raise BadRequestException("Only admin and manager can export inventory reports")

        if min_stock >= max_stock:
            raise BadRequestException("Min stock must be less than Max stock")

        if min_stock < 0 or max_stock < 0:
            raise BadRequestException("Stock values must be non-negative")

        result = self.query.execute(min_stock, max_stock)
        self.query.close()

        # Process data to add type column
        data = []
        for item in result:
            stock_qty = item["stock_quantity"]
            if stock_qty < min_stock:
                item_type = "Low Stock"
            else:  # stock_qty > max_stock
                item_type = "Overstock"
            
            data.append({
                "Product Name": item["product_name"],
                "Unit": item["unit"] if item["unit"] else "N/A",
                "Stock Quantity": stock_qty,
                "Type": item_type
            })

        df = pd.DataFrame(data)

        # Save to buffer
        buf = io.StringIO()
        df.to_csv(buf, index=False)
        buf.seek(0)

        return StreamingResponse(
            iter([buf.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=inventory_report_min{min_stock}_max{max_stock}.csv"}
        )
