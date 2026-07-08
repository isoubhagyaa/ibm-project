"""
test_agents.py
--------------
Basic integration smoke-tests for all four Nutrition Agent sub-agents.
Validates that each agent receives a query and returns a structured response.

Usage:
    python scripts/test_agents.py

Requirements:
    pip install ibm-watsonx-ai requests
    Ensure config/api_keys.yaml is populated.
"""

import json
import os
import sys
from pathlib import Path

try:
    import yaml
    from ibm_watsonx_ai import Credentials
    from ibm_watsonx_ai.foundation_models import ModelInference
except ImportError as e:
    print(f"[ERROR] Missing dependency: {e}")
    print("Run: pip install ibm-watsonx-ai pyyaml")
    sys.exit(1)

BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / "config" / "api_keys.yaml"

# ---------------------------------------------------------------------------
# Load credentials
# ---------------------------------------------------------------------------
def load_config() -> dict:
    if not CONFIG_PATH.exists():
        print(f"[ERROR] Missing credentials file: {CONFIG_PATH}")
        print("Copy config/api_keys.yaml.example → config/api_keys.yaml and fill in values.")
        sys.exit(1)
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)

# ---------------------------------------------------------------------------
# Shared model factory
# ---------------------------------------------------------------------------
def get_model(model_id: str, creds: dict) -> ModelInference:
    credentials = Credentials(
        url=creds.get("WATSONX_ENDPOINT", "https://us-south.ml.cloud.ibm.com"),
        api_key=creds["IBM_CLOUD_API_KEY"],
    )
    return ModelInference(
        model_id=model_id,
        credentials=credentials,
        project_id=creds["WATSONX_PROJECT_ID"],
        params={"max_new_tokens": 400, "temperature": 0.3},
    )

# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------
TESTS = [
    {
        "agent": "Nutrition Knowledge Agent",
        "model": "ibm/granite-13b-chat-v2",
        "prompt": (
            "System: You are a Nutrition Knowledge Agent. Return structured nutritional info.\n"
            "User: What are the nutritional values of 100g of cooked brown rice?"
        ),
        "expect_keywords": ["calories", "carb", "protein"],
    },
    {
        "agent": "Diet Recommendation Agent",
        "model": "ibm/granite-13b-instruct-v2",
        "prompt": (
            "System: You are a Diet Recommendation Agent. Generate a 1-day meal plan.\n"
            "User: Create a 1800-calorie vegetarian meal plan for a 35-year-old woman with Type 2 diabetes."
        ),
        "expect_keywords": ["breakfast", "lunch", "dinner"],
    },
    {
        "agent": "Health Advisory Agent",
        "model": "ibm/granite-13b-chat-v2",
        "prompt": (
            "System: You are a Health Advisory Agent specializing in preventive nutrition.\n"
            "User: What dietary changes should someone with hypertension make? Keep it brief."
        ),
        "expect_keywords": ["sodium", "potassium", "DASH"],
    },
    {
        "agent": "Food Log & Feedback Agent",
        "model": "ibm/granite-3-8b-instruct",
        "prompt": (
            "System: You are a Food Log & Feedback Agent. Analyze the meal and estimate calories.\n"
            "User: I had 2 scrambled eggs with 2 slices of whole wheat toast and an orange for breakfast."
        ),
        "expect_keywords": ["calories", "protein", "carb"],
    },
]

# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
def run_tests():
    config = load_config()
    passed = 0
    failed = 0

    for test in TESTS:
        print(f"\n{'='*60}")
        print(f"[TEST] {test['agent']}")
        print(f"{'='*60}")

        model = get_model(test["model"], config)

        try:
            response = model.generate_text(prompt=test["prompt"])
            print(f"[RESPONSE SNIPPET]\n{response[:300]}...")

            # Basic keyword checks
            missing = [kw for kw in test["expect_keywords"] if kw.lower() not in response.lower()]
            if missing:
                print(f"[WARN] Missing expected keywords: {missing}")
                failed += 1
            else:
                print(f"[PASS] All expected keywords found.")
                passed += 1

        except Exception as e:
            print(f"[FAIL] Agent call error: {e}")
            failed += 1

    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed out of {len(TESTS)} tests")
    print(f"{'='*60}")
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
