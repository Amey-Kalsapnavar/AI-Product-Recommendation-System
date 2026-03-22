from app.mock_products import enrich_recommendations
import json
import os

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "../../ml_service/models/")

# ── Cache ──────────────────────────────────────────────
_popularity = None
_cf         = None
_hybrid     = None

def load_models():
    global _popularity, _cf, _hybrid
    if _popularity is None:
        print("⚡ Loading pre-computed models...")
        with open(MODELS_DIR + "popularity_scores.json") as f:
            _popularity = json.load(f)
        with open(MODELS_DIR + "cf_scores.json") as f:
            _cf = json.load(f)
        with open(MODELS_DIR + "hybrid_scores.json") as f:
            _hybrid = json.load(f)
        print("✅ Models loaded instantly!")

# ── 1. Popularity ──────────────────────────────────────
def get_popularity_recommendations(top_n=10):
    load_models()
    results = [
        {
            "rank"        : i + 1,
            "product_id"  : r['product_id'],
            "avg_rating"  : round(r['avg_rating'], 3),
            "rating_count": int(r['rating_count']),
            "score"       : round(r['score'], 4)
        }
        for i, r in enumerate(_popularity[:top_n])
    ]
    return enrich_recommendations(results)

# ── 2. Collaborative Filtering ─────────────────────────
def get_cf_recommendations(user_id: str, top_n=10):
    load_models()
    if user_id not in _cf:
        print(f"⚠️ User {user_id} not in CF cache, using fallback")
        return get_popularity_recommendations(top_n)
    results = [
        {
            "rank"      : i + 1,
            "product_id": r['product_id'],
            "cf_score"  : r['cf_score']
        }
        for i, r in enumerate(_cf[user_id][:top_n])
    ]
    return enrich_recommendations(results)

# ── 3. Hybrid ──────────────────────────────────────────
def get_hybrid_recommendations(user_id: str, top_n=10):
    load_models()
    if user_id not in _hybrid:
        print(f"⚠️ User {user_id} not in Hybrid cache, using fallback")
        return get_popularity_recommendations(top_n)
    results = [
        {
            "rank"             : i + 1,
            "product_id"       : r['product_id'],
            "hybrid_score"     : r['hybrid_score'],
            "popularity_score" : r['popularity_score'],
            "cf_score"         : r['cf_score']
        }
        for i, r in enumerate(_hybrid[user_id][:top_n])
    ]
    return enrich_recommendations(results)

# ── 4. Get sample users ────────────────────────────────
def get_sample_users(n=10):
    load_models()
    return list(_cf.keys())[:n]