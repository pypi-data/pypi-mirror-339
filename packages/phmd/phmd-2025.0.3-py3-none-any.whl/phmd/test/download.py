from phmd import download
from phmd import datasets

X = download.download('CURVES', force=True)
exit()

#X = datasets.load('JNUB', 'fault', force_download=True)

ds = datasets.Dataset("CWRU")
print(ds.describe())


datasets.Dataset.search(features='vibra')

task = ds['fault']
task.method = 'features'

sets = task[0]
