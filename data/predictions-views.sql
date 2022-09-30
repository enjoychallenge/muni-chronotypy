DROP MATERIALIZED VIEW IF EXISTS joint_rows_predictions_geom CASCADE;
create MATERIALIZED view joint_rows_predictions_geom
AS
select pred.sxy_id,
       chr((ascii('A') - 1 + pred.tren_typ_6)::integer) as tren_typ,
       chr((ascii('A') - 1 + pred.predikce_6)::integer) as predikce_6,
       case when pred.predikce_6 in (1,2,3) then 'ABC' else 'DEF' end as predikce_2,
       ST_MakeEnvelope(
                   cast(split_part(pred.sxy_id, '-', 1) as int) * cast(split_part(pred.sxy_id, '-', 2) as int),
                   cast(split_part(pred.sxy_id, '-', 1) as int) * cast(split_part(pred.sxy_id, '-', 3) as int),
                   cast(split_part(pred.sxy_id, '-', 1) as int) * (cast(split_part(pred.sxy_id, '-', 2) as int) + 1),
                   cast(split_part(pred.sxy_id, '-', 1) as int) * (cast(split_part(pred.sxy_id, '-', 3) as int) + 1),
                   3035
           ) as geometry
from joint_rows_predictions pred
;
