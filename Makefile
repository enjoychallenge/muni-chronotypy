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

db-guess-import:
	docker-compose run --rm gdal ogr2ogr -overwrite -oo HEADERS=YES -oo AUTODETECT_TYPE=YES -nln chronotyp_guess -f PostgreSQL "PG:host=postgresql port=5432 dbname=gis user=docker password=docker" data/derived/zsj_full_guess.csv

db-guess-export:
	docker-compose run --rm gdal ogr2ogr -overwrite -lco ENCODING=UTF-8 -f "ESRI Shapefile" /data/derived/chronotyp_guess.shp "PG:host=postgresql port=5432 dbname=gis user=docker password=docker" -sql "select zsj_kod, zsj_nazev, builtup_area as built_area, inhabited_flats as flats, occupied_jobs as jobs, usually_resident_population as usual_pop, retail_sales_area as retailarea, chronotyp, chronotyp_guessed as cht_guess, zsj.originalnihranice from chronotyp_guess left join zsj on zsj.kod = chronotyp_guess.zsj_kod;"

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
