CREATE INDEX idx_joint_rows_ruian_geom ON joint_rows_ruian USING GIST (geom);

DROP table IF EXISTS imposm_school_3035 CASCADE;
create table imposm_school_3035 as
select st_transform(st_buffer(sch.geometry, 2), 3035) geom_3035_buffer,
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
with
joint_rows_ruian_osm_with_osm_type as (
    select ruian.kod,
           coalesce(sch.osm_id, schn.osm_id) osm_id,
           coalesce(sch.amenity, schn.amenity) osm_amenity,
           coalesce(sch.building, schn.building) osm_building,
           case when sch.amenity is not null and sch.building is not null then 10
                when schn.amenity is not null and schn.building is not null then 15
                when sch.amenity is not null then 20
                when sch.building is not null then 21
                when schn.amenity is not null then 22
                when schn.building is not null then 23
               end osm_type
    from joint_rows_ruian ruian left join
         imposm_school_3035 sch on st_contains(sch.geom_3035_buffer, ruian.geom) or
                                   (st_intersects(sch.geom_3035_buffer, ruian.geom) and
                                   st_area(ST_Intersection(sch.geom_3035_buffer, ruian.geom)) >= 0.5 * st_area(ruian.geom)) left join
         imposm_school_3035_node schn on sch.osm_id is null and st_within(schn.geom_3035, ruian.geom))
     ,
joint_rows_ruian_osm_with_rank as (
    select *,
           rank() over(partition by kod order by osm_type, osm_id) osm_rank
    from joint_rows_ruian_osm_with_osm_type
     )
select kod,
       osm_id,
       osm_amenity,
       osm_building
from joint_rows_ruian_osm_with_rank
where osm_rank = 1
;
