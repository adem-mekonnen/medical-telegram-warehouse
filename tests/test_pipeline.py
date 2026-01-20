
import os
import sys

# Simple test to ensure project structure exists
def test_project_structure():
    assert os.path.exists("src"), "Source directory missing"
    assert os.path.exists("medical_warehouse"), "dbt project missing"
    assert os.path.exists("api"), "API directory missing"

# Simple test to ensure API imports work
def test_api_import():
    try:
        from api.main import app
        assert app is not None
    except ImportError:
        assert False, "Failed to import FastAPI app"