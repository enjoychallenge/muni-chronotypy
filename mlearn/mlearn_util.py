import logging

import numpy as np
import pandas as pd

from pandas import set_option
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold

from sklearn.linear_model import LogisticRegression, SGDRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC, SVR
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier, AdaBoostClassifier
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.gaussian_process import GaussianProcessClassifier, GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from sklearn.cross_decomposition import PLSRegression

from sklearn.metrics import r2_score, mean_absolute_error, max_error, SCORERS


from . import precision_output

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(filename)s] [%(levelname)s]:\t%(message)s')
logger = logging.getLogger(__name__)


def print_dataset_info(dataset, grouping_column):
    # logger.info(f"  Scattering matrix")
    # scatter_matrix(dataset)
    # logger.info(f"  Showing pyplot")
    # pyplot.show()

    set_option('display.width', 100)
    set_option('precision', 2)
    logger.info('****************************************************************************************************')
    logger.info(f'Describe each attribute\n{dataset.describe()}')

    logger.info('****************************************************************************************************')
    count_class = dataset.groupby(grouping_column).size()
    logger.info(f'Show target data distribution\n{count_class}')

    logger.info('****************************************************************************************************')
    correlations = dataset.corr(method='pearson')
    logger.info(f'Show correlation between attributes\n{correlations}')

    unstack_correlations = correlations.abs().unstack()
    logger.info(f'unstack_correlations\n{unstack_correlations}')
    pairs_to_drop = set()
    cols = correlations.columns
    for i in range(0, correlations.shape[1]):
        for j in range(0, i + 1):
            pairs_to_drop.add((cols[i], cols[j]))
    au_corr = unstack_correlations.drop(labels=pairs_to_drop).sort_values(ascending=False)
    # au_corr = unstack_correlations.sort_values(ascending=False)
    logger.info(f'Highest correlations\n{au_corr[0:20]}')

    logger.info('****************************************************************************************************')
    logger.info(f'Show attribute skewness\n{dataset.skew()}')


def split_dataset(dataset):
    # # Split-out validation dataset
    array = dataset.values
    X = array[:, 1:-1]
    y = array[:, -1]
    y = np.array(y, dtype='uint8')

    logger.info(f'\n{X[:5]}')
    logger.info(f'\n{y[:5]}')

    logger.info(f"  Prepare datasets")
    X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.35, random_state=1, shuffle=True,)

    logger.info(f'X: train={X_train.shape}, validation={X_validation.shape}')
    logger.info(f'Y: train={Y_train.shape}, validation={Y_validation.shape}')

    train_val, train_cnt = np.unique(Y_train, return_counts=True)
    val_val, val_cnt = np.unique(Y_validation, return_counts=True)
    logger.info(f'train_val.grouping={train_val}:{train_cnt}')
    logger.info(f'val_val.grouping={val_val}:{val_cnt}')
    return X, y, X_train, X_validation, Y_train, Y_validation


