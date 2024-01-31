# Chronotopes

## Download data
Either configure [Google Drive **Shared Drive** (Team Drive)](https://rclone.org/drive/) using `rclone config` and run `make download-data`, or download [`raw` folder](https://drive.google.com/drive/folders/1ly6ypgG6LG3fiLFmBDLnCrJNb_XK40ay) into `data/raw` manually. You have to copy training data `grocery_stores_2023-05-25.csv` into `data/raw/` manually.

## Input data
- RUIAN attributes: `data/raw/stavebni_objekty_jmk_atributy_3035.gpkg` (currently not used for learning)
- BUG attributes: `data/raw/cell_values_bmo.csv`
- Grocery stores data: `data/raw/grocery_stores_2023-05-25.csv`

## Import data
```bash
# start database
make up

# import data to database (RUIAN attributes, BUG attributes, chronotope annotations)
make db-import

# ensure materialized views in database (create dummy columns from RUIAN)
make db-ensure-views
```

### Database
Table `cell_values` contains 28,322 BMO cells with cell BUG attributes.

Table `all_rows_all_columns` contains 516,453 building parts divided by BMO cells, each building part holds attributes of building (RUIAN). There are 25,059 cells with at least one building part.

Materialized view `cell_ruian_training` contains 25,059 cells with RUIAN attributes.

Materialized view `grocery_stores_geom` contains 36,972 annotated "popularity". Each record is related to one hour of a week of one grocery store (i.e. one grocery store consists of max 168 records).

## Machine learning
```bash
make learn
```

The script `make learn` joins BUG attributes from `cell_values` and annotations from `grocery_stores_geom`.

Popularity is predicted only for BMO and only for records whose annotated popularity > 0. 

Predictions are saved in following tables:
- `all_with_predictions` (17,331 records) one record = one predicted value
- `all_predictions_geom` (219 records) prediction statistics per grocery store
- `all_predictions_csv` (2,856) two records per grocery store and day of week (popularity and predicted popularity in each hour of the day)

Model precisions are located in `mlearn/precision.csv` file.

Export predictions for all cells:
```bash
make db-predictions-export
```
Predictions are located in `data/derived/predikce.shp` and `predikce_obchod_den.csv` files.
