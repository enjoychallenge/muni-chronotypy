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
all_rows_ds_full = pd.read_sql('''
select t.sxy_id,
-- resident_population_91c66b_brno,
access_city_center_public_transport_8_lvls_5db20f_brno,
builtup_area_bc23b0_brno,
builtup_area_5_level_d21689_brno,
emotion_dontlike_3b56cb_brno,
emotion_like_aff639_brno,
emotion_missing_62c4e1_brno,
pm10_c8a0c3_brno,
vegetation_index_7_level_95bb86_brno,
park_greenery_area_dece19_brno,
-- elevation_1b8a79_brno,
landcover_urban_atlas_69ef7e_brno,
road_street_path_length_d64419_brno,
number_of_accidents_f42092_brno,
-- number_of_accidents_in_the_daytime_6f4d22_brno,
-- number_of_accidents_in_the_nighttime_5655a5_brno,
number_of_deaths_caused_by_accidents_e2a6d5_brno,
occupied_jobs_e64c61_brno,
number_of_offences_57a7b1_brno,
-- number_of_offences_aa7492_brno,
number_of_retail_grocery_shops_c873fa_brno,
number_of_serious_injuries_caused_by_accidents_01bcff_brno,
-- number_of_service_facilities_85921e_brno,
number_of_retail_shops_801f27_brno,
number_of_slight_injuries_caused_by_accidents_cdd154_brno,
retail_sales_area_65f9a7_brno,
accessbility_public_transport_7_level_4b067d_bmo,
-- number_of_accidents_0358cb_bmo,
number_of_accidents_in_the_daytime_40a49b_bmo,
number_of_accidents_in_the_nighttime_062631_bmo,
number_of_deaths_caused_by_accidents_b18286_bmo,
number_of_serious_injuries_caused_by_accidents_e0c176_bmo,
number_of_slight_injuries_caused_by_accidents_001947_bmo,
-- us_res_pop_high_edu_lvl_tertiary_hier_profes_schools_5ea7da_bmo,
-- us_res_pop_high_edu_lvl_primary_or_incomplete_a68b58_bmo,
-- us_res_pop_high_edu_lvl_secondary_graduated_f9c74f_bmo,
acces_city_center_public_transport_9_levels_be96f2_jmk,
general_services_accessibility_f42fff_jmk,
number_of_pv_power_stations_b61301_jmk,
pv_power_stations_capacity_31a2ed_jmk,
landcover_urban_atlas_3level_change_adfa93_jmk,
elevation_07eb7d_jmk,
landcover_urban_atlas_3level_39feb2_jmk,
road_street_length_4d64b2_jmk,
number_of_accidents_f02900_jmk,
number_of_flats_built_1920_1945_cee901_jmk,
number_of_flats_built_1946_1960_3b06c3_jmk,
number_of_flats_built_1961_1970_c4552c_jmk,
number_of_flats_built_1971_1980_5da6fe_jmk,
number_of_flats_built_1981_1990_927a67_jmk,
number_of_flats_built_1991_2000_064593_jmk,
number_of_flats_built_2001_2011_5500d8_jmk,
number_of_flats_built_till_1919_d7a5f9_jmk,
-- number_of_inhab_flats_0d42ff_jmk,
-- number_of_inhab_flats_in_apartment_buildings_67a645_jmk,
number_of_inhab_flats_in_family_houses_55aa2b_jmk,
number_of_inhab_flats_in_prefab_apartment_build_bdfcdf_jmk,
usually_resident_population_e15d37_jmk,
-- usually_resident_population_age_0_5_d6ffb6_jmk,
-- usually_resident_population_age_15_19_d67e77_jmk,
usually_resident_population_age_20_24_521338_jmk,
-- usually_resident_population_age_25_29_0917ac_jmk,
-- usually_resident_population_age_30_34_cab1af_jmk,
-- usually_resident_population_age_35_39_3e3752_jmk,
-- usually_resident_population_age_40_44_8f2992_jmk,
-- usually_resident_population_age_45_49_0c4c2d_jmk,
-- usually_resident_population_age_50_54_a68966_jmk,
-- usually_resident_population_age_55_59_e10179_jmk,
-- usually_resident_population_age_60_64_cca04e_jmk,
usually_resident_population_age_65_plus_c662c6_jmk,
-- usually_resident_population_age_6_14_ebdbce_jmk,
-- us_res_pop_highedulvl_sec_grad_or_tert_prof_schols_efeb42_jmk,
us_res_pop_high_edu_lvl_no_education_622c58_jmk,
-- us_res_pop_high_edu_lvl_primary_89a90c_jmk,
-- us_res_pop_high_edu_lvl_secondary_not_graduated_df1937_jmk,
-- us_res_pop_high_edu_lvl_tertiary_university_d9de47_jmk,
ascii(t.type) - ascii('A') + 1 type
from cell_training t inner join
     cell_values cv on t.sxy_id = cv.sxy_id
where cv.resident_population_91c66b_brno is not null
  and cv.access_city_center_public_transport_8_lvls_5db20f_brno is not null
;''', con=sql_engine)

all_rows_ds = all_rows_ds_full

dataset = all_rows_ds.copy()

# logger.info(f"  Scattering matrix")
# scatter_matrix(dataset)
# logger.info(f"  Showing pyplot")
# pyplot.show()

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
logger.info(f'Results for validation set')
model.fit(X_train, Y_train)
predictions = model.predict(X_validation)

logger.info(f'accuracy_score={accuracy_score(Y_validation, predictions)}')
logger.info(f'confusion_matrix=\n{confusion_matrix(Y_validation, predictions)}')
logger.info(f'classification_report=\n{classification_report(Y_validation, predictions)}')

logger.info('****************************************************************************************************')
logger.info(f'Results for whole dataset')
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
