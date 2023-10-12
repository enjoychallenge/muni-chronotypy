import logging
import numpy as np

import settings
import psycopg2.extras
import pandas as pd


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(filename)s] [%(levelname)s]:\t%(message)s')
logger = logging.getLogger(__name__)

logger.info('****************************************************************************************************')
logger.info('****************************************************************************************************')
logger.info('****************************************************************************************************')
logger.info('****************************************************************************************************')
logger.info('****************************************************************************************************')
logger.info('****************************************************************************************************')
logger.info(f"Let's import few CSV files.")
logger.info('****************************************************************************************************')

DIRECTORY = '/data/raw/'

conn = psycopg2.connect(settings.PG_CONN)

conn.autocommit = True
cursor = conn.cursor()

sql_drop = '''
DROP MATERIALIZED VIEW IF EXISTS grocery_stores_geom CASCADE;
DROP MATERIALIZED VIEW IF EXISTS cell_values_geom CASCADE;
'''
cursor.execute(sql_drop)

logger.info('\nStarting with cell_values table')

sql_drop = '''
DROP TABLE IF EXISTS cell_values;'''
cursor.execute(sql_drop)

sql_create = '''CREATE TABLE cell_values(sxy_id char(15), 
resident_population_91c66b_brno float,
access_city_center_public_transport_8_lvls_5db20f_brno float,
builtup_area_bc23b0_brno float,
builtup_area_5_level_d21689_brno float,
emotion_dontlike_3b56cb_brno float,
emotion_like_aff639_brno float,
emotion_missing_62c4e1_brno float,
pm10_c8a0c3_brno float,
vegetation_index_7_level_95bb86_brno float,
park_greenery_area_dece19_brno float,
elevation_1b8a79_brno float,
landcover_urban_atlas_69ef7e_brno float,
road_street_path_length_d64419_brno float,
number_of_accidents_f42092_brno float,
number_of_accidents_in_the_daytime_6f4d22_brno float,
number_of_accidents_in_the_nighttime_5655a5_brno float,
number_of_deaths_caused_by_accidents_e2a6d5_brno float,
occupied_jobs_e64c61_brno float,
number_of_offences_57a7b1_brno float,
number_of_offences_aa7492_brno float,
number_of_retail_grocery_shops_c873fa_brno float,
number_of_serious_injuries_caused_by_accidents_01bcff_brno float,
number_of_service_facilities_85921e_brno float,
number_of_retail_shops_801f27_brno float,
number_of_slight_injuries_caused_by_accidents_cdd154_brno float,
retail_sales_area_65f9a7_brno float,
accessbility_public_transport_7_level_4b067d_bmo float,
number_of_accidents_0358cb_bmo float,
number_of_accidents_in_the_daytime_40a49b_bmo float,
number_of_accidents_in_the_nighttime_062631_bmo float,
number_of_deaths_caused_by_accidents_b18286_bmo float,
number_of_serious_injuries_caused_by_accidents_e0c176_bmo float,
number_of_slight_injuries_caused_by_accidents_001947_bmo float,
us_res_pop_high_edu_lvl_tertiary_hier_profes_schools_5ea7da_bmo float,
us_res_pop_high_edu_lvl_primary_or_incomplete_a68b58_bmo float,
us_res_pop_high_edu_lvl_secondary_graduated_f9c74f_bmo float,
acces_city_center_public_transport_9_levels_be96f2_jmk float,
general_services_accessibility_f42fff_jmk float,
number_of_pv_power_stations_b61301_jmk float,
pv_power_stations_capacity_31a2ed_jmk float,
landcover_urban_atlas_3level_change_adfa93_jmk float,
elevation_07eb7d_jmk float,
landcover_urban_atlas_3level_39feb2_jmk float,
road_street_length_4d64b2_jmk float,
number_of_accidents_f02900_jmk float,
number_of_flats_built_1920_1945_cee901_jmk float,
number_of_flats_built_1946_1960_3b06c3_jmk float,
number_of_flats_built_1961_1970_c4552c_jmk float,
number_of_flats_built_1971_1980_5da6fe_jmk float,
number_of_flats_built_1981_1990_927a67_jmk float,
number_of_flats_built_1991_2000_064593_jmk float,
number_of_flats_built_2001_2011_5500d8_jmk float,
number_of_flats_built_till_1919_d7a5f9_jmk float,
number_of_inhab_flats_0d42ff_jmk float,
number_of_inhab_flats_in_apartment_buildings_67a645_jmk float,
number_of_inhab_flats_in_family_houses_55aa2b_jmk float,
number_of_inhab_flats_in_prefab_apartment_build_bdfcdf_jmk float,
usually_resident_population_e15d37_jmk float,
usually_resident_population_age_0_5_d6ffb6_jmk float,
usually_resident_population_age_15_19_d67e77_jmk float,
usually_resident_population_age_20_24_521338_jmk float,
usually_resident_population_age_25_29_0917ac_jmk float,
usually_resident_population_age_30_34_cab1af_jmk float,
usually_resident_population_age_35_39_3e3752_jmk float,
usually_resident_population_age_40_44_8f2992_jmk float,
usually_resident_population_age_45_49_0c4c2d_jmk float,
usually_resident_population_age_50_54_a68966_jmk float,
usually_resident_population_age_55_59_e10179_jmk float,
usually_resident_population_age_60_64_cca04e_jmk float,
usually_resident_population_age_65_plus_c662c6_jmk float,
usually_resident_population_age_6_14_ebdbce_jmk float,
us_res_pop_highedulvl_sec_grad_or_tert_prof_schols_efeb42_jmk float,
us_res_pop_high_edu_lvl_no_education_622c58_jmk float,
us_res_pop_high_edu_lvl_primary_89a90c_jmk float,
us_res_pop_high_edu_lvl_secondary_not_graduated_df1937_jmk float,
us_res_pop_high_edu_lvl_tertiary_university_d9de47_jmk float
);'''
cursor.execute(sql_create)

