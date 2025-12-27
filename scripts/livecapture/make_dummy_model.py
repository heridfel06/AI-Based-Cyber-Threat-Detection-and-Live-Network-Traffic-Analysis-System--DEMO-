# make_dummy_model.py
import joblib
from sklearn.ensemble import RandomForestClassifier

# tiny synthetic dataset
X = []
y = []
for _ in range(400):
    X.append([10, 2000, 7, 3, 5, 1, 200, 2])
    y.append(0)
for _ in range(150):
    X.append([400, 800000, 350, 20, 80, 120, 200, 80])
    y.append(1)

clf = RandomForestClassifier(n_estimators=50, random_state=42)
clf.fit(X,y)
joblib.dump(clf,'model.pkl')
print("Saved model.pkl")
