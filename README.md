# 🛍️ Products REST API — FastAPI + Streamlit Dashboard

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?logo=pydantic&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

### 🔗 Live Links

| | |
|---|---|
| 🖥️ **Live Dashboard** | [fastapi-appucts-crud-api.streamlit.app](https://fastapi-appucts-crud-api-o7l6lscmhrn2mcr8jocjpf.streamlit.app/) |
| 📘 **Live API Docs (Swagger UI)** | [fastapi-products-crud-api-2.onrender.com/docs](https://fastapi-products-crud-api-2.onrender.com/docs) |
| 💻 **Source Code** | [github.com/Gargik283/fastapi-products-crud-api](https://github.com/Gargik283/fastapi-products-crud-api) |

> ⏳ The API runs on Render's free tier, so the **first request after a period of inactivity can take 30–60 seconds** while the server wakes up. Data changes made on the live demo are temporary and reset when the server restarts.

---

A full **CRUD REST API** built with **FastAPI**, backed by JSON-file storage and validated with **Pydantic v2**, paired with an interactive **Streamlit dashboard** for testing every endpoint without leaving the browser — no Postman required. Both parts are deployed: the API on **Render** and the dashboard on **Streamlit Community Cloud**.

> Built as a hands-on backend engineering project: request validation, query-based filtering/sorting/pagination, and a clean service-layer separation between routes, schemas, and data access.

---

## 📸 Preview

| Browse, filter & paginate | Create, update & delete |
|---|---|
| ![Dashboard - browse products](screenshots/dashboard-browse.png) | ![Dashboard - create product](screenshots/dashboard-create.png) |

---

## ✨ Features

- **Full CRUD** on a `Product` resource — `GET`, `POST`, `PUT`, `DELETE`
- **Search** products by name (case-insensitive substring match)
- **Sort** by price, ascending or descending
- **Pagination** via `limit` / `offset` query parameters
- **Partial updates** — `PUT` only overwrites the fields you send
- **Schema validation** with Pydantic v2 (price > 0, rating 0–5, string length limits, etc.)
- **Auto-generated interactive docs** at [`/docs`](https://fastapi-products-crud-api-2.onrender.com/docs) (Swagger UI) and `/openapi.json`
- **Dependency-injected** data loading (`Depends`) for clean, testable route handlers
- **Streamlit control panel** to exercise every route visually — health check, browse, lookup, create, update, delete
- **Deployed end to end** — API on Render, dashboard on Streamlit Community Cloud

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
| Deployment | Render (API), Streamlit Community Cloud (dashboard) |

---

## 📂 Project Structure

```
.
├── backend/
│   ├── __init__.py
│   └── app/
│       ├── __init__.py
│       ├── main.py               # FastAPI app & route definitions
│       ├── schema/
│       │   ├── __init__.py
│       │   └── product.py        # Pydantic models (Product, ProductUpdate)
│       └── services/
│           ├── __init__.py
│           └── products.py       # Data access layer (load/save/CRUD helpers)
├── data/
│   └── products.json             # Persisted product records
├── streamlit_app.py              # Interactive dashboard for the API
├── requirements.txt
├── .gitignore
└── LICENSE
```

---

## 🚀 Run It Locally

### 1. Clone & install
```bash
git clone https://github.com/Gargik283/fastapi-products-crud-api.git
cd fastapi-products-crud-api
pip install -r requirements.txt
```

### 2. Configure environment
Create a `.env` file in the project root:
```
BASE_URL=data/products.json
```

### 3. Run the API
```bash
uvicorn backend.app.main:app --reload
```
Visit **http://127.0.0.1:8000/docs** for the interactive Swagger UI.

### 4. Run the dashboard
In a second terminal:
```bash
streamlit run streamlit_app.py
```
The sidebar defaults to the hosted API. To use your local server instead, set the URL to `http://127.0.0.1:8000`.

---

## 🔌 API Reference

Base URL: `https://fastapi-products-crud-api-2.onrender.com`

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

Built by **Gargi Kundu** — Data Analyst transitioning from an Electronics & VLSI background, focused on SQL, Python, Power BI, and backend fundamentals.

- 💼 LinkedIn: [linkedin.com/in/gargi-kundu](https://www.linkedin.com/in/gargi-kundu/)
- 🐙 GitHub: [github.com/Gargik283](https://github.com/Gargik283)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
