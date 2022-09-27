import logging
import settings
import psycopg2


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

logger.info('\nStarting with cell_training table')

sql_drop = '''DROP TABLE IF EXISTS cell_training;'''
cursor.execute(sql_drop)
sql_create = '''CREATE TABLE cell_training(sxy_id char(15), type char(1));'''
cursor.execute(sql_create)

sql_copy = '''COPY cell_training(sxy_id, type)
FROM '/data/raw/cell_training_bmo.csv'
DELIMITER ','
CSV HEADER;'''

cursor.execute(sql_copy)

sql_cnt = 'select count(*) from cell_training'
cursor.execute(sql_cnt)
cnt = cursor.fetchone()
logger.info(f'  Rows imported into DB: {cnt[0]}')

logger.info('****************************************************************************************************')

logger.info('\nStarting with cell_values table')

sql_drop = '''DROP TABLE IF EXISTS cell_values;'''
cursor.execute(sql_drop)
sql_create = '''CREATE TABLE cell_values(sxy_id char(15), 
resident_population float,
accessibility_city_center_public_transport_8_levels float,
builtup_area float,
builtup_area_5_level float,
emotion_dontlike float,
emotion_like float,
emotion_missing float,
pm10 float,
vegetation_index_7_level float,
park_greenery_area float,
elevation float,
landcover_urban_atlas varchar,
road_street_path_length float,
number_of_accidents float,
number_of_accidents_in_the_daytime float,
number_of_accidents_in_the_nighttime float,
number_of_deaths_caused_by_accidents float,
occupied_jobs float,
number_of_offences float,
number_of_offences_2 float,
number_of_retail_grocery_shops float,
number_of_serious_injuries_caused_by_accidents float,
number_of_service_facilities float,
number_of_retail_shops float,
number_of_slight_injuries_caused_by_accidents float,
retail_sales_area float,
accessbility_public_transport_7_level float,
number_of_accidents_2 float,
number_of_accidents_in_the_daytime_2 float,
number_of_accidents_in_the_nighttime_2 float,
number_of_deaths_caused_by_accidents_2 float,
number_of_serious_injuries_caused_by_accidents_2 float,
number_of_slight_injuries_caused_by_accidents_2 float,
top_edu_lvl_tertiary_higher_professional_schools float,
top_edu_lvl_primary_or_incomplete float,
top_edu_lvl_secondary_graduated float,
accessibility_city_center_public_transport_9_levels float,
general_services_accessibility float,
number_of_pv_power_stations float,
pv_power_stations_capacity float,
landcover_urban_atlas_3level_change float,
elevation_2 float,
landcover_urban_atlas_3level float,
road_street_length float,
number_of_accidents_3 float,
number_of_flats_built_1920_1945 float,
number_of_flats_built_1946_1960 float,
number_of_flats_built_1961_1970 float,
number_of_flats_built_1971_1980 float,
number_of_flats_built_1981_1990 float,
number_of_flats_built_1991_2000 float,
number_of_flats_built_2001_2011 float,
number_of_flats_built_till_1919 float,
number_of_inhabited_flats float,
number_of_inhabited_flats_in_apartment_buildings float,
number_of_inhabited_flats_in_family_houses float,
number_of_inhabited_flats_in_prefab_apartment_buildings float,
usually_resident_population float,
usually_resident_population_age_0_5 float,
usually_resident_population_age_15_19 float,
usually_resident_population_age_20_24 float,
usually_resident_population_age_25_29 float,
usually_resident_population_age_30_34 float,
usually_resident_population_age_35_39 float,
usually_resident_population_age_40_44 float,
usually_resident_population_age_45_49 float,
usually_resident_population_age_50_54 float,
usually_resident_population_age_55_59 float,
usually_resident_population_age_60_64 float,
usually_resident_population_age_65_plus float,
usually_resident_population_age_6_14 float,
top_edu_lvl_secondary_graduated_or_tertiary_higher_professional_schools float,
top_edu_lvl_no_education float,
top_edu_lvl_primary float,
top_edu_lvl_secondary_not_graduated float,
top_edu_lvl_tertiary_university float
);'''
cursor.execute(sql_create)

sql_copy = '''COPY cell_values(
sxy_id,
resident_population,
accessibility_city_center_public_transport_8_levels,
builtup_area,
builtup_area_5_level,
emotion_dontlike,
emotion_like,
emotion_missing,
pm10,
vegetation_index_7_level,
park_greenery_area,
elevation,
landcover_urban_atlas,
road_street_path_length,
number_of_accidents,
number_of_accidents_in_the_daytime,
number_of_accidents_in_the_nighttime,
number_of_deaths_caused_by_accidents,
occupied_jobs,
number_of_offences,
number_of_offences_2,
number_of_retail_grocery_shops,
number_of_serious_injuries_caused_by_accidents,
number_of_service_facilities,
number_of_retail_shops,
number_of_slight_injuries_caused_by_accidents,
retail_sales_area,
accessbility_public_transport_7_level,
number_of_accidents_2,
number_of_accidents_in_the_daytime_2,
number_of_accidents_in_the_nighttime_2,
number_of_deaths_caused_by_accidents_2,
number_of_serious_injuries_caused_by_accidents_2,
number_of_slight_injuries_caused_by_accidents_2,
top_edu_lvl_tertiary_higher_professional_schools,
top_edu_lvl_primary_or_incomplete,
top_edu_lvl_secondary_graduated,
accessibility_city_center_public_transport_9_levels,
general_services_accessibility,
number_of_pv_power_stations,
pv_power_stations_capacity,
landcover_urban_atlas_3level_change,
elevation_2,
landcover_urban_atlas_3level,
road_street_length,
number_of_accidents_3,
number_of_flats_built_1920_1945,
number_of_flats_built_1946_1960,
number_of_flats_built_1961_1970,
number_of_flats_built_1971_1980,
number_of_flats_built_1981_1990,
number_of_flats_built_1991_2000,
number_of_flats_built_2001_2011,
number_of_flats_built_till_1919,
number_of_inhabited_flats,
number_of_inhabited_flats_in_apartment_buildings,
number_of_inhabited_flats_in_family_houses,
number_of_inhabited_flats_in_prefab_apartment_buildings,
usually_resident_population,
usually_resident_population_age_0_5,
usually_resident_population_age_15_19,
usually_resident_population_age_20_24,
usually_resident_population_age_25_29,
usually_resident_population_age_30_34,
usually_resident_population_age_35_39,
usually_resident_population_age_40_44,
usually_resident_population_age_45_49,
usually_resident_population_age_50_54,
usually_resident_population_age_55_59,
usually_resident_population_age_60_64,
usually_resident_population_age_65_plus,
usually_resident_population_age_6_14,
top_edu_lvl_secondary_graduated_or_tertiary_higher_professional_schools,
top_edu_lvl_no_education,
top_edu_lvl_primary,
top_edu_lvl_secondary_not_graduated,
top_edu_lvl_tertiary_university
)
FROM '/data/raw/cell_values_bmo.csv'
DELIMITER ','
CSV HEADER;'''

cursor.execute(sql_copy)

sql_cnt = 'select count(*) from cell_values'
cursor.execute(sql_cnt)
cnt = cursor.fetchone()
logger.info(f'  Rows imported into DB: {cnt[0]}')
