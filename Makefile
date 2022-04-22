.PHONY: test

download-data:
	rclone sync --progress gdrive-chronotopy:/06_Vystupy/01_priprava_terenovaci_casti/strojove_uceni/raw data/raw

up:
	docker-compose up -d postgresql

gdal-bash:
	docker-compose run --rm gdal bash

psql:
	docker-compose run -e PGPASSWORD=docker --entrypoint "psql -U docker -p 5432 -h postgresql gis" --rm postgresql

db-import:
	docker-compose run --rm gdal ogr2ogr -nln all_rows_all_columns -overwrite -f PostgreSQL "PG:host=postgresql port=5432 dbname=gis user=docker password=docker" /data/raw/stavebni_objekty_jmk_atributy_3035.gpkg stavebni_objekty_jmk_atributy_3035
	docker-compose run --rm gdal ogr2ogr -nln joint_rows_ruian -overwrite -f PostgreSQL "PG:host=postgresql port=5432 dbname=gis user=docker password=docker" data/raw/stavebni_objekty_jmk_3035_full_geom.gpkg stavebni_objekty_jmk_3035

db-ensure-views:
	docker-compose run -e PGPASSWORD=docker --entrypoint "psql -U docker -p 5432 -h postgresql gis" --rm postgresql psql -f /data/views.sql

db-predictions-export:
	mkdir -p data/derived
	docker-compose run --rm gdal ogr2ogr -overwrite -lco ENCODING=UTF-8 -f "ESRI Shapefile" /data/derived/predikce.shp "PG:host=postgresql port=5432 dbname=gis user=docker password=docker" -sql "select * from joint_rows_predictions_geom;"

stop-all-docker-containers:
	docker stop $$(docker ps -q)

upload-data:
	rclone copy --progress data/derived gdrive-chronotopy:/06_Vystupy/01_priprava_terenovaci_casti/strojove_uceni/derived

learn:
	docker-compose run --rm --no-deps trainer python /app/mlearn1.py

bash:
	docker-compose run --rm --no-deps trainer bash

bash-root:
	docker-compose run --rm --no-deps --user root trainer bash

build:
	docker-compose build trainer
