DROP TABLE IF EXISTS lab02_photo;
DROP TABLE IF EXISTS lab02_photographer_cameras;
DROP TABLE IF EXISTS lab02_photographer_locations;
DROP TABLE IF EXISTS lab02_camera;
DROP TABLE IF EXISTS lab02_location;
DROP TABLE IF EXISTS lab02_photographer;

--
-- Create model Camera
--
CREATE TABLE `lab02_camera` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(64) NOT NULL, `year_created` date NOT NULL, `version` integer NOT NULL);
--
-- Create model Location
--
CREATE TABLE `lab02_location` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(64) NOT NULL, `lat` double precision NOT NULL, `lng` double precision NOT NULL, `accessible` bool NOT NULL);
--
-- Create model Photo
--
CREATE TABLE `lab02_photo` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(64) NOT NULL, `aperture` double precision NOT NULL, `iso` integer NOT NULL, `shot_time` datetime(6) NOT NULL, `camera_id` integer NOT NULL, `location_id` integer NOT NULL);
--
-- Create model Photographer
--
CREATE TABLE `lab02_photographer` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(64) NOT NULL, `level` integer NOT NULL, `email` varchar(254) NOT NULL UNIQUE);
CREATE TABLE `lab02_photographer_cameras` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `photographer_id` integer NOT NULL, `camera_id` integer NOT NULL);
CREATE TABLE `lab02_photographer_locations` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `photographer_id` integer NOT NULL, `location_id` integer NOT NULL);
--
-- Add field photographer to photo
--
ALTER TABLE `lab02_photo` ADD COLUMN `photographer_id` integer NOT NULL;
ALTER TABLE `lab02_photo` ALTER COLUMN `photographer_id` DROP DEFAULT;
ALTER TABLE `lab02_photo` ADD CONSTRAINT `lab02_photo_camera_id_b11adf2f_fk_lab02_camera_id` FOREIGN KEY (`camera_id`) REFERENCES `lab02_camera` (`id`);
ALTER TABLE `lab02_photo` ADD CONSTRAINT `lab02_photo_location_id_60c6bbc5_fk_lab02_location_id` FOREIGN KEY (`location_id`) REFERENCES `lab02_location` (`id`);
ALTER TABLE `lab02_photographer_cameras` ADD CONSTRAINT `lab02_photogra_photographer_id_b8d131d2_fk_lab02_photographer_id` FOREIGN KEY (`photographer_id`) REFERENCES `lab02_photographer` (`id`);
ALTER TABLE `lab02_photographer_cameras` ADD CONSTRAINT `lab02_photographer_cameras_camera_id_af2ef068_fk_lab02_camera_id` FOREIGN KEY (`camera_id`) REFERENCES `lab02_camera` (`id`);
ALTER TABLE `lab02_photographer_cameras` ADD CONSTRAINT `lab02_photographer_cameras_photographer_id_47e9524f_uniq` UNIQUE (`photographer_id`, `camera_id`);
ALTER TABLE `lab02_photographer_locations` ADD CONSTRAINT `lab02_photogra_photographer_id_de438085_fk_lab02_photographer_id` FOREIGN KEY (`photographer_id`) REFERENCES `lab02_photographer` (`id`);
ALTER TABLE `lab02_photographer_locations` ADD CONSTRAINT `lab02_photographer_loc_location_id_c4196dd6_fk_lab02_location_id` FOREIGN KEY (`location_id`) REFERENCES `lab02_location` (`id`);
ALTER TABLE `lab02_photographer_locations` ADD CONSTRAINT `lab02_photographer_locations_photographer_id_9b12428d_uniq` UNIQUE (`photographer_id`, `location_id`);
CREATE INDEX `lab02_photo_2a69462d` ON `lab02_photo` (`photographer_id`);
ALTER TABLE `lab02_photo` ADD CONSTRAINT `lab02_photo_photographer_id_028d7cef_fk_lab02_photographer_id` FOREIGN KEY (`photographer_id`) REFERENCES `lab02_photographer` (`id`);

