CREATE DATABASE IF NOT EXISTS srsdb;
USE srsdb;

CREATE TABLE IF NOT EXISTS `users` (
  `pid` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `uuid` varchar(56) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `sms` varchar(25) DEFAULT NULL,
  `created` int(11) DEFAULT NULL,
  `lastseen` int(11) DEFAULT NULL
);
