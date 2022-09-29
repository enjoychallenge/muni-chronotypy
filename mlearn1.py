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
all_rows_ds_full = pd.read_sql('''select cv.*, ascii(t.type) - ascii('A') + 1 type
from cell_training t inner join
     cell_values cv on t.sxy_id = cv.sxy_id
where cv.resident_population_91c66b_brno is not null
  and cv.access_city_center_public_transport_8_lvls_5db20f_brno is not null
;''', con=sql_engine)

all_rows_ds = all_rows_ds_full

dataset = all_rows_ds.copy()

logger.info(f"  Scattering matrix")
scatter_matrix(dataset)
logger.info(f"  Showing pyplot")
pyplot.show()

set_option('display.width', 100)
set_option('precision', 2)
logger.info('****************************************************************************************************')
logger.info(f'Describe each attribute\n{dataset.describe()}')

logger.info('****************************************************************************************************')
count_class = dataset.groupby('type').size()
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

# LR: 0.461321 (0.078462)
# LDA: 0.416714 (0.062598)
# KNN: 0.339921 (0.087462)
# CART: 0.480802 (0.039210)
# NB: 0.434783 (0.077533)
# SVM: 0.269339 (0.005357)

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

logger.info('****************************************************************************************************')
all_rows = all_rows_ds.values[:, 1:-1]
logger.info(f'Describe each attribute\n{all_rows_ds.describe()}')

all_predictions = model.predict(all_rows)
#
# df_chronotyp = pd.DataFrame({'predikce': all_predictions})
# df_predictions = pd.concat([all_rows_ds.loc[:, ['kod']], df_chronotyp], axis=1, sort=False)
# joined_df = all_rows_ds_full.join(df_predictions.set_index('kod'), on='kod', how='left')
#
# with sql_engine.connect() as con:
#     con.execute("DROP TABLE IF EXISTS joint_rows_predictions CASCADE;")
#
# joined_df.to_sql("joint_rows_predictions", sql_engine)
#
# with sql_engine.connect() as con:
#     with open("data/predictions-views.sql") as file:
#         query = sqlalchemy.text(file.read())
#         con.execute(query)
