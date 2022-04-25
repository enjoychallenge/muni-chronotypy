# https://machinelearningmastery.com/machine-learning-in-python-step-by-step/

# compare algorithms
import pandas as pd
from pandas import set_option
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
import settings
import sqlalchemy

sql_engine = sqlalchemy.create_engine(settings.PG_URL)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(filename)s] [%(levelname)s]:\t%(message)s')
logger = logging.getLogger(__name__)

logger.info('****************************************************************************************************')
logger.info('****************************************************************************************************')
logger.info('****************************************************************************************************')
logger.info('****************************************************************************************************')
logger.info('****************************************************************************************************')
logger.info('****************************************************************************************************')
logger.info(f"Let's learn something.")
logger.info('****************************************************************************************************')

# Load dataset
logger.info(f"  Reading from DB")
dataset = pd.read_sql('select * from train_rows_important_columns', con=sql_engine)

logger.info(f"  Scattering matrix")
scatter_matrix(dataset)
logger.info(f"  Showing pyplot")
pyplot.show()

set_option('display.width', 100)
set_option('precision', 2)
logger.info('****************************************************************************************************')
logger.info(f'Describe each attribute\n{dataset.describe()}')

logger.info('****************************************************************************************************')
count_class = dataset.groupby('trenovacitypkod').size()
logger.info(f'Show target data distribution\n{count_class}')

logger.info('****************************************************************************************************')
correlations = dataset.corr(method='pearson')
logger.info(f'Show correlation between attributes\n{correlations}')

logger.info('****************************************************************************************************')
logger.info(f'Show attribute skewness\n{dataset.skew()}')

# # Split-out validation dataset
array = dataset.values
X = array[:, 1:-1]
y = array[:, -1]
y = np.array(y, dtype='uint8')

logger.info(f'\n{X[:5]}')
logger.info(f'\n{y[:5]}')

logger.info(f"  Prepare datasets")
X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.20, random_state=1, shuffle=True)

logger.info(f'X: train={X_train.shape}, validation={X_validation.shape}')
logger.info(f'Y: train={Y_train.shape}, validation={Y_validation.shape}')

logger.info('****************************************************************************************************')
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

logger.info('****************************************************************************************************')
best_model = models[3]
logger.info(f'Best model: {best_model[0]}')
model = best_model[1]
logger.info(f'Results for fit')
model.fit(X_train, Y_train)
predictions = model.predict(X_validation)

logger.info(f'accuracy_score={accuracy_score(Y_validation, predictions)}')
logger.info(f'confusion_matrix=\n{confusion_matrix(Y_validation, predictions)}')
logger.info(f'classification_report=\n{classification_report(Y_validation, predictions)}')

logger.info('****************************************************************************************************')
logger.info(f'Results for predict')
predictions = model.predict(X)
logger.info(f'accuracy_score={accuracy_score(y, predictions)}')
logger.info(f'confusion_matrix=\n{confusion_matrix(y, predictions)}')
logger.info(f'classification_report=\n{classification_report(y, predictions)}')

df_chronotyp = pd.DataFrame({'chronotyp_guessed': predictions})
df_export = pd.concat([dataset.loc[:, ['kod']], df_chronotyp], axis=1, sort=False)

with sql_engine.connect() as con:
	con.execute("DROP TABLE IF EXISTS train_rows_predictions CASCADE;")

df_export.to_sql("train_rows_predictions", sql_engine)

all_rows_ds = pd.read_sql('select * from joint_rows_important_columns', con=sql_engine)
all_rows = all_rows_ds.values[:, 1:-1]
logger.info('****************************************************************************************************')
logger.info(f'Describe each attribute\n{all_rows_ds.describe()}')

all_predictions = model.predict(all_rows)

df_chronotyp = pd.DataFrame({'chronotyp_guessed': all_predictions})
df_export = pd.concat([all_rows_ds.loc[:, ['kod']], df_chronotyp], axis=1, sort=False)

with sql_engine.connect() as con:
	con.execute("DROP TABLE IF EXISTS joint_rows_predictions CASCADE;")

df_export.to_sql("joint_rows_predictions", sql_engine)

with sql_engine.connect() as con:
	with open("data/predictions-views.sql") as file:
		query = sqlalchemy.text(file.read())
		con.execute(query)
