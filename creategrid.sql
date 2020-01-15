CREATE OR REPLACE FUNCTION ST_CreateFishnet(
        extent_geom geometry,
        xsize float8, ysize float8,
        x0 float8 DEFAULT 0, y0 float8 DEFAULT 0,
        OUT "row" integer, OUT col integer,
        OUT geom geometry)
    RETURNS SETOF record AS
$$
DECLARE
   xmin    NUMERIC;
   ymin    NUMERIC;
   xmax    NUMERIC;
   ymax    NUMERIC;
   xmin_idx    INT;
   ymin_idx    INT;
   xmax_idx    INT;
   ymax_idx    INT;
   srid    INT;
BEGIN
SELECT floor(ST_XMin($1)/$2)*$2 into xmin;
SELECT ceil(ST_XMax($1)/$2)*$2 into xmax;
SELECT floor(ST_YMin($1)/$3)*$3 into ymin;
SELECT ceil(ST_YMax($1)/$3)*$3 into ymax;
xmin_idx := (xmin/$2)::INT;
xmax_idx := (xmax/$2)::INT;
ymin_idx := (ymin/$3)::INT;
ymax_idx := (ymax/$3)::INT;
SELECT st_srid($1) into srid;
RETURN QUERY SELECT i + 1 AS row, j + 1 AS col, st_setsrid(ST_Translate(cell, j * $2 + $4, i * $3 + $5), srid) AS geom
FROM generate_series(ymin_idx, ymax_idx - 1) AS i,
     generate_series(xmin_idx, xmax_idx - 1) AS j,
(
SELECT ('POLYGON((0 0, 0 '||$3||', '||$2||' '||$3||', '||$2||' 0,0 0))')::geometry AS cell
) AS foo;
END $$ LANGUAGE plpgsql IMMUTABLE STRICT;
/*
USAGE:

with zsj_extent as (
select st_transform(st_union(originalnihranice), 3035) as geom
from zsj
), grid as (
select net.*
from zsj_extent, st_createfishnet(zsj_extent.geom, 250, 250) net
)
select -1, -1, geom from zsj_extent
union all
select grid.*
from grid, zsj_extent
where st_intersects(grid.geom, zsj_extent.geom)

 */