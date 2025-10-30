import pandas as pd
from prophet import Prophet
import pickle

def train_model(df, product_id, periods=30):
    """
    Trains a Prophet model for a given product.
    Args:
        df (pd.DataFrame): The input DataFrame containing 'date', 'product_id', and 'units_sold'.
        product_id (int): The ID of the product to train the model for.
        periods (int): Number of days to forecast.
    Returns:
        Prophet model: The trained Prophet model.
        pd.DataFrame: The forecast DataFrame.
    """
    product_df = df[df['product_id'] == product_id].copy()
    product_df = product_df.rename(columns={'date': 'ds', 'units_sold': 'y'})
    # Ensure 'ds' is datetime and sort
    product_df['ds'] = pd.to_datetime(product_df['ds'])
    product_df = product_df.sort_values(by='ds')
    # Initialize and train Prophet model
    model = Prophet()
    model.fit(product_df)
    # Create future dataframe for forecasting
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    print(f"Prophet model trained and forecast generated for product_id: {product_id}")
    return model, forecast

def save_model(model, product_id, path="./models/"):
    """
    Saves the trained Prophet model to a file.
    Args:
        model (Prophet): The trained Prophet model.
        product_id (int): The ID of the product the model was trained for.
        path (str): The directory to save the model.
    """
    with open(f"{path}prophet_model_{product_id}.pkl", 'wb') as f:
        pickle.dump(model, f)
    print(f"Model for product_id {product_id} saved to {path}prophet_model_{product_id}.pkl")

def load_model(product_id, path="./models/"):
    """
    Loads a trained Prophet model from a file.
    Args:
        product_id (int): The ID of the product the model was trained for.
        path (str): The directory where the model is saved.
    Returns:
        Prophet model: The loaded Prophet model.
    """
    try:
        with open(f"{path}prophet_model_{product_id}.pkl", 'rb') as f:
            model = pickle.load(f)
        print(f"Model for product_id {product_id} loaded from {path}prophet_model_{product_id}.pkl")
        return model
    except FileNotFoundError:
        print(f"Error: Model file not found for product_id {product_id} at {path}")
        return None

if __name__ == "__main__":
    # Example usage
    # Assuming you have a preprocessed DataFrame from data_processing.py
    from data.data_ingestion import load_data
    from data.data_processing import clean_and_engineer_features
    sample_file_path = "./data/sample_sales_data.csv"
    df_raw = load_data(sample_file_path)
    df_processed = clean_and_engineer_features(df_raw)
    if df_processed is not None:
        # Train model for product_id 1
        model_1, forecast_1 = train_model(df_processed, product_id=1)
        if model_1:
            save_model(model_1, product_id=1)
            print("Forecast for product 1:")
            print(forecast_1[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
        # Train model for product_id 2
        model_2, forecast_2 = train_model(df_processed, product_id=2)
        if model_2:
            save_model(model_2, product_id=2)
            print("Forecast for product 2:")
            print(forecast_2[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
        # Example of loading a model
        loaded_model = load_model(product_id=1)
        if loaded_model:
            print("Model loaded successfully.")