sql_copy = '''COPY cell_values(
sxy_id,
resident_population_91c66b_brno,
access_city_center_public_transport_8_lvls_5db20f_brno,
builtup_area_bc23b0_brno,
builtup_area_5_level_d21689_brno,
emotion_dontlike_3b56cb_brno,
emotion_like_aff639_brno,
emotion_missing_62c4e1_brno,
pm10_c8a0c3_brno,
vegetation_index_7_level_95bb86_brno,
park_greenery_area_dece19_brno,
elevation_1b8a79_brno,
landcover_urban_atlas_69ef7e_brno,
road_street_path_length_d64419_brno,
number_of_accidents_f42092_brno,
number_of_accidents_in_the_daytime_6f4d22_brno,
number_of_accidents_in_the_nighttime_5655a5_brno,
number_of_deaths_caused_by_accidents_e2a6d5_brno,
occupied_jobs_e64c61_brno,
number_of_offences_57a7b1_brno,
number_of_offences_aa7492_brno,
number_of_retail_grocery_shops_c873fa_brno,
number_of_serious_injuries_caused_by_accidents_01bcff_brno,
number_of_service_facilities_85921e_brno,
number_of_retail_shops_801f27_brno,
number_of_slight_injuries_caused_by_accidents_cdd154_brno,
retail_sales_area_65f9a7_brno,
accessbility_public_transport_7_level_4b067d_bmo,
number_of_accidents_0358cb_bmo,
number_of_accidents_in_the_daytime_40a49b_bmo,
number_of_accidents_in_the_nighttime_062631_bmo,
number_of_deaths_caused_by_accidents_b18286_bmo,
number_of_serious_injuries_caused_by_accidents_e0c176_bmo,
number_of_slight_injuries_caused_by_accidents_001947_bmo,
us_res_pop_high_edu_lvl_tertiary_hier_profes_schools_5ea7da_bmo,
us_res_pop_high_edu_lvl_primary_or_incomplete_a68b58_bmo,
us_res_pop_high_edu_lvl_secondary_graduated_f9c74f_bmo,
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
number_of_inhab_flats_0d42ff_jmk,
number_of_inhab_flats_in_apartment_buildings_67a645_jmk,
number_of_inhab_flats_in_family_houses_55aa2b_jmk,
number_of_inhab_flats_in_prefab_apartment_build_bdfcdf_jmk,
usually_resident_population_e15d37_jmk,
usually_resident_population_age_0_5_d6ffb6_jmk,
usually_resident_population_age_15_19_d67e77_jmk,
usually_resident_population_age_20_24_521338_jmk,
usually_resident_population_age_25_29_0917ac_jmk,
usually_resident_population_age_30_34_cab1af_jmk,
usually_resident_population_age_35_39_3e3752_jmk,
usually_resident_population_age_40_44_8f2992_jmk,
usually_resident_population_age_45_49_0c4c2d_jmk,
usually_resident_population_age_50_54_a68966_jmk,
usually_resident_population_age_55_59_e10179_jmk,
usually_resident_population_age_60_64_cca04e_jmk,
usually_resident_population_age_65_plus_c662c6_jmk,
usually_resident_population_age_6_14_ebdbce_jmk,
us_res_pop_highedulvl_sec_grad_or_tert_prof_schols_efeb42_jmk,
us_res_pop_high_edu_lvl_no_education_622c58_jmk,
us_res_pop_high_edu_lvl_primary_89a90c_jmk,
us_res_pop_high_edu_lvl_secondary_not_graduated_df1937_jmk,
us_res_pop_high_edu_lvl_tertiary_university_d9de47_jmk
)
FROM '/data/raw/cell_values_bmo.csv'
DELIMITER ','
CSV HEADER;'''

