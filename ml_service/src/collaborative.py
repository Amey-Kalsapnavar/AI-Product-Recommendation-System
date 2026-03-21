import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
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

# ── 2. Create User-Item Matrix ─────────────────────────
def create_user_item_matrix(df, sample_users=500):
    """
    Creates a matrix: rows=users, columns=products, values=ratings
    We sample users to keep it manageable in memory
    """
    print(f"\n📐 Creating User-Item Matrix...")

    # Take top users by rating count (most active users)
    top_users = df['user_id'].value_counts().head(sample_users).index
    df_sample = df[df['user_id'].isin(top_users)]

    matrix = df_sample.pivot_table(
        index='user_id',
        columns='product_id',
        values='rating',
        fill_value=0
    )

    print(f"  Matrix shape     : {matrix.shape[0]} users × {matrix.shape[1]} products")
    return matrix, df_sample

# ── 3. User-Based Collaborative Filtering ─────────────
def user_based_cf(matrix, target_user_index=0, top_n=10):
    """
    Find similar users to target user, then recommend
    products those similar users liked
    """
    print(f"\n👥 USER-BASED COLLABORATIVE FILTERING")
    print("="*45)

    # Calculate cosine similarity between ALL users
    user_similarity = cosine_similarity(matrix)
    user_sim_df = pd.DataFrame(
        user_similarity,
        index=matrix.index,
        columns=matrix.index
    )

    # Pick target user
    target_user = matrix.index[target_user_index]
    print(f"  Target User      : {target_user}")

    # Get top 5 most similar users (excluding self)
    similar_users = user_sim_df[target_user].sort_values(ascending=False)[1:6]
    print(f"\n  Top 5 Similar Users:")
    for user, score in similar_users.items():
        print(f"    {user[:20]}... → similarity: {score:.4f}")

    # Find products target user has NOT rated
    target_ratings   = matrix.loc[target_user]
    unrated_products = target_ratings[target_ratings == 0].index

    # Score unrated products based on similar users' ratings
    scores = {}
    for product in unrated_products:
        weighted_sum = 0
        similarity_sum = 0
        for user, sim_score in similar_users.items():
            rating = matrix.loc[user, product]
            if rating > 0:
                weighted_sum   += sim_score * rating
                similarity_sum += sim_score
        if similarity_sum > 0:
            scores[product] = weighted_sum / similarity_sum

    # Get top N recommendations
    recommendations = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    rec_df = pd.DataFrame(recommendations, columns=['product_id', 'predicted_rating'])
    rec_df.index += 1

    print(f"\n🏆 Top {top_n} Recommended Products for this User:")
    print(rec_df.to_string())
    return rec_df

# ── 4. Item-Based Collaborative Filtering ─────────────
def item_based_cf(matrix, target_user_index=0, top_n=10):
    """
    Find products similar to what the user already liked,
    then recommend those similar products
    """
    print(f"\n📦 ITEM-BASED COLLABORATIVE FILTERING")
    print("="*45)

    # Calculate cosine similarity between ALL products
    # Transpose matrix so rows=products, columns=users
    item_similarity = cosine_similarity(matrix.T)
    item_sim_df = pd.DataFrame(
        item_similarity,
        index=matrix.columns,
        columns=matrix.columns
    )

    # Pick target user
    target_user = matrix.index[target_user_index]
    print(f"  Target User      : {target_user}")

    # Get products the user has rated highly (rating >= 4)
    target_ratings  = matrix.loc[target_user]
    liked_products  = target_ratings[target_ratings >= 4].index.tolist()
    print(f"  Products liked   : {len(liked_products)}")

    if not liked_products:
        print("  ⚠️ User has no highly rated products. Try a different user.")
        return None

    # Find unrated products
    unrated_products = target_ratings[target_ratings == 0].index

    # Score unrated products based on similarity to liked products
    scores = {}
    for product in unrated_products:
        sim_scores = []
        for liked in liked_products:
            if product in item_sim_df.columns and liked in item_sim_df.index:
                sim_scores.append(item_sim_df.loc[liked, product])
        if sim_scores:
            scores[product] = np.mean(sim_scores)

    # Get top N recommendations
    recommendations = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    rec_df = pd.DataFrame(recommendations, columns=['product_id', 'similarity_score'])
    rec_df.index += 1

    print(f"\n🏆 Top {top_n} Similar Products Recommended:")
    print(rec_df.to_string())
    return rec_df

# ── 5. Save Results ────────────────────────────────────
def save_results(user_rec, item_rec):
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    if user_rec is not None:
        user_rec.to_csv(OUTPUT_PATH + "user_based_recommendations.csv", index=False)
        print(f"\n💾 User-based results saved")
    if item_rec is not None:
        item_rec.to_csv(OUTPUT_PATH + "item_based_recommendations.csv", index=False)
        print(f"💾 Item-based results saved")

# ── Pipeline ───────────────────────────────────────────
if __name__ == "__main__":
    # Load
    df = load_data()

    # Create matrix with top 500 active users
    matrix, df_sample = create_user_item_matrix(df, sample_users=500)

    # Run both CF methods for user at index 0
    user_rec = user_based_cf(matrix, target_user_index=0, top_n=10)
    item_rec = item_based_cf(matrix, target_user_index=0, top_n=10)

    # Save
    save_results(user_rec, item_rec)

    print("\n🎉 Collaborative Filtering complete!")