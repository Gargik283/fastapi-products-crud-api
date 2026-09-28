import json
import os
import requests
import streamlit as st

# --------------------------------------------------------------------------
# Page config
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="FastAPI Products Dashboard",
    page_icon="🛍️",
    layout="wide",
)

# --------------------------------------------------------------------------
# Sidebar — backend connection
# --------------------------------------------------------------------------
st.sidebar.header("⚙️ Backend Connection")
DEFAULT_API_URL = os.getenv("API_URL", "https://fastapi-products-crud-api-2.onrender.com")
BASE_URL = st.sidebar.text_input("FastAPI base URL", value=DEFAULT_API_URL).rstrip("/")
st.sidebar.caption(
    "Hosted on Render (free tier) - the first request may take up to a minute to wake up.\n\n"
    "To run locally: `uvicorn backend.app.main:app --reload` and set the URL to `http://127.0.0.1:8000`"
)

st.title("🛍️ FastAPI Products Dashboard")
st.caption(f"Backend: `{BASE_URL}`")

left, right = st.columns(2)


def api_get(path, params=None):
    return requests.get(f"{BASE_URL}{path}", params=params, timeout=10)


def api_post(path, json_body=None):
    return requests.post(f"{BASE_URL}{path}", json=json_body, timeout=10)


def api_put(path, json_body=None):
    return requests.put(f"{BASE_URL}{path}", json=json_body, timeout=10)


def api_delete(path):
    return requests.delete(f"{BASE_URL}{path}", timeout=10)


# ==========================================================================
# LEFT COLUMN
# ==========================================================================
with left:

    # ---- 1) Health & OpenAPI Routes ----
    st.subheader("1) Health & OpenAPI Routes")
    h1, h2 = st.columns(2)

    with h1:
        if st.button("Check / (root)"):
            try:
                r = api_get("/")
                st.success(f"Status: {r.status_code}")
                st.json(r.json())
            except Exception as e:
                st.error(f"Request failed: {e}")

    with h2:
        if st.button("Load OpenAPI JSON"):
            try:
                r = api_get("/openapi.json")
                st.success(f"Status: {r.status_code}")
                st.json(r.json())
            except Exception as e:
                st.error(f"Request failed: {e}")

    st.markdown(f"📄 Interactive docs: [{BASE_URL}/docs]({BASE_URL}/docs)")

    st.divider()

    # ---- 2) Browse Products ----
    st.subheader("2) Browse Products (GET /products)")

    name = st.text_input("Search by product name", value="", key="search_name")
    sort_by_price = st.checkbox("Sort by price", key="sort_price")
    order = st.selectbox("Order", ["asc", "desc"], key="order", disabled=not sort_by_price)
    limit = st.slider("Limit", min_value=1, max_value=100, value=10, key="limit")
    offset = st.slider("Offset", min_value=0, max_value=100, value=0, key="offset")

    if st.button("Fetch products", type="primary"):
        params = {
            "sort_by_price": sort_by_price,
            "order": order,
            "limit": limit,
            "offset": offset,
        }
        if name.strip():
            params["name"] = name.strip()

        try:
            r = api_get("/products", params=params)
            if r.status_code == 200:
                data = r.json()
                st.success(f"Total matching: {data.get('total', 0)}")
                st.dataframe(data.get("items", []), use_container_width=True)
            else:
                st.error(f"{r.status_code}: {r.json().get('detail', r.text)}")
        except Exception as e:
            st.error(f"Request failed: {e}")

# ==========================================================================
# RIGHT COLUMN
# ==========================================================================
with right:

    # ---- 3) Product by ID ----
    st.subheader("3) Product by ID (GET /products/{id})")
    pid_lookup = st.number_input("Product ID", min_value=1, step=1, key="lookup_id")

    if st.button("Fetch by ID"):
        try:
            r = api_get(f"/products/{int(pid_lookup)}")
            if r.status_code == 200:
                st.json(r.json())
            else:
                st.error(f"{r.status_code}: {r.json().get('detail', r.text)}")
        except Exception as e:
            st.error(f"Request failed: {e}")

    st.divider()

    # ---- 4) Create Product ----
    st.subheader("4) Create Product (POST /products)")

    with st.form("create_product_form"):
        c_name = st.text_input("Name")
        c_brand = st.text_input("Brand")
        c_category = st.text_input("Category")
        c_description = st.text_area("Description", max_chars=200)
        c_price = st.number_input("Price (INR)", min_value=0.0, step=1.0)
        c_stock = st.number_input("Stock", min_value=0, step=1)
        c_rating = st.slider("Rating", min_value=0.0, max_value=5.0, value=0.0, step=0.1)
        c_reviews = st.number_input("Reviews", min_value=0, step=1)
        c_in_stock = st.checkbox("In stock", value=True)
        submitted = st.form_submit_button("Create", type="primary")

    if submitted:
        payload = {
            "name": c_name,
            "brand": c_brand,
            "category": c_category,
            "description": c_description,
            "price": c_price,
            "currency": "INR",
            "stock": c_stock,
            "rating": c_rating,
            "reviews": c_reviews,
            "in_stock": c_in_stock,
        }
        try:
            r = api_post("/products", json_body=payload)
            if r.status_code == 201:
                st.success("Product created!")
                st.json(r.json())
            else:
                st.error(f"{r.status_code}: {r.json().get('detail', r.text)}")
        except Exception as e:
            st.error(f"Request failed: {e}")

    st.divider()

    # ---- 5) Update & Delete ----
    st.subheader("5) Update & Delete (PUT /products/{id}, DELETE /products/{id})")

    pid_edit = st.number_input("Product ID to update/delete", min_value=1, step=1, key="edit_id")
    update_json = st.text_area(
        "Fields to update (JSON)",
        value='{\n  "price": 1999,\n  "stock": 20\n}',
        height=140,
    )

    u1, u2 = st.columns(2)
    with u1:
        if st.button("Update", type="primary"):
            try:
                body = json.loads(update_json)
                r = api_put(f"/products/{int(pid_edit)}", json_body=body)
                if r.status_code == 200:
                    st.success("Product updated!")
                    st.json(r.json())
                else:
                    st.error(f"{r.status_code}: {r.json().get('detail', r.text)}")
            except json.JSONDecodeError:
                st.error("Invalid JSON in the update field.")
            except Exception as e:
                st.error(f"Request failed: {e}")

    with u2:
        if st.button("🗑️ Delete", type="secondary"):
            try:
                r = api_delete(f"/products/{int(pid_edit)}")
                if r.status_code == 200:
                    st.success("Product deleted!")
                    st.json(r.json())
                else:
                    st.error(f"{r.status_code}: {r.json().get('detail', r.text)}")
            except Exception as e:
                st.error(f"Request failed: {e}")