def models_cross_validation(train_input, train_annotations):
    logger.info('****************************************************************************************************')
    # # Spot Check Algorithms
    models = []
    results = []
    # https://pythonguides.com/scikit-learn-classification/
    # https://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html

    # some regression vs classification models
    # https://www.turing.com/kb/scikit-learn-cheatsheet-methods-for-classification-and-regression

    # regression
    models.append(('SGDR', SGDRegressor(random_state=1)))
    models.append(('DTR', DecisionTreeRegressor(random_state=1)))
    models.append(('KNR', KNeighborsRegressor()))
    # models.append(('SVRl', SVR(kernel='linear')))
    models.append(('SVRrbf', SVR(kernel='rbf')))
    models.append(('SVRp', SVR(kernel='poly')))
    # ExtraTreesRegressor, RandomForestRegressor, AdaBoostRegressor
    models.append(('MLPR', MLPRegressor(alpha=1, max_iter=1000, random_state=1)))
    models.append(('KR', KernelRidge()))
    models.append(('GPR', GaussianProcessRegressor(random_state=1)))
    models.append(('PLSR', PLSRegression()))

    # classification
    models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr', random_state=1)))
    models.append(('CART', DecisionTreeClassifier(random_state=1)))
    models.append(('DTC', DecisionTreeClassifier(max_depth=5, random_state=1)))
    models.append(('KNN', KNeighborsClassifier()))
    models.append(('LDA', LinearDiscriminantAnalysis()))
    models.append(('QDA', QuadraticDiscriminantAnalysis()))
    models.append(('NB', GaussianNB()))
    models.append(('SVM', SVC(gamma='auto', random_state=1)))
    # models.append(('SVC_lin', SVC(kernel="linear", C=0.025),))
    models.append(('ETC', ExtraTreesClassifier(random_state=1)))
    models.append(('RFC', RandomForestClassifier(random_state=1)))
    models.append(('ABC', AdaBoostClassifier(random_state=1)))
    models.append(('MLPC', MLPClassifier(alpha=1, max_iter=1000, random_state=1)))
    # models.append(('GPC', GaussianProcessClassifier(1.0 * RBF(1.0))))

    # evaluate each model in turn
    kfold = StratifiedKFold(n_splits=5, random_state=1, shuffle=True, )
    for name, model in models:
        # See https://stackoverflow.com/a/42266274
        # or https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation
        logger.info(f'Starting cross validation using model {name}')
        # logger.info(f'sorted(sklearn.metrics.SCORERS.keys())={sorted(SCORERS.keys())}')
        cv_results = cross_val_score(model, train_input, train_annotations, cv=kfold, scoring='r2')
        logger.info('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))
        results.append((name, model, cv_results.mean(), cv_results.std()))

    logger.info('models_cross_validation DONE')
    return results


def evaluate_model(model, input_attributes, annotations):
    validation_predictions = model.predict(input_attributes)

    logger.info(f'r2_score={r2_score(annotations, validation_predictions)}')
    logger.info(f'mean_absolute_error=\n{mean_absolute_error(annotations, validation_predictions)}')
    logger.info(f'max_error =\n{max_error(annotations, validation_predictions)}')
    return r2_score(annotations, validation_predictions)


def fit_and_evaluate_model(model, X_train, Y_train, X_validation, Y_validation, X, y):
    model.fit(X_train, Y_train)

    logger.info('****************************************************************************************************')
    logger.info(f'Results for validation set')
    validation_r2_score = evaluate_model(model, X_validation, Y_validation)

    logger.info('****************************************************************************************************')
    logger.info(f'Results for whole dataset')
    evaluate_model(model, X, y)

    return model, validation_r2_score


def get_model_and_predictions_from_dataset(dataset, ):
    tren_typ_name = dataset.columns[-1]
    training_dataset = dataset.loc[dataset[tren_typ_name] > 0]
    print_dataset_info(training_dataset, tren_typ_name)
    X, y, X_train, X_validation, Y_train, Y_validation = split_dataset(training_dataset)

    cross_val_results = models_cross_validation(X_train, Y_train)

    best_model = max(cross_val_results, key=lambda p: p[2])
    logger.info(f'Best model: {best_model[0]}')
    model = best_model[1]
    model, validation_r2_score = fit_and_evaluate_model(model, X_train, Y_train, X_validation, Y_validation, X, y)

    logger.info('****************************************************************************************************')
    all_rows = dataset.values[:, 1:-1]
    logger.info(f'Describe each attribute\n{dataset.describe()}')

    all_predictions = model.predict(all_rows)
    return best_model + (validation_r2_score,), all_predictions, cross_val_results


def make_predictions(input_ds, output_ds, *, pred_column_name, columns_to_drop=None, id_columns=None):
    id_columns = id_columns or ['id']
    columns_to_drop = columns_to_drop or []
    input_ds = input_ds.drop(columns_to_drop, axis=1)
    training_ds = input_ds.drop(id_columns, axis=1)
    model_tuple, all_predictions, cross_val_results = get_model_and_predictions_from_dataset(training_ds, )

    df_predictions = pd.DataFrame({pred_column_name: all_predictions})
    df_predictions_id = pd.concat([input_ds.loc[:, id_columns], df_predictions], axis=1, sort=False)

    precision_output.output_precision(pred_column_name, cross_val_results, model_tuple)
    return output_ds.merge(df_predictions_id.set_index(id_columns), left_on=id_columns, right_on=id_columns, how='inner')


def split_category_columns(data_frame, category_columns):
    return pd.get_dummies(data_frame, columns=category_columns, dtype='bool')


def move_columns_back(data_frame, last_columns):
    return pd.concat([data_frame.drop(last_columns, axis=1), data_frame[last_columns]], axis=1, sort=False)
