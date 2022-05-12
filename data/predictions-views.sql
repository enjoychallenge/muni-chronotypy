DROP MATERIALIZED VIEW IF EXISTS joint_rows_predictions_geom CASCADE;
create MATERIALIZED view joint_rows_predictions_geom
AS
select te.kod,
       te.trenovacitypkod::int train_kod,
       coalesce(te.finaltypkod, te.predikce)::int final_kod,
       ru.geom,
       te.finaltypkod::int alg_kod,
       te.predikce::int ml_kod
from joint_rows_predictions te
inner join joint_rows_ruian ru on ru.kod = te.kod
;
