# capture_requirements.py
import subprocess
import sys
import joblib
import sklearn

def get_dependency_versions():
    """Get versions of all packages used by the model"""
    model = joblib.load("model.joblib")
    packages = {
        'scikit-learn': sklearn.__version__,
        # Add other critical packages here
    }
    return packages

def generate_requirements(packages):
    """Generate requirements.txt with pinned versions"""
    with open("requirements.txt", "w") as f:
        f.write(f"scikit-learn=={packages['scikit-learn']}\n")
        f.write(f"numpy=={np.__version__}\n")  # numpy is always needed
        f.write("flask==2.3.2\n")  # Your web framework
        f.write(f"joblib=={joblib.__version__}\n")

if __name__ == "__main__":
    packages = get_dependency_versions()
    generate_requirements(packages)
    print("Generated requirements.txt with training environment versions!")