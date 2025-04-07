def a1a():
    import numpy as np
    import matplotlib.pyplot as plt

    x = np.arange(-6.0, 6.0, 0.1)
    y = 3 * x + 2
    y_noise = 2 * np.random.normal(size=x.size)
    ydata = y + y_noise
    plt.plot(x, ydata, 'bo', label='Noisy data')
    plt.plot(x, y, 'r', label='Original line: y = 3x + 2')
    plt.xlabel('Independent Variable')
    plt.ylabel('Dependent Variable')
    plt.title('Linear Function with Noise')
    plt.legend()
    plt.grid(True)
    plt.show()
