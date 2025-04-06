# omsatyawanpathak.py (your module file)
import matplotlib.pyplot as plt

class OmSatyawanPathak:
    @staticmethod
    def bar(x, y, title="Bar Graph", xlabel="X Axis", ylabel="Y Axis"):
        """Create a bar graph effortlessly."""
        plt.bar(x, y)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def histogram(data, bins=10, title="Histogram", xlabel="Value", ylabel="Frequency"):
        """Create a histogram effortlessly."""
        plt.hist(data, bins=bins)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

# Example usage (for testing):
if __name__ == "__main__":
    # Test bar graph
    x = ["A", "B", "C"]
    y = [10, 20, 15]
    OmSatyawanPathak.bar(x, y, title="Sample Bar Graph")

    # Test histogram
    data = [1, 2, 2, 3, 3, 3, 4, 4, 5]
    OmSatyawanPathak.histogram(data, title="Sample Histogram")