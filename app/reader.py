import pandas as pd
from app.db import Database

class Reader:
    def __init__(self):
        self.db = Database()
        self.engine = self.db.get_engine()

    def read_sql(self):
        # Read the SQL query from the file
        

        query = """SELECT TOP 10
                    o.UserId,
                    u.Username,
                    o.ProductId,
                    p.Name AS Product,
                    c.Name AS Category,
                    o.Quantity,
                    o.TotalPrice,
                    o.OrderDate
                FROM Orders o
                JOIN Users u ON o.UserId = u.Id
                JOIN Products p ON o.ProductId = p.ProductId
                JOIN Categories c ON p.CategoryId = c.CategoryId
                ORDER BY o.OrderDate;
                """

        df = pd.read_sql(query, self.engine)

        user_item = df.pivot_table(
            index="UserId",
            columns="ProductId",
            values="Quantity",
            aggfunc="sum",
            fill_value=0
        )

        return user_item