import matplotlib.pyplot as plt
import numpy as np

# Plot example point cloud
X = np.random.rand(100, 2)
plt.scatter(X[:, 0], X[:, 1])
plt.title("Example Point Cloud")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.show()
