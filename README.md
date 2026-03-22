# 🤖 TechShop AI — Intelligent Product Recommendation System

> An end-to-end AI-powered ecommerce recommendation system built with Python, FastAPI, React and Machine Learning. Analyzes 7.8M+ real Amazon Electronics reviews to deliver personalized product recommendations through 3 different ML models.

---

## 🌟 Live Demo

| Service | URL |
|---------|-----|
| 🛍️ Frontend (React) | http://localhost:3000 |
| ⚙️ Backend API | http://127.0.0.1:8000 |
| 📚 API Docs (Swagger) | http://127.0.0.1:8000/docs |

**Test User IDs for personalized recommendations:**
```
ADLVFFE4VBT8
A5JLAU2ARJ0BO
A3OXHLG6DIBRWS
```

---

## 📸 Screenshots

### 🏠 Home Page — Popular Products
![Home Page](docs/screenshots/home.png)

### 🔀 AI Recommended — Hybrid Model
![AI Recommended](docs/screenshots/hybrid.png)

---

## 🏗️ Project Architecture
```
AI-Product-Recommendation-System/
│
├── 🔧 backend/                         → FastAPI REST API Server
│   └── app/
│       ├── main.py                     → App entry point + CORS
│       ├── ml_engine.py                → ML models integration (instant ⚡)
│       ├── mock_products.py            → Product catalog with images & prices
│       ├── database.py                 → MongoDB connection
│       ├── models/
│       │   ├── product_model.py        → Product schema
│       │   └── interaction_model.py    → User interaction schema
│       └── routes/
│           ├── product_routes.py       → Product CRUD endpoints
│           ├── interaction_routes.py   → Interaction tracking
│           └── recommendation_routes.py → ML recommendation endpoints
│
├── 🧠 ml_service/                      → Machine Learning Pipeline
│   ├── data/
│   │   ├── raw/                        → Original dataset (not tracked)
│   │   └── processed/                  → Cleaned dataset (not tracked)
│   ├── models/                         → Pre-computed JSON scores ⚡
│   │   ├── popularity_scores.json      → Top 100 popular products
│   │   ├── cf_scores.json              → CF scores per user
│   │   └── hybrid_scores.json          → Hybrid scores per user
│   ├── src/
│   │   ├── preprocess.py               → Data cleaning pipeline
│   │   ├── popularity.py               → Popularity-based recommender
│   │   ├── collaborative.py            → Collaborative filtering
│   │   ├── hybrid.py                   → Hybrid recommendation system
│   │   └── precompute.py               → Pre-computation script ⚡
│   └── outputs/                        → Charts and result CSVs
│
├── 🎨 frontend/                        → React Ecommerce UI
│   └── src/
│       ├── App.js                      → Main app with all components
│       └── App.css                     → Dark theme ecommerce styles
│
└── 📄 README.md
```

---

## 🧠 ML Models Implemented

### 1. 🏆 Popularity-Based Recommender
Recommends the most popular products across all users — great for new users with no history.

- Uses **IMDB Weighted Rating Formula** to balance rating quality vs quantity
- Formula: `Score = (v/(v+m)) × R + (m/(v+m)) × C`
- **Not personalized** — same recommendations for everyone
- Fast and reliable fallback when user data is unavailable

| Variable | Meaning |
|----------|---------|
| `R` | Average rating of the product |
| `v` | Number of ratings for the product |
| `m` | Minimum votes required (70th percentile) |
| `C` | Global mean rating across all products |

---

### 2. 🤝 Collaborative Filtering (Item-Based)
Finds products similar to what the user has already highly rated.

- Uses **Cosine Similarity** to measure product similarity
- Considers products rated ≥ 4 stars as "liked"
- Built with **pandas + scikit-learn** (no external ML libraries)
- **Personalized** — unique recommendations per user

**How it works:**
```
User liked: [Headphones, Mouse, Keyboard]
        ↓
Find products similar to these using cosine similarity
        ↓
Recommend: [Earbuds, Mousepad, USB Hub...]
```

---

### 3. 🔀 Hybrid Recommendation System
Combines both approaches for the most accurate recommendations.

- Weighted formula: `Score = 0.4 × Popularity + 0.6 × CF`
- Handles **cold start problem** — falls back to popularity when CF data unavailable
- **Best of both worlds** — personalized + reliable
- Used by Amazon, Netflix in production
```
Popularity Score (40%) ──┐
                          ├──→ Hybrid Score → Top 10 Results
CF Score (60%)       ────┘
```

---

### ⚡ Pre-computation Strategy
All ML scores are **pre-computed and cached** as JSON files for instant API responses.

| Approach | Response Time |
|----------|--------------|
| Live computation | 2-5 minutes ❌ |
| Pre-computed cache | < 1 second ✅ |

> In production this would be scheduled nightly using **Celery + Redis** or **Apache Airflow**.

---

## 📊 Dataset

| Property | Value |
|----------|-------|
| **Source** | Amazon Electronics Reviews (Kaggle) |
| **Original size** | 7,824,482 ratings |
| **After preprocessing** | 2,109,869 ratings |
| **Active users** | 253,994 |
| **Active products** | 145,199 |
| **Matrix sparsity** | 99.99% |
| **Rating range** | 1.0 – 5.0 |

### Rating Distribution
```
1★  ████░░░░░░  901,765
2★  ██░░░░░░░░  456,322
3★  ███░░░░░░░  633,073
4★  ███████░░░  1,485,781
5★  █████████░  4,347,541
```

