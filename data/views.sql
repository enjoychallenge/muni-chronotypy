DROP VIEW IF EXISTS train_rows_all_columns CASCADE;
create view train_rows_all_columns
AS
select *
from all_rows_all_columns
where "trenovacitypkod" is not null
;
-- CREATE INDEX all_rows_all_columns_spidx ON all_rows_all_columns USING gist (geom);



DROP VIEW IF EXISTS train_rows_important_columns CASCADE;
create view train_rows_important_columns
AS
select
       "fid",
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
       "trenovacitypkod"
from train_rows_all_columns
;
