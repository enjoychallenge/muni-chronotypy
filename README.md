# Chronotopes

## Download data
Either configure [Google Drive **Shared Drive** (Team Drive)](https://rclone.org/drive/) using `rclone config` and run `make download-data`, or download [`raw` folder](https://drive.google.com/drive/folders/1ly6ypgG6LG3fiLFmBDLnCrJNb_XK40ay) into `data/raw` manually.

## Import data
```bash
# start database
make up

# import data to database (BUG attributes, RUIAN attributes, chronotope annotations)
make db-import

# ensure materialized views in database
make db-ensure-views
```

### Database
Table `cell_values` contains 28,322 BMO cells with cell BUG attributes.

Table `all_rows_all_columns` contains 516,453 building parts divided by BMO cells, each building part holds attributes of building (RUIAN). There are 25,059 cells with at least one building part.

Table `jmk_cell_chronotopes_annotations` contains 116,922 JMK cells with 440 annotated cells. Annotation uses 6 types of chronotopes.

Materialized view `cell_ruian_training` contains 25,059 cells with RUIAN attributes.

## Machine learning
```bash
make learn
```

The script `make learn` joins BUG attributes from `cell_values`, RUIAN attributes from `cell_ruian_training` and annotations from `jmk_cell_chronotopes_annotations`.

Chronotope types are predicted only for cells with built-up area > 500 m2. It lowers original 28,322 BMO cells to 5,771 cells in BMO and 1,776 cells in Brno.

The script computes cross validation of 14 models, chooses the best (the one with the highest precision), fits and evaluates the model giving its accuracy, and finally predicts chronotope of each cell. This process is done four times:
- for BMO cells and 6 chronotope types A, B, C, D, E, F
- for Brno cells and 6 chronotope types A, B, C, D, E, F
- for BMO cells and 2 chronotope types ABC, DEF
- for Brno cells and 2 chronotope types ABC, DEF

## Upload data
Either run `make upload-data`, or upload contents of `data/derived`  into [`derived` folder](https://drive.google.com/drive/folders/1veKmByAmkgi-ZcmspxQD3CTmuLUUYCaC) manually.

