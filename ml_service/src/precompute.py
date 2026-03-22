import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json
import os
import warnings
warnings.filterwarnings('ignore')

CLEAN_PATH = os.path.join(os.path.dirname(__file__), "../data/processed/clean_ratings.csv")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "../models/")

def load_data():
    print("📂 Loading dataset...")
    df = pd.read_csv(CLEAN_PATH)
    print(f"✅ Loaded: {len(df):,} ratings")
    return df

def precompute_popularity(df):
    print("\n📊 Pre-computing Popularity Scores...")
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

    min_s = stats['score'].min()
    max_s = stats['score'].max()
    stats['normalized_score'] = (stats['score'] - min_s) / (max_s - min_s)

    top_100 = stats.sort_values('score', ascending=False).head(100)
    result  = top_100[['product_id','avg_rating','rating_count',
                        'score','normalized_score']].to_dict('records')

    with open(OUTPUT_DIR + "popularity_scores.json", 'w') as f:
        json.dump(result, f)

    print(f"✅ Saved top 100 popular products")
    return stats

def precompute_cf_fast(df, pop_stats):
    print("\n🤝 Pre-computing CF Scores (Fast Mode)...")

    # ── Key optimization: only use top 500 products ──
    top_products = pop_stats.sort_values(
        'score', ascending=False
    ).head(500)['product_id'].tolist()

    # Only top 200 active users
    top_users = df['user_id'].value_counts().head(200).index.tolist()

    # Filter to only top products and users
    df_sample = df[
        df['user_id'].isin(top_users) &
        df['product_id'].isin(top_products)
    ]

    print(f"  Filtered dataset: {len(df_sample):,} ratings")

    matrix = df_sample.pivot_table(
        index='user_id',
        columns='product_id',
        values='rating',
        fill_value=0
    )

    print(f"  Matrix shape: {matrix.shape} ← much smaller!")

    # Compute item similarity — now fast!
    print("  Computing item similarity...")
    item_similarity = cosine_similarity(matrix.T)
    item_sim_df = pd.DataFrame(
        item_similarity,
        index=matrix.columns,
        columns=matrix.columns
    )
    print("  ✅ Similarity computed!")

    # Pre-compute for top 100 users
    cf_results = {}
    users_to_process = [u for u in top_users if u in matrix.index]

    print(f"  Computing CF for {len(users_to_process)} users...")
    for i, user_id in enumerate(users_to_process):
        user_ratings     = matrix.loc[user_id]
        liked_products   = user_ratings[user_ratings >= 4].index.tolist()
        unrated_products = user_ratings[user_ratings == 0].index

        if not liked_products:
            continue

        scores = {}
        for product in unrated_products:
            sim_scores = [
                item_sim_df.loc[liked, product]
                for liked in liked_products
                if liked in item_sim_df.index
            ]
            if sim_scores:
                scores[product] = float(np.mean(sim_scores))

        if scores:
            min_s = min(scores.values())
            max_s = max(scores.values())
            if max_s > min_s:
                scores = {
                    p: (s - min_s) / (max_s - min_s)
                    for p, s in scores.items()
                }

        top_10 = sorted(
            scores.items(), key=lambda x: x[1], reverse=True
        )[:10]

        cf_results[user_id] = [
            {"product_id": p, "cf_score": round(s, 4)}
            for p, s in top_10
        ]

        if (i + 1) % 20 == 0:
            print(f"  Processed {i+1}/{len(users_to_process)} users...")

    with open(OUTPUT_DIR + "cf_scores.json", 'w') as f:
        json.dump(cf_results, f)

    print(f"✅ Saved CF scores for {len(cf_results)} users")
    return cf_results

def precompute_hybrid(pop_stats, cf_results):
    print("\n🔀 Pre-computing Hybrid Scores...")

    pop_dict      = pop_stats.set_index('product_id')['normalized_score'].to_dict()
    hybrid_results = {}

    for user_id, cf_recs in cf_results.items():
        hybrid = []
        for rec in cf_recs:
            pid          = rec['product_id']
            cf_s         = rec['cf_score']
            pop_s        = pop_dict.get(pid, 0)
            hybrid_score = (0.4 * pop_s) + (0.6 * cf_s)
            hybrid.append({
                "product_id"       : pid,
                "hybrid_score"     : round(hybrid_score, 4),
                "popularity_score" : round(pop_s, 4),
                "cf_score"         : round(cf_s, 4)
            })

        hybrid.sort(key=lambda x: x['hybrid_score'], reverse=True)
        hybrid_results[user_id] = hybrid[:10]

    with open(OUTPUT_DIR + "hybrid_scores.json", 'w') as f:
        json.dump(hybrid_results, f)

    print(f"✅ Saved Hybrid scores for {len(hybrid_results)} users")

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df        = load_data()
    pop_stats = precompute_popularity(df)
    cf_results = precompute_cf_fast(df, pop_stats)
    precompute_hybrid(pop_stats, cf_results)

    print("\n🎉 Pre-computation complete! All scores saved.")
    print("⚡ API responses will now be instant!")