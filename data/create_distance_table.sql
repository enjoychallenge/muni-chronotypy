drop table if exists cell_distance;

-- 5min
create table cell_distance as
with cells as (
select c.sxy_id, c.geom, ST_Centroid(c.geom) centroid
from cell_values_geom c
)
select c1.sxy_id sxy_id_1,
       c2.sxy_id sxy_id_2,
       ST_Distance(c1.centroid, c2.centroid) dist
from cells c1 inner join
     cells c2 on ST_DWithin(c1.centroid, c2.centroid, 5000)
;

-- 34s
CREATE INDEX idx_cell_distance_c1_dist ON cell_distance (sxy_id_1, dist);
