import sys
from pathlib import Path
import unittest

# Ensure backend is importable
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.models.aiModel import FilterCondition, FilterObject  # type: ignore
from app.services.filter_engine import (
    apply_filter_conditions,
    apply_sorting,
    execute_operation,
    load_traffic_data,
    process_filter,
)  # type: ignore


class FilterEngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataset = load_traffic_data()
        assert cls.dataset, "traffic.csv must have sample data for tests"

    def test_filter_conditions_direction(self):
        cond = [FilterCondition(field="Direction", operator="==", value="North")]
        filtered = apply_filter_conditions(self.dataset, cond)
        self.assertTrue(all(row["Direction"] == "North" for row in filtered))

    def test_filter_conditions_speed_gt(self):
        cond = [FilterCondition(field="Speed", operator=">", value="50")]
        filtered = apply_filter_conditions(self.dataset, cond)
        self.assertTrue(all(int(row["Speed"]) > 50 for row in filtered))

    def test_sorting_desc_speed(self):
        sorted_rows = apply_sorting(self.dataset[:10], "Speed", "descending")
        speeds = [row["Speed"] for row in sorted_rows]
        self.assertEqual(speeds, sorted(speeds, reverse=True))

    def test_execute_operation_count(self):
        result = execute_operation(self.dataset, "count_vehicles")
        self.assertIsInstance(result, dict)
        self.assertIn("count", result)
        self.assertEqual(result["count"], len(self.dataset))

    def test_execute_operation_average(self):
        result = execute_operation(self.dataset, "average_speed")
        self.assertIsInstance(result, dict)
        self.assertIn("average_speed", result)

    def test_execute_operation_max(self):
        result = execute_operation(self.dataset, "max_speed")
        self.assertIsInstance(result, dict)
        self.assertIn("max_speed", result)
        self.assertEqual(result["max_speed"], max(int(r["Speed"]) for r in self.dataset))

    def test_process_filter_pipeline(self):
        filt = FilterObject(
            conditions=[
                FilterCondition(field="Direction", operator="==", value="North"),
                FilterCondition(field="Speed", operator=">", value="50"),
            ],
            operation="count_vehicles",
            sort_by="Speed",
            sort_direction="descending",
        )
        result = process_filter(filt)
        self.assertIsInstance(result, dict)
        self.assertIn("count", result)
        self.assertGreaterEqual(result["count"], 0)


if __name__ == "__main__":
    unittest.main()
