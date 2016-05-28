DROP TRIGGER IF EXISTS ins_relations;

delimiter //

CREATE TRIGGER ins_relations AFTER INSERT ON `lab02db`.`lab02_photo`
FOR EACH ROW
BEGIN
	IF NEW.photographer_id IS NOT NULL THEN
		SET @ph_cam = (SELECT id from lab02_photographer_cameras WHERE
				photographer_id = NEW.photographer_id AND camera_id = NEW.camera_id);
		IF @ph_cam IS NULL THEN
			INSERT INTO `lab02db`.`lab02_photographer_cameras`(photographer_id,
					camera_id) VALUES(NEW.photographer_id, NEW.camera_id);
		END IF;
   		SET @ph_loc = (SELECT id from lab02_photographer_locations WHERE
				photographer_id = NEW.photographer_id AND location_id = NEW.location_id);
		IF @ph_loc IS NULL THEN
			INSERT INTO `lab02db`.`lab02_photographer_locations`(photographer_id,
					location_id) VALUES(NEW.photographer_id, NEW.location_id);
		END IF;
	END IF;
END;
//
delimiter ;

SHOW TRIGGERS LIKE 'lab02_photo';

SELECT * from lab02_photographer_cameras WHERE
		photographer_id = 78 AND camera_id = 94;