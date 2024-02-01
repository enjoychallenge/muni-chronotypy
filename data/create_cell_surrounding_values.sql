drop table if exists cell_surrounding_values;

-- 41s
create table cell_surrounding_values as
select cd.sxy_id_1 sxy_id,
       avg(case when cd.dist <= 1000 then accessbility_public_transport_7_level_4b067d_bmo end) accessbility_public_transport_7_level_4b067d_bmo_1km,
       avg(case when cd.dist <= 3000 then accessbility_public_transport_7_level_4b067d_bmo end) accessbility_public_transport_7_level_4b067d_bmo_3km,
       avg(case when cd.dist <= 1000 then number_of_accidents_in_the_daytime_40a49b_bmo end) number_of_accidents_in_the_daytime_40a49b_bmo_1km,
       avg(case when cd.dist <= 3000 then number_of_accidents_in_the_daytime_40a49b_bmo end) number_of_accidents_in_the_daytime_40a49b_bmo_3km,
       avg(case when cd.dist <= 1000 then number_of_accidents_in_the_nighttime_062631_bmo end) number_of_accidents_in_the_nighttime_062631_bmo_1km,
       avg(case when cd.dist <= 3000 then number_of_accidents_in_the_nighttime_062631_bmo end) number_of_accidents_in_the_nighttime_062631_bmo_3km,
       avg(case when cd.dist <= 1000 then us_res_pop_high_edu_lvl_tertiary_hier_profes_schools_5ea7da_bmo end) us_res_pop_high_edu_lvl_ter_hier_profes_schools_5ea7da_bmo_1km,
       avg(case when cd.dist <= 3000 then us_res_pop_high_edu_lvl_tertiary_hier_profes_schools_5ea7da_bmo end) us_res_pop_high_edu_lvl_ter_hier_profes_schools_5ea7da_bmo_3km,
       avg(case when cd.dist <= 1000 then us_res_pop_high_edu_lvl_primary_or_incomplete_a68b58_bmo end) us_res_pop_high_edu_lvl_primary_or_incomplete_a68b58_bmo_1km,
       avg(case when cd.dist <= 3000 then us_res_pop_high_edu_lvl_primary_or_incomplete_a68b58_bmo end) us_res_pop_high_edu_lvl_primary_or_incomplete_a68b58_bmo_3km,
       avg(case when cd.dist <= 1000 then us_res_pop_high_edu_lvl_secondary_graduated_f9c74f_bmo end) us_res_pop_high_edu_lvl_secondary_graduated_f9c74f_bmo_1km,
       avg(case when cd.dist <= 3000 then us_res_pop_high_edu_lvl_secondary_graduated_f9c74f_bmo end) us_res_pop_high_edu_lvl_secondary_graduated_f9c74f_bmo_3km,
       avg(case when cd.dist <= 1000 then acces_city_center_public_transport_9_levels_be96f2_jmk end) acces_city_center_public_transport_9_levels_be96f2_jmk_1km,
       avg(case when cd.dist <= 3000 then acces_city_center_public_transport_9_levels_be96f2_jmk end) acces_city_center_public_transport_9_levels_be96f2_jmk_3km,
       avg(case when cd.dist <= 1000 then general_services_accessibility_f42fff_jmk end) general_services_accessibility_f42fff_jmk_1km,
       avg(case when cd.dist <= 3000 then general_services_accessibility_f42fff_jmk end) general_services_accessibility_f42fff_jmk_3km,
       avg(case when cd.dist <= 1000 then elevation_07eb7d_jmk end) elevation_07eb7d_jmk_1km,
       avg(case when cd.dist <= 3000 then elevation_07eb7d_jmk end) elevation_07eb7d_jmk_3km,
       avg(case when cd.dist <= 1000 then road_street_length_4d64b2_jmk end) road_street_length_4d64b2_jmk1km,
       avg(case when cd.dist <= 3000 then road_street_length_4d64b2_jmk end) road_street_length_4d64b2_jmk_3km,
       avg(case when cd.dist <= 1000 then number_of_accidents_f02900_jmk end) number_of_accidents_f02900_jmk_1km,
       avg(case when cd.dist <= 3000 then number_of_accidents_f02900_jmk end) number_of_accidents_f02900_jmk_3km,
       avg(case when cd.dist <= 1000 then number_of_flats_built_1920_1945_cee901_jmk end) number_of_flats_built_1920_1945_cee901_jmk_1km,
       avg(case when cd.dist <= 3000 then number_of_flats_built_1920_1945_cee901_jmk end) number_of_flats_built_1920_1945_cee901_jmk_3km,
       avg(case when cd.dist <= 1000 then number_of_flats_built_1946_1960_3b06c3_jmk end) number_of_flats_built_1946_1960_3b06c3_jmk_1km,
       avg(case when cd.dist <= 3000 then number_of_flats_built_1946_1960_3b06c3_jmk end) number_of_flats_built_1946_1960_3b06c3_jmk_3km,
       avg(case when cd.dist <= 1000 then number_of_flats_built_1961_1970_c4552c_jmk end) number_of_flats_built_1961_1970_c4552c_jmk_1km,
       avg(case when cd.dist <= 3000 then number_of_flats_built_1961_1970_c4552c_jmk end) number_of_flats_built_1961_1970_c4552c_jmk_3km,
       avg(case when cd.dist <= 1000 then number_of_flats_built_1971_1980_5da6fe_jmk end) number_of_flats_built_1971_1980_5da6fe_jmk_1km,
       avg(case when cd.dist <= 3000 then number_of_flats_built_1971_1980_5da6fe_jmk end) number_of_flats_built_1971_1980_5da6fe_jmk_3km,
       avg(case when cd.dist <= 1000 then number_of_flats_built_1981_1990_927a67_jmk end) number_of_flats_built_1981_1990_927a67_jmk_1km,
       avg(case when cd.dist <= 3000 then number_of_flats_built_1981_1990_927a67_jmk end) number_of_flats_built_1981_1990_927a67_jmk_3km,
       avg(case when cd.dist <= 1000 then number_of_flats_built_1991_2000_064593_jmk end) number_of_flats_built_1991_2000_064593_jmk_1km,
       avg(case when cd.dist <= 3000 then number_of_flats_built_1991_2000_064593_jmk end) number_of_flats_built_1991_2000_064593_jmk_3km,
       avg(case when cd.dist <= 1000 then number_of_flats_built_2001_2011_5500d8_jmk end) number_of_flats_built_2001_2011_5500d8_jmk_1km,
       avg(case when cd.dist <= 3000 then number_of_flats_built_2001_2011_5500d8_jmk end) number_of_flats_built_2001_2011_5500d8_jmk_3km,
       avg(case when cd.dist <= 1000 then number_of_flats_built_till_1919_d7a5f9_jmk end) number_of_flats_built_till_1919_d7a5f9_jmk_1km,
       avg(case when cd.dist <= 3000 then number_of_flats_built_till_1919_d7a5f9_jmk end) number_of_flats_built_till_1919_d7a5f9_jmk_3km,
       avg(case when cd.dist <= 1000 then number_of_inhab_flats_in_family_houses_55aa2b_jmk end) number_of_inhab_flats_in_family_houses_55aa2b_jmk_1km,
       avg(case when cd.dist <= 3000 then number_of_inhab_flats_in_family_houses_55aa2b_jmk end) number_of_inhab_flats_in_family_houses_55aa2b_jmk_3km,
       avg(case when cd.dist <= 1000 then number_of_inhab_flats_in_prefab_apartment_build_bdfcdf_jmk end) number_of_inhab_flats_in_prefab_apartment_build_bdfcdf_jmk_1km,
       avg(case when cd.dist <= 3000 then number_of_inhab_flats_in_prefab_apartment_build_bdfcdf_jmk end) number_of_inhab_flats_in_prefab_apartment_build_bdfcdf_jmk_3km,
       avg(case when cd.dist <= 1000 then usually_resident_population_e15d37_jmk end) usually_resident_population_e15d37_jmk_1km,
       avg(case when cd.dist <= 3000 then usually_resident_population_e15d37_jmk end) usually_resident_population_e15d37_jmk_3km,
       avg(case when cd.dist <= 1000 then usually_resident_population_age_20_24_521338_jmk end) usually_resident_population_age_20_24_521338_jmk_1km,
       avg(case when cd.dist <= 3000 then usually_resident_population_age_20_24_521338_jmk end) usually_resident_population_age_20_24_521338_jmk_3km,
       avg(case when cd.dist <= 1000 then usually_resident_population_age_65_plus_c662c6_jmk end) usually_resident_population_age_65_plus_c662c6_jmk_1km,
       avg(case when cd.dist <= 3000 then usually_resident_population_age_65_plus_c662c6_jmk end) usually_resident_population_age_65_plus_c662c6_jmk_3km,
       avg(case when cd.dist <= 1000 then us_res_pop_high_edu_lvl_no_education_622c58_jmk end) us_res_pop_high_edu_lvl_no_education_622c58_jmk_1km,
       avg(case when cd.dist <= 3000 then us_res_pop_high_edu_lvl_no_education_622c58_jmk end) us_res_pop_high_edu_lvl_no_education_622c58_jmk_3km
from cell_distance cd inner join
     cell_values_geom c on c.sxy_id = cd.sxy_id_2
group by cd.sxy_id_1
;

-- 0s
CREATE INDEX idx_cell_surrounding_values_sxy_id ON cell_surrounding_values (sxy_id);
