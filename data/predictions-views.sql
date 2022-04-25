DROP MATERIALIZED VIEW IF EXISTS joint_rows_predictions_geom CASCADE;
create MATERIALIZED view joint_rows_predictions_geom
AS
select ta.kod, ta.trenovacitypkod, te.chronotyp_guessed, ta.geom
from joint_rows_all_columns ta
left join joint_rows_predictions te on (ta.kod = te.kod)
;
