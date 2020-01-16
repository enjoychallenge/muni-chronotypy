DROP MATERIALIZED VIEW IF EXISTS region CASCADE;
create materialized view region
AS
select ST_MakePolygon(st_exteriorring(st_union(originalnihranice))) as geom
from zsj
;
CREATE INDEX region_spidx ON region USING gist (geom);

DROP MATERIALIZED VIEW IF EXISTS region_div CASCADE;
create materialized view region_div
AS
select
  row_number() over () AS div_id,
  sub_view.*
from (
  SELECT
    st_makevalid((st_dump(st_subdivide(geom, 100))).geom) as geom
  FROM region
) sub_view
;
CREATE INDEX region_div_spidx ON region_div USING gist (geom);

DROP MATERIALIZED VIEW IF EXISTS cell CASCADE;
create materialized view cell
AS
with t1 as (
SELECT cell_id, div_id as region_div_id, st_intersection(wkb_geometry, region_div.geom) as geom
FROM bug_landcover, region_div
where st_intersects(wkb_geometry, region_div.geom)
), t2 as (
select cell_id, st_union(geom) as geom
from t1
group by cell_id
)
select *, st_area(geom) as area
from t2
;
CREATE INDEX cell_spidx ON cell USING gist (geom);

DROP MATERIALIZED VIEW IF EXISTS cell_x_zsj CASCADE;
create materialized view cell_x_zsj
AS
SELECT
  zsj.kod as zsj_kod,
  cell.cell_id,
  st_area(st_intersection(cell.geom, zsj.originalnihranice))/cell.area as cell_area_ratio
FROM zsj
JOIN cell
ON ST_Intersects(cell.geom, zsj.originalnihranice)
order by zsj.kod, cell.cell_id
;

