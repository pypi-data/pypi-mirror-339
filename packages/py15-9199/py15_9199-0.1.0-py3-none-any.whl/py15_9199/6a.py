import numpy as np
import matplotlib.pyplot as plt

# Input and output datasets
X = np.array([
    [0, 0, 0],
    [0, 0, 1],
    [0, 1, 0],
    [0, 1, 1],
    [1, 0, 0],
    [1, 0, 1],
    [1, 1, 0],
    [1, 1, 1]
])
Y = np.array([[0], [1], [1], [0], [1], [0], [0], [1]])

# Weight initialization
W1 = np.random.randn(3, 4)
W2 = np.random.randn(4, 1)

# Sigmoid activation function
sigmoid = lambda x: 1 / (1 + np.exp(-x))

# Training loop
for _ in range(10000):
    A1 = sigmoid(np.dot(X, W1))
    A2 = sigmoid(np.dot(A1, W2))

    # Backpropagation and weight updates
    W2 += np.dot(A1.T, (Y - A2) * A2 * (1 - A2))
    W1 += np.dot(X.T, np.dot((Y - A2) * A2 * (1 - A2), W2.T) * A1 * (1 - A1))

# Visualization
fig, ax = plt.subplots()

# Input to hidden layer connections
for i in range(3):
    for j in range(4):
        ax.plot([0, 1], [i, j], 'k-')

# Hidden to output layer connections
for i in range(4):
    ax.plot([1, 2], [i, 0], 'k-')

# Nodes: red for input, blue for hidden, green for output
ax.scatter([0, 0, 0], [0, 1, 2], s=100, c='red')      # Input layer
ax.scatter([1, 1, 1, 1], [0, 1, 2, 3], s=100, c='blue') # Hidden layer
ax.scatter([2], [0], s=100, c='green')                 # Output layer

# Final prediction after training
output = sigmoid(np.dot(sigmoid(np.dot(X, W1)), W2))
print("Predicted Output:\n", output)

plt.axis('off')
plt.title('Simple Neural Network Structure')
plt.show()
