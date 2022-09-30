DROP MATERIALIZED VIEW IF EXISTS joint_rows_predictions_geom CASCADE;
create MATERIALIZED view joint_rows_predictions_geom
AS
select pred.sxy_id,
       pred.tren_typ,
       pred.predikce,
       ST_MakeEnvelope(
                   cast(split_part(pred.sxy_id, '-', 1) as int) * cast(split_part(pred.sxy_id, '-', 2) as int),
                   cast(split_part(pred.sxy_id, '-', 1) as int) * cast(split_part(pred.sxy_id, '-', 3) as int),
                   cast(split_part(pred.sxy_id, '-', 1) as int) * (cast(split_part(pred.sxy_id, '-', 2) as int) + 1),
                   cast(split_part(pred.sxy_id, '-', 1) as int) * (cast(split_part(pred.sxy_id, '-', 3) as int) + 1),
                   3035
           ) as geometry
from joint_rows_predictions pred
;
