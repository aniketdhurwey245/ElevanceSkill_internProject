import matplotlib.pyplot as plt

def plot_model_comparison(models, scores):
    plt.figure()
    plt.bar(models, scores)
    plt.xlabel("Models")
    plt.ylabel("Score")
    plt.title("Model Performance Comparison")
    plt.savefig("outputs/model_comparison.png")
    plt.close()

def plot_data_growth(timestamps, counts):
    plt.figure()
    plt.plot(timestamps, counts)
    plt.xlabel("Time")
    plt.ylabel("Data Size")
    plt.title("Knowledge Base Growth")
    plt.savefig("outputs/data_growth.png")
    plt.close()