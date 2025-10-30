import pandas as pd
from sklearn.preprocessing import LabelEncoder

def clean_and_engineer_features(df):
    """
    Cleans the data and engineers new features.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The processed DataFrame with new features.
    """
    if df is None:
        return None

    # Convert 'date' column to datetime objects
    df['date'] = pd.to_datetime(df['date'])

    # Handle missing values (example: fill with 0 or mean/median)
    # For simplicity, let's fill numerical NaNs with 0 and categorical with 'Unknown'
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna('Unknown')
        else:
            df[col] = df[col].fillna(0)

    # Feature Engineering
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_of_week'] = df['date'].dt.dayofweek
    df['day_of_year'] = df['date'].dt.dayofyear
    df['week_of_year'] = df['date'].dt.isocalendar().week.astype(int)
    df['quarter'] = df['date'].dt.quarter

    # Example of encoding categorical features if any (e.g., product_id if it were string)
    # For now, product_id is assumed to be numerical. If it were categorical, you'd do:
    # le = LabelEncoder()
    # df['product_id_encoded'] = le.fit_transform(df['product_id'])

    print("Data cleaning and feature engineering completed.")
    return df

if __name__ == "__main__":
    # Example usage with dummy data
    dummy_data = {
        'product_id': [1, 1, 2, 2, 1],
        'date': ['2023-01-01', '2023-01-02', '2023-01-01', '2023-01-02', '2023-01-03'],
        'units_sold': [10, 12, 5, 7, 15],
        'current_stock': [100, 90, 50, 45, 80],
        'price': [10.0, 10.0, 20.0, 20.0, 10.0],
        'promotions': [0, 0, 1, 0, 0]
    }
    dummy_df = pd.DataFrame(dummy_data)

    processed_df = clean_and_engineer_features(dummy_df)
    if processed_df is not None:
        print("Processed Data head:")
        print(processed_df.head())
        print("Processed Data info:")
        processed_df.info()