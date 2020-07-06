CREATE VIEW collission_data AS SELECT * FROM vehicle_collissions NATURAL JOIN building_to_collissions WHERE house_id= :v1;

UPDATE final_buildings_set SET total_collissions = (SELECT COUNT(*) FROM building_to_collissions WHERE house_id= :v1 ) WHERE house_id= :v1;
UPDATE final_buildings_set SET total_injured = (SELECT SUM(num_injured) FROM collission_data ) WHERE house_id= :v1;
UPDATE final_buildings_set SET total_killed = (SELECT SUM(num_killed) FROM collission_data ) WHERE house_id= :v1;
UPDATE final_buildings_set SET total_affected = (SELECT total_killed+total_injured FROM final_buildings_set WHERE house_id= :v1 ) WHERE house_id= :v1;