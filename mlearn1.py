# https://machinelearningmastery.com/machine-learning-in-python-step-by-step/

# compare algorithms
import numpy as np
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

with sql_engine.connect() as con:
    query = f'''
DROP MATERIALIZED VIEW IF EXISTS grocery_stores_grouped_geom CASCADE;
CREATE MATERIALIZED VIEW grocery_stores_grouped_geom
AS
select ROW_NUMBER() OVER (ORDER BY (SELECT 1)) AS rowid,
       cid::varchar,
       day,
       min(category_name) category_name,
       min(geom) geom,
       min(sxy_id) sxy_id
from grocery_stores_geom
group by cid, day
'''
    con.execute(query)

# Load dataset
logger.info(f"  Reading from DB")
grocery_fit_data_raw = pd.read_sql('''
select
-- resident_population_91c66b_brno,
-- cv.access_city_center_public_transport_8_lvls_5db20f_brno,
-- cv.builtup_area_bc23b0_brno,
-- cv.builtup_area_5_level_d21689_brno,
-- cv.emotion_dontlike_3b56cb_brno,
-- cv.emotion_like_aff639_brno,
-- cv.emotion_missing_62c4e1_brno,
-- cv.pm10_c8a0c3_brno,
-- cv.vegetation_index_7_level_95bb86_brno,
-- cv.park_greenery_area_dece19_brno,
-- elevation_1b8a79_brno,
-- cv.landcover_urban_atlas_69ef7e_brno,
-- cv.road_street_path_length_d64419_brno,
-- cv.number_of_accidents_f42092_brno,
-- number_of_accidents_in_the_daytime_6f4d22_brno,
-- number_of_accidents_in_the_nighttime_5655a5_brno,
-- cv.number_of_deaths_caused_by_accidents_e2a6d5_brno,
-- cv.occupied_jobs_e64c61_brno,
-- cv.number_of_offences_57a7b1_brno,
-- number_of_offences_aa7492_brno,
-- cv.number_of_retail_grocery_shops_c873fa_brno,
-- cv.number_of_serious_injuries_caused_by_accidents_01bcff_brno,
-- number_of_service_facilities_85921e_brno,
-- cv.number_of_retail_shops_801f27_brno,
-- cv.number_of_slight_injuries_caused_by_accidents_cdd154_brno,
-- cv.retail_sales_area_65f9a7_brno,
cv.accessbility_public_transport_7_level_4b067d_bmo,
-- cv.number_of_accidents_0358cb_bmo,
cv.number_of_accidents_in_the_daytime_40a49b_bmo,
cv.number_of_accidents_in_the_nighttime_062631_bmo,
-- cv.number_of_deaths_caused_by_accidents_b18286_bmo,
-- cv.number_of_serious_injuries_caused_by_accidents_e0c176_bmo,
-- cv.number_of_slight_injuries_caused_by_accidents_001947_bmo,
cv.us_res_pop_high_edu_lvl_tertiary_hier_profes_schools_5ea7da_bmo,
cv.us_res_pop_high_edu_lvl_primary_or_incomplete_a68b58_bmo,
cv.us_res_pop_high_edu_lvl_secondary_graduated_f9c74f_bmo,
cv.acces_city_center_public_transport_9_levels_be96f2_jmk,
cv.general_services_accessibility_f42fff_jmk,
cv.number_of_pv_power_stations_b61301_jmk,
cv.pv_power_stations_capacity_31a2ed_jmk,
-- landcover_urban_atlas_3level_change_adfa93_jmk,
cv.elevation_07eb7d_jmk,
cv.landcover_urban_atlas_3level_39feb2_jmk as landcover_39feb2,
cv.road_street_length_4d64b2_jmk,
cv.number_of_accidents_f02900_jmk,
cv.number_of_flats_built_1920_1945_cee901_jmk,
cv.number_of_flats_built_1946_1960_3b06c3_jmk,
cv.number_of_flats_built_1961_1970_c4552c_jmk,
cv.number_of_flats_built_1971_1980_5da6fe_jmk,
cv.number_of_flats_built_1981_1990_927a67_jmk,
cv.number_of_flats_built_1991_2000_064593_jmk,
cv.number_of_flats_built_2001_2011_5500d8_jmk,
cv.number_of_flats_built_till_1919_d7a5f9_jmk,
-- number_of_inhab_flats_0d42ff_jmk,
-- number_of_inhab_flats_in_apartment_buildings_67a645_jmk,
cv.number_of_inhab_flats_in_family_houses_55aa2b_jmk,
cv.number_of_inhab_flats_in_prefab_apartment_build_bdfcdf_jmk,
cv.usually_resident_population_e15d37_jmk,
-- usually_resident_population_age_0_5_d6ffb6_jmk,
-- usually_resident_population_age_15_19_d67e77_jmk,
cv.usually_resident_population_age_20_24_521338_jmk,
-- usually_resident_population_age_25_29_0917ac_jmk,
-- usually_resident_population_age_30_34_cab1af_jmk,
-- usually_resident_population_age_35_39_3e3752_jmk,
-- usually_resident_population_age_40_44_8f2992_jmk,
-- usually_resident_population_age_45_49_0c4c2d_jmk,
-- usually_resident_population_age_50_54_a68966_jmk,
-- usually_resident_population_age_55_59_e10179_jmk,
-- usually_resident_population_age_60_64_cca04e_jmk,
cv.usually_resident_population_age_65_plus_c662c6_jmk,
-- usually_resident_population_age_6_14_ebdbce_jmk,
-- us_res_pop_highedulvl_sec_grad_or_tert_prof_schols_efeb42_jmk,
cv.us_res_pop_high_edu_lvl_no_education_622c58_jmk,
-- us_res_pop_high_edu_lvl_primary_89a90c_jmk,
-- us_res_pop_high_edu_lvl_secondary_not_graduated_df1937_jmk,
-- us_res_pop_high_edu_lvl_tertiary_university_d9de47_jmk,
gs.rowid,
gs.cid,
gs.category_name,
gs.day,
(select max(gsg.popularity) from grocery_stores_geom gsg where gsg.cid = gs.cid and gsg.day = gs.day and gsg.hour_idx = 0)::float8 pplr_0,
(select max(gsg.popularity) from grocery_stores_geom gsg where gsg.cid = gs.cid and gsg.day = gs.day and gsg.hour_idx = 1)::float8 pplr_1,
(select max(gsg.popularity) from grocery_stores_geom gsg where gsg.cid = gs.cid and gsg.day = gs.day and gsg.hour_idx = 2)::float8 pplr_2,
(select max(gsg.popularity) from grocery_stores_geom gsg where gsg.cid = gs.cid and gsg.day = gs.day and gsg.hour_idx = 3)::float8 pplr_3,
(select max(gsg.popularity) from grocery_stores_geom gsg where gsg.cid = gs.cid and gsg.day = gs.day and gsg.hour_idx = 4)::float8 pplr_4,
(select max(gsg.popularity) from grocery_stores_geom gsg where gsg.cid = gs.cid and gsg.day = gs.day and gsg.hour_idx = 5)::float8 pplr_5,
(select max(gsg.popularity) from grocery_stores_geom gsg where gsg.cid = gs.cid and gsg.day = gs.day and gsg.hour_idx = 6)::float8 pplr_6,
(select max(gsg.popularity) from grocery_stores_geom gsg where gsg.cid = gs.cid and gsg.day = gs.day and gsg.hour_idx = 7)::float8 pplr_7,
(select max(gsg.popularity) from grocery_stores_geom gsg where gsg.cid = gs.cid and gsg.day = gs.day and gsg.hour_idx = 8)::float8 pplr_8,
(select max(gsg.popularity) from grocery_stores_geom gsg where gsg.cid = gs.cid and gsg.day = gs.day and gsg.hour_idx = 9)::float8 pplr_9,
(select max(gsg.popularity) from grocery_stores_geom gsg where gsg.cid = gs.cid and gsg.day = gs.day and gsg.hour_idx = 10)::float8 pplr_10,
(select max(gsg.popularity) from grocery_stores_geom gsg where gsg.cid = gs.cid and gsg.day = gs.day and gsg.hour_idx = 11)::float8 pplr_11,
(select max(gsg.popularity) from grocery_stores_geom gsg where gsg.cid = gs.cid and gsg.day = gs.day and gsg.hour_idx = 12)::float8 pplr_12,
(select max(gsg.popularity) from grocery_stores_geom gsg where gsg.cid = gs.cid and gsg.day = gs.day and gsg.hour_idx = 13)::float8 pplr_13,
(select max(gsg.popularity) from grocery_stores_geom gsg where gsg.cid = gs.cid and gsg.day = gs.day and gsg.hour_idx = 14)::float8 pplr_14,
(select max(gsg.popularity) from grocery_stores_geom gsg where gsg.cid = gs.cid and gsg.day = gs.day and gsg.hour_idx = 15)::float8 pplr_15,
(select max(gsg.popularity) from grocery_stores_geom gsg where gsg.cid = gs.cid and gsg.day = gs.day and gsg.hour_idx = 16)::float8 pplr_16,
(select max(gsg.popularity) from grocery_stores_geom gsg where gsg.cid = gs.cid and gsg.day = gs.day and gsg.hour_idx = 17)::float8 pplr_17,
(select max(gsg.popularity) from grocery_stores_geom gsg where gsg.cid = gs.cid and gsg.day = gs.day and gsg.hour_idx = 18)::float8 pplr_18,
(select max(gsg.popularity) from grocery_stores_geom gsg where gsg.cid = gs.cid and gsg.day = gs.day and gsg.hour_idx = 19)::float8 pplr_19,
(select max(gsg.popularity) from grocery_stores_geom gsg where gsg.cid = gs.cid and gsg.day = gs.day and gsg.hour_idx = 20)::float8 pplr_20,
(select max(gsg.popularity) from grocery_stores_geom gsg where gsg.cid = gs.cid and gsg.day = gs.day and gsg.hour_idx = 21)::float8 pplr_21,
(select max(gsg.popularity) from grocery_stores_geom gsg where gsg.cid = gs.cid and gsg.day = gs.day and gsg.hour_idx = 22)::float8 pplr_22,
(select max(gsg.popularity) from grocery_stores_geom gsg where gsg.cid = gs.cid and gsg.day = gs.day and gsg.hour_idx = 23)::float8 pplr_23
from grocery_stores_grouped_geom gs inner join
     cell_values_geom cv on (gs.sxy_id = cv.sxy_id)
where (select percentile_disc(0) WITHIN GROUP (ORDER BY hour_idx) as opening_hour_idx from grocery_stores_geom gsg where gsg.cid = gs.cid and gsg.day = gs.day and gsg.popularity > 0) is not null
;''', con=sql_engine)

