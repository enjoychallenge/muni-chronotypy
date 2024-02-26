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
grocery_fit_data_raw = pd.read_sql('''
select
'train' set,
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
gs.hour,
gs.popularity
from grocery_stores_geom gs inner join
     cell_values_geom cv on (gs.sxy_id = cv.sxy_id)
where gs.popularity > 0
union all
select
'eval',
cv.accessbility_public_transport_7_level_4b067d_bmo,
cv.number_of_accidents_in_the_daytime_40a49b_bmo,
cv.number_of_accidents_in_the_nighttime_062631_bmo,
cv.us_res_pop_high_edu_lvl_tertiary_hier_profes_schools_5ea7da_bmo,
cv.us_res_pop_high_edu_lvl_primary_or_incomplete_a68b58_bmo,
cv.us_res_pop_high_edu_lvl_secondary_graduated_f9c74f_bmo,
cv.acces_city_center_public_transport_9_levels_be96f2_jmk,
cv.general_services_accessibility_f42fff_jmk,
cv.number_of_pv_power_stations_b61301_jmk,
cv.pv_power_stations_capacity_31a2ed_jmk,
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
cv.number_of_inhab_flats_in_family_houses_55aa2b_jmk,
cv.number_of_inhab_flats_in_prefab_apartment_build_bdfcdf_jmk,
cv.usually_resident_population_e15d37_jmk,
cv.usually_resident_population_age_20_24_521338_jmk,
cv.usually_resident_population_age_65_plus_c662c6_jmk,
cv.us_res_pop_high_edu_lvl_no_education_622c58_jmk,
gs.ogc_fid rowid,
gs.cid cid,
'Grocery store' category_name,
days_tab.day,
hour_tab.hour,
null popularity
from unknown_grocery_stores gs inner join
     cell_values_geom cv on ST_Contains(cv.geom, st_transform(gs.wkb_geometry, 3035)),
     (select day from generate_series(0, 6) day) days_tab,
     (select hour from generate_series(0, 23) hour) hour_tab
where hour_tab.hour >= gs.first_hour
  and hour_tab.hour <= gs.last_hour
;''', con=sql_engine)

training_column = 'popularity'
last_columns = [training_column]
columns_to_split = ['landcover_39feb2', 'category_name', 'day']
id_columns = ['rowid', 'cid']
pred_column_name = f'pred_{training_column}'
group_columns = ['cid']

grocery_fit_data_all = mlearn_util.move_columns_back(
    mlearn_util.split_category_columns(grocery_fit_data_raw, columns_to_split),
    last_columns
)
grocery_fit_data_train = grocery_fit_data_all[grocery_fit_data_all['set'] == 'train'].drop(columns=['set'])

logger.info('****************************************************************************************************')
logger.info('Learning')
logger.info('****************************************************************************************************')
logger.info(f"shape={grocery_fit_data_train.shape}")

joined_df, model_tuple = mlearn_util.make_predictions(input_ds=grocery_fit_data_train,
                                                      output_ds=grocery_fit_data_train,
                                                      pred_column_name=pred_column_name,
                                                      columns_to_drop=[],
                                                      id_columns=id_columns,
                                                      group_columns=group_columns,
                                                      )

logger.info('****************************************************************************************************')
logger.info('Creating output all_with_predictions')

with sql_engine.connect() as con:
    con.execute("DROP TABLE IF EXISTS all_with_predictions CASCADE;")

joined_df.to_sql("all_with_predictions", sql_engine)

logger.info('Creating output all_predictions_geom')

