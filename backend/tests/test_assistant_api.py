import sys
from pathlib import Path
import json
import unittest

# Ensure backend is importable
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.api.assistant import (
    build_mock_filter,
    generate_mock_llm_response,
    validate_json,
)  # type: ignore
from app.models.aiModel import FilterObject  # type: ignore


class AssistantApiTests(unittest.TestCase):
    def test_build_mock_filter_direction_speed(self):
        filt = build_mock_filter("list north vehicles faster than 55 kph sorted by speed descending")
        self.assertIsInstance(filt, FilterObject)
        self.assertEqual(filt.operation, "list_vehicles")
        self.assertEqual(filt.sort_by, "Speed")
        self.assertEqual(filt.sort_direction, "descending")
        # Ensure direction and speed conditions exist
        fields = {c.field for c in filt.conditions}
        self.assertIn("Direction", fields)
        self.assertIn("Speed", fields)

    def test_generate_mock_llm_response_round_trip(self):
        filt = build_mock_filter("how many south vehicles")
        raw = generate_mock_llm_response("how many south vehicles")
        data = json.loads(raw)
        self.assertIsInstance(data, dict)
        self.assertIn("operation", data)
        self.assertEqual(data.get("operation"), filt.operation)

    def test_validate_json_returns_filter_object(self):
        filt = build_mock_filter("max speed for north lane 1")
        raw = json.dumps(filt.model_dump())
        parsed = validate_json(raw)
        self.assertIsInstance(parsed, FilterObject)
        self.assertEqual(parsed.operation, "max_speed")
        self.assertTrue(parsed.conditions)

    def test_validate_json_rejects_bad_operator(self):
        bad = {"conditions": [{"field": "Speed", "operator": "INVALID", "value": "50"}]}
        with self.assertRaises(Exception):
            validate_json(json.dumps(bad))


if __name__ == "__main__":
    unittest.main()
