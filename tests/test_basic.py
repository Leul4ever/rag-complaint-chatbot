import os

def test_project_structure():
    """Basic test to ensure project structure is intact."""
    assert os.path.exists("notebooks/Task_1_EDA_and_Preprocessing.ipynb")
    assert os.path.exists("README.md")
    assert os.path.exists("requirements.txt")

def test_data_dirs():
    """Ensure data directories exist."""
    assert os.path.exists("data/raw")
    assert os.path.exists("data/processed")
