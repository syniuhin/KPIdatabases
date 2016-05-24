DROP TRIGGER IF EXISTS ins_relations;

delimiter //

CREATE TRIGGER ins_relations AFTER INSERT ON `lab02db`.`lab02_photo`
FOR EACH ROW
BEGIN
	IF @trigger_disabled IS NULL AND NEW.photographer_id IS NOT NULL THEN
		INSERT INTO `lab02db`.`lab02_photographer_cameras`(photographer_id, camera_id) VALUES(NEW.photographer_id, NEW.camera_id);
        INSERT INTO `lab02db`.`lab02_photographer_locations`(photographer_id, location_id) VALUES(NEW.photographer_id, NEW.location_id);
	END IF;
END;
//
delimiter ;

SHOW TRIGGERS LIKE 'lab02_photo';