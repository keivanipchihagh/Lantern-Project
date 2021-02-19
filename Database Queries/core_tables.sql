CREATE TABLE `core_message` (
  `id` int PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
  `content` varchar(300) NOT NULL COMMENT 'The transmitted massage',
  `ip` varchar(15) COMMENT 'IP Address the message is transmitted from',
  `sender` varchar(6) COMMENT 'Sender',
  `datetime` datetime NOT NULL COMMENT 'Time of the message submission',
  `session_id` int NOT NULL COMMENT 'Foreign Key'
);

CREATE TABLE `core_session` (
  `id` int PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
  `session_key` varchar(64) UNIQUE NOT NULL COMMENT 'Unique key for the session',
  `status` ENUM ('open', 'closed') NOT NULL COMMENT 'Current state of the session',
  `starred` boolean NOT NULL DEFAULT 0 COMMENT 'Starred message',
  `date_opened` datetime NOT NULL COMMENT 'Starting datetime',
  `date_closed` datetime COMMENT 'Ending datetime',
  `user_id` int COMMENT 'Foreign Key',
  `site_id` int NOT NULL COMMENT 'Foreign Key'
);

CREATE TABLE `core_user` (
  `id` int PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
  `firstname` varchar(30) NOT NULL COMMENT 'Firstname',
  `lastname` varchar(30) NOT NULL COMMENT 'Lastname',
  `email` varchar(50) UNIQUE NOT NULL COMMENT 'Email Address',
  `username` varchar(30) UNIQUE NOT NULL COMMENT 'Unique username',
  `password` varchar(30) NOT NULL COMMENT 'SHA-512 hashed password',
  `phonenumber` varchar(12) NOT NULL COMMENT 'Phone Number',
  `role` ENUM ('staff', 'admin', 'agent') NOT NULL COMMENT 'Role of the user',
  `country` varchar(30) COMMENT 'Country',
  `city` varchar(30) COMMENT 'City',
  `bio` varchar(75) COMMENT 'Bio',
  `rating` float COMMENT 'Rating of the user: 8.7 / 10',
  `user_key` varchar(255) UNIQUE NOT NULL COMMENT 'Unique key for the user',
  `last_login` datetime COMMENT 'Last online datetime',
  `date_joined` datetime COMMENT 'datetime the user was registered',
  `site_id` int NOT NULL COMMENT 'Foregin Key'
);

CREATE TABLE `core_site` (
  `id` int PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
  `url` varchar(50) UNIQUE NOT NULL COMMENT 'Registered URL',
  `private_key` varchar(512) UNIQUE NOT NULL COMMENT 'Public API key',
  `public_key` varchar(512) UNIQUE NOT NULL COMMENT 'Private API key',
  `date_joined` datetime NOT NULL COMMENT 'Registered datetime',
  `date_expires` datetime NOT NULL COMMENT 'Expire due datetime',
  `service` boolean COMMENT 'Accept service'
);

ALTER TABLE `core_message` ADD FOREIGN KEY (`session_id`) REFERENCES `core_session` (`id`);

ALTER TABLE `core_session` ADD FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`);

ALTER TABLE `core_user` ADD FOREIGN KEY (`site_id`) REFERENCES `core_site` (`id`);

ALTER TABLE `core_session` ADD FOREIGN KEY (`site_id`) REFERENCES `core_site` (`id`);
