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

precision_output.prepare_csv_output()

# Load dataset
logger.info(f"  Reading from DB")
ds_bmo_bug_annotation = pd.read_sql('''
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
-- landcover_urban_atlas_3level_change_adfa93_jmk,
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
ascii(t.typ) - ascii('A') + 1 as tren_typ_6,
case
    when t.typ in ('A', 'B', 'C') then 1
    when t.typ in ('D', 'E', 'F') then 2
    end as tren_typ_2
from cell_values cv left join
     jmk_cell_chronotopes_annotations t on t.sxy_id = cv.sxy_id
order by cv.sxy_id asc
;''', con=sql_engine)

ds_bmo_ruian = pd.read_sql('''select * from cell_ruian_training''', con=sql_engine)

ds_bmo_annotated = ds_bmo_bug_annotation.join(ds_bmo_ruian.set_index('sxy_id'), on='sxy_id', how='left')

# there are missing many cells in ruian dataset (fields, forests, ...), so fill the ruian values with 0
ruian_columns = list(ds_bmo_ruian.columns)
ds_bmo_annotated[ruian_columns] = ds_bmo_annotated[ruian_columns].fillna(0)

last_columns = ['tren_typ_6', 'tren_typ_2']

brno_category_columns = ['landcover_urban_atlas_69ef7e_brno', 'landcover_urban_atlas_3level_39feb2_jmk']
ds_bmo_annotated = mlearn_util.move_columns_back(
    mlearn_util.split_category_columns(ds_bmo_annotated, brno_category_columns),
    last_columns
)

all_rows_brno_ds_full = ds_bmo_annotated.loc[(ds_bmo_annotated['builtup_area_bc23b0_brno'] > 500) & (ds_bmo_annotated['access_city_center_public_transport_8_lvls_5db20f_brno'].notnull())].reset_index(drop=True)

bmo_cols_to_drop = [col for col in ds_bmo_annotated.columns if col.endswith('brno') or col.find('_brno_') > 0]
ds_bmo_annotation_train = ds_bmo_annotated.drop(bmo_cols_to_drop, axis=1)
bmo_filtering_columns = [col for col in ds_bmo_annotated.columns if col.startswith('landcover_urban_atlas_3level_39feb2_jmk_1')]
all_rows_bmo_ds_full = ds_bmo_annotation_train.loc[ds_bmo_annotated[bmo_filtering_columns].sum(axis=1) > 0].reset_index(drop=True)

joined_df = all_rows_bmo_ds_full

logger.info('****************************************************************************************************')
logger.info('Brno')
logger.info('****************************************************************************************************')
logger.info(f"shape={all_rows_brno_ds_full.shape}")

joined_df = mlearn_util.make_predictions(input_ds=all_rows_brno_ds_full, output_ds=joined_df, pred_column_name='predikce_brno_6', area='Brno', columns_to_drop=['tren_typ_2'])

joined_df = mlearn_util.make_predictions(input_ds=all_rows_brno_ds_full, output_ds=joined_df, pred_column_name='predikce_brno_2', area='Brno', columns_to_drop=['tren_typ_6'])

logger.info('****************************************************************************************************')
logger.info('BMO')
logger.info('****************************************************************************************************')
logger.info(f"shape={all_rows_bmo_ds_full.shape}")

joined_df = mlearn_util.make_predictions(input_ds=all_rows_bmo_ds_full, output_ds=joined_df, pred_column_name='predikce_bmo_6', area='BMO', columns_to_drop=['tren_typ_2'])

joined_df = mlearn_util.make_predictions(input_ds=all_rows_bmo_ds_full, output_ds=joined_df, pred_column_name='predikce_bmo_2', area='BMO', columns_to_drop=['tren_typ_6'])

with sql_engine.connect() as con:
    con.execute("DROP TABLE IF EXISTS joint_rows_predictions CASCADE;")

joined_df.to_sql("joint_rows_predictions", sql_engine)

with sql_engine.connect() as con:
    with open("data/predictions-views.sql") as file:
        query = sqlalchemy.text(file.read())
        con.execute(query)

ds_check_results = pd.read_sql('''
select count(*)
 cnt_rows,
       count(predikce_brno_2) cnt_p_brno_2,
       count(predikce_brno_6) cnt_p_brno_6,
       count(predikce_bmo_2) cnt_p_bmo_2,
       count(predikce_bmo_6) cnt_p_bmo_6
from joint_rows_predictions
;''', con=sql_engine)

assert ds_check_results['cnt_rows'][0] == 3570, f'ds_check_results={ds_check_results}'
assert ds_check_results['cnt_p_brno_6'][0] == 1360, f'ds_check_results={ds_check_results}'
assert ds_check_results['cnt_p_brno_2'][0] == 1360, f'ds_check_results={ds_check_results}'
assert ds_check_results['cnt_p_bmo_6'][0] == 3570, f'ds_check_results={ds_check_results}'
assert ds_check_results['cnt_p_bmo_2'][0] == 3570, f'ds_check_results={ds_check_results}'

logger.info('****************************************************************************************************')
