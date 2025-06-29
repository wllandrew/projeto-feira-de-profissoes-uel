import pandas as pd
import sklearn as SVC
import joblib as jl
from sklearn.model_selection import train_test_split, GridSearchCV

dataset = pd.read_csv("")

X = dataset.drop(colums=["Jumping"])
y = dataset["Jumping"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

param_grid = {
        "C" : [0.1, 1, 10, 100],
        "gamma" : [1, .1, .01, .001],
        "kernel" : ["rbf", "linear"]
    }

grid = GridSearchCV(SVC(), param_grid=param_grid, refit=True, verbose=3

