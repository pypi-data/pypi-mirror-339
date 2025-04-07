import matplotlib.pyplot as plt 
from sklearn.datasets import make_classification 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import Perceptron 
from sklearn.neural_network import MLPClassifier 
from sklearn.metrics import accuracy_score 
X, y = make_classification(n_samples=200, n_features=20, n_classes=2, 
random_state=42) 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, 
random_state=42) 
single_layer = Perceptron(max_iter=1000, random_state=42) 
multi_layer = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=1000, 
random_state=42) 
single_layer.fit(X_train, y_train) 
multi_layer.fit(X_train, y_train) 
accuracies = [ 
accuracy_score(y_test, single_layer.predict(X_test)), 
accuracy_score(y_test, multi_layer.predict(X_test)) 
] 
# Plot results 
plt.bar(['Single-Layer', 'Multilayer'], accuracies, color=['blue', 'green']) 
plt.ylabel('Accuracy') 
plt.title('Model Accuracy Comparison') 
plt.ylim(0, 1) 
plt.show()