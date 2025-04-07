def a9a():
    import numpy as np

    def locally_weighted_regression(x, y, query_point, tau):
        x = np.array(x)
        y = np.array(y)
        query_point = np.array(query_point)
        x = np.c_[np.ones(len(x)), x]  # Adding intercept term

        # Calculate weights
        m = len(x)
        weights = np.exp(-np.sum((x - query_point) ** 2, axis=1) / (2 * tau ** 2))

        # Calculate weighted least squares
        W = np.diag(weights)
        theta = np.linalg.inv(x.T @ W @ x) @ x.T @ W @ y

        # Predict using the model parameters
        query_point = np.append([1], query_point)  # Adding intercept to query point
        prediction = query_point @ theta
        return prediction

    # Example usage:
    if __name__ == '__main__':
        x = [1, 2, 3, 4, 5]
        y = [2, 3, 4, 5, 6]
        query_point = [3.5]
        tau = 1.0
        prediction = locally_weighted_regression(x, y, query_point, tau)
        print(f'Prediction at {query_point} is {prediction}')
