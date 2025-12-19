import sys
from pathlib import Path
import unittest

# Ensure backend directory is on the import path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.models.aiModel import FilterCondition, FilterObject  # type: ignore
from app.services.sql_engine import generate_sql_query, execute_sql_query  # type: ignore


class SqlEngineTests(unittest.TestCase):
    def test_generate_sql_count(self):
        filt = FilterObject(operation="count_vehicles", conditions=[])
        sql = generate_sql_query(filt)
        self.assertEqual(sql.strip(), "SELECT COUNT(*) as count FROM vehicles")

    def test_generate_sql_average_with_conditions_and_sort(self):
        filt = FilterObject(
            operation="average_speed",
            conditions=[
                FilterCondition(field="Direction", operator="==", value="North"),
                FilterCondition(field="Speed", operator=">", value="50"),
            ],
            sort_by="Speed",
            sort_direction="descending",
        )
        sql = generate_sql_query(filt)
        self.assertIn("SELECT AVG(Speed) as average_speed FROM vehicles", sql)
        self.assertIn("Direction == 'North' AND Speed > 50", sql)
        self.assertIn("ORDER BY Speed DESC", sql)

    def test_count_vehicles(self):
        result = execute_sql_query("SELECT COUNT(*) as count FROM vehicles")
        self.assertIsInstance(result, dict)
        self.assertIn("count", result)
        self.assertGreaterEqual(result["count"], 0)

    def test_average_speed(self):
        result = execute_sql_query("SELECT AVG(Speed) as average_speed FROM vehicles")
        self.assertIsInstance(result, dict)
        self.assertIn("average_speed", result)
        self.assertIsInstance(result["average_speed"], (int, float))

    def test_max_speed(self):
        result = execute_sql_query("SELECT MAX(Speed) as max_speed FROM vehicles")
        self.assertIsInstance(result, dict)
        self.assertIn("max_speed", result)
        self.assertGreaterEqual(result["max_speed"], 0)

    def test_list_records(self):
        result = execute_sql_query("SELECT * FROM vehicles LIMIT 5")
        self.assertIsInstance(result, list)
        self.assertLessEqual(len(result), 5)
        if result:
            sample = result[0]
            self.assertIn("CollectionTime", sample)
            self.assertIn("Direction", sample)
            self.assertIn("Lane", sample)
            self.assertIn("Speed", sample)


if __name__ == "__main__":
    unittest.main()