### Dataset Setup
> Dataset not included due to file size (700MB+)
```bash
# 1. Download from Kaggle
# https://www.kaggle.com/datasets/vibivij/amazon-electronics-rating-datasetrecommendation

# 2. Place in correct folder
mv ratings_Electronics.csv ml_service/data/raw/

# 3. Run preprocessing
cd ml_service/src
python preprocess.py

# 4. Pre-compute ML scores (run once)
python precompute.py
```

---

## 🚀 API Endpoints

### Recommendation Endpoints
| Method | Endpoint | Description | Response Time |
|--------|----------|-------------|--------------|
| GET | `/recommendations/popular` | Top N popular products | ⚡ Instant |
| GET | `/recommendations/collaborative/{user_id}` | CF recommendations | ⚡ Instant |
| GET | `/recommendations/hybrid/{user_id}` | Hybrid recommendations | ⚡ Instant |
| GET | `/recommendations/users/sample` | Get valid test user IDs | ⚡ Instant |

### Product Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products` | Get all products |
| POST | `/add-product` | Add a new product |
| POST | `/track-interaction` | Track user interaction |
| GET | `/interactions` | Get all interactions |

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
      "cf_score": 0.9958,
      "name": "Bose QuietComfort 45 Headphones",
      "brand": "Bose",
      "category": "Headphones",
      "price": 329.99,
      "rating": 4.85,
      "image": "https://..."
    }
  ]
}
```

---

## 🛍️ Frontend Features

- 🏠 **Hero Section** — Stats (7.8M+ reviews, 3 ML models, 145K+ products)
- 🏆 **Popular Tab** — Top 10 globally popular products
- 🤝 **For You Tab** — Collaborative filtering results
- 🔀 **AI Recommended Tab** — Hybrid model results
- 🔍 **User ID Search** — Get personalized recommendations
- 🛒 **Add to Cart** — Interactive cart functionality
- ⭐ **Star Ratings** — Visual rating display
- 📱 **Responsive** — Works on all screen sizes
- 🌙 **Dark Theme** — Professional dark UI

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React.js | UI framework |
| **Styling** | CSS3 | Dark theme design |
| **HTTP Client** | Axios | API calls |
| **Backend** | FastAPI + Python | REST API server |
| **Server** | Uvicorn | ASGI server |
| **Database** | MongoDB | Product & interaction storage |
| **ML** | Pandas, NumPy | Data manipulation |
| **ML** | Scikit-learn | Cosine similarity |
| **Visualization** | Matplotlib, Seaborn | Charts and plots |
| **Version Control** | Git + GitHub | Code management |

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB running locally

### 1️⃣ Clone Repository
```bash
git clone https://github.com/Amey-Kalsapnavar/AI-Product-Recommendation-System.git
cd AI-Product-Recommendation-System
```

### 2️⃣ Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3️⃣ ML Service Setup
```bash
cd ml_service
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# Download dataset from Kaggle and place in data/raw/
# Then run:
cd src
python preprocess.py         # Clean data
python precompute.py         # Pre-compute ML scores ⚡
```

### 4️⃣ Frontend Setup
```bash
cd frontend
npm install
npm start
```

### 5️⃣ Open in Browser
```
http://localhost:3000
```

---

## 📈 Results

### Top 10 Popular Products
| Rank | Product | Avg Rating | Ratings | Score |
|------|---------|-----------|---------|-------|
| 1 | Sony WH-1000XM4 Headphones | 4.95 | 105 | 4.888 |
| 2 | Logitech MX Master 3 Mouse | 4.91 | 201 | 4.882 |
| 3 | Apple AirPods Pro | 4.88 | 324 | 4.865 |
| 4 | Samsung 970 EVO SSD | 4.87 | 873 | 4.865 |
| 5 | Anker 65W USB-C Charger | 4.94 | 84 | 4.863 |

### Hybrid Model Sample Output
```
User: ADLVFFE4VBT8
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Rank  Product          Hybrid  Pop    CF
#1    B0082E9K7U       0.9697  0.9303 0.9960
#2    B00HFFDDLG       0.9318  0.8778 0.9678
#3    B00CZDT30S       0.9182  0.8373 0.9721
```

---

## 🗺️ Project Roadmap

- [x] Backend setup (FastAPI + MongoDB)
- [x] Dataset collection (7.8M Amazon reviews)
- [x] Data preprocessing pipeline
- [x] Popularity-Based Recommendation
- [x] Collaborative Filtering (Item-Based)
- [x] Hybrid Recommendation System
- [x] ML API Integration with FastAPI
- [x] Pre-computation for instant responses ⚡
- [x] Mock product catalog with images & prices
- [x] React Ecommerce Frontend UI
- [x] Dark theme with product cards
- [x] Add to Cart functionality
- [ ] User Authentication (JWT)
- [ ] Real user registration & login
- [ ] Order history
- [ ] Deployment (AWS/Vercel)

---

## 📝 Key Learnings

- Building end-to-end ML pipelines from raw data to production API
- Implementing 3 types of recommendation algorithms from scratch
- Handling large datasets (7.8M rows) efficiently with pandas
- Designing RESTful APIs with FastAPI
- Connecting ML models to web applications
- React frontend development with API integration
- Git version control best practices

---

## 👨‍💻 Author

**Amey Kalsapnavar**
Individual Internship Project

[![GitHub](https://img.shields.io/badge/GitHub-Amey--Kalsapnavar-blue)](https://github.com/Amey-Kalsapnavar)

---

## 📄 License

This project is built for educational and internship purposes.