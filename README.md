# 🛍️ Products REST API — FastAPI + Streamlit Dashboard

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?logo=pydantic&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

A full **CRUD REST API** built with **FastAPI**, backed by JSON-file storage and validated with **Pydantic v2**, paired with an interactive **Streamlit dashboard** for testing every endpoint without leaving the browser — no Postman required.

> Built as a hands-on backend engineering project: request validation, query-based filtering/sorting/pagination, and a clean service-layer separation between routes, schemas, and data access.

---

## 📸 Preview

| Browse, filter & paginate | Create, update & delete |
|---|---|
| ![Dashboard - browse products](screenshots/dashboard-browse.png) | ![Dashboard - create product](screenshots/dashboard-create.png) |

*(Add your own screenshots to a `screenshots/` folder and update the paths above.)*

---

## ✨ Features

- **Full CRUD** on a `Product` resource — `GET`, `POST`, `PUT`, `DELETE`
- **Search** products by name (case-insensitive substring match)
- **Sort** by price, ascending or descending
- **Pagination** via `limit` / `offset` query parameters
- **Partial updates** — `PUT` only overwrites the fields you send
- **Schema validation** with Pydantic v2 (price > 0, rating 0–5, string length limits, etc.)
- **Auto-generated interactive docs** at `/docs` (Swagger UI) and `/openapi.json`
- **Dependency-injected** data loading (`Depends`) for clean, testable route handlers
- **Streamlit control panel** to exercise every route visually — health check, browse, lookup, create, update, delete

---

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| API framework | FastAPI |
| Validation | Pydantic v2 |
| Server | Uvicorn |
| Storage | JSON file (`data/products.json`) |
| Config | python-dotenv |
| Dashboard / API client | Streamlit + Requests |

---

## 📂 Project Structure

```
.
├── backend/
│   └── app/
│       ├── schema/
│       │   └── product.py        # Pydantic models (Product, ProductUpdate)
│       └── services/
│           └── products.py       # Data access layer (load/save/CRUD helpers)
├── data/
│   └── products.json             # Persisted product records
├── main.py                       # FastAPI app & route definitions
├── streamlit_app.py              # Interactive dashboard for the API
├── .env                          # BASE_URL config
└── requirements.txt
```

---

## 🚀 Getting Started

### 1. Clone & install
```bash
git clone https://github.com/Gargik283/<repo-name>.git
cd <repo-name>
pip install -r requirements.txt
```

### 2. Configure environment
Create a `.env` file in the project root:
```
BASE_URL=data/products.json
```

### 3. Run the API
```bash
uvicorn main:app --reload
```
Visit **http://127.0.0.1:8000/docs** for the interactive Swagger UI.

### 4. Run the dashboard
In a second terminal:
```bash
streamlit run streamlit_app.py
```
Set the backend URL in the sidebar (defaults to `http://127.0.0.1:8000`) and start testing.

---

## 🔌 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `GET` | `/products` | List products — supports `name`, `sort_by_price`, `order`, `limit`, `offset` |
| `GET` | `/products/{id}` | Fetch a single product by ID |
| `POST` | `/products` | Create a new product |
| `PUT` | `/products/{id}` | Partially update a product |
| `DELETE` | `/products/{id}` | Delete a product |

**Example — filter & sort:**
```
GET /products?name=headphones&sort_by_price=true&order=desc&limit=5&offset=0
```

**Example — create a product:**
```json
POST /products
{
  "name": "Wireless Headphones",
  "description": "Noise-cancelling wireless headphones with Bluetooth connectivity.",
  "category": "Electronics",
  "brand": "ShopEase",
  "price": 2499,
  "stock": 32,
  "rating": 3.8,
  "reviews": 57,
  "in_stock": true
}
```

---

## 🗺️ Possible Next Steps

- Swap JSON-file storage for PostgreSQL / SQLAlchemy
- Add authentication (JWT) for write operations
- Add automated tests with `pytest` + `TestClient`
- Containerize with Docker

---

## 👤 About

Built by **Gargi** — Data Analyst transitioning from an Electronics & VLSI background, focused on SQL, Python, Power BI, and backend fundamentals.

- GitHub: [github.com/Gargik283](https://github.com/Gargik283)

---

## 📄 License

This project is licensed under the MIT License.