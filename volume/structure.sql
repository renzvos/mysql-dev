SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
#Setting Up Users

#Administration
GRANT SELECT,INSERT,UPDATE ON *.* TO 'admin'@'%';
CREATE USER 'staff_reader'@'%' IDENTIFIED BY 'this@is@staff@reader';
GRANT SELECT, LOCK TABLES, SHOW VIEW ON *.* TO 'staff_reader'@'%';

#Apps
CREATE USER 'rex_prealpha'@'172.0.0.2' IDENTIFIED BY 'this.is.a.rex.prealpha';
GRANT SELECT,INSERT,UPDATE ON rex_prealpha.* TO 'rex_prealpha'@'172.0.0.2';

#Backup Automation
CREATE USER 'backupclient'@'localhost' IDENTIFIED BY 'arshad956';
GRANT LOCK TABLES, SHOW VIEW, RELOAD ON *.* TO 'backupclient'@'localhost'; 
GRANT SELECT ON rex_prealpha.* TO 'backupclient'@'localhost'; 

#Structure for Rex-prealpha
START TRANSACTION;
CREATE DATABASE IF NOT EXISTS rex_prealpha;
USE rex_prealpha;
CREATE TABLE `events` (
  `id` int(11) NOT NULL,
  `session_id` int(11) NOT NULL,
  `datetime` datetime NOT NULL DEFAULT current_timestamp(),
  `action` varchar(30) NOT NULL,
  `window` varchar(100) NOT NULL,
  `tail` int(11) DEFAULT NULL,
  `extra_data` mediumtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE `passwords` (
  `name` varchar(30) NOT NULL,
  `passcode` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `sessions` (
  `id` int(11) NOT NULL,
  `datetime` datetime NOT NULL DEFAULT current_timestamp(),
  `project_name` varchar(50) NOT NULL,
  `source` int(11) NOT NULL,
  `user_id` varchar(60) NOT NULL,
  `entry_page` varchar(250) NOT NULL,
  `extra_data` mediumtext NOT NULL,
  `network_location` varchar(100) NOT NULL,
  `gps_location` varchar(100) NOT NULL,
  `device` varchar(100) NOT NULL,
  `project_version` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




CREATE TABLE `sources` (
  `id` int(11) NOT NULL,
  `plan_name` varchar(50) NOT NULL,
  `mode` varchar(20) NOT NULL,
  `extra_data` mediumtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


ALTER TABLE `events`
  ADD PRIMARY KEY (`id`),
  ADD KEY `session_link` (`session_id`),
  ADD KEY `tail_link` (`tail`);


ALTER TABLE `sessions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `source_c` (`source`);


ALTER TABLE `sources`
  ADD PRIMARY KEY (`id`);



ALTER TABLE `events`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;


ALTER TABLE `sessions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;

ALTER TABLE `sources`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=0;


ALTER TABLE `events`
  ADD CONSTRAINT `session_link` FOREIGN KEY (`session_id`) REFERENCES `sessions` (`id`),
  ADD CONSTRAINT `tail_link` FOREIGN KEY (`tail`) REFERENCES `events` (`id`);


ALTER TABLE `sessions`
  ADD CONSTRAINT `source_c` FOREIGN KEY (`source`) REFERENCES `sources` (`id`);
COMMIT;


INSERT INTO `sources` (`id`, `plan_name`, `mode`, `extra_data`) VALUES
(1, '', 'Free', '{}');


INSERT INTO `sessions` (`id`, `datetime`, `project_name`, `source`, `user_id`, `entry_page`, `extra_data`, `network_location`, `gps_location`, `device`, `project_version`) VALUES
(1, '2022-02-09 09:44:13', 'REX Server', 1, '', '', '', '{}', '{}', '', '1.0.0');

INSERT INTO `passwords` (`name`, `passcode`) VALUES
('masterpassword', 'arshadnazirbabu');
