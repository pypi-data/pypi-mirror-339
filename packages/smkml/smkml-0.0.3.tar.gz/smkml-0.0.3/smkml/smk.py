import numpy as np
import matplotlib.pyplot as plt
import warnings
from sklearn.cluster import KMeans
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.decomposition import PCA
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SMK:
    def __init__(self, n_clusters=3, kernel="linear", C=1.0, p=2,
                 enable_grid_search=False, param_grid=None, enable_cv=False):
        self.n_clusters = n_clusters
        self.kernel = kernel
        self.C = C
        self.p = p  
        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
        self.svm = SVC(kernel=kernel, C=C, probability=True)
        self.mode = None
        self.enable_grid_search = enable_grid_search
        self.param_grid = param_grid if param_grid else {
            'C': [0.1, 1, 10],
            'kernel': ['linear', 'rbf', 'poly'],
            'degree': [2, 3, 4]
        }
        self.enable_cv = enable_cv

    def fit(self, X, y=None):
        X_scaled = self.scaler.fit_transform(X)

        if y is None:
            self.mode = "clustering"
            self.kmeans.fit(X_scaled)
        else:
            self.mode = "classification"

            if self.kernel in ["rbf", "poly"]:
                warnings.warn("[LIMITATION] Complex kernels may reduce interpretability.")
            if len(X_scaled) > 10000:
                warnings.warn("[LIMITATION] Large datasets may significantly increase training time.")

            if self.enable_grid_search:
                logging.info("Running GridSearchCV for optimal SVM parameters...")
                grid_search = GridSearchCV(SVC(probability=True), self.param_grid, cv=5)
                grid_search.fit(X_scaled, y)
                self.svm = grid_search.best_estimator_
                logging.info(f"Best SVM parameters found: {grid_search.best_params_}")
            else:
                self.svm = SVC(kernel=self.kernel, C=self.C, probability=True)
                self.svm.fit(X_scaled, y)

            if self.enable_cv:
                logging.info("Running 5-fold Cross-Validation Report...")
                scores = cross_val_score(self.svm, X_scaled, y, cv=5)
                logging.info(f"Cross-validation scores: {scores}")
                logging.info(f"Mean accuracy: {scores.mean():.4f}")

        return self

    def predict(self, X):
        if self.mode is None:
            raise ValueError("Model must be trained using `fit` before predictions.")

        X_scaled = self.scaler.transform(X)
        return self.svm.predict(X_scaled) if self.mode == "classification" else self.kmeans.predict(X_scaled)

    def fit_predict(self, X):
        self.fit(X)
        return self.kmeans.labels_

    def score(self, X, y=None):
        if self.mode is None:
            raise ValueError("Model must be trained before scoring.")

        X_scaled = self.scaler.transform(X)
        if self.mode == "classification":
            if y is None:
                raise ValueError("Labels required for classification scoring.")
            return accuracy_score(y, self.svm.predict(X_scaled))
        return self.kmeans.inertia_

    def compute_distance(self, x, y, metric="euclidean"):
        if metric == "euclidean":
            return np.sqrt(np.sum((x - y) ** 2))
        elif metric == "manhattan":
            return np.sum(np.abs(x - y))
        elif metric == "minkowski":
            return np.power(np.sum(np.abs(x - y) ** self.p), 1 / self.p)
        else:
            raise ValueError("Unsupported distance metric.")

    def visualize_clusters(self, X):
        if self.mode != "clustering":
            raise ValueError("Visualization only available in clustering mode.")

        X_scaled = self.scaler.transform(X)
        reduced = PCA(n_components=2).fit_transform(X_scaled)
        labels = self.kmeans.predict(X_scaled)

        plt.scatter(reduced[:, 0], reduced[:, 1], c=labels, cmap='viridis')
        plt.title("KMeans Cluster Visualization (2D PCA)")
        plt.xlabel("Component 1")
        plt.ylabel("Component 2")
        plt.grid(True)
        plt.show()

    def get_params(self):
        return {
            "mode": self.mode,
            "n_clusters": self.n_clusters,
            "kernel": self.kernel,
            "C": self.C,
            "p": self.p,
            "grid_search": self.enable_grid_search,
            "cross_validation": self.enable_cv
        }

    def analyze_knn_limitations(self):
        return [
            "❌ Doesn't scale well with large datasets (lazy learner).",
            "❌ Suffers from the curse of dimensionality.",
            "❌ Prone to overfitting with noisy/high-dimensional data."
        ]

    def analyze_svm_limitations(self):
        return [
            "⚠️ Not suitable for large datasets due to high computation cost.",
            "⚠️ Sensitive to kernel and parameter choices.",
            "⚠️ Cannot handle missing values and large feature-to-sample ratio well.",
            "⚠️ Lacks probabilistic output; only deterministic margins.",
            "⚠️ Memory-intensive (stores kernel matrix).",
            "⚠️ Needs careful normalization and tuning.",
            "⚠️ Difficult to interpret model decisions."
        ]

    def svm_diagnostic_report(self):
        return {
            "Efficiency": "⚠️ Decreases with dataset size (runtime/memory).",
            "Normalization": "⚠️ Needs feature scaling and hyperparameter tuning.",
            "Probability Estimation": "⚠️ No direct probability estimation unless enabled.",
            "Interpretability": "⚠️ Complex kernels make SVM hard to interpret."
        }