with sql_engine.connect() as con:
    query = f'''
DROP table IF EXISTS all_predictions_geom;
create table all_predictions_geom
AS
with tmp_pred as (
    select gs.cid,
           gs.day,
           gs.hour_idx,
           gs.category_name,
           p.popularity as pplr,
           p.pred_popularity as pred_pplr,
           abs(p.pred_popularity - p.popularity) as pred_err,
           gs.geom,
           p.evaluation
    from all_with_predictions p
        inner join grocery_stores_geom gs on gs.rowid = p.rowid
    order by cid, day, hour_idx
)
select
    cid,
    category_name category,
    sum(case when evaluation then 1 else 0 end) evaluation_cnt,
    count(*) records,
    count(case when pred_err = 0 then null else pred_err end) cnt_errors,
    ROUND(sum(pred_err) * 1000 / count(*)) / 1000 avg_err,
    min(pred_err) min_err,
    max(pred_err) max_err,
    geom
from tmp_pred
group by cid, category_name, geom
order by avg_err
'''
    con.execute(query)

logger.info('Creating output all_predictions_csv')

with sql_engine.connect() as con:
    query = f'''
DROP table IF EXISTS all_predictions_csv;
create table all_predictions_csv
AS
with tmp_pred as (
select gs.cid::varchar,
       gs.day,
       gs.hour_idx,
       gs.category_name,
       p.evaluation,
       p.popularity as pplr,
       p.pred_popularity as pred_pplr,
       abs(p.pred_popularity - p.popularity) as pred_err,
       gs.geom
from all_with_predictions p inner join
    grocery_stores_geom gs on gs.rowid = p.rowid
)
select gs.cid::varchar,
       gs.day,
       gs.category_name category,
       'pplr' type,
       count(*) records,
       NULL evaluation_cnt,
       NULL evaluation_hour_idxs,
       NULL cnt_errors,
       NULL avg_err,
       NULL min_err,
       NULL max_err,
       max(gs.pplr) filter (where gs.hour_idx = 0) pplr_4,
       max(gs.pplr) filter (where gs.hour_idx = 1) pplr_5,
       max(gs.pplr) filter (where gs.hour_idx = 2) pplr_6,
       max(gs.pplr) filter (where gs.hour_idx = 3) pplr_7,
       max(gs.pplr) filter (where gs.hour_idx = 4) pplr_8,
       max(gs.pplr) filter (where gs.hour_idx = 5) pplr_9,
       max(gs.pplr) filter (where gs.hour_idx = 6) pplr_10,
       max(gs.pplr) filter (where gs.hour_idx = 7) pplr_11,
       max(gs.pplr) filter (where gs.hour_idx = 8) pplr_12,
       max(gs.pplr) filter (where gs.hour_idx = 9) pplr_13,
       max(gs.pplr) filter (where gs.hour_idx = 10) pplr_14,
       max(gs.pplr) filter (where gs.hour_idx = 11) pplr_15,
       max(gs.pplr) filter (where gs.hour_idx = 12) pplr_16,
       max(gs.pplr) filter (where gs.hour_idx = 13) pplr_17,
       max(gs.pplr) filter (where gs.hour_idx = 14) pplr_18,
       max(gs.pplr) filter (where gs.hour_idx = 15) pplr_19,
       max(gs.pplr) filter (where gs.hour_idx = 16) pplr_20,
       max(gs.pplr) filter (where gs.hour_idx = 17) pplr_21,
       max(gs.pplr) filter (where gs.hour_idx = 18) pplr_22,
       max(gs.pplr) filter (where gs.hour_idx = 19) pplr_23,
       max(gs.pplr) filter (where gs.hour_idx = 20) pplr_0,
       max(gs.pplr) filter (where gs.hour_idx = 21) pplr_1,
       max(gs.pplr) filter (where gs.hour_idx = 22) pplr_2,
       max(gs.pplr) filter (where gs.hour_idx = 23) pplr_3
from tmp_pred gs
group by gs.cid,
         gs.category_name,
         gs.day
union all
select gs.cid::varchar,
       gs.day,
       gs.category_name category,
       'pred_pplr',
       count(*) records,
       sum(case when evaluation then 1 else 0 end) evaluation_cnt,
       STRING_AGG(case when evaluation then hour_idx::varchar end, ',' order by hour_idx asc) evaluation_hour_idxs,
       count(case when gs.pred_err = 0 then null else gs.pred_err end) cnt_errors,
       ROUND(sum(gs.pred_err) * 1000 / count(*)) / 1000 avg_err,
       min(gs.pred_err) min_err,
       max(gs.pred_err) max_err,
       max(gs.pred_pplr) filter (where gs.hour_idx = 0) pred_pplr_4,
       max(gs.pred_pplr) filter (where gs.hour_idx = 1) pred_pplr_5,
       max(gs.pred_pplr) filter (where gs.hour_idx = 2) pred_pplr_6,
       max(gs.pred_pplr) filter (where gs.hour_idx = 3) pred_pplr_7,
       max(gs.pred_pplr) filter (where gs.hour_idx = 4) pred_pplr_8,
       max(gs.pred_pplr) filter (where gs.hour_idx = 5) pred_pplr_9,
       max(gs.pred_pplr) filter (where gs.hour_idx = 6) pred_pplr_10,
       max(gs.pred_pplr) filter (where gs.hour_idx = 7) pred_pplr_11,
       max(gs.pred_pplr) filter (where gs.hour_idx = 8) pred_pplr_12,
       max(gs.pred_pplr) filter (where gs.hour_idx = 9) pred_pplr_13,
       max(gs.pred_pplr) filter (where gs.hour_idx = 10) pred_pplr_14,
       max(gs.pred_pplr) filter (where gs.hour_idx = 11) pred_pplr_15,
       max(gs.pred_pplr) filter (where gs.hour_idx = 12) pred_pplr_16,
       max(gs.pred_pplr) filter (where gs.hour_idx = 13) pred_pplr_17,
       max(gs.pred_pplr) filter (where gs.hour_idx = 14) pred_pplr_18,
       max(gs.pred_pplr) filter (where gs.hour_idx = 15) pred_pplr_19,
       max(gs.pred_pplr) filter (where gs.hour_idx = 16) pred_pplr_20,
       max(gs.pred_pplr) filter (where gs.hour_idx = 17) pred_pplr_21,
       max(gs.pred_pplr) filter (where gs.hour_idx = 18) pred_pplr_22,
       max(gs.pred_pplr) filter (where gs.hour_idx = 19) pred_pplr_23,
       max(gs.pred_pplr) filter (where gs.hour_idx = 20) pred_pplr_0,
       max(gs.pred_pplr) filter (where gs.hour_idx = 21) pred_pplr_1,
       max(gs.pred_pplr) filter (where gs.hour_idx = 22) pred_pplr_2,
       max(gs.pred_pplr) filter (where gs.hour_idx = 23) pred_pplr_3
from tmp_pred gs
group by gs.cid,
         gs.category_name,
         gs.day
order by cid, day, type
'''
    con.execute(query)

