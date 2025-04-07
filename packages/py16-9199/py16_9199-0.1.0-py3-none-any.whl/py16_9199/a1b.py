def a1b():
    import matplotlib.pyplot as plt
    import numpy as np

    def logistic_equation(x):
        return 1 / (1 + np.exp(-x))

    x_values = np.linspace(-10, 10, 20)  
    y_values = logistic_equation(x_values)

    plt.figure(figsize=(8, 5))
    plt.plot(x_values, y_values, label='Logistic Curve: y = 1 / (1 + exp(-x))', color='blue')
    plt.scatter(x_values, y_values, color='red', marker='o', s=10)  

    plt.title('Basic Logistic Regression Curve')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()
