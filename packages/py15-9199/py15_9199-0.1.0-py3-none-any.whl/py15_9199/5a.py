import matplotlib.pyplot as plt 
from sklearn.datasets import load_iris, load_wine, load_breast_cancer 
from sklearn.model_selection import train_test_split 
from sklearn.naive_bayes import GaussianNB 
from sklearn.metrics import accuracy_score 
datasets = {'Iris': load_iris(), 'Wine': load_wine(), 'Breast Cancer': 
load_breast_cancer()} 
accuracies = [] 
for name, data in datasets.items(): 
    X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, 
    test_size=0.2, random_state=42) 
    clf = GaussianNB().fit(X_train, y_train) 
    accuracies.append(accuracy_score(y_test, clf.predict(X_test))) 
    print(f"{name}: {accuracies[-1]:.2f}") 
plt.bar(datasets.keys(), accuracies) 
plt.xlabel('Dataset') 
plt.ylabel('Accuracy') 
plt.title('Naive Bayes Classifier Accuracy') 
plt.show() 
