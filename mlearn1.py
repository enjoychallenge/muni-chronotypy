# https://machinelearningmastery.com/machine-learning-in-python-step-by-step/

# compare algorithms
import pandas as pd
from pandas import read_csv
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import numpy as np

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(filename)s] [%(levelname)s]:\t%(message)s')
logger = logging.getLogger(__name__)

logger.info(f"Let's learn something.")

# Load dataset
url = "data/derived/train_rows_important_columns.csv"
logger.info(f"  Reading csv")
dataset = read_csv(url, )

logger.info(f"  Scattering matrix")
# scatter_matrix(dataset)
logger.info(f"  Showing pyplot")
# pyplot.show()

# # Split-out validation dataset
array = dataset.values
# X = array[:, 1:69]
X = array[:, 1:4]
y = array[:, -1]
y = np.array(y, dtype='uint8')

logger.info(X[:5])
logger.info(y[:5])
logger.info(f"  Prepare datasets")
X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.20, random_state=1, shuffle=True)

logger.info(f'X: train={X_train.shape}, validation={X_validation.shape}')
logger.info(f'Y: train={Y_train.shape}, validation={Y_validation.shape}')


# # Spot Check Algorithms
models = []
models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC(gamma='auto')))
# evaluate each model in turn
results = []
names = []
kfold = StratifiedKFold(n_splits=7, random_state=1, shuffle=True, )
for name, model in models:
	logger.info(f'Starting training model {name}')
	cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
	results.append(cv_results)
	names.append(name)
	logger.info('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))

# LR: 0.631028 (0.107070)
# LDA: 0.627668 (0.056587)
# KNN: 0.500000 (0.058633)
# CART: 0.540119 (0.072839)
# NB: 0.460277 (0.109231)
# SVM: 0.543874 (0.019460)

model = DecisionTreeClassifier()
model.fit(X_train, Y_train)
predictions = model.predict(X_validation)

logger.info(f'accuracy_score={accuracy_score(Y_validation, predictions)}')
logger.info(f'confusion_matrix={confusion_matrix(Y_validation, predictions)}')
logger.info(f'classification_report={classification_report(Y_validation, predictions)}')

predictions = model.predict(X)
logger.info(f'accuracy_score={accuracy_score(y, predictions)}')
logger.info(f'confusion_matrix={confusion_matrix(y, predictions)}')
logger.info(f'classification_report={classification_report(y, predictions)}')

df_chronotyp = pd.DataFrame({'chronotyp_guessed': predictions})
df_export = pd.concat([dataset, df_chronotyp], axis=1, sort=False)
df_export.to_csv('data/derived/zsj_full_guess.csv', encoding='utf-8', index=False)
