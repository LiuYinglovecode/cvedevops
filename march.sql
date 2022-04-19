DROP TABLE IF EXISTS march;
CREATE TABLE march (
  `id` int NOT NULL AUTO_INCREMENT,
  `ip` VARCHAR(32) NOT NULL,
  `os` VARCHAR(20),
  `levels` VARCHAR(2),
  `vulneral` VARCHAR(100),
  `software` VARCHAR(50),
  `status` VARCHAR(3),
  `method` VARCHAR(255),
  PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='ipcveinfo';
