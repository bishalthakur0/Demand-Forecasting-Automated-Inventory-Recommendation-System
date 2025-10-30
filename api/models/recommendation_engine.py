def recommend_reorder_quantity(product_id, predicted_demand, current_stock, lead_time, buffer_stock=20):
    """
    Recommends the reorder quantity based on predicted demand, current stock, lead time, and buffer stock.

    Args:
        product_id (int): The unique identifier for the product.
        predicted_demand (float): The predicted demand for the product over the next period.
        current_stock (int): The current stock level of the product.
        lead_time (int): The lead time required to restock the product (in days or weeks).
        buffer_stock (int): The minimum safety stock to maintain (default is 20 units).

    Returns:
        dict: A dictionary containing the product ID, reorder recommendation, and reorder quantity.
    """
    # Calculate the required stock to meet predicted demand plus buffer stock
    required_stock = predicted_demand * lead_time + buffer_stock

    # Calculate the reorder quantity if current stock is less than required stock
    if current_stock < required_stock:
        reorder_quantity = required_stock - current_stock
        recommendation = "Reorder Needed"
    else:
        reorder_quantity = 0
        recommendation = "Stock Sufficient"

    return {
        "product_id": product_id,
        "recommendation": recommendation,
        "reorder_quantity": reorder_quantity,
        "current_stock": current_stock,
        "predicted_demand": predicted_demand,
        "required_stock": required_stock
    }

# Example usage
if __name__ == "__main__":
    # Sample data
    product_id = 101
    predicted_demand = 50.0  # Predicted demand for the product
    current_stock = 30  # Current stock level
    lead_time = 2  # Lead time in weeks
    buffer_stock = 20  # Buffer stock

    # Get reorder recommendation
    recommendation = recommend_reorder_quantity(product_id, predicted_demand, current_stock, lead_time, buffer_stock)
    print(recommendation)
