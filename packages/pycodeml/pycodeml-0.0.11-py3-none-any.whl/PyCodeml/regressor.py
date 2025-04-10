# import pickle
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import r2_score
# from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
# from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
# from sklearn.svm import SVR
# from sklearn.tree import DecisionTreeRegressor

# class RegressorTrainer:
#     def __init__(self, dataset, target_column):
#         """
#         Initialize the trainer with a dataset and target column.
#         Args:
#             dataset (pd.DataFrame): Clean numeric dataset.
#             target_column (str): Name of the column to predict.
#         """
#         self.dataset = dataset
#         self.target_column = target_column
#         self.models = {
#             "Linear Regression": LinearRegression(),
#             "Random Forest": RandomForestRegressor(),
#             "Support Vector Machine": SVR(),
#             "Decision Tree": DecisionTreeRegressor(),
#             "Gradient Boosting": GradientBoostingRegressor(),
#             "Ridge Regression": Ridge(),
#             "Lasso Regression": Lasso(),
#             "Elastic Net": ElasticNet(),
#         }
#         self.best_model = None
#         self.best_r2 = float('-inf')

#     def train_and_get_best_model(self):
#         """
#         Train multiple models and return the one with the highest R² score.
#         Returns:
#             Trained model with the best R² score.
#         """
#         X = self.dataset.drop(columns=[self.target_column])
#         y = self.dataset[self.target_column]

#         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

#         for model_name, model in self.models.items():
#             model.fit(X_train, y_train)
#             predictions = model.predict(X_test)
#             r2 = r2_score(y_test, predictions)

#             if r2 > self.best_r2:
#                 self.best_r2 = r2
#                 self.best_model = model

#         print(f"Best Model: {type(self.best_model).__name__} with R²: {self.best_r2:.4f}")
#         return self.best_model

#     def save_best_model(self, path="best_model.pkl"):
#         """
#         Save the best model to a file.
#         Args:
#             path (str): File path for saving the model.
#         """
#         if self.best_model:
#             with open(path, "wb") as file:
#                 pickle.dump(self.best_model, file)
#             print(f"Best model saved to {path}")
#         else:
#             print("No model to save. Train models first!")



import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor

class RegressorTrainer:
    def __init__(self, dataset, target_column):
        self.dataset = dataset
        self.target_column = target_column
        self.models = {
            "Linear Regression": LinearRegression(),
            "Random Forest": RandomForestRegressor(),
            "Support Vector Machine": SVR(),
            "Decision Tree": DecisionTreeRegressor(),
            "Gradient Boosting": GradientBoostingRegressor(),
            "Ridge Regression": Ridge(),
            "Lasso Regression": Lasso(),
            "Elastic Net": ElasticNet(),
        }
        self.best_model = None
        self.best_r2 = float('-inf')
        self.results = []

    def train_and_get_best_model(self):
        X = self.dataset.drop(columns=[self.target_column])
        y = self.dataset[self.target_column]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

        print(f"{'Model':<25}{'Train R²':<15}{'Test R²':<15}{'Status':<15}")
        print("-" * 70)

        for model_name, model in self.models.items():
            model.fit(X_train, y_train)

            train_pred = model.predict(X_train)
            test_pred = model.predict(X_test)

            train_r2 = r2_score(y_train, train_pred)
            test_r2 = r2_score(y_test, test_pred)

            # Detect overfitting or underfitting
            if train_r2 - test_r2 > 0.15:
                status = "Overfitting"
            elif test_r2 - train_r2 > 0.15:
                status = "Underfitting"
            else:
                status = "Good Fit"

            self.results.append({
                "Model": model_name,
                "Train R²": train_r2,
                "Test R²": test_r2,
                "Status": status
            })

            print(f"{model_name:<25}{train_r2:<15.4f}{test_r2:<15.4f}{status:<15}")

            if test_r2 > self.best_r2:
                self.best_r2 = test_r2
                self.best_model = model

        print(f"\nBest Model: {type(self.best_model).__name__} with Test R²: {self.best_r2:.4f}")
        return self.best_model

    def save_best_model(self, path="best_model.pkl"):
        if self.best_model:
            with open(path, "wb") as file:
                pickle.dump(self.best_model, file)
            print(f"Best model saved to {path}")
        else:
            print("No model to save. Train models first!")
