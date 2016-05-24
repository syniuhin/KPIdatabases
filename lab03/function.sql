SELECT * FROM lab02_camera;

DROP FUNCTION IF EXISTS camera_usage;

delimiter $$

CREATE FUNCTION camera_usage(cam_id INTEGER) RETURNS INTEGER
BEGIN
RETURN (SELECT COUNT(*) FROM lab02_photographer_cameras
		WHERE lab02_photographer_cameras.camera_id = cam_id);
END;

$$ delimiter ;

