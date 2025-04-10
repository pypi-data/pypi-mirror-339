import seaborn as sns
import matplotlib.pyplot as plt
from sylegendarium import Legendarium, load_experiment_pd, load_experiments
import numpy as np  


if __name__ == "__main__":


    # Create an instance of the class
    exp = Legendarium(f"test", "Test experiment", "experiments")

    # Create a parameter
    exp.create_parameter("algorithm", "Greedy")
    exp.create_parameter("max_distance", 100.0)

    # Create a metric
    exp.create_metric("reward", float, "Reward function", "points")
    exp.create_metric("map", np.ndarray, "Mean map", "%")

    for run in range(3):

        # Write data
        for i in range(100):
            exp.write(run = run, step = i, reward = np.random.rand(), map = np.random.rand(100,100))

    # Save the data
    exp.save()

    # Load the data
    df = load_experiments("experiments")
    print(df.head())

    import seaborn as sns
    import matplotlib.pyplot as plt
    try:
        sns.lineplot(data = df, x = "step", y = "reward", hue = "run")
    except:
        plt.plot(df["step"].values, df["reward"].values, label = df["run"].values)
    plt.show()