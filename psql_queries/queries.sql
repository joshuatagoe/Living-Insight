CREATE TABLE num_mh_service_building AS (SELECT house_id, COUNT(*) AS num_mental_services FROM house_id_mental_health GROUP BY house_id);
CREATE TABLE total_subway_entrances_building AS (SELECT house_id, COUNT(*) AS subway_entrances FROM building_to_subway GROUP BY house_id);
SELECT house_id, COUNT(*) AS total_collissions, SUM(num_injured) AS total_injured, SUM(num_killed) AS total_killed FROM vehicle_collissions NATURAL JOIN building_to_collissions GROUP BY house_id;
DELETE FROM vehicle_collissions WHERE collision_id ISNULL;
ALTER TABLE vehicle_collissions ALTER COLUMN num_injured TYPE INT USING num_injured::integer;
CREATE TABLE vehicle_collission_total_data_building AS (SELECT house_id, COUNT(*) AS total_collissions, SUM(num_injured) AS total_injured, SUM(num_killed) AS total_killed FROM vehicle_collissions NATURAL JOIN building_to_collissions GROUP by house_id);
SELECT DISTINCT * FROM building_to_air_quality NATURAL JOIN air_quality WHERE house_id='B00269850-I1' AND year_description='2013';
SELECT DISTINCT * FROM building_to_air_quality NATURAL JOIN air_quality WHERE house_id='B00269850-I1';
SELECT DISTINCT * FROM building_to_air_quality NATURAL JOIN air_quality WHERE house_id='B00269850-I1' AND geo_type_name!='Borough';
SELECT DISTINCT * FROM building_to_air_quality NATURAL JOIN air_quality WHERE house_id='M00174424-I1' AND geo_type_name!='Borough';
SELECT * FROM building_id_to_crime_id NATURAL JOIN nyp_crime_data WHERE house_id='M00174424-I1';
SELECT  LAW_CAT_CD, OFNS_DESC FROM building_id_to_crime_id NATURAL JOIN nypd_crime_data WHERE house_id='B00269850-I1';


/* Calculate total number of felonies and misdemeanor complaints around every building */
WITH UPD AS ( SELECT  * FROM building_id_to_crime_id NATURAL JOIN nypd_crime_data WHERE house_id='B00269850-I1'; ) SELECT "LAW_CAT_CD", "OFNS_DESC" FROM upd;
CREATE TABLE num_felonies AS SELECT house_id, COUNT(*) AS total_felonies FROM building_id_to_crime_id NATURAL JOIN nypd_crime_data WHERE "LAW_CAT_CD"='FELONY' GROUP BY house_id;
CREATE TABLE num_misdemeanors AS SELECT house_id, COUNT(*) AS total_misdemeanors FROM building_id_to_crime_id NATURAL JOIN nypd_crime_data WHERE "LAW_CAT_CD"='MISDEMEANOR' GROUP BY house_id;
CREATE TABLE num_violations AS SELECT house_id, COUNT(*) AS total_violations FROM building_id_to_crime_id NATURAL JOIN nypd_crime_data WHERE "LAW_CAT_CD"='VIOLATION' GROUP BY house_id;
CREATE TABLE felonies_aggregate_data AS SELECT avg(total_felonies) AS mean_felonies, stddev(total_felonies) AS sd_felonies FROM num_felonies;
CREATE TABLE misdemeanors_aggregate_data AS SELECT avg(total_misdemeanors) AS mean_misdemeanors, stddev(total_misdemeanors) AS sd_misdemeanors FROM num_misdemeanors;
CREATE TABLE violations_aggregate_data AS SELECT avg(total_violations) AS mean_violations, stddev(total_violations) AS sd_violations FROM num_violations;
/*run this query whenever you need to calculate # of complaints for each crime type, KY_CD and arrange by most frequently occuring */
SELECT "KY_CD", "OFNS_DESC" COUNT(*) AS total_complaints FROM building_id_to_crime_id NATURAL JOIN nypd_crime_data WHERE "house_id"='B00269850-I1' GROUP BY "KY_CD" ORDER BY total_complaints DESC;


WITH upd2 AS (WITH upd AS (SELECT house_id, COUNT(*) AS num_mental_services FROM house_id_mental_health GROUP BY house_id) SELECT * FROM buildings INNER JOIN upd ON buildings.house_id=upd.house_id) SELECT * FROM upd2 NATURAL JOIN mental_health;
WITH upd AS ( SELECT * FROM house_id_mental_health WHERE house_id='M00174424-I1' ) SELECT * FROM mental_health INNER JOIN upd ON mental_health.query_id=upd.query_id;
WITH upd AS ( SELECT * FROM building_to_collissions WHERE house_id='B00269850-I1') SELECT * FROM vehicle_collissions INNER JOIN upd ON vehicle_collissions.collision_id=upd.collision_id WHERE (num_injured,num_killed) IS NOT NULL ORDER BY (num_killed+num_injured) DESC LIMIT 20;

/* calculate mean and standard deviation */
/*mH used as an example */

CREATE TABLE num_services AS SELECT house_id, COUNT(*) AS total_services FROM house_id_mental_health NATURAL JOIN mental_health GROUP BY house_id;
CREATE TABLE mh_aggregate_data AS SELECT avg(total_services) AS avg_services, stddev(total_services) AS sd_services FROM num_services;

/*subway_entrances*/
CREATE TABLE num_subway AS SELECT house_id, COUNT(*) AS total_entrances FROM building_to_subway NATURAL JOIN subway_entrances GROUP BY house_id;
CREATE TABLE subway_aggregate_data AS SELECT avg(total_entrances) AS avg_entrances, stddev(total_entrances) AS sd_entrances FROM num_subway;


/* colissions */
CREATE TABLE num_collissions AS SELECT house_id, COUNT(*) AS total_collissions, SUM(num_injured) AS total_injured, SUM(num_killed) AS total_killed, SUM(num_injured+num_killed) AS total_affected FROM building_to_collissions NATURAL JOIN vehicle_collissions GROUP BY house_id;
CREATE TABLE collissions_aggregate_data AS SELECT avg(total_collissions) AS mean_collissions, stddev(total_collissions) AS sd_collissions, avg(total_injured) AS avg_injured, stddev(total_injured) AS sd_injured, avg(total_killed) AS avg_killed, stddev(total_killed) AS sd_killed, AVG(total_affected) AS avg_affected, stddev(total_affected) AS sd_affected FROM num_collissions;

/* create new table that JOINs all tables to main buildings table */
CREATE TABLE final_buildings_set AS SELECT * FROM buildings_with_kml NATURAL JOIN  num_services NATURAL JOIN mh_aggregate_data NATURAL JOIN num_subway NATURAL JOIN num_collissions NATURAL JOIN num_felonies NATURAL JOIN num_misdemeanors NATURAL JOIN num_violations;