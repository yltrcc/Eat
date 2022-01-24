/*
Navicat MySQL Data Transfer

Source Server         : eat_system
Source Server Version : 80020
Source Host           : localhost:3306
Source Database       : eat_system

Target Server Type    : MYSQL
Target Server Version : 80020
File Encoding         : 65001

Date: 2021-05-09 14:14:35
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for tb_comment
-- ----------------------------
DROP TABLE IF EXISTS `tb_comment`;
CREATE TABLE `tb_comment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `comment` varchar(255) DEFAULT NULL,
  `user_id` int NOT NULL COMMENT '用户主键',
  `food_id` int NOT NULL COMMENT '食物主键',
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_name` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

-- ----------------------------
-- Records of tb_comment
-- ----------------------------

-- ----------------------------
-- Table structure for tb_food
-- ----------------------------
DROP TABLE IF EXISTS `tb_food`;
CREATE TABLE `tb_food` (
    `food_id` int NOT NULL AUTO_INCREMENT,
    `food_name` varchar(20) NOT NULL,
    `food_cal` varchar(20) NOT NULL,
    `taste` varchar(10) NOT NULL,
    `location` varchar(20) NOT NULL,
    `recorde` int DEFAULT NULL,
    `add_time` datetime NOT NULL,
    `user_id` int NOT NULL COMMENT '创建用户主键',
    PRIMARY KEY (`food_id`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

-- ----------------------------
-- Records of tb_food
-- ----------------------------
INSERT INTO `tb_food`
(`food_name`, `food_cal`, `taste`, `location`, `recorde`, `add_time`)
VALUES
('羊肉粉', '100KJ', '酸、甜', '二食堂一楼', null, '2021-05-08 13:04:45'),
('马玉涛麻辣烫', '200KJ', '清汤、辣', '二食堂二楼', null, '2021-05-08 13:06:24')
;

-- ----------------------------
-- Table structure for tb_like
-- ----------------------------
DROP TABLE IF EXISTS `tb_like`;
CREATE TABLE `tb_like` (
  `id` int NOT NULL,
  `user_id` int NOT NULL,
  `food_id` int NOT NULL,
  `ltime` datetime NOT NULL,
  `lcount` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

-- ----------------------------
-- Records of tb_like
-- ----------------------------

-- ----------------------------
-- Table structure for tb_user
-- ----------------------------
DROP TABLE IF EXISTS `tb_user`;
CREATE TABLE `tb_user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(20) NOT NULL,
  `login_name` varchar(20) NOT NULL,
  `pwd` varchar(20) NOT NULL,
  `sex` varchar(20) NOT NULL,
  `identity` varchar(20) NOT NULL,
  `tel` varchar(11) NOT NULL,
  `state` int NOT NULL,
  `add_time` datetime NOT NULL,
  PRIMARY KEY (`user_id`),
  KEY `user_name` (`user_name`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

-- ----------------------------
-- Records of tb_user
-- ----------------------------
INSERT INTO `tb_user`
(`user_name`, `login_name`, `pwd`, `sex`, `identity`, `tel`, `state`, `add_time`)
VALUES
('王丽', 'wangli', 'abcdef', '女', '学生', '17723409875', 0, '2021-05-08 13:00:28'),
('张三', 'zhangsan', '123456', '男', '管理员', '13875909988', 0, '2021-05-08 12:56:24'),
('李四', 'lisi', '123467', '男', '学生', '13908710034', 0, '2021-05-08 12:59:26')
;
