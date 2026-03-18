import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

CLEAN_PATH  = os.path.join(os.path.dirname(__file__), "../data/processed/clean_ratings.csv")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "../outputs/popular_products.csv")

def load_clean_data(filepath=CLEAN_PATH):
    df = pd.read_csv(filepath)
    print(f"✅ Loaded clean data: {len(df):,} ratings")
    return df

def compute_popularity(df, percentile=0.70):
    product_stats = df.groupby('product_id').agg(
        avg_rating   = ('rating', 'mean'),
        rating_count = ('rating', 'count')
    ).reset_index()

    C = product_stats['avg_rating'].mean()
    m = product_stats['rating_count'].quantile(percentile)

    print(f"\n📐 Popularity Parameters:")
    print(f"  Global mean rating (C) : {C:.2f}")
    print(f"  Min ratings threshold  : {m:.0f} (top {int((1-percentile)*100)}%)")

    product_stats['weighted_score'] = (
        (product_stats['rating_count'] / (product_stats['rating_count'] + m))
        * product_stats['avg_rating']
        +
        (m / (product_stats['rating_count'] + m))
        * C
    )

    return product_stats.sort_values('weighted_score', ascending=False)

def get_top_n(popularity_df, n=10):
    top_n = popularity_df.head(n).reset_index(drop=True)
    top_n.index += 1
    print(f"\n🏆 Top {n} Popular Products:")
    print(top_n[['product_id','avg_rating','rating_count','weighted_score']].to_string())
    return top_n

def plot_top_products(top_n, n=10):
    os.makedirs(os.path.join(os.path.dirname(__file__), "../outputs"), exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f'Top {n} Popular Products', fontsize=14, fontweight='bold')

    axes[0].barh(top_n['product_id'].str[-8:], top_n['weighted_score'], color='steelblue')
    axes[0].invert_yaxis()
    axes[0].set_title('Weighted Popularity Score')
    axes[0].set_xlabel('Score')

    axes[1].barh(top_n['product_id'].str[-8:], top_n['rating_count'], color='coral')
    axes[1].invert_yaxis()
    axes[1].set_title('Number of Ratings')
    axes[1].set_xlabel('Count')

    plt.tight_layout()
    chart_path = os.path.join(os.path.dirname(__file__), "../outputs/popular_products.png")
    plt.savefig(chart_path, dpi=150)
    print(f"\n📊 Chart saved → {chart_path}")
    plt.show()

def save_results(top_n, path=OUTPUT_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    top_n.to_csv(path, index=False)
    print(f"💾 Results saved → {path}")

if __name__ == "__main__":
    df        = load_clean_data()
    pop_df    = compute_popularity(df, percentile=0.70)
    top_n     = get_top_n(pop_df, n=10)
    plot_top_products(top_n, n=10)
    save_results(top_n)
    print("\n🎉 Popularity-Based Recommender complete!")