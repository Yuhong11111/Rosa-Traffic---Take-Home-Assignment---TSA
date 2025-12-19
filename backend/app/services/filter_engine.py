import csv
from typing import List, Dict, Any
from pathlib import Path
from ..models.aiModel import FilterObject, FilterCondition


def load_traffic_data() -> List[Dict[str, Any]]:
    # Load traffic data from CSV file.
    data_path = Path(__file__).parent.parent / "data" / "traffic.csv"
    
    records = []
    with open(data_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Convert numeric fields to appropriate types
            records.append({
                "CollectionTime": row["CollectionTime"],
                "Direction": row["Direction"],
                "Lane": int(row["Lane"]),
                "Speed": int(row["Speed"]),
            })
    
    return records


def apply_filter_conditions(records: List[Dict[str, Any]], conditions: List[FilterCondition]) -> List[Dict[str, Any]]:
    # Filter records based on conditions.
    filtered_records = records
    
    for condition in conditions:
        field = condition.field
        operator = condition.operator
        value = condition.value
        
        if operator == "==":
            filtered_records = [
                r for r in filtered_records
                if str(r.get(field)) == str(value)
            ]
        elif operator == "!=":
            filtered_records = [
                r for r in filtered_records
                if str(r.get(field)) != str(value)
            ]
        elif operator == ">":
            filtered_records = [
                r for r in filtered_records
                if int(r.get(field, 0)) > int(value)
            ]
        elif operator == "<":
            filtered_records = [
                r for r in filtered_records
                if int(r.get(field, 0)) < int(value)
            ]
        elif operator == ">=":
            filtered_records = [
                r for r in filtered_records
                if int(r.get(field, 0)) >= int(value)
            ]
        elif operator == "<=":
            filtered_records = [
                r for r in filtered_records
                if int(r.get(field, 0)) <= int(value)
            ]
    
    return filtered_records


def apply_sorting(records: List[Dict[str, Any]], sort_by: str, sort_direction: str = "ascending") -> List[Dict[str, Any]]:
    # Sort records based on sort_by field and direction。
    if not sort_by:
        return records
    
    # Determine if we should sort numerically or as strings
    reverse = sort_direction.lower() == "descending"
    
    # Try to sort numerically, fall back to string sorting
    try:
        return sorted(records, key=lambda x: int(x.get(sort_by, 0)), reverse=reverse)
    except (ValueError, TypeError):
        return sorted(records, key=lambda x: str(x.get(sort_by, "")), reverse=reverse)


def execute_operation(records: List[Dict[str, Any]], operation: str) -> Any:
    # Execute the specified operation on filtered records.
    if not operation or operation == "list_vehicles":
        # Return the filtered records
        return records
    
    elif operation == "count_vehicles":
        # Return count of vehicles
        return {"count": len(records)}
    
    elif operation == "average_speed":
        # Calculate average speed
        if not records:
            return {"average_speed": 0}
        total_speed = sum(int(r.get("Speed", 0)) for r in records)
        average = total_speed / len(records)
        return {"average_speed": round(average, 2)}
    
    elif operation == "max_speed":
        # Find maximum speed
        if not records:
            return {"max_speed": None}
        max_speed = max(int(r.get("Speed", 0)) for r in records)
        return {"max_speed": max_speed}
    
    else:
        # Default: return records
        return records


def process_filter(filter_object: FilterObject) -> Any:
    """
    Main function to process a filter object.
    
    Steps:
    1. Load traffic data
    2. Apply filter conditions
    3. Apply sorting if specified
    4. Execute operation and return response
    """
    # Load traffic data
    records = load_traffic_data()
    
    # Apply conditions
    filtered_records = apply_filter_conditions(records, filter_object.conditions)
    
    # Apply sorting if specified
    if filter_object.sort_by:
        filtered_records = apply_sorting(
            filtered_records,
            filter_object.sort_by,
            filter_object.sort_direction or "ascending"
        )
    
    # Execute operation and return response
    result = execute_operation(filtered_records, filter_object.operation)
    
    return result