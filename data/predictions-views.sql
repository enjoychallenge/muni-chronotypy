DROP MATERIALIZED VIEW IF EXISTS joint_rows_predictions_geom CASCADE;
create MATERIALIZED view joint_rows_predictions_geom
AS
select ta.kod, ta.trenovacitypkod, te.predikce, ru.geom
from joint_rows_all_columns ta
inner join joint_rows_ruian ru on ru.kod = ta.kod
left join joint_rows_predictions te on (ta.kod = te.kod)
;
