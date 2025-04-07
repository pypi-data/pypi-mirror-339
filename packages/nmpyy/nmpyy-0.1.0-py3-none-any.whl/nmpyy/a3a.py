def a3a(): 
    import matplotlib.pyplot as plt
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    from sklearn.neighbors import KNeighborsClassifier
    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    knn = KNeighborsClassifier(n_neighbors=3).fit(X_train, y_train)
    y_pred = knn.predict(X_test)
    for i, (t, p) in enumerate(zip(y_test, y_pred)):
        print(f"Sample {i}: True={t}, Predicted={p}, {'Correct' if t == p else 'Wrong'}")
    plt.scatter(
        X_test[:, 0], X_test[:, 1],
        c=(y_test == y_pred),
        cmap='RdYlGn',
        edgecolor='k'
    )
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.title("KNN Classification Results (Correct vs Wrong)")
    plt.show()
