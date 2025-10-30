import pandas as pd
import os

def load_data(file_path):
    """
    Loads data from a CSV file.
    If the file is not found, it creates a dummy CSV for testing purposes.
    
    Args:
        file_path (str): The path to the CSV file.
    
    Returns:
        pd.DataFrame: The loaded data.
    """
    if not os.path.exists(file_path):
        print(f"File not found at {file_path}. Creating dummy data.")
        # Create a dummy CSV for testing purposes
        dummy_data = {
            'product_id': [1, 1, 2, 2, 1],
            'date': ['2023-01-01', '2023-01-02', '2023-01-01', '2023-01-02', '2023-01-03'],
            'units_sold': [10, 12, 5, 7, 15],
            'current_stock': [100, 90, 50, 45, 80],
            'price': [10.0, 10.0, 20.0, 20.0, 10.0],
            'promotions': [0, 0, 1, 0, 0]
        }
        dummy_df = pd.DataFrame(dummy_data)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        dummy_df.to_csv(file_path, index=False)
        print(f"Dummy data created at {file_path}")
    
    try:
        df = pd.read_csv(file_path)
        print(f"Successfully loaded data from {file_path}")
        return df
    except Exception as e:
        print(f"An error occurred while loading data: {e}")
        return None

if __name__ == "__main__":
    sample_file_path = "./data/sample_sales_data.csv"
    df = load_data(sample_file_path)
    if df is not None:
        print("Data head:")
        print(df.head())
