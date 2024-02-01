drop table if exists cell_surrounding_values;

-- 1s
create table cell_surrounding_values as
select cd.sxy_id_1 sxy_id,
       sum(usually_resident_population_e15d37_jmk) usually_resident_population_e15d37_jmk_3km
from cell_distance cd inner join
     cell_values_geom c on c.sxy_id = cd.sxy_id_2
where cd.dist <= 3000
group by cd.sxy_id_1
;

-- 0s
CREATE INDEX idx_cell_surrounding_values_sxy_id ON cell_surrounding_values (sxy_id);
