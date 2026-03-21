import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings('ignore')

CLEAN_PATH  = os.path.join(os.path.dirname(__file__), "../data/processed/clean_ratings.csv")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "../outputs/")

# ── 1. Load Data ───────────────────────────────────────
def load_data(filepath=CLEAN_PATH):
    df = pd.read_csv(filepath)
    print(f"✅ Loaded: {len(df):,} ratings")
    return df

# ── 2. Popularity Score ────────────────────────────────
def get_popularity_scores(df):
    """Compute weighted popularity score for all products"""
    print("\n📊 Computing Popularity Scores...")

    stats = df.groupby('product_id').agg(
        avg_rating   = ('rating', 'mean'),
        rating_count = ('rating', 'count')
    ).reset_index()

    C = stats['avg_rating'].mean()
    m = stats['rating_count'].quantile(0.70)

    stats['popularity_score'] = (
        (stats['rating_count'] / (stats['rating_count'] + m)) * stats['avg_rating'] +
        (m / (stats['rating_count'] + m)) * C
    )

    # Normalize to 0-1 range
    min_s = stats['popularity_score'].min()
    max_s = stats['popularity_score'].max()
    stats['popularity_score'] = (stats['popularity_score'] - min_s) / (max_s - min_s)

    print(f"  Popularity scores computed for {len(stats):,} products")
    return stats.set_index('product_id')['popularity_score'].to_dict()

# ── 3. CF Score (Item-Based) ───────────────────────────
def get_cf_scores(df, target_user, sample_users=500):
    """Compute item-based CF scores for a specific user"""
    print(f"\n🤝 Computing CF Scores for user...")

    # Sample top active users + make sure target user is included
    top_users = df['user_id'].value_counts().head(sample_users).index.tolist()
    if target_user not in top_users:
        top_users.append(target_user)

    df_sample = df[df['user_id'].isin(top_users)]

    # Create user-item matrix
    matrix = df_sample.pivot_table(
        index='user_id',
        columns='product_id',
        values='rating',
        fill_value=0
    )

    if target_user not in matrix.index:
        print("  ⚠️ Target user not found in matrix")
        return {}

    # Item similarity
    item_similarity = cosine_similarity(matrix.T)
    item_sim_df = pd.DataFrame(
        item_similarity,
        index=matrix.columns,
        columns=matrix.columns
    )

    # Get products user liked
    user_ratings    = matrix.loc[target_user]
    liked_products  = user_ratings[user_ratings >= 4].index.tolist()
    unrated_products = user_ratings[user_ratings == 0].index

    if not liked_products:
        print("  ⚠️ No highly rated products found for this user")
        return {}

    # Score unrated products
    cf_scores = {}
    for product in unrated_products:
        sim_scores = [
            item_sim_df.loc[liked, product]
            for liked in liked_products
            if liked in item_sim_df.index
        ]
        if sim_scores:
            cf_scores[product] = np.mean(sim_scores)

    # Normalize to 0-1
    if cf_scores:
        min_s = min(cf_scores.values())
        max_s = max(cf_scores.values())
        if max_s > min_s:
            cf_scores = {
                p: (s - min_s) / (max_s - min_s)
                for p, s in cf_scores.items()
            }

    print(f"  CF scores computed for {len(cf_scores):,} products")
    return cf_scores

# ── 4. Hybrid Combination ──────────────────────────────
def hybrid_recommend(popularity_scores, cf_scores,
                     pop_weight=0.4, cf_weight=0.6, top_n=10):
    """
    Combine popularity and CF scores with weights
    Final Score = 0.4 × popularity + 0.6 × CF
    """
    print(f"\n🔀 Combining Scores...")
    print(f"  Popularity weight : {pop_weight*100:.0f}%")
    print(f"  CF weight         : {cf_weight*100:.0f}%")

    all_products = set(popularity_scores.keys()) | set(cf_scores.keys())

    hybrid_scores = {}
    for product in all_products:
        pop = popularity_scores.get(product, 0)
        cf  = cf_scores.get(product, 0)
        hybrid_scores[product] = (pop_weight * pop) + (cf_weight * cf)

    # Sort and get top N
    top_products = sorted(
        hybrid_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_n]

    result_df = pd.DataFrame(top_products, columns=['product_id', 'hybrid_score'])
    result_df.index += 1

    # Add individual scores for transparency
    result_df['popularity_score'] = result_df['product_id'].map(
        lambda x: round(popularity_scores.get(x, 0), 4)
    )
    result_df['cf_score'] = result_df['product_id'].map(
        lambda x: round(cf_scores.get(x, 0), 4)
    )

    print(f"\n🏆 Top {top_n} Hybrid Recommendations:")
    print(result_df.to_string())
    return result_df

# ── 5. Visualize ───────────────────────────────────────
def plot_hybrid(result_df, top_n=10):
    fig, ax = plt.subplots(figsize=(10, 6))

    x = range(len(result_df))
    width = 0.3

    ax.bar([i - width for i in x], result_df['popularity_score'],
           width, label='Popularity (40%)', color='steelblue')
    ax.bar(x, result_df['cf_score'],
           width, label='CF Score (60%)', color='coral')
    ax.bar([i + width for i in x], result_df['hybrid_score'],
           width, label='Hybrid Score', color='green')

    ax.set_xticks(list(x))
    ax.set_xticklabels(result_df['product_id'].str[-8:], rotation=45)
    ax.set_title('Hybrid Recommendation Scores', fontweight='bold')
    ax.set_ylabel('Score')
    ax.legend()
    plt.tight_layout()

    chart_path = OUTPUT_PATH + "hybrid_recommendations.png"
    plt.savefig(chart_path, dpi=150)
    print(f"\n📊 Chart saved → {chart_path}")
    plt.show()

# ── 6. Save Results ────────────────────────────────────
def save_results(result_df):
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    path = OUTPUT_PATH + "hybrid_recommendations.csv"
    result_df.to_csv(path, index=False)
    print(f"💾 Results saved → {path}")

# ── Pipeline ───────────────────────────────────────────
if __name__ == "__main__":
    df = load_data()

    # Pick a target user from the dataset
    target_user = df['user_id'].value_counts().index[0]
    print(f"\n🎯 Target User: {target_user}")

    # Get scores from both models
    popularity_scores = get_popularity_scores(df)
    cf_scores         = get_cf_scores(df, target_user, sample_users=500)

    # Combine into hybrid
    result_df = hybrid_recommend(
        popularity_scores,
        cf_scores,
        pop_weight=0.4,
        cf_weight=0.6,
        top_n=10
    )

    plot_hybrid(result_df)
    save_results(result_df)

    print("\n🎉 Hybrid Recommendation System complete!")