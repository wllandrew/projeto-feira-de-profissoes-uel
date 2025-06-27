from sklearn.model_selection import train_test_split
from sklearn import svm
import pandas as pd
import os
import joblib

DATASET_PATH = os.path.join(os.getcwd(), 'jumping-dataset.csv')

csv = pd.read_csv(DATASET_PATH)

y = csv["Jumping"]
x = csv.drop(columns=["Jumping"])

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2)

model = svm.SVC(kernel='rbf', gamma='auto', probability=True)
model.fit(x_train, y_train)

score = model.score(x_test, y_test)
probabilidades = model.predict_proba(x_test)

for p in probabilidades:
    print(f"Não pulando: {p[0]*100:.1f}% | Pulando: {p[1]*100:.1f}%")

print(f'Score: ', score)

path_model = 'jumping-svm-model.pkl'
joblib.dump(model, path_model)
print(f"Modelo salvo como {path_model}")