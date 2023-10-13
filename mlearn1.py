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
-- cv.accessbility_public_transport_7_level_4b067d_bmo,
-- number_of_accidents_0358cb_bmo,
-- cv.number_of_accidents_in_the_daytime_40a49b_bmo,
-- cv.number_of_accidents_in_the_nighttime_062631_bmo,
-- cv.number_of_deaths_caused_by_accidents_b18286_bmo,
-- cv.number_of_serious_injuries_caused_by_accidents_e0c176_bmo,
-- cv.number_of_slight_injuries_caused_by_accidents_001947_bmo,
-- us_res_pop_high_edu_lvl_tertiary_hier_profes_schools_5ea7da_bmo,
-- us_res_pop_high_edu_lvl_primary_or_incomplete_a68b58_bmo,
-- us_res_pop_high_edu_lvl_secondary_graduated_f9c74f_bmo,
cv.acces_city_center_public_transport_9_levels_be96f2_jmk,
cv.general_services_accessibility_f42fff_jmk,
cv.number_of_pv_power_stations_b61301_jmk,
cv.pv_power_stations_capacity_31a2ed_jmk,
-- landcover_urban_atlas_3level_change_adfa93_jmk,
cv.elevation_07eb7d_jmk,
cv.landcover_urban_atlas_3level_39feb2_jmk,
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
;''', con=sql_engine)

# ds_garmin_fit_data_columns = list(ds_garmin_fit_data.columns)
# ds_garmin_fit_data[ds_garmin_fit_data_columns] = ds_garmin_fit_data[ds_garmin_fit_data_columns].fillna(0)

training_column = 'popularity'

last_columns = [training_column]

grocery_fit_data = mlearn_util.move_columns_back(
    mlearn_util.split_category_columns(grocery_fit_data_raw, ['category_name', 'day']),
    last_columns
)

logger.info('****************************************************************************************************')
logger.info('Learning')
logger.info('****************************************************************************************************')
logger.info(f"shape={grocery_fit_data.shape}")

joined_df = mlearn_util.make_predictions(input_ds=grocery_fit_data,
                                         output_ds=grocery_fit_data,
                                         pred_column_name=f'pred_{training_column}',
                                         columns_to_drop=[],
                                         id_columns=['rowid', 'cid'],
                                         )

with sql_engine.connect() as con:
    con.execute("DROP TABLE IF EXISTS all_with_predictions CASCADE;")

joined_df.to_sql("all_with_predictions", sql_engine)

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
           gs.geom
    from all_with_predictions p
        inner join grocery_stores_geom gs on gs.rowid = p.rowid
    order by cid, day, hour_idx
)
select
    cid,
    category_name,
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

# ds_check_results = pd.read_sql('''
# select count(*)
#  cnt_rows,
#        count(heart_rate_avg_perc) cnt_heart_rate_avg_perc,
#        count(pred_heart_rate_avg_perc) cnt_pred_heart_rate_avg_perc
# from all_with_predictions
# ;''', con=sql_engine)

# assert ds_check_results['cnt_rows'][0] == 12888, f'ds_check_results={ds_check_results}'
# assert ds_check_results['cnt_heart_rate_avg_perc'][0] == 12888, f'ds_check_results={ds_check_results}'
# assert ds_check_results['cnt_pred_heart_rate_avg_perc'][0] == 12888, f'ds_check_results={ds_check_results}'

precision_output.output_stats()
logger.info('****************************************************************************************************')