logger.info('****************************************************************************************************')
logger.info('Predicting')
logger.info('')
unknown_grocery_raw = grocery_fit_data_all.loc[grocery_fit_data_all['set'] == 'eval'].drop(columns=['set'])
df_unknown_predictions_raw = unknown_grocery_raw.copy()
unknown_grocery = unknown_grocery_raw.drop(columns=id_columns).values[:, :-1]

all_unknown_predictions = model_tuple[1].predict(unknown_grocery)
df_all_unknown_predictions = pd.DataFrame({pred_column_name: all_unknown_predictions})

df_unknown_predictions_raw[pred_column_name] = all_unknown_predictions
df_unknown_predictions = df_unknown_predictions_raw.loc[:, id_columns + ['day_0', 'day_1', 'day_2', 'day_3', 'day_4', 'day_5', 'day_6',
                                                                         'hour', pred_column_name]]

with sql_engine.connect() as con:
    con.execute("DROP TABLE IF EXISTS unknown_predictions_raw CASCADE;")

df_unknown_predictions.to_sql("unknown_predictions_raw", sql_engine)

with sql_engine.connect() as con:
    query = f'''
DROP table IF EXISTS unknown_predictions_geom;
create table unknown_predictions_geom
as
with pred_tmp as (
select pred.*,
       case when pred.day_0 then 0
             when pred.day_1 then 1
             when pred.day_2 then 2
             when pred.day_3 then 3
             when pred.day_4 then 4
             when pred.day_5 then 5
             when pred.day_6 then 6
           end as day
from unknown_predictions_raw pred
)
select gs.cid::varchar,
       gs.name,
       gs.open_hours,
       gs.wkb_geometry,
       pred.day,
       max(pred.pred_popularity) filter (where pred.hour = 0) pred_pplr_0,
       max(pred.pred_popularity) filter (where pred.hour = 1) pred_pplr_1,
       max(pred.pred_popularity) filter (where pred.hour = 2) pred_pplr_2,
       max(pred.pred_popularity) filter (where pred.hour = 3) pred_pplr_3,
       max(pred.pred_popularity) filter (where pred.hour = 4) pred_pplr_4,
       max(pred.pred_popularity) filter (where pred.hour = 5) pred_pplr_5,
       max(pred.pred_popularity) filter (where pred.hour = 6) pred_pplr_6,
       max(pred.pred_popularity) filter (where pred.hour = 7) pred_pplr_7,
       max(pred.pred_popularity) filter (where pred.hour = 8) pred_pplr_8,
       max(pred.pred_popularity) filter (where pred.hour = 9) pred_pplr_9,
       max(pred.pred_popularity) filter (where pred.hour = 10) pred_pplr_10,
       max(pred.pred_popularity) filter (where pred.hour = 11) pred_pplr_11,
       max(pred.pred_popularity) filter (where pred.hour = 12) pred_pplr_12,
       max(pred.pred_popularity) filter (where pred.hour = 13) pred_pplr_13,
       max(pred.pred_popularity) filter (where pred.hour = 14) pred_pplr_14,
       max(pred.pred_popularity) filter (where pred.hour = 15) pred_pplr_15,
       max(pred.pred_popularity) filter (where pred.hour = 16) pred_pplr_16,
       max(pred.pred_popularity) filter (where pred.hour = 17) pred_pplr_17,
       max(pred.pred_popularity) filter (where pred.hour = 18) pred_pplr_18,
       max(pred.pred_popularity) filter (where pred.hour = 19) pred_pplr_19,
       max(pred.pred_popularity) filter (where pred.hour = 20) pred_pplr_20,
       max(pred.pred_popularity) filter (where pred.hour = 21) pred_pplr_21,
       max(pred.pred_popularity) filter (where pred.hour = 22) pred_pplr_22,
       max(pred.pred_popularity) filter (where pred.hour = 23) pred_pplr_23
from unknown_grocery_stores gs inner join
     pred_tmp pred on pred.cid = gs.cid

group by gs.cid,
         gs.name,
         pred.day,
         gs.open_hours,
         gs.wkb_geometry
order by cid, day
;'''
    con.execute(query)

    query = """
INSERT INTO all_predictions_csv (
    cid, day, category, type, records, evaluation_cnt, evaluation_hour_idxs, cnt_errors, avg_err, min_err, max_err,
    pplr_4, pplr_5, pplr_6, pplr_7, pplr_8, pplr_9, pplr_10, pplr_11, pplr_12, pplr_13, pplr_14, pplr_15, pplr_16,
    pplr_17, pplr_18, pplr_19, pplr_20, pplr_21, pplr_22, pplr_23, pplr_0, pplr_1, pplr_2, pplr_3
)
select name, day, 'Grocery store' as category, 'pred_pplr' as type,
       null, null, null, null, null, null, null,
       pred_pplr_4, pred_pplr_5, pred_pplr_6, pred_pplr_7, pred_pplr_8, pred_pplr_9, pred_pplr_10, pred_pplr_11,
       pred_pplr_12, pred_pplr_13, pred_pplr_14, pred_pplr_15, pred_pplr_16, pred_pplr_17, pred_pplr_18, pred_pplr_19,
       pred_pplr_20, pred_pplr_21, pred_pplr_22, pred_pplr_23, pred_pplr_0, pred_pplr_1, pred_pplr_2, pred_pplr_3
from unknown_predictions_geom
"""
    con.execute(query)

logger.info('****************************************************************************************************')
