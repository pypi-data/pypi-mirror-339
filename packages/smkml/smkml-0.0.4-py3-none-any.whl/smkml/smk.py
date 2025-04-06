import numpy as np
from sklearn.cluster import KMeans
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import warnings

class SMK:
    def __init__(
        self,
        n_clusters=3,
        kernel="linear",
        C=1.0,
        p=2,
        enable_grid_search=False,
        param_grid=None
    ):
        self.n_clusters = n_clusters
        self.kernel = kernel
        self.C = C
        self.p = p  # For Minkowski distance
        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
        self.svm = SVC(kernel=kernel, C=C)
        self.mode = None
        self.enable_grid_search = enable_grid_search
        self.param_grid = param_grid if param_grid is not None else {
            'C': [0.1, 1],
            'kernel': ['linear', 'rbf'],
            'gamma': ['scale']
        }

    def fit(self, X, y=None):
        X_scaled = self.scaler.fit_transform(X)

        if y is None:
            self.mode = "clustering"
            self.kmeans.fit(X_scaled)
        else:
            self.mode = "classification"
            if self.enable_grid_search:
                if len(X_scaled) > 1000:
                    print("[WARNING] Grid Search is enabled and may be slow on large datasets.")
                print("[INFO] Running Grid Search for best SVM parameters...")
                grid_search = GridSearchCV(SVC(), self.param_grid, cv=3, n_jobs=-1)
                grid_search.fit(X_scaled, y)
                self.svm = grid_search.best_estimator_
                print(f"[INFO] Best parameters found: {grid_search.best_params_}")
            else:
                self.svm = SVC(kernel=self.kernel, C=self.C)
                self.svm.fit(X_scaled, y)

        return self

    def predict(self, X):
        if self.mode is None:
            raise ValueError("Model must be trained using `fit` before making predictions.")
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
                raise ValueError("Labels are required for classification scoring.")
            return accuracy_score(y, self.svm.predict(X_scaled))
        return self.kmeans.inertia_

    @staticmethod
    def fast_distance(x, y, p=2, metric="euclidean"):
        if metric == "euclidean":
            return np.linalg.norm(x - y)
        elif metric == "manhattan":
            return np.sum(np.abs(x - y))
        elif metric == "minkowski":
            return np.sum(np.abs(x - y) ** p) ** (1 / p)
        else:
            raise ValueError("Unsupported distance metric.")

    def visualize_clusters(self, X, sample_size=300):
        if self.mode != "clustering":
            raise ValueError("Clustering visualization is only available in clustering mode.")

        X_scaled = self.scaler.transform(X)
        if len(X_scaled) > sample_size:
            indices = np.random.choice(len(X_scaled), sample_size, replace=False)
            X_sample = X_scaled[indices]
        else:
            X_sample = X_scaled

        reduced = PCA(n_components=2).fit_transform(X_sample)
        labels = self.kmeans.predict(X_sample)

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
            "grid_search": self.enable_grid_search
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
            "⚠️ Needs normalization and parameter tuning.",
            "⚠️ Hard to interpret decisions."
        ]

    def get_kernel_formula(self):
        return {
            "rbf": "K(x, x') = exp(-gamma * ||x - x'||^2)",
            "poly": "K(x, x') = (x · x' + c)^d where d = degree"
        }
