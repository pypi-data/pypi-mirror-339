import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler

data, _ = make_blobs(n_samples=200, centers=3, random_state=42)
data = StandardScaler().fit_transform(data)

models = [GaussianMixture(3), KMeans(3, n_init=10)]
labels = [model.fit_predict(data) for model in models]

plt.figure(figsize=(10, 4))
for i, (label, title) in enumerate(zip(labels, ["EM Algorithm", "K-Means"])):
    plt.subplot(1, 2, i + 1)
    plt.scatter(data[:, 0], data[:, 1], c=label, cmap='viridis', alpha=0.6)
    plt.title(title)

plt.show()