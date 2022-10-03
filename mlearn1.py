# https://machinelearningmastery.com/machine-learning-in-python-step-by-step/

# compare algorithms
import pandas as pd
import logging
import settings
import sqlalchemy

from mlearn import mlearn_util, precision_output

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
select cv.sxy_id,
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
ascii(t.type) - ascii('A') + 1 as tren_typ_6,
case
    when t.type in ('A', 'B', 'C') then 1
    when t.type in ('D', 'E', 'F') then 2
    end as tren_typ_2
from cell_values cv left join
     cell_training t on t.sxy_id = cv.sxy_id
where cv.builtup_area_bc23b0_brno > 500
  and cv.access_city_center_public_transport_8_lvls_5db20f_brno is not null
;''', con=sql_engine)

precision_output.prepare_csv_output()

# Predicting 6 chronotopes
all_rows_ds_6 = all_rows_ds_full.drop(['tren_typ_2'], axis=1)
model_6, all_predictions_6, cross_val_results_6 = mlearn_util.get_model_and_predictions_from_dataset(all_rows_ds_6, model_name='LDA',)

df_chronotyp_6 = pd.DataFrame({'predikce_6': all_predictions_6})
df_predictions_6 = pd.concat([all_rows_ds_6.loc[:, ['sxy_id']], df_chronotyp_6], axis=1, sort=False)

precision_output.output_precision('Prediction_6', 'Brno', cross_val_results_6, model_6)

# Predicting 2 main chronotopes
all_rows_ds_2 = all_rows_ds_full.drop(['tren_typ_6'], axis=1)
model_2, all_predictions_2, cross_val_results_2 = mlearn_util.get_model_and_predictions_from_dataset(all_rows_ds_2, model_name='NB')

df_chronotyp_2 = pd.DataFrame({'predikce_2': all_predictions_2})
df_predictions_2 = pd.concat([all_rows_ds_2.loc[:, ['sxy_id']], df_chronotyp_2], axis=1, sort=False)

precision_output.output_precision('Prediction_2', 'Brno', cross_val_results_2, model_2)

joined_df = all_rows_ds_full.join(df_predictions_6.set_index('sxy_id'), on='sxy_id', how='left').join(df_predictions_2.set_index('sxy_id'), on='sxy_id', how='left')

with sql_engine.connect() as con:
    con.execute("DROP TABLE IF EXISTS joint_rows_predictions CASCADE;")

joined_df.to_sql("joint_rows_predictions", sql_engine)

with sql_engine.connect() as con:
    with open("data/predictions-views.sql") as file:
        query = sqlalchemy.text(file.read())
        con.execute(query)

logger.info('****************************************************************************************************')
logger.info(f'Best model for tren_typ_6: {model_6[0]}')
logger.info(f'accuracy_score for tren_typ_6={model_6[-1]}')
logger.info(f'Best model for tren_typ_2: {model_2[0]}')
logger.info(f'accuracy_score for tren_typ_2={model_2[-1]}')
