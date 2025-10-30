import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("Demand Forecasting & Inventory Recommendation System")

# --- Sidebar for User Inputs ---
st.sidebar.header("Input Parameters")

product_id_input = st.sidebar.number_input("Product ID", min_value=1, value=1, step=1)
safety_stock_input = st.sidebar.number_input("Safety Stock", min_value=0.0, value=50.0, step=1.0)
current_stock_input = st.sidebar.number_input("Current Stock", min_value=0.0, value=100.0, step=1.0)

# --- Main Content Area ---
st.header("Prediction and Recommendation")

if st.sidebar.button("Get Recommendation"):
    # Call the FastAPI backend
    API_URL = "http://api:8000/predict"  # Assuming FastAPI runs on port 8000 and has a /predict endpoint
    payload = {
        "product_id": product_id_input,
        "safety_stock": safety_stock_input,
        "current_stock": current_stock_input
    }
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            result = response.json()
            st.success("Prediction and Recommendation Successful!")

            col1, col2 = st.columns(2)
            with col1:
                st.subheader(f"Product ID: {result['product_id']}")
                st.metric(label="Forecasted Demand (Next 30 Days)", value=f"{result['forecasted_demand_next_30_days']:.2f}")
                st.metric(label="Recommended Reorder Quantity", value=f"{result['recommended_reorder_quantity']:.2f}")

            with col2:
                st.subheader("Forecast Details")
                forecast_df = pd.DataFrame(result['forecast_details'])
                forecast_df['ds'] = pd.to_datetime(forecast_df['ds'])
                forecast_df = forecast_df.set_index('ds')

                st.line_chart(forecast_df[['yhat', 'yhat_lower', 'yhat_upper']])
                st.write("Daily Forecast (Next 30 Days):")
                st.dataframe(forecast_df.head())

        else:
            st.error(f"Error from API: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the API. Please ensure the FastAPI application is running.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

st.markdown("""
--- 
### How to Use:
1. Ensure the FastAPI backend is running (e.g., `uvicorn api.main:app --host 0.0.0.0 --port 8000`).
2. Enter the Product ID, Safety Stock, and Current Stock in the sidebar.
3. Click 'Get Recommendation' to see the forecasted demand and recommended reorder quantity.
""")