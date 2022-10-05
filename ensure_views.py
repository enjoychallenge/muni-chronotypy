import logging
import settings
import sqlalchemy

sql_engine = sqlalchemy.create_engine(settings.PG_URL)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(filename)s] [%(levelname)s]:\t%(message)s')
logger = logging.getLogger(__name__)


CATEGORY_COLUMNS = [
    "typstavebnihoobjektukod",
    "zpusobvyuzitikod",
    "druhkonstrukcekod",
    "pripojenikanalizacekod",
    "pripojeniplynkod",
    "pripojenivodovodkod",
    "vybavenivytahemkod",
    "zpusobvytapenikod",
    "zpvybu",
    "ksd_cz_cc",
    "jdruhdo",
    "jobdvys",
    "jvlastd",
    "druhvlabud",
    "katcbyt",
    "charakterzsjkod",
]

DYNAMIC_DUMMY_QUERY_TEMPLATE = """
DROP MATERIALIZED VIEW IF EXISTS cell_ruian_training CASCADE;
CREATE MATERIALIZED VIEW cell_ruian_training as
with parts_with_area as (select *, st_area(geom) as part_area
                         from all_rows_all_columns),
     parts_with_rank as (select *,
                              rank() over(partition by kod order by part_area desc, id asc) part_area_rank
                       from parts_with_area),
     buildings_with_area as (select kod, sum(st_area(geom)) as building_area
                        from all_rows_all_columns
                        group by kod
                        order by kod),
     parts_with_ratio as (
         select part.*, bldg.building_area, part_area/building_area as area_ratio
         from parts_with_rank part left join buildings_with_area bldg on (part.kod = bldg.kod)
     )
select
       bug_cell_id,
       sum(coalesce(pocetbytu, sum_byt, 0) * area_ratio) as pocetbytu,
       PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY coalesce(pocetpodlazi, pocpodbud, 1)) as pocetpodlazi,
       sum(coalesce(budobyev, 0) * area_ratio) as budobyev,
       sum(coalesce(budobytsl, 0) * area_ratio) as budobytsl,
       sum(coalesce(budobyosl, 0) * area_ratio) as budobyosl,
       {dummy_columns}
from parts_with_ratio
group by bug_cell_id
order by bug_cell_id;
"""


def get_distinct_values(column):
    with sql_engine.connect() as con:
        query = sqlalchemy.text(
            f"""
select distinct {column}
from all_rows_all_columns
order by {column}
            """
        )
        result = con.execute(query)
    return result


def main():
    params = tuple()
    sql_parts = []
    logger.info(f"Reading distinct values from {len(CATEGORY_COLUMNS)} category columns.")
    for column in CATEGORY_COLUMNS:
        for row in get_distinct_values(column):
            value = row[0]
            if value is None:
                continue
            sql_parts.append(
                f"""
                   sum(case when {column} = %s then part_area else 0 end) {column}_{value}_area,
                   sum(case when {column} = %s then area_ratio else 0 end) {column}_{value}_cnt
                """
            )
            params += (value, value)

    logger.info(f"Found {len(sql_parts)} not-null values, going to create {len(sql_parts) * 2} dummy columns.")

    with sql_engine.connect() as conn:
        conn.exec_driver_sql(
            DYNAMIC_DUMMY_QUERY_TEMPLATE.format(dummy_columns=', '.join(sql_parts)),
            params
        )


if __name__ == "__main__":
    main()
