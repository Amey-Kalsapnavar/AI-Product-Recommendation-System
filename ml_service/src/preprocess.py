import pandas as pd
import numpy as np
import os

RAW_PATH   = os.path.join(os.path.dirname(__file__), "../data/raw/ratings_Electronics.csv")
CLEAN_PATH = os.path.join(os.path.dirname(__file__), "../data/processed/clean_ratings.csv")

def load_data(filepath=RAW_PATH):
    print("📂 Loading dataset...")
    df = pd.read_csv(
        filepath,
        names=['user_id', 'product_id', 'rating', 'timestamp']
    )
    print(f"✅ Loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df

def explore_data(df):
    print("\n" + "="*45)
    print("📊  DATASET OVERVIEW")
    print("="*45)
    print(f"  Total ratings    : {len(df):,}")
    print(f"  Unique users     : {df['user_id'].nunique():,}")
    print(f"  Unique products  : {df['product_id'].nunique():,}")
    print(f"  Rating range     : {df['rating'].min()} – {df['rating'].max()}")
    print(f"\n  Missing values:")
    print(df.isnull().sum().to_string(header=False))
    print(f"\n  Rating distribution:")
    print(df['rating'].value_counts().sort_index().to_string(header=False))
    print("="*45)

def clean_data(df, min_user_ratings=5, min_product_ratings=5):
    print("\n🧹 Cleaning data...")
    before = len(df)
    df = df.drop_duplicates(subset=['user_id', 'product_id'])
    print(f"  Duplicates removed     : {before - len(df):,}")
    df = df.dropna()

    user_counts    = df['user_id'].value_counts()
    product_counts = df['product_id'].value_counts()

    df = df[df['user_id'].isin(user_counts[user_counts >= min_user_ratings].index)]
    df = df[df['product_id'].isin(product_counts[product_counts >= min_product_ratings].index)]

    print(f"\n✅ Clean dataset ready:")
    print(f"  Ratings          : {len(df):,}")
    print(f"  Active users     : {df['user_id'].nunique():,}")
    print(f"  Active products  : {df['product_id'].nunique():,}")

    total_possible = df['user_id'].nunique() * df['product_id'].nunique()
    sparsity = (1 - len(df) / total_possible) * 100
    print(f"  Matrix sparsity  : {sparsity:.2f}%")
    return df

def save_clean_data(df, output_path=CLEAN_PATH):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\n💾 Saved → {output_path}")

if __name__ == "__main__":
    df = load_data()
    explore_data(df)
    df = clean_data(df)
    save_clean_data(df)
    print("\n🎉 Preprocessing complete! Ready for model building.")