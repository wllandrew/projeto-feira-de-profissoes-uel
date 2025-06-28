from sklearn.model_selection import train_test_split
from sklearn import svm
import pandas as pd
import os
import joblib

DATASET_PATH = os.path.join(os.getcwd(), 'dataset/dataset.csv')

csv = pd.read_csv(DATASET_PATH)

y = csv["Jumping"]
x = csv.drop(columns=["Jumping"])

print('Separando dataset...')
X_train, X_test, y_train, y_test = train_test_split(x.to_numpy(), y.to_numpy(), test_size=0.2)
print('Dataset pronto!')


model = svm.SVC(kernel='rbf', probability=True)
# model = svm.SVC(kernel='linear', probability=True)
print('Treinando modelo...')
model.fit(X_train, y_train)
print('Modelo treinado!')

print('Analisando acurácia...')
score = model.score(X_test, y_test)
probabilidades = model.predict_proba(X_test)

for p in probabilidades:
    print(f"Não pulando: {p[0]*100:.1f}% | Pulando: {p[1]*100:.1f}%")

print(f'Score: ', score)

path_model = 'models/jumping-svm-model.pkl'
joblib.dump(model, path_model)
print(f"Modelo salvo como {path_model}")