import numpy as np
import matplotlib.pyplot as plt

class AnalyzeFit:
    def __init__(self, title=None, x_label=None, y_label=None):
            plt.title(title)
            plt.xlabel(x_label)
            plt.ylabel(y_label)

    def add_data(self, data):
        for i in data:
            plt.plot(i)

    def show(self):
        plt.show()