DROP VIEW IF EXISTS joint_rows_all_columns CASCADE;
create view joint_rows_all_columns
as
with all_with_rank as (select *,
                              rank() over(partition by kod order by st_area(geom) desc, id asc) area_rank
                       from all_rows_all_columns)
select awr.*,
       coalesce(c2.oprava, c2.trenovacit) new_trenovacitypkod,
       osm.osm_id,
       osm.osm_amenity,
       osm.osm_building
from all_with_rank awr left join
     joint_rows_ruian_osm osm on osm.kod = awr.kod left join
     corrections_2 c2 on c2.kod = awr.kod
where awr.area_rank = 1
;

DROP VIEW IF EXISTS joint_rows_important_columns CASCADE;
create view joint_rows_important_columns
AS
select
--        "fid",
       "kod",
       "typstavebnihoobjektukod",
       "zpusobvyuzitikod",
--        "druhkonstrukcekod",
--        "obestavenyprostor",
--        "pocetbytu",
--        "pocetpodlazi",
--        "podlahovaplocha",
--        "pripojenikanalizacekod",
--        "pripojeniplynkod",
--        "pripojenivodovodkod",
--        "vybavenivytahemkod",
--        "zastavenaplocha",
--        "zpusobvytapenikod",
--        "zpusobochranykod",
       "pop_age_0_5",
       "pop_age_6_14",
       "pop_age_15_19",
       "pop_age_20_24",
       "pop_age_25_29",
       "pop_age_30_34",
       "pop_age_35_39",
       "pop_age_40_44",
       "pop_age_45_49",
       "pop_age_50_54",
       "pop_age_55_59",
       "pop_age_60_64",
       "pop_age_65_plus",
--        "pc_budov",
--        "kvalita",
--        "vchod",
--        "typ_cis",
--        "typ_adresy",
--        "tvybu",
--        "zpvybu",
--        "ksd_cz_cc",
--        "jdruhdo",
--        "jkanal",
--        "jmaterz",
--        "jobdvys",
--        "jplyn",
--        "jppodla",
--        "justope",
--        "jvlastd",
--        "jvodovd",
--        "druhvlabud",
--        "zastplobud",
--        "obeprobud",
--        "podplobud",
--        "pocpodbud",
--        "pribudvod",
--        "zpvytbud",
--        "vybudvyt",
--        "rohbud",
--        "sum_byt",
--        "katcbyt",
--        "budobyev",
--        "druhplyn",
--        "topmehl",
--        "topmeved",
--        "ruianteaid",
--        "budobytsl",
--        "budobyosl",
       "charakterzsjkod",
--        "calculated_index_skola",
--        "calculated_index_65_plus",
       "osm_amenity",
       "osm_building",
       new_trenovacitypkod "trenovacitypkod"
from joint_rows_all_columns
-- Remove 55 rows without zpusobvyuzitikod
where zpusobvyuzitikod is not null
;
