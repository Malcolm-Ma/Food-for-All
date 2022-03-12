-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: localhost    Database: foodforall
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add user',7,'add_user'),(26,'Can change user',7,'change_user'),(27,'Can delete user',7,'delete_user'),(28,'Can view user',7,'view_user'),(29,'Can add param',8,'add_param'),(30,'Can change param',8,'change_param'),(31,'Can delete param',8,'delete_param'),(32,'Can view param',8,'view_param'),(33,'Can add project',9,'add_project'),(34,'Can change project',9,'change_project'),(35,'Can delete project',9,'delete_project'),(36,'Can view project',9,'view_project');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$320000$retkp6B7Bg2dz4m2a20iEr$vAlontg08KJXy4nDhQ1OeRIiqmS5RGDMmHzlxPp5q0Q=','2022-03-11 17:05:49.689325',1,'apex','','','team08.apex@gmail.com',1,1,'2022-03-11 17:05:29.796040');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `database_param`
--

DROP TABLE IF EXISTS `database_param`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `database_param` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `key` varchar(256) NOT NULL,
  `value` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `database_param`
--

LOCK TABLES `database_param` WRITE;
/*!40000 ALTER TABLE `database_param` DISABLE KEYS */;
/*!40000 ALTER TABLE `database_param` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `database_project`
--

DROP TABLE IF EXISTS `database_project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `database_project` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `pid` varchar(64) NOT NULL,
  `uid` varchar(64) NOT NULL,
  `title` varchar(256) NOT NULL,
  `intro` varchar(256) NOT NULL,
  `region` varchar(256) NOT NULL,
  `background_image` varchar(256) NOT NULL,
  `total_num` int NOT NULL,
  `current_num` int NOT NULL,
  `start_time` int NOT NULL,
  `end_time` int NOT NULL,
  `details` longtext NOT NULL,
  `price` double NOT NULL,
  `donate_history` longtext NOT NULL,
  `charity` varchar(256) NOT NULL,
  `charity_avatar` varchar(256) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `pid` (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `database_project`
--

LOCK TABLES `database_project` WRITE;
/*!40000 ALTER TABLE `database_project` DISABLE KEYS */;
INSERT INTO `database_project` VALUES (3,'1','1','1','1','CHN','tyl.jpg',100,0,1646958139,1647958139,'1',30,'','',''),(4,'2','1','2','2','CHN','tyl.jpg',100,0,1646958139,1647958139,'2',30,'','',''),(5,'3','1','3','3','CHN','tyl.jpg',100,0,1646958139,1647958139,'3',30,'','',''),(6,'4','1','4','4','CHN','tyl.jpg',100,0,1646958139,1647958139,'4',30,'','',''),(7,'5','1','5','5','CHN','tyl.jpg',100,0,1646958139,1647958139,'5',30,'','',''),(8,'6','1','6','6','CHN','tyl.jpg',100,0,1646958139,1647958139,'6',30,'','',''),(9,'7','1','7','7','CHN','tyl.jpg',100,0,1646958139,1647958139,'7',30,'','',''),(10,'8','1','8','8','CHN','tyl.jpg',100,0,1646958139,1647958139,'8',30,'','',''),(11,'9','1','9','9','CHN','tyl.jpg',100,0,1646958139,1647958139,'9',30,'','',''),(12,'10','1','10','10','CHN','tyl.jpg',100,0,1646958139,1647958139,'10',30,'','',''),(13,'11','1','11','11','CHN','tyl.jpg',100,0,1646958139,1647958139,'11',30,'','',''),(14,'12','1','12','12','CHN','tyl.jpg',100,0,1646958139,1647958139,'12',30,'','',''),(15,'13','1','13','13','CHN','tyl.jpg',100,0,1646958139,1647958139,'13',30,'','',''),(16,'14','1','14','14','CHN','tyl.jpg',100,0,1646958139,1647958139,'14',30,'','',''),(17,'15','1','15','15','CHN','tyl.jpg',100,0,1646958139,1647958139,'15',30,'','',''),(18,'16','1','16','16','CHN','tyl.jpg',100,0,1646958139,1647958139,'16',30,'','',''),(19,'17','1','17','17','CHN','tyl.jpg',100,0,1646958139,1647958139,'17',30,'','',''),(20,'18','1','18','18','CHN','tyl.jpg',100,0,1646958139,1647958139,'18',30,'','',''),(21,'19','1','19','19','CHN','tyl.jpg',100,0,1646958139,1647958139,'19',30,'','',''),(22,'20','1','20','20','CHN','tyl.jpg',100,0,1646958139,1647958139,'20',30,'','',''),(23,'21','1','21','21','CHN','tyl.jpg',100,0,1646958139,1647958139,'21',30,'','',''),(24,'22','1','22','22','CHN','tyl.jpg',100,0,1646958139,1647958139,'22',30,'','',''),(25,'23','1','23','23','CHN','tyl.jpg',100,0,1646958139,1647958139,'23',30,'','',''),(26,'24','1','24','24','CHN','tyl.jpg',100,0,1646958139,1647958139,'24',30,'','',''),(27,'25','1','25','25','CHN','tyl.jpg',100,0,1646958139,1647958139,'25',30,'','',''),(28,'26','1','26','26','CHN','tyl.jpg',100,0,1646958139,1647958139,'26',30,'','',''),(29,'27','1','27','27','CHN','tyl.jpg',100,0,1646958139,1647958139,'27',30,'','',''),(30,'28','1','28','28','CHN','tyl.jpg',100,0,1646958139,1647958139,'28',30,'','',''),(31,'29','1','29','29','CHN','tyl.jpg',100,0,1646958139,1647958139,'29',30,'','',''),(32,'30','1','30','30','CHN','tyl.jpg',100,0,1646958139,1647958139,'30',30,'','',''),(33,'31','1','31','31','CHN','tyl.jpg',100,0,1646958139,1647958139,'31',30,'','',''),(34,'32','1','32','32','CHN','tyl.jpg',100,0,1646958139,1647958139,'32',30,'','',''),(35,'33','1','33','33','CHN','tyl.jpg',100,0,1646958139,1647958139,'33',30,'','',''),(36,'34','1','34','34','CHN','tyl.jpg',100,0,1646958139,1647958139,'34',30,'','',''),(37,'35','1','35','35','CHN','tyl.jpg',100,0,1646958139,1647958139,'35',30,'','',''),(38,'36','1','36','36','CHN','tyl.jpg',100,0,1646958139,1647958139,'36',30,'','',''),(39,'37','1','37','37','CHN','tyl.jpg',100,0,1646958139,1647958139,'37',30,'','',''),(40,'38','1','38','38','CHN','tyl.jpg',100,0,1646958139,1647958139,'38',30,'','',''),(41,'39','1','39','39','CHN','tyl.jpg',100,0,1646958139,1647958139,'39',30,'','',''),(42,'40','1','40','40','CHN','tyl.jpg',100,0,1646958139,1647958139,'40',30,'','',''),(43,'41','1','41','41','CHN','tyl.jpg',100,0,1646958139,1647958139,'41',30,'','',''),(44,'42','1','42','42','CHN','tyl.jpg',100,0,1646958139,1647958139,'42',30,'','',''),(45,'43','1','43','43','CHN','tyl.jpg',100,0,1646958139,1647958139,'43',30,'','',''),(46,'44','1','44','44','CHN','tyl.jpg',100,0,1646958139,1647958139,'44',30,'','',''),(47,'45','1','45','45','CHN','tyl.jpg',100,0,1646958139,1647958139,'45',30,'','',''),(48,'46','1','46','46','CHN','tyl.jpg',100,0,1646958139,1647958139,'46',30,'','',''),(49,'47','1','47','47','CHN','tyl.jpg',100,0,1646958139,1647958139,'47',30,'','',''),(50,'48','1','48','48','CHN','tyl.jpg',100,0,1646958139,1647958139,'48',30,'','',''),(51,'49','1','49','49','CHN','tyl.jpg',100,0,1646958139,1647958139,'49',30,'','','');
/*!40000 ALTER TABLE `database_project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `database_user`
--

DROP TABLE IF EXISTS `database_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `database_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `uid` varchar(64) NOT NULL,
  `mail` varchar(254) NOT NULL,
  `password` varchar(256) NOT NULL,
  `name` varchar(256) NOT NULL,
  `avatar` varchar(256) NOT NULL,
  `type` int NOT NULL,
  `region` varchar(256) NOT NULL,
  `project` longtext NOT NULL,
  `regis_time` int NOT NULL,
  `last_login_time` int NOT NULL,
  `donate_history` longtext NOT NULL,
  `share_mail_history` varchar(512) NOT NULL,
  `currency_type` varchar(256) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uid` (`uid`),
  UNIQUE KEY `email` (`mail`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `database_user`
--

LOCK TABLES `database_user` WRITE;
/*!40000 ALTER TABLE `database_user` DISABLE KEYS */;
INSERT INTO `database_user` VALUES (1,'qwerrytu','ty_liang@foxmail.com','123456','tyl','tyl.jpg',2,'CHN','',1646958039,1647123102,'','',''),(4,'asqwrefd','531273646@qq.com','123456','tyl','tyl.jpg',2,'CHN','',1646958039,1646958139,'','',''),(6,'asdfcxsdafzvz','ty_liang','123456','tyl','tyl.jpg',2,'CHN','',1646958039,1646958139,'','','');
/*!40000 ALTER TABLE `database_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(8,'DataBase','param'),(9,'DataBase','project'),(7,'DataBase','user'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2022-03-10 16:46:03.772803'),(2,'auth','0001_initial','2022-03-10 16:46:04.149887'),(3,'admin','0001_initial','2022-03-10 16:46:04.235906'),(4,'admin','0002_logentry_remove_auto_add','2022-03-10 16:46:04.243908'),(5,'admin','0003_logentry_add_action_flag_choices','2022-03-10 16:46:04.250910'),(6,'contenttypes','0002_remove_content_type_name','2022-03-10 16:46:04.321925'),(7,'auth','0002_alter_permission_name_max_length','2022-03-10 16:46:04.362935'),(8,'auth','0003_alter_user_email_max_length','2022-03-10 16:46:04.417948'),(9,'auth','0004_alter_user_username_opts','2022-03-10 16:46:04.431950'),(10,'auth','0005_alter_user_last_login_null','2022-03-10 16:46:04.506968'),(11,'auth','0006_require_contenttypes_0002','2022-03-10 16:46:04.521971'),(12,'auth','0007_alter_validators_add_error_messages','2022-03-10 16:46:04.535974'),(13,'auth','0008_alter_user_username_max_length','2022-03-10 16:46:04.613991'),(14,'auth','0009_alter_user_last_name_max_length','2022-03-10 16:46:04.684007'),(15,'auth','0010_alter_group_name_max_length','2022-03-10 16:46:04.759024'),(16,'auth','0011_update_proxy_permissions','2022-03-10 16:46:04.776027'),(17,'auth','0012_alter_user_first_name_max_length','2022-03-10 16:46:04.852044'),(18,'sessions','0001_initial','2022-03-10 16:46:04.888052'),(19,'DataBase','0001_initial','2022-03-10 18:45:41.725540'),(20,'DataBase','0002_param_project','2022-03-10 18:52:11.785178'),(21,'DataBase','0003_alter_project_end_time_alter_project_start_time_and_more','2022-03-11 00:26:27.073180'),(22,'DataBase','0004_rename_email_user_mail','2022-03-11 03:29:04.733502'),(23,'DataBase','0005_alter_project_uid','2022-03-11 14:31:28.787222'),(24,'DataBase','0006_rename_passwd_user_password_project_charity','2022-03-12 02:21:38.435603'),(25,'DataBase','0007_project_charity_avatar','2022-03-12 02:24:24.480472'),(26,'DataBase','0008_user_currency_type','2022-03-12 16:39:42.187369');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('mle59l9im5lwtapuw4x5zqoffsin9t3j','.eJxVjMsOwiAQRf-FtSE8WgGX7vsNZJgZpGogKe3K-O_apAvd3nPOfYkI21ri1nmJM4mL0OL0uyXAB9cd0B3qrUlsdV3mJHdFHrTLqRE_r4f7d1Cgl29trKMQEppAZ0OEySMYZ513nBUPGfKQzcierQefwWnm0SkAxRrTwCTeHwOOOS0:1nSii5:TJYQA5OLJTOW02tbP5wo--vzqkN_xys8nWCAnRAIi7U','2022-03-25 17:05:49.692325');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-03-12 22:34:37
