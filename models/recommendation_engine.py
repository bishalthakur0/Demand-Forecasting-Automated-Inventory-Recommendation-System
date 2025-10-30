def recommend_reorder_quantity(forecasted_demand, safety_stock, current_stock):
    """
    Calculates the optimal reorder quantity based on forecasted demand, safety stock, and current stock.

    Args:
        forecasted_demand (float): The predicted demand for the next period.
        safety_stock (float): The buffer stock to prevent stock-outs.
        current_stock (float): The current quantity of stock on hand.

    Returns:
        float: The recommended reorder quantity. Returns 0 if the calculated quantity is negative.
    """
    reorder_qty = forecasted_demand + safety_stock - current_stock
    return max(0, reorder_qty)

if __name__ == "__main__":
    # Example usage
    forecasted_demand_example = 150
    safety_stock_example = 50
    current_stock_example = 100

    recommended_qty = recommend_reorder_quantity(forecasted_demand_example, safety_stock_example, current_stock_example)
    print(f"Forecasted Demand: {forecasted_demand_example}")
    print(f"Safety Stock: {safety_stock_example}")
    print(f"Current Stock: {current_stock_example}")
    print(f"Recommended Reorder Quantity: {recommended_qty}")

    # Example with negative reorder quantity
    forecasted_demand_example_2 = 20
    safety_stock_example_2 = 10
    current_stock_example_2 = 50
    recommended_qty_2 = recommend_reorder_quantity(forecasted_demand_example_2, safety_stock_example_2, current_stock_example_2)
    print(f"\nForecasted Demand: {forecasted_demand_example_2}")
    print(f"Safety Stock: {safety_stock_example_2}")
    print(f"Current Stock: {current_stock_example_2}")
    print(f"Recommended Reorder Quantity: {recommended_qty_2}")