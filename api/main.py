from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from typing import Dict

from models.forecasting_model import load_model, train_model
from models.recommendation_engine import recommend_reorder_quantity
from data.data_ingestion import load_data
from data.data_processing import clean_and_engineer_features

app = FastAPI()

# In-memory store for models and data (for demonstration purposes)
# In a real application, this would be a database or a more robust model store
models: Dict[int, any] = {}
data_store: pd.DataFrame = pd.DataFrame()

class PredictionRequest(BaseModel):
    product_id: int
    safety_stock: float = 0.0
    current_stock: float = 0.0

@app.on_event("startup")
async def startup_event():
    global data_store
    # Load and preprocess data on startup
    # In a real scenario, this would be a more robust data loading process
    sample_file_path = "./data/sample_sales_data.csv"
    df_raw = load_data(sample_file_path)
    if df_raw is None:
        raise RuntimeError("Failed to load initial data for API.")
    data_store = clean_and_engineer_features(df_raw)
    if data_store is None:
        raise RuntimeError("Failed to clean and engineer features for initial data.")

    # Train models for all unique products on startup
    unique_product_ids = data_store['product_id'].unique()
    for product_id in unique_product_ids:
        try:
            model, _ = train_model(data_store, product_id=product_id)
            models[product_id] = model
            print(f"Model for product {product_id} trained and loaded.")
        except Exception as e:
            print(f"Error training model for product {product_id}: {e}")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/predict")
async def predict_demand_and_recommend(request: PredictionRequest):
    product_id = request.product_id
    safety_stock = request.safety_stock
    current_stock = request.current_stock

    if product_id not in models:
        raise HTTPException(status_code=404, detail=f"Model for product_id {product_id} not found. Please train the model first.")

    model = models[product_id]

    # Make future dataframe for prediction (30 days as per requirement)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    # Get the forecasted demand for the next 30 days (sum of yhat)
    # For simplicity, let's take the sum of the next 30 days' forecasted demand
    # In a real scenario, you might want to consider a more nuanced approach
    forecasted_demand_next_30_days = forecast['yhat'].iloc[-30:].sum()

    reorder_quantity = recommend_reorder_quantity(
        forecasted_demand=forecasted_demand_next_30_days,
        safety_stock=safety_stock,
        current_stock=current_stock
    )

    return {
        "product_id": product_id,
        "forecasted_demand_next_30_days": forecasted_demand_next_30_days,
        "recommended_reorder_quantity": reorder_quantity,
        "forecast_details": forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30).to_dict(orient="records")
    }