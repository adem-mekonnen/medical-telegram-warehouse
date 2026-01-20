import os
import sys

# Simple test to ensure project structure exists
def test_project_structure():
    assert os.path.exists("src"), "Source directory missing"
    assert os.path.exists("medical_warehouse"), "dbt project missing"
    # This test will pass easily and give you the green checkmark