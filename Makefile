.PHONY: test

download-data:
	rclone copy gdrive-jirikozel:/business/altimapo/chronotypy/data data/raw
	cd data/raw && { curl -O https://vdp.cuzk.cz/vymenny_format/soucasna/20191231_OB_582786_UKSH.xml.zip ; cd -; }
	unzip data/raw/20191231_OB_582786_UKSH.xml.zip -d data/raw/
	rm -rf data/raw/20191231_OB_582786_UKSH.xml.zip
	cd data/raw && { curl -O https://brnourbangrid.cz/static/grid-data/brnourbangrid--usually_resident_population--2011-03-26--e15d37.zip ; cd -; }
	cd data/raw && { curl -O https://brnourbangrid.cz/static/grid-data/brnourbangrid--occupied_jobs--2018--e64c61.zip ; cd -; }
	cd data/raw && { curl -O https://brnourbangrid.cz/static/grid-data/brnourbangrid--landcover_urban_atlas--2012--69ef7e.zip ; cd -; }
	cd data/raw && { curl -O https://brnourbangrid.cz/static/grid-data/brnourbangrid--builtup_area--2011--bc23b0.zip ; cd -; }
	cd data/raw && { curl -O https://brnourbangrid.cz/static/grid-data/brnourbangrid--number_of_inhabited_flats--2011-03-26--0d42ff.zip ; cd -; }
	mkdir -p data/derived
	rm -rf data/derived/*
	xlsx2csv -n prac_den data/raw/brno_2018_wd_RLI.xlsx data/derived/brno_2018_wd_RLI.csv

up:
	docker-compose up -d postgresql

gdal-bash:
	docker-compose run --rm gdal sh

psql:
	docker-compose run -e PGPASSWORD=docker --entrypoint "psql -U docker -p 5432 -h postgresql gis" --rm postgresql

db-fix-epsg-5514:
	docker-compose run -e PGPASSWORD=docker --entrypoint "psql -U docker -p 5432 -h postgresql gis -f /data/5514.sql" --rm postgresql

db-import:
	docker-compose run --rm gdal ogr2ogr -t_srs EPSG:3035 -nln zsj -f PostgreSQL "PG:host=postgresql port=5432 dbname=gis user=docker password=docker" /data/raw/20191231_OB_582786_UKSH.xml Zsj
	docker-compose run --rm gdal ogr2ogr -t_srs EPSG:3035 -nln bug_usually_resident_population -f PostgreSQL "PG:host=postgresql port=5432 dbname=gis user=docker password=docker" /vsizip/data/raw/brnourbangrid--usually_resident_population--2011-03-26--e15d37.zip
	docker-compose run --rm gdal ogr2ogr -t_srs EPSG:3035 -nln bug_occupied_jobs -f PostgreSQL "PG:host=postgresql port=5432 dbname=gis user=docker password=docker" /vsizip/data/raw/brnourbangrid--occupied_jobs--2018--e64c61.zip
	docker-compose run --rm gdal ogr2ogr -t_srs EPSG:3035 -nln bug_landcover -f PostgreSQL "PG:host=postgresql port=5432 dbname=gis user=docker password=docker" /vsizip/data/raw/brnourbangrid--landcover_urban_atlas--2012--69ef7e.zip
	docker-compose run --rm gdal ogr2ogr -t_srs EPSG:3035 -nln bug_builtup_area -f PostgreSQL "PG:host=postgresql port=5432 dbname=gis user=docker password=docker" /vsizip/data/raw/brnourbangrid--builtup_area--2011--bc23b0.zip
	docker-compose run --rm gdal ogr2ogr -t_srs EPSG:3035 -nln bug_inhabited_flats -f PostgreSQL "PG:host=postgresql port=5432 dbname=gis user=docker password=docker" /vsizip/data/raw/brnourbangrid--number_of_inhabited_flats--2011-03-26--0d42ff.zip
	docker-compose run --rm gdal ogr2ogr -overwrite -oo HEADERS=YES -oo AUTODETECT_TYPE=YES -nln chronotyp -f PostgreSQL "PG:host=postgresql port=5432 dbname=gis user=docker password=docker" /data/derived/brno_2018_wd_RLI.csv -sql 'select problém as problem, zsj_číslo_1 as zsj_kod, zsj_číslo_t as zsj_cislo_t, obyv, "0" as h0, "1" as h1, "2" as h2, "3" as h3, "4" as h4, "5" as h5, "6" as h6, "7" as h7, "8" as h8, "9" as h9, "10" as h10, "11" as h11, "12" as h12, "13" as h13, "14" as h14, "15" as h15, "16" as h16, "17" as h17, "18" as h18, "19" as h19, "20" as h20, "21" as h21, "22" as h22, "23" as h23 from brno_2018_wd_RLI'

stop-all-docker-containers:
	docker stop $$(docker ps -q)

