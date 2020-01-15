.PHONY: test

download-data:
	rclone copy gdrive-jirikozel:/business/altimapo/chronotypy/data data/raw
	cd data/raw && { curl -O https://vdp.cuzk.cz/vymenny_format/soucasna/20191231_OB_582786_UKSH.xml.zip ; cd -; }
	unzip data/raw/20191231_OB_582786_UKSH.xml.zip -d data/raw/
	rm -rf data/raw/20191231_OB_582786_UKSH.xml.zip

up:
	docker-compose up -d postgresql

gdal-bash:
	docker-compose run --rm gdal sh

psql:
	docker-compose run -e PGPASSWORD=docker --entrypoint "psql -U docker -p 5432 -h postgresql gis" --rm postgresql

db-fix-epsg-5514:
	docker-compose run -e PGPASSWORD=docker --entrypoint "psql -U docker -p 5432 -h postgresql gis -f /data/5514.sql" --rm postgresql

db-import:
	docker-compose run --rm gdal ogr2ogr -t_srs EPSG:3857 -nln zsj -f PostgreSQL "PG:host=postgresql port=5432 dbname=gis user=docker password=docker" /data/raw/20191231_OB_582786_UKSH.xml Zsj

