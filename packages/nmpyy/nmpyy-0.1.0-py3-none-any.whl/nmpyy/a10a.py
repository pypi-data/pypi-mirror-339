def a10a():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    file_path = r'F:\heart-2.csv'  
    data = pd.read_csv(file_path)
    print("Original dataset:")
    print(data.head())
    X = data.drop(columns=['target'])  
    y = data['target']
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    pca = PCA(n_components=2)  
    X_pca = pca.fit_transform(X_scaled)
    print("\nOriginal shape:", X.shape)
    print("Reduced shape:", X_pca.shape)
    plt.figure(figsize=(10, 6))
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='viridis', edgecolor='k', s=50)
    plt.title('PCA of Heart Dataset')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.colorbar(label='Target')
    plt.grid(True)
    plt.show()