--
-- Alter field photographer on photo
--
ALTER TABLE `lab02_photo` DROP FOREIGN KEY `lab02_photo_photographer_id_028d7cef_fk_lab02_photographer_id`;
ALTER TABLE `lab02_photo` MODIFY `photographer_id` integer NULL;
ALTER TABLE `lab02_photo` ADD CONSTRAINT `lab02_photo_photographer_id_028d7cef_fk_lab02_photographer_id` FOREIGN KEY (`photographer_id`) REFERENCES `lab02_photographer` (`id`);
--
-- Alter field cameras on photographer
--
ALTER TABLE `lab02_photographer_cameras` DROP FOREIGN KEY `lab02_photographer_cameras_camera_id_af2ef068_fk_lab02_camera_id`;
ALTER TABLE `lab02_photographer_cameras` ADD CONSTRAINT `lab02_photographer_cameras_camera_id_af2ef068_fk_lab02_camera_id` FOREIGN KEY (`camera_id`) REFERENCES `lab02_camera` (`id`);
ALTER TABLE `lab02_photographer_cameras` DROP FOREIGN KEY `lab02_photogra_photographer_id_b8d131d2_fk_lab02_photographer_id`;
ALTER TABLE `lab02_photographer_cameras` ADD CONSTRAINT `lab02_photogra_photographer_id_b8d131d2_fk_lab02_photographer_id` FOREIGN KEY (`photographer_id`) REFERENCES `lab02_photographer` (`id`);
--
-- Alter field locations on photographer
--
ALTER TABLE `lab02_photographer_locations` DROP FOREIGN KEY `lab02_photographer_loc_location_id_c4196dd6_fk_lab02_location_id`;
ALTER TABLE `lab02_photographer_locations` ADD CONSTRAINT `lab02_photographer_loc_location_id_c4196dd6_fk_lab02_location_id` FOREIGN KEY (`location_id`) REFERENCES `lab02_location` (`id`);
ALTER TABLE `lab02_photographer_locations` DROP FOREIGN KEY `lab02_photogra_photographer_id_de438085_fk_lab02_photographer_id`;
ALTER TABLE `lab02_photographer_locations` ADD CONSTRAINT `lab02_photogra_photographer_id_de438085_fk_lab02_photographer_id` FOREIGN KEY (`photographer_id`) REFERENCES `lab02_photographer` (`id`);

--
-- Alter field photographer on photo
--
ALTER TABLE `lab02_photo` DROP FOREIGN KEY `lab02_photo_photographer_id_028d7cef_fk_lab02_photographer_id`;
ALTER TABLE `lab02_photo` ADD CONSTRAINT `lab02_photo_photographer_id_028d7cef_fk_lab02_photographer_id` FOREIGN KEY (`photographer_id`) REFERENCES `lab02_photographer` (`id`);

--
-- Alter field cameras on photographer
--
ALTER TABLE `lab02_photographer_cameras` DROP FOREIGN KEY `lab02_photographer_cameras_camera_id_af2ef068_fk_lab02_camera_id`;
ALTER TABLE `lab02_photographer_cameras` ADD CONSTRAINT `lab02_photographer_cameras_camera_id_af2ef068_fk_lab02_camera_id` FOREIGN KEY (`camera_id`) REFERENCES `lab02_camera` (`id`);
ALTER TABLE `lab02_photographer_cameras` DROP FOREIGN KEY `lab02_photogra_photographer_id_b8d131d2_fk_lab02_photographer_id`;
ALTER TABLE `lab02_photographer_cameras` ADD CONSTRAINT `lab02_photogra_photographer_id_b8d131d2_fk_lab02_photographer_id` FOREIGN KEY (`photographer_id`) REFERENCES `lab02_photographer` (`id`);
--
-- Alter field locations on photographer
--
ALTER TABLE `lab02_photographer_locations` DROP FOREIGN KEY `lab02_photographer_loc_location_id_c4196dd6_fk_lab02_location_id`;
ALTER TABLE `lab02_photographer_locations` ADD CONSTRAINT `lab02_photographer_loc_location_id_c4196dd6_fk_lab02_location_id` FOREIGN KEY (`location_id`) REFERENCES `lab02_location` (`id`);
ALTER TABLE `lab02_photographer_locations` DROP FOREIGN KEY `lab02_photogra_photographer_id_de438085_fk_lab02_photographer_id`;
ALTER TABLE `lab02_photographer_locations` ADD CONSTRAINT `lab02_photogra_photographer_id_de438085_fk_lab02_photographer_id` FOREIGN KEY (`photographer_id`) REFERENCES `lab02_photographer` (`id`);
