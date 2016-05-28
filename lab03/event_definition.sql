SELECT @@global.event_scheduler;

SET @@global.event_scheduler = 1;

DROP EVENT IF EXISTS clear_photos;

CREATE EVENT clear_photos
	ON SCHEDULE EVERY 1 DAY
    STARTS CURRENT_TIMESTAMP
	COMMENT 'Clears all the photos'
	DO
        DELETE FROM `lab02db`.`lab02_photo` WHERE camera_id IN
			(SELECT id FROM `lab02db`.`lab02_camera` WHERE name LIKE "Leica%");

ALTER EVENT clear_photos
	ON SCHEDULE EVERY 1 MINUTE
    STARTS CURRENT_TIMESTAMP;
                       
DELETE FROM `lab02db`.`lab02_photo` WHERE camera_id IN
	(SELECT id FROM `lab02db`.`lab02_camera` WHERE name LIKE "Leica%");