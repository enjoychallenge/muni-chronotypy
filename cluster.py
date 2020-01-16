# https://stackoverflow.com/a/37409396
import numpy as np
import pandas as pd
import scipy.cluster.hierarchy as hac
from scipy.cluster.hierarchy import fcluster
from numpy import genfromtxt


my_data = genfromtxt('data/derived/brno_2018_wd_RLI.csv', delimiter=',', skip_header=1, usecols=(6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29))
my_data2 = my_data[np.all(my_data >= 0, axis=1)]

dataframe = pd.DataFrame(my_data2)
# Z = hac.linkage(dataframe, method='single', metric='correlation')
# results = fcluster(Z, 40, criterion='maxclust')
Z = hac.linkage(dataframe, method='complete', metric='correlation')
results = fcluster(Z, 20, criterion='maxclust')

