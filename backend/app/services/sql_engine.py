from ..models.aiModel import FilterObject


def generate_sql_query(filter_object: FilterObject) -> str:
    """Generate SQL query from FilterObject for demonstration purposes only.
    
    This shows users what SQL query would be executed, even though
    the actual filtering is done by the Python filter_engine.
    """
    # Build SELECT clause based on operation
    if filter_object.operation == "count_vehicles":
        select_clause = "COUNT(*) as count"
    elif filter_object.operation == "average_speed":
        select_clause = "AVG(Speed) as average_speed"
    elif filter_object.operation == "max_speed":
        select_clause = "MAX(Speed) as max_speed"
    else:  # list_vehicles
        select_clause = "*"
    
    # Build WHERE clause from conditions
    where_parts = []
    for condition in filter_object.conditions:
        field = condition.field
        operator = condition.operator
        value = condition.value
        
        # Handle string vs numeric comparisons
        if field in ("Direction",):
            # String comparison - quote the value
            where_parts.append(f"{field} {operator} '{value}'")
        else:
            # Numeric comparison - no quotes
            where_parts.append(f"{field} {operator} {value}")
    
    where_clause = " AND ".join(where_parts) if where_parts else ""
    
    # Build ORDER BY clause
    order_clause = ""
    if filter_object.sort_by:
        direction = filter_object.sort_direction or "ascending"
        order_direction = "ASC" if direction == "ascending" else "DESC"
        order_clause = f"ORDER BY {filter_object.sort_by} {order_direction}"
    
    # Combine into full SQL query
    sql = f"SELECT {select_clause} FROM vehicles"
    if where_clause:
        sql += f" WHERE {where_clause}"
    if order_clause:
        sql += f" {order_clause}"
    
    return sql

