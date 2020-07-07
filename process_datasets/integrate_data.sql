-- update mh services data
UPDATE final_buildings_set SET total_services = (SELECT COUNT(*) FROM house_id_mental_health WHERE house_id= :v1 ) WHERE house_id= :v1;

-- update subway_entrance
UPDATE final_buildings_set SET total_entrances = (SELECT COUNT(*) FROM building_to_subway WHERE house_id= :v1 ) WHERE house_id= :v1;

-- update crime data
DROP VIEW IF EXISTS crime_data
CREATE VIEW crime_data AS SELECT * FROM nypd_crime_data NATURAL JOIN building_id_to_crime_id WHERE house_id= :v1;
UPDATE final_buildings_set SET total_felonies = (SELECT COUNT(*) FROM crime_data WHERE "LAW_CAT_CD"='FELONY') WHERE house_id= :v1;
UPDATE final_buildings_set SET total_misdemeanors = (SELECT COUNT(*) FROM crime_data WHERE "LAW_CAT_CD"='MISDEMEANOR' ) WHERE house_id= :v1;
UPDATE final_buildings_set SET total_violations = (SELECT COUNT(*) FROM crime_data WHERE "LAW_CAT_CD"='VIOLATION' ) WHERE house_id= :v1;
UPDATE final_buildings_set SET total_crimes = (SELECT total_felonies+total_misdemeanors+total_violations FROM final_buildings_set WHERE house_id= :v1 ) WHERE house_id= :v1;



-- update collission_data
DROP VIEW IF EXISTS collission_data;
CREATE VIEW collission_data AS SELECT * FROM vehicle_collissions NATURAL JOIN building_to_collissions WHERE house_id= :v1;

UPDATE final_buildings_set SET total_collissions = (SELECT COUNT(*) FROM building_to_collissions WHERE house_id= :v1 ) WHERE house_id= :v1;
UPDATE final_buildings_set SET total_injured = (SELECT SUM(num_injured) FROM collission_data ) WHERE house_id= :v1;
UPDATE final_buildings_set SET total_killed = (SELECT SUM(num_killed) FROM collission_data ) WHERE house_id= :v1;
UPDATE final_buildings_set SET total_affected = (SELECT total_killed+total_injured FROM final_buildings_set WHERE house_id= :v1 ) WHERE house_id= :v1;
