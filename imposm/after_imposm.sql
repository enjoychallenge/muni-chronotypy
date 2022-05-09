CREATE INDEX idx_joint_rows_ruian_geom ON joint_rows_ruian USING GIST (geom);

DROP table IF EXISTS imposm_school_3035 CASCADE;
create table imposm_school_3035 as
select st_transform(st_buffer(sch.geometry, 20), 3035) geom_3035_buffer,
       sch.*
from osm_import.school sch
;

CREATE INDEX idx_imposm_school_3035_geom_3035 ON imposm_school_3035 USING GIST (geom_3035_buffer);

DROP table IF EXISTS imposm_school_3035_node CASCADE;
create table imposm_school_3035_node as
select st_transform(sch.geometry, 3035) geom_3035,
       sch.*
from osm_import.school_node sch
;

CREATE INDEX idx_imposm_school_3035_node_geom_3035 ON imposm_school_3035_node USING GIST (geom_3035);


DROP MATERIALIZED VIEW IF EXISTS joint_rows_ruian_osm CASCADE;
create MATERIALIZED view joint_rows_ruian_osm as
select ruian.kod,
       case when exists(select from imposm_school_3035 sch where st_contains(sch.geom_3035_buffer, ruian.geom)) then 1
            else case when exists(select from imposm_school_3035_node schn where st_within(schn.geom_3035, ruian.geom)) then 1
                      else 0
                 end
       end is_school
from joint_rows_ruian ruian
;
