# Chronotopes

## Download data
Either configure [Google Drive **Shared Drive** (Team Drive)](https://rclone.org/drive/) using `rclone config` and run `make download-data`, or download [`raw` folder](https://drive.google.com/drive/folders/1ly6ypgG6LG3fiLFmBDLnCrJNb_XK40ay) into `data/raw` manually.

## Import data
```bash
# start database
make up

# import data to database
make db-import

# ensure database views
make db-ensure-views
```

## Machine learning
```bash
make learn
```

## Upload data
Either run `make upload-data`, or upload contents of `data/derived`  into [`derived` folder](https://drive.google.com/drive/folders/1veKmByAmkgi-ZcmspxQD3CTmuLUUYCaC) manually.

