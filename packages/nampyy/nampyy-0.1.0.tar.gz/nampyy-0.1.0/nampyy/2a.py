def a2a():
    import numpy as np 
    import matplotlib.pyplot as plt 
    from sklearn.datasets import make_classification 
    from sklearn.svm import SVC 
    X, y = make_classification(n_samples=100, n_features=2, n_informative=2, 
    n_redundant=0,  
    n_repeated=0, n_clusters_per_class=1, random_state=42) 
    clf = SVC(kernel='linear').fit(X, y) 
    xx, yy = np.meshgrid(np.linspace(X[:, 0].min()-1, X[:, 0].max()+1, 500), 
    np.linspace(X[:, 1].min()-1, X[:, 1].max()+1, 500)) 
    Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape) 
    plt.contourf(xx, yy, Z > 0, alpha=0.3, cmap='coolwarm') 
    plt.contour(xx, yy, Z, levels=[0], colors='black', linestyles='--') 
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap='coolwarm', edgecolor='k') 
    plt.show()