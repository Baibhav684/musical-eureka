import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from app.db import Database
from app.reader import Reader

class Recommender:
    def __init__(self):
        self.db = Database()
        self.reader = Reader()

    def get_recommendations(self, user_id, top_n=5):
        user_item = self.reader.read_sql()

        if user_id not in user_item.index:
            return []

        similarity_matrix = cosine_similarity(user_item)

        similarity_df = pd.DataFrame(
            similarity_matrix,
            index=user_item.index,
            columns=user_item.index
        )

        similar_users = (
            similarity_df[user_id]
            .drop(user_id)
            .sort_values(ascending=False)
        )

        purchased_products = set(
            user_item.loc[user_id][user_item.loc[user_id] > 0].index
        )

        scores = {}

        for similar_user_id, similarity_score in similar_users.items():
            products = user_item.loc[similar_user_id]

            for product_id, quantity in products.items():
                if quantity > 0 and product_id not in purchased_products:
                    scores[product_id] = (
                        scores.get(product_id, 0)
                        + similarity_score * quantity
                    )

        ranked_products = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_n]

        product_ids = [product_id for product_id, score in ranked_products]
 
        if not product_ids:
            return []

        engine = Database().get_engine()
        
        placeholders = ",".join("?" for _ in product_ids)

        query = f"""
        SELECT
            ProductId,
            Name,
            Description,
            Price,
            CategoryId,
            IsAvailable
        FROM Products
        WHERE ProductId IN ({placeholders})
        """

        products_df = pd.read_sql(query,engine,params=tuple(product_ids))

        score_map = dict(ranked_products)

        products_df["RecommendationScore"] = (
            products_df["ProductId"].map(score_map)
        )

        products_df = products_df.sort_values(
            "RecommendationScore",
            ascending=False
        )

        return products_df.to_dict(orient="records")