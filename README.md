# 🤖 AI Product Recommendation System

An intelligent product recommendation system built with Python, FastAPI, and Machine Learning. Uses real Amazon Electronics data to provide personalized product recommendations through multiple ML approaches.

---

## 🏗️ Project Architecture
```
AI-Product-Recommendation-System/
├── backend/                  → FastAPI REST API server
│   └── app/
│       ├── main.py           → App entry point
│       ├── ml_engine.py      → ML models integration
│       ├── models/           → Database models
│       └── routes/           → API endpoints
├── ml_service/               → Machine Learning pipeline
│   ├── data/
│   │   ├── raw/              → Original dataset (not tracked)
│   │   └── processed/        → Cleaned dataset (not tracked)
│   ├── src/
│   │   ├── preprocess.py     → Data cleaning pipeline
│   │   ├── popularity.py     → Popularity-based recommender
│   │   ├── collaborative.py  → Collaborative filtering
│   │   └── hybrid.py         → Hybrid recommendation system
│   └── outputs/              → Charts and result CSVs
└── frontend/                 → React/Next.js UI (in progress)
```

---

## 🧠 ML Models Implemented

### 1. Popularity-Based Recommender
- Recommends globally popular products
- Uses **IMDB Weighted Rating Formula**
- Formula: `Score = (v/(v+m)) × R + (m/(v+m)) × C`
- Not personalized — same for all users

### 2. Collaborative Filtering (Item-Based)
- Personalized recommendations per user
- Uses **Cosine Similarity** to find similar products
- Based on user's highly rated products (≥ 4 stars)
- Built with pandas + scikit-learn

### 3. Hybrid Recommendation System
- Combines Popularity + Collaborative Filtering
- Weighted formula: `Score = 0.4 × Popularity + 0.6 × CF`
- Most accurate and robust approach
- Best of both worlds

---

## 📊 Dataset

- **Source:** Amazon Electronics Reviews (Kaggle)
- **Original size:** 7,824,482 ratings
- **After preprocessing:** 2,109,869 ratings
- **Active users:** 253,994
- **Active products:** 145,199
- **Matrix sparsity:** 99.99%

### Dataset Setup
> Dataset is not included in the repo due to file size.

1. Download `ratings_Electronics.csv` from [Kaggle](https://www.kaggle.com/datasets/vibivij/amazon-electronics-rating-datasetrecommendation)
2. Place it in `ml_service/data/raw/`
3. Run preprocessing:
```bash
cd ml_service/src
python preprocess.py
```

---

## 🚀 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/recommendations/popular` | Top N popular products |
| GET | `/recommendations/collaborative/{user_id}` | CF recommendations for user |
| GET | `/recommendations/hybrid/{user_id}` | Hybrid recommendations for user |
| GET | `/products` | Get all products |
| POST | `/add-product` | Add a new product |
| POST | `/track-interaction` | Track user interaction |

### Example Response — Hybrid API
```json
{
  "type": "hybrid",
  "user_id": "ADLVFFE4VBT8",
  "count": 10,
  "recommendations": [
    {
      "rank": 1,
      "product_id": "B0082E9K7U",
      "hybrid_score": 0.9696,
      "popularity_score": 0.9303,
      "cf_score": 0.9958
    }
  ]
}
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI, Uvicorn |
| Database | MongoDB |
| ML | Pandas, NumPy, Scikit-learn |
| Visualization | Matplotlib, Seaborn |
| Frontend | React / Next.js (planned) |
| Version Control | Git, GitHub |

---

## ⚙️ Local Setup

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### ML Service
```bash
cd ml_service
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# Run ML pipeline
cd src
python preprocess.py
python popularity.py
python collaborative.py
python hybrid.py
```

### API Documentation
Visit `http://127.0.0.1:8000/docs` for interactive Swagger UI

---

## 📈 Results

### Top Popular Products (Sample)
| Rank | Product ID | Avg Rating | Ratings | Score |
|------|-----------|-----------|---------|-------|
| 1 | B005LJQPE0 | 4.95 | 105 | 4.888 |
| 2 | B0033PRWSW | 4.91 | 201 | 4.882 |
| 3 | B007SZ0E1K | 4.88 | 324 | 4.865 |

---

## 🗺️ Project Roadmap

- [x] Backend setup (FastAPI + MongoDB)
- [x] Dataset collection and preprocessing
- [x] Popularity-Based Recommendation
- [x] Collaborative Filtering
- [x] Hybrid Recommendation System
- [x] ML API Integration with FastAPI
- [ ] React Frontend UI
- [ ] User Authentication
- [ ] Real-time recommendations

---

## 👨‍💻 Author

**Amey Kalsapnavar**
Individual Internship Project