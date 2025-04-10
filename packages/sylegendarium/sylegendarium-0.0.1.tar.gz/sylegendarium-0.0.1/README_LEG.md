Legendarium
===========

* Python library to make an efficient use of data
* License: MIT
* Compatible With: python 3.0+

Develop API Usage
-----------------

<pre>
<code>
>>>from sylegendarium import Legendarium
>>>data_saver = Legendarium(experiment_name=f'experiment', experiment_description='tutorial experiment', path='Experiments')
>>>data_saver.create_parameter("algorithm", "Greedy")
>>>data_saver.create_metric("rewards", list, "Rewards obtained by the agents", "points")
>>>data_saver.write(rewards=0)
>>>data_saver.save()

>>>from sylegendarium import load_experiment_pd, load_experiments
>>>df = load_experiments("Experiments") #Load all the experiments in a directory and return a pandas dataframe
>>>print(df.head())

>>>df = load_experiment_pd('experiment', 'Experiments') # Load the metrics as a pandas dataframe
>>>print(df.head())
</code>
</pre>