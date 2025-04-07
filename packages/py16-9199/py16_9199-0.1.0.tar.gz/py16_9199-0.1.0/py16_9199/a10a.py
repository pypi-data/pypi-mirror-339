def a10a():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler

    # Load the dataset
    file_path = r'F:\heart-2.csv'  # Replace with your actual file path
    data = pd.read_csv(file_path)

    # Display the first few rows and columns of the dataset for inspection
    print("Original dataset:")
    print(data.head())

    # Separate features (X) and target (y) if applicable
    X = data.drop(columns=['target'])  # Assuming 'target' is the target column and not part of features
    y = data['target']

    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Instantiate PCA with desired number of components
    pca = PCA(n_components=2)  # Example: reducing to 2 principal components

    # Fit PCA to the scaled data
    X_pca = pca.fit_transform(X_scaled)

    # Print the original and reduced dimensions
    print("\nOriginal shape:", X.shape)
    print("Reduced shape:", X_pca.shape)

    # Visualize PCA results
    plt.figure(figsize=(10, 6))
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='viridis', edgecolor='k', s=50)
    plt.title('PCA of Heart Dataset')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.colorbar(label='Target')
    plt.grid(True)
    plt.show()
