/*
Navicat MariaDB Data Transfer

Source Server         : 192.168.12.120
Source Server Version : 100027
Source Host           : 192.168.12.120:3306
Source Database       : useradmin

Target Server Type    : MariaDB
Target Server Version : 100027
File Encoding         : 65001

Date: 2016-10-30 17:22:02
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for privileges
-- ----------------------------
DROP TABLE IF EXISTS `privileges`;
CREATE TABLE `privileges` (
  `pid` int(11) NOT NULL AUTO_INCREMENT,
  `pname` varchar(64) NOT NULL,
  `plist` set('show_local','show_all','update_user') NOT NULL DEFAULT 'show_local',
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of privileges
-- ----------------------------
INSERT INTO `privileges` VALUES ('1', 'user', 'show_local');
INSERT INTO `privileges` VALUES ('2', 'admin', 'show_local,show_all,update_user');

-- ----------------------------
-- Table structure for userinfo
-- ----------------------------
DROP TABLE IF EXISTS `userinfo`;
CREATE TABLE `userinfo` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `pwd` char(41) NOT NULL,
  `email` varchar(128) NOT NULL,
  `privilege_id` int(11) NOT NULL,
  PRIMARY KEY (`uid`),
  KEY `fk_u_p` (`privilege_id`),
  CONSTRAINT `fk_u_p` FOREIGN KEY (`privilege_id`) REFERENCES `privileges` (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of userinfo
-- ----------------------------
INSERT INTO `userinfo` VALUES ('1', 'huxianglin', '*A3107092EE4306A7FEBEEAB4F42F8A2E93699510', 'a714585725@qq.com', '2');
INSERT INTO `userinfo` VALUES ('3', 'yuanhao', '*5A37C13BF8F3C3B1D271F89AE911D44192F5EC05', 'yuanhao@qq.com', '2');
INSERT INTO `userinfo` VALUES ('4', 'alex', '*8258F2618980E77E5220ECD738182656223809C1', 'alex3715@163.com', '1');
