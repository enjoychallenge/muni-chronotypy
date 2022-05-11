DROP MATERIALIZED VIEW IF EXISTS joint_rows_predictions_geom CASCADE;
create MATERIALIZED view joint_rows_predictions_geom
AS
select te.kod,
       te.trenovacitypkod train_kod,
       coalesce(te.finaltypkod, te.predikce) final_kod,
       ru.geom,
       te.finaltypkod alg_kod,
       te.predikce ml_kod
from joint_rows_predictions te
inner join joint_rows_ruian ru on ru.kod = te.kod
;
