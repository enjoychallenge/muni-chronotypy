DROP MATERIALIZED VIEW IF EXISTS train_rows_predictions_geom CASCADE;
create MATERIALIZED view train_rows_predictions_geom
AS
select ta.fid, ta.trenovacitypkod, te.chronotyp_guessed, ta.geom
from train_rows_all_columns ta
left join train_rows_predictions te on (ta.fid = te.fid)
;

DROP MATERIALIZED VIEW IF EXISTS all_rows_predictions_geom CASCADE;
create MATERIALIZED view all_rows_predictions_geom
AS
select ta.fid, ta.trenovacitypkod, te.chronotyp_guessed, ta.geom
from all_rows_all_columns ta
left join all_rows_predictions te on (ta.fid = te.fid)
;
