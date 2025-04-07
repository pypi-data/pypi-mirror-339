def a7a():
    import pandas as pd
    from sklearn.tree import DecisionTreeClassifier
    import matplotlib.pyplot as plt
    import numpy as np
    data = pd.DataFrame({
        'Outlook': ['Sunny', 'Sunny', 'Overcast', 'Rainy', 'Rainy', 'Sunny'],
        'Temp': ['Hot', 'Hot', 'Hot', 'Mild', 'Cool', 'Mild'],
        'Humidity': ['High', 'High', 'High', 'High', 'Normal', 'Normal'],
        'Play': ['No', 'No', 'Yes', 'Yes', 'Yes', 'Yes']
    })
    X = pd.get_dummies(data[['Outlook', 'Temp', 'Humidity']])
    y = data['Play']
    clf = DecisionTreeClassifier(criterion='entropy').fit(X, y)
    features = X.columns
    info_gain = clf.feature_importances_
    plt.figure(figsize=(10, 6))
    plt.barh(features, info_gain, color='skyblue')
    plt.xlabel('Information Gain')
    plt.title('Information Gain for Each Feature (ID3 Algorithm)')
    plt.gca().invert_yaxis()
    plt.show()
    _, counts = np.unique(y, return_counts=True)
    probabilities = counts / counts.sum()
    entropy_value = -np.sum(probabilities * np.log2(probabilities))
    print(f"Overall Entropy of 'Play': {entropy_value:.3f}")
