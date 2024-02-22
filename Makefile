.PHONY: test

download-data:
	rclone copy --progress gdrive-chronotopy:/06_Vystupy/01_priprava_terenovaci_casti/strojove_uceni/raw data/raw

up:
	docker-compose up -d postgresql

gdal-bash:
	docker-compose run --rm gdal bash

psql:
	docker-compose run -e PGPASSWORD=docker --entrypoint "psql -U docker -p 5432 -h postgresql gis" --rm postgresql

db-import:
	docker-compose run --rm gdal ogr2ogr -nln all_rows_all_columns -overwrite -f PostgreSQL "PG:host=postgresql port=5432 dbname=gis user=docker password=docker" /data/raw/stavebni_objekty_jmk_atributy_3035.gpkg stavebni_objekty_jmk_atributy_3035
	docker-compose run --rm --no-deps trainer python /app/import_csv.py
	docker-compose run --rm gdal ogr2ogr -nln unknown_grocery_stores -overwrite -f PostgreSQL "PG:host=postgresql port=5432 dbname=gis user=docker password=docker" /data/raw/unknown_grocery_stores.geojson new_grocery_stores

db-ensure-views:
	docker-compose run --rm --no-deps trainer python /app/ensure_views.py

db-predictions-export:
	mkdir -p data/derived
	docker-compose run --rm gdal ogr2ogr -overwrite -lco ENCODING=UTF-8 -f "ESRI Shapefile" /data/derived/predikce.shp "PG:host=postgresql port=5432 dbname=gis user=docker password=docker" -sql "select * from all_predictions_geom;"
	rm -rf data/derived/predikce_obchod_den.csv
	docker-compose run -e PGPASSWORD=docker --entrypoint "psql -U docker -p 5432 -h postgresql gis" --rm postgresql -c "COPY all_predictions_csv TO '/data/derived/predikce_obchod_den.csv' DELIMITER ',' CSV HEADER;"
	docker-compose run -e PGPASSWORD=docker --entrypoint "bash" --rm postgresql -c "chmod 666 /data/derived/predikce_obchod_den.csv"
	docker-compose run --rm gdal ogr2ogr -overwrite -lco ENCODING=UTF-8 -f "ESRI Shapefile" /data/derived/predikce_unknown_grocery.shp "PG:host=postgresql port=5432 dbname=gis user=docker password=docker" -sql "select * from unknown_predictions_geom;"


stop-all-docker-containers:
	docker stop $$(docker ps -q)

learn:
	docker-compose run --rm --no-deps trainer python /app/mlearn1.py

bash:
	docker-compose run --rm --no-deps trainer bash

bash-root:
	docker-compose run --rm --no-deps --user root trainer bash

build:
	docker-compose build trainer

imposm-download-data:
	mkdir -p temp/imposm
	docker-compose -f docker-compose.yml run --rm --no-deps imposm wget -O /temp/imposm/sample.osm.pbf https://download.geofabrik.de/europe/czech-republic-latest.osm.pbf

imposm-import-data:
	docker-compose -f docker-compose.yml up -d postgresql
	docker-compose -f docker-compose.yml run --rm imposm imposm import -config /app/imposm/config.json -dbschema-import osm_import -dbschema-production osm -dbschema-backup osm_backup -read /temp/imposm/sample.osm.pbf -write
	docker-compose run -e PGPASSWORD=docker --entrypoint "psql -U docker -p 5432 -h postgresql gis" --rm postgresql psql -f /imposm/after_imposm.sql

imposm-bash:
	docker-compose run --rm imposm bash