training_columns = ['pplr_0', 'pplr_1', 'pplr_2', 'pplr_3', 'pplr_4', 'pplr_5', 'pplr_6', 'pplr_7', 'pplr_8', 'pplr_9',
                    'pplr_10', 'pplr_11', 'pplr_12', 'pplr_13', 'pplr_14', 'pplr_15', 'pplr_16', 'pplr_17', 'pplr_18', 'pplr_19',
                    'pplr_20', 'pplr_21', 'pplr_22', 'pplr_23', ]

last_columns = training_columns.copy()

grocery_fit_data_raw[training_columns] = grocery_fit_data_raw[training_columns].apply(pd.to_numeric, downcast='float')

grocery_fit_data = mlearn_util.move_columns_back(
    mlearn_util.split_category_columns(grocery_fit_data_raw, ['landcover_39feb2', 'category_name']),
    last_columns
)

logger.info('****************************************************************************************************')
logger.info('Learning')
logger.info('****************************************************************************************************')
logger.info(f"shape={grocery_fit_data.shape}")

joined_df = mlearn_util.make_predictions(input_ds=grocery_fit_data,
                                         output_ds=grocery_fit_data,
                                         training_columns=training_columns,
                                         columns_to_drop=[],
                                         id_columns=['rowid', 'cid',],
                                         )

