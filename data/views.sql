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

DROP MATERIALIZED VIEW IF EXISTS zsj_full CASCADE;
create materialized view zsj_full
AS
select
  zsj.kod as zsj_kod,
  zsj.nazev as zsj_nazev,
  zsj.originalnihranice as geom,
  round(sum(cell_x_zsj.cell_area_ratio * bug_builtup_area.value)) as builtup_area,
  round(sum(cell_x_zsj.cell_area_ratio * bug_inhabited_flats.value)) as inhabited_flats,
  round(sum(cell_x_zsj.cell_area_ratio * bug_occupied_jobs.value)) as occupied_jobs,
  round(sum(cell_x_zsj.cell_area_ratio * bug_usually_resident_population.value)) as usually_resident_population,
  round(sum(cell_x_zsj.cell_area_ratio * bug_retail_sales_area.value)) as retail_sales_area,
  case
    when chronotyp_cluster.cluster_id in (1,3) then 'U'
    when chronotyp_cluster.cluster_id in (10,16,17) then 'A'
	else 'o'
  end as chronotyp
from zsj
  left join chronotyp_cluster on zsj.kod = chronotyp_cluster.zsj_kod
  left join cell_x_zsj on zsj.kod = cell_x_zsj.zsj_kod
  left join bug_builtup_area on cell_x_zsj.cell_id = bug_builtup_area.cell_id
  left join bug_inhabited_flats on cell_x_zsj.cell_id = bug_inhabited_flats.cell_id
  left join bug_occupied_jobs on cell_x_zsj.cell_id = bug_occupied_jobs.cell_id
  left join bug_usually_resident_population on cell_x_zsj.cell_id = bug_usually_resident_population.cell_id
  left join bug_retail_sales_area on cell_x_zsj.cell_id = bug_retail_sales_area.cell_id
group by zsj.kod, zsj.nazev, zsj.originalnihranice, chronotyp_cluster.cluster_id
;
CREATE INDEX zsj_full_spidx ON zsj_full USING gist (geom);

