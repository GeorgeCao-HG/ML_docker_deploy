from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib

iris = load_iris()
model = RandomForestClassifier().fit(iris.data, iris.target)
joblib.dump(model, "model.joblib")