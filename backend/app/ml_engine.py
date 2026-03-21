import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
import warnings
warnings.filterwarnings('ignore')

# ── Path to clean data ─────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
CLEAN_PATH = os.path.join(BASE_DIR, "../../ml_service/data/processed/clean_ratings.csv")

# ── Cache: load data once, reuse every request ─────────
_df         = None
_pop_scores = None

def get_data():
    global _df
    if _df is None:
        print("📂 Loading dataset into memory...")
        _df = pd.read_csv(CLEAN_PATH)
        print(f"✅ Dataset loaded: {len(_df):,} ratings")
    return _df

# ── 1. Popularity-Based ────────────────────────────────
def get_popularity_recommendations(top_n=10):
    df = get_data()

    stats = df.groupby('product_id').agg(
        avg_rating   = ('rating', 'mean'),
        rating_count = ('rating', 'count')
    ).reset_index()

    C = stats['avg_rating'].mean()
    m = stats['rating_count'].quantile(0.70)

    stats['score'] = (
        (stats['rating_count'] / (stats['rating_count'] + m)) * stats['avg_rating'] +
        (m / (stats['rating_count'] + m)) * C
    )

    top = stats.sort_values('score', ascending=False).head(top_n)

    return [
        {
            "rank": i + 1,
            "product_id": row['product_id'],
            "avg_rating": round(row['avg_rating'], 3),
            "rating_count": int(row['rating_count']),
            "score": round(row['score'], 4)
        }
        for i, row in enumerate(top.to_dict('records'))
    ]

# ── 2. Collaborative Filtering ─────────────────────────
def get_cf_recommendations(user_id: str, top_n=10):
    df = get_data()

    # Check if user exists
    if user_id not in df['user_id'].values:
        return {"error": f"User '{user_id}' not found in dataset"}

    # Sample top users + target user
    top_users = df['user_id'].value_counts().head(500).index.tolist()
    if user_id not in top_users:
        top_users.append(user_id)

    df_sample = df[df['user_id'].isin(top_users)]
    matrix = df_sample.pivot_table(
        index='user_id', columns='product_id',
        values='rating', fill_value=0
    )

    if user_id not in matrix.index:
        return {"error": "User not found in matrix"}

    item_similarity  = cosine_similarity(matrix.T)
    item_sim_df      = pd.DataFrame(item_similarity,
                                    index=matrix.columns,
                                    columns=matrix.columns)

    user_ratings     = matrix.loc[user_id]
    liked_products   = user_ratings[user_ratings >= 4].index.tolist()
    unrated_products = user_ratings[user_ratings == 0].index

    if not liked_products:
        return {"error": "User has no highly rated products"}

    scores = {}
    for product in unrated_products:
        sim_scores = [
            item_sim_df.loc[liked, product]
            for liked in liked_products
            if liked in item_sim_df.index
        ]
        if sim_scores:
            scores[product] = float(np.mean(sim_scores))

    top = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]

    return [
        {"rank": i+1, "product_id": p, "cf_score": round(s, 4)}
        for i, (p, s) in enumerate(top)
    ]

# ── 3. Hybrid ──────────────────────────────────────────
def get_hybrid_recommendations(user_id: str, top_n=10,
                                pop_weight=0.4, cf_weight=0.6):
    df = get_data()

    if user_id not in df['user_id'].values:
        return {"error": f"User '{user_id}' not found in dataset"}

    # Popularity scores
    stats = df.groupby('product_id').agg(
        avg_rating   = ('rating', 'mean'),
        rating_count = ('rating', 'count')
    ).reset_index()
    C = stats['avg_rating'].mean()
    m = stats['rating_count'].quantile(0.70)
    stats['pop_score'] = (
        (stats['rating_count'] / (stats['rating_count'] + m)) * stats['avg_rating'] +
        (m / (stats['rating_count'] + m)) * C
    )
    min_s = stats['pop_score'].min()
    max_s = stats['pop_score'].max()
    stats['pop_score'] = (stats['pop_score'] - min_s) / (max_s - min_s)
    pop_scores = stats.set_index('product_id')['pop_score'].to_dict()

    # CF scores
    cf_result = get_cf_recommendations(user_id, top_n=9999)
    if isinstance(cf_result, dict) and "error" in cf_result:
        return cf_result
    cf_scores = {r['product_id']: r['cf_score'] for r in cf_result}

    # Normalize CF scores
    if cf_scores:
        min_c = min(cf_scores.values())
        max_c = max(cf_scores.values())
        if max_c > min_c:
            cf_scores = {p: (s-min_c)/(max_c-min_c) for p, s in cf_scores.items()}

    # Combine
    all_products = set(pop_scores.keys()) | set(cf_scores.keys())
    hybrid = {
        p: (pop_weight * pop_scores.get(p, 0)) + (cf_weight * cf_scores.get(p, 0))
        for p in all_products
    }

    top = sorted(hybrid.items(), key=lambda x: x[1], reverse=True)[:top_n]

    return [
        {
            "rank": i+1,
            "product_id": p,
            "hybrid_score": round(s, 4),
            "popularity_score": round(pop_scores.get(p, 0), 4),
            "cf_score": round(cf_scores.get(p, 0), 4)
        }
        for i, (p, s) in enumerate(top)
    ]