logger.info('****************************************************************************************************')
logger.info('Creating output all_with_predictions')

with sql_engine.connect() as con:
    con.execute("DROP TABLE IF EXISTS all_with_predictions CASCADE;")

joined_df.to_sql("all_with_predictions", sql_engine)

logger.info('Creating output all_predictions_geom')

# with sql_engine.connect() as con:
#     query = f'''
# DROP table IF EXISTS all_predictions_geom;
# create table all_predictions_geom
# AS
# with tmp_pred as (
#     select gs.cid,
#            gs.day,
#            gs.category_name,
#            gs.geom,
#            gs.pplr_0
#     from all_with_predictions p
#         inner join grocery_stores_grouped_geom gs on gs.cid = p.cid and gs.day = p.day
#     order by cid, day
# )
# select
#     cid,
#     category_name category,
#     24 records,
#     count(case when pred_err = 0 then null else pred_err end) cnt_errors,
#     ROUND(sum(pred_err) * 1000 / count(*)) / 1000 avg_err,
#     min(pred_err) min_err,
#     max(pred_err) max_err,
#     geom
# from all_with_predictions p
#     inner join grocery_stores_grouped_geom gs on gs.cid = p.cid and gs.day = p.day
# group by cid, category_name, geom
# order by avg_err
# '''
#     con.execute(query)
#
# logger.info('Creating output all_predictions_csv')
#
# with sql_engine.connect() as con:
#     query = f'''
# DROP table IF EXISTS all_predictions_csv;
# create table all_predictions_csv
# AS
# select gs.cid::varchar,
#        gs.day,
#        gs.category_name,
#        p.pplr_8 as pplr_8,
#        p.pplr_9 as pplr_9,
#        p.pred_pplr_8 as pred_pplr_8,
#        p.pred_pplr_9 as pred_pplr_9,
#        abs(p.pred_pplr_8 - p.pplr_8) + abs(p.pred_pplr_9 - p.pplr_9) as pred_err,
#        gs.geom
# from all_with_predictions p inner join
#     grocery_stores_grouped_geom gs on gs.cid = p.cid
#                                   and gs.day = p.day
# '''
#     con.execute(query)

logger.info('****************************************************************************************************')