cursor.execute(sql_copy)

sql_cnt = 'select count(*) from cell_values'
cursor.execute(sql_cnt)
cnt = cursor.fetchone()
logger.info(f'  Rows imported into DB: {cnt[0]}')

logger.info('****************************************************************************************************')
logger.info('Import Grocery stores data')

sql_drop = '''DROP TABLE IF EXISTS grocery_stores;'''
cursor.execute(sql_drop)

cursor.execute(f'''
CREATE TABLE grocery_stores(
  cid varchar(50),
  category_name varchar(50),
  lat char(10),
  lon char(10),
  day smallint,
  hour smallint,
  hour_idx smallint,
  popularity smallint
);
''')

DAYS = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']


def is_popularity_filled(row):
    for day in DAYS:
        first_hour_column = f'popularTimesHistogram/{day}/0/hour'
        first_hour_raw = row[first_hour_column]
        if not np.isnan(first_hour_raw):
            return True
    return False


df_stores_raw = pd.read_csv('/data/raw/grocery_stores_2023-05-25.csv')
logger.info(f'df_stores_raw.shape={df_stores_raw.shape}')
for index, row in df_stores_raw.iterrows():
    if not is_popularity_filled(row):
        continue
    for day_idx, day in enumerate(DAYS):
        hours = {hour: 0 for hour in range(0, 24)}
        for column_idx in range(0, 24):
            hour_column = f'popularTimesHistogram/{day}/{column_idx}/hour'
            popularity_column = f'popularTimesHistogram/{day}/{column_idx}/occupancyPercent'
            hour = row[hour_column]
            popularity = row[popularity_column]
            assert np.isnan(hour) == np.isnan(popularity)
            if np.isnan(hour):
                continue
            hours[hour] = round(popularity)

        values = [
            (
                row["cid"],
                row["categoryName"],
                row["location/lat"],
                row["location/lng"],
                day_idx,
                hour,
                (hour + 20) % 24,
                popularity,
            )
            for hour, popularity in hours.items()
        ]
        query = """
        insert into grocery_stores(
          cid,
          category_name,
          lat,
          lon,
          day,
          hour,
          hour_idx,
          popularity
        ) values %s;
        """
        psycopg2.extras.execute_values(cursor, query, values)

cursor.execute(f'''
create MATERIALIZED view cell_values_geom
AS
select cv.*,
       ST_MakeEnvelope(
               cast(split_part(cv.sxy_id, '-', 1) as int) * cast(split_part(cv.sxy_id, '-', 2) as int),
               cast(split_part(cv.sxy_id, '-', 1) as int) * cast(split_part(cv.sxy_id, '-', 3) as int),
               cast(split_part(cv.sxy_id, '-', 1) as int) * (cast(split_part(cv.sxy_id, '-', 2) as int) + 1),
               cast(split_part(cv.sxy_id, '-', 1) as int) * (cast(split_part(cv.sxy_id, '-', 3) as int) + 1),
               3035
       ) geom
from cell_values cv
;''')

cursor.execute(f'''
create MATERIALIZED view grocery_stores_geom
AS
with lat_lon as MATERIALIZED (
    select gs.lat, gs.lon
    from grocery_stores gs
    group by gs.lat, gs.lon
), lat_lon_geom as MATERIALIZED (
    select ll.*,
           st_transform(st_setSRID(ST_Point(ll.lon::float, ll.lat::float), 4326), 3035) geom
    from lat_lon ll
), lat_lon_geom_cell as MATERIALIZED (
    select llg.*, cv.sxy_id
    from lat_lon_geom llg
             inner join
         cell_values_geom cv on ST_Contains(cv.geom, llg.geom)
)
select ROW_NUMBER() OVER (ORDER BY (SELECT 1)) AS rowid,
       gs.*,
       llgc.sxy_id
from grocery_stores gs
    inner join
          lat_lon_geom_cell llgc on (llgc.lat = gs.lat and llgc.lon = gs.lon)
;''')
