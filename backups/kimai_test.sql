-- MySQL dump 10.13  Distrib 8.3.0, for Linux (x86_64)
--
-- Host: localhost    Database: kimai
-- ------------------------------------------------------
-- Server version	8.3.0

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
-- Table structure for table `kimai2_access_token`
--

DROP TABLE IF EXISTS `kimai2_access_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_access_token` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `token` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_usage` datetime DEFAULT NULL COMMENT '(DC2Type:datetime_immutable)',
  `expires_at` datetime DEFAULT NULL COMMENT '(DC2Type:datetime_immutable)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQ_6FB0DB1E5F37A13B` (`token`),
  KEY `IDX_6FB0DB1EA76ED395` (`user_id`),
  CONSTRAINT `FK_6FB0DB1EA76ED395` FOREIGN KEY (`user_id`) REFERENCES `kimai2_users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_access_token`
--

LOCK TABLES `kimai2_access_token` WRITE;
/*!40000 ALTER TABLE `kimai2_access_token` DISABLE KEYS */;
INSERT INTO `kimai2_access_token` VALUES (1,1,'8b994b19fb1716a78c7898069','kimaistan','2026-04-24 20:30:46','2026-12-31 23:59:59');
/*!40000 ALTER TABLE `kimai2_access_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_activities`
--

DROP TABLE IF EXISTS `kimai2_activities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_activities` (
  `id` int NOT NULL AUTO_INCREMENT,
  `project_id` int DEFAULT NULL,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `comment` text COLLATE utf8mb4_unicode_ci,
  `visible` tinyint(1) NOT NULL,
  `color` varchar(7) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `time_budget` int NOT NULL DEFAULT '0',
  `budget` double NOT NULL DEFAULT '0',
  `budget_type` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `billable` tinyint(1) NOT NULL DEFAULT '1',
  `invoice_text` longtext COLLATE utf8mb4_unicode_ci,
  `number` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT NULL COMMENT '(DC2Type:datetime_immutable)',
  PRIMARY KEY (`id`),
  KEY `IDX_8811FE1C166D1F9C` (`project_id`),
  KEY `IDX_8811FE1C7AB0E859166D1F9C` (`visible`,`project_id`),
  KEY `IDX_8811FE1C7AB0E859166D1F9C5E237E06` (`visible`,`project_id`,`name`),
  KEY `IDX_8811FE1C7AB0E8595E237E06` (`visible`,`name`),
  CONSTRAINT `FK_8811FE1C166D1F9C` FOREIGN KEY (`project_id`) REFERENCES `kimai2_projects` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_activities`
--

LOCK TABLES `kimai2_activities` WRITE;
/*!40000 ALTER TABLE `kimai2_activities` DISABLE KEYS */;
INSERT INTO `kimai2_activities` VALUES (1,1,'Pointage journalier',NULL,1,'#00bfff',0,0,NULL,1,NULL,'0002','2026-04-24 15:01:42'),(2,2,'Astreinte',NULL,1,NULL,0,0,NULL,1,NULL,'0003','2026-04-24 15:04:50');
/*!40000 ALTER TABLE `kimai2_activities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_activities_meta`
--

DROP TABLE IF EXISTS `kimai2_activities_meta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_activities_meta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `activity_id` int NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `value` text COLLATE utf8mb4_unicode_ci,
  `visible` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQ_A7C0A43D81C060965E237E06` (`activity_id`,`name`),
  KEY `IDX_A7C0A43D81C06096` (`activity_id`),
  CONSTRAINT `FK_A7C0A43D81C06096` FOREIGN KEY (`activity_id`) REFERENCES `kimai2_activities` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_activities_meta`
--

LOCK TABLES `kimai2_activities_meta` WRITE;
/*!40000 ALTER TABLE `kimai2_activities_meta` DISABLE KEYS */;
/*!40000 ALTER TABLE `kimai2_activities_meta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_activities_rates`
--

DROP TABLE IF EXISTS `kimai2_activities_rates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_activities_rates` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `activity_id` int DEFAULT NULL,
  `rate` double NOT NULL,
  `fixed` tinyint(1) NOT NULL,
  `internal_rate` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQ_4A7F11BEA76ED39581C06096` (`user_id`,`activity_id`),
  KEY `IDX_4A7F11BEA76ED395` (`user_id`),
  KEY `IDX_4A7F11BE81C06096` (`activity_id`),
  CONSTRAINT `FK_4A7F11BE81C06096` FOREIGN KEY (`activity_id`) REFERENCES `kimai2_activities` (`id`) ON DELETE CASCADE,
  CONSTRAINT `FK_4A7F11BEA76ED395` FOREIGN KEY (`user_id`) REFERENCES `kimai2_users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_activities_rates`
--

LOCK TABLES `kimai2_activities_rates` WRITE;
/*!40000 ALTER TABLE `kimai2_activities_rates` DISABLE KEYS */;
/*!40000 ALTER TABLE `kimai2_activities_rates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_activities_teams`
--

DROP TABLE IF EXISTS `kimai2_activities_teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_activities_teams` (
  `activity_id` int NOT NULL,
  `team_id` int NOT NULL,
  PRIMARY KEY (`activity_id`,`team_id`),
  KEY `IDX_986998DA81C06096` (`activity_id`),
  KEY `IDX_986998DA296CD8AE` (`team_id`),
  CONSTRAINT `FK_986998DA296CD8AE` FOREIGN KEY (`team_id`) REFERENCES `kimai2_teams` (`id`) ON DELETE CASCADE,
  CONSTRAINT `FK_986998DA81C06096` FOREIGN KEY (`activity_id`) REFERENCES `kimai2_activities` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_activities_teams`
--

LOCK TABLES `kimai2_activities_teams` WRITE;
/*!40000 ALTER TABLE `kimai2_activities_teams` DISABLE KEYS */;
/*!40000 ALTER TABLE `kimai2_activities_teams` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_bookmarks`
--

DROP TABLE IF EXISTS `kimai2_bookmarks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_bookmarks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQ_4016EF25A76ED3955E237E06` (`user_id`,`name`),
  KEY `IDX_4016EF25A76ED395` (`user_id`),
  CONSTRAINT `FK_4016EF25A76ED395` FOREIGN KEY (`user_id`) REFERENCES `kimai2_users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_bookmarks`
--

LOCK TABLES `kimai2_bookmarks` WRITE;
/*!40000 ALTER TABLE `kimai2_bookmarks` DISABLE KEYS */;
INSERT INTO `kimai2_bookmarks` VALUES (1,1,'dashboard','default','[{\"id\":\"PaginatedWorkingTimeChart\",\"options\":[]},{\"id\":\"DurationMonth\",\"options\":[]},{\"id\":\"DurationWeek\",\"options\":[]},{\"id\":\"DurationToday\",\"options\":[]},{\"id\":\"DurationYear\",\"options\":[]}]');
/*!40000 ALTER TABLE `kimai2_bookmarks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_configuration`
--

DROP TABLE IF EXISTS `kimai2_configuration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_configuration` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `value` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQ_1C5D63D85E237E06` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_configuration`
--

LOCK TABLES `kimai2_configuration` WRITE;
/*!40000 ALTER TABLE `kimai2_configuration` DISABLE KEYS */;
INSERT INTO `kimai2_configuration` VALUES (1,'defaults.user.timezone','UTC'),(2,'defaults.user.language','fr'),(3,'defaults.user.theme','auto'),(4,'theme.avatar_url','0'),(5,'defaults.customer.timezone','UTC'),(6,'defaults.customer.country','FR'),(7,'customer.choice_pattern','{name}'),(8,'customer.number_format','{cc,4}'),(9,'customer.rules.allow_duplicate_number','0');
/*!40000 ALTER TABLE `kimai2_configuration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_customers`
--

DROP TABLE IF EXISTS `kimai2_customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_customers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `number` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `comment` text COLLATE utf8mb4_unicode_ci,
  `visible` tinyint(1) NOT NULL,
  `company` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `contact` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address` text COLLATE utf8mb4_unicode_ci,
  `country` varchar(2) COLLATE utf8mb4_unicode_ci NOT NULL,
  `currency` varchar(3) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fax` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mobile` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(75) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `homepage` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `timezone` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `color` varchar(7) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `time_budget` int NOT NULL DEFAULT '0',
  `budget` double NOT NULL DEFAULT '0',
  `vat_id` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `budget_type` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `billable` tinyint(1) NOT NULL DEFAULT '1',
  `invoice_template_id` int DEFAULT NULL,
  `invoice_text` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime DEFAULT NULL COMMENT '(DC2Type:datetime_immutable)',
  `address_line1` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address_line2` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address_line3` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `postcode` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `city` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `buyer_reference` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `IDX_5A9760447AB0E859` (`visible`),
  KEY `IDX_5A97604412946D8B` (`invoice_template_id`),
  CONSTRAINT `FK_5A97604412946D8B` FOREIGN KEY (`invoice_template_id`) REFERENCES `kimai2_invoice_templates` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_customers`
--

LOCK TABLES `kimai2_customers` WRITE;
/*!40000 ALTER TABLE `kimai2_customers` DISABLE KEYS */;
INSERT INTO `kimai2_customers` VALUES (1,'Pointage_Stan','0002',NULL,1,NULL,NULL,NULL,'DE','EUR',NULL,NULL,NULL,NULL,NULL,'UTC','#ff00ff',0,0,NULL,NULL,1,NULL,NULL,'2026-04-24 14:59:29',NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `kimai2_customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_customers_comments`
--

DROP TABLE IF EXISTS `kimai2_customers_comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_customers_comments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `created_by_id` int NOT NULL,
  `message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL,
  `pinned` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `IDX_A5B142D99395C3F3` (`customer_id`),
  KEY `IDX_A5B142D9B03A8386` (`created_by_id`),
  CONSTRAINT `FK_A5B142D99395C3F3` FOREIGN KEY (`customer_id`) REFERENCES `kimai2_customers` (`id`) ON DELETE CASCADE,
  CONSTRAINT `FK_A5B142D9B03A8386` FOREIGN KEY (`created_by_id`) REFERENCES `kimai2_users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_customers_comments`
--

LOCK TABLES `kimai2_customers_comments` WRITE;
/*!40000 ALTER TABLE `kimai2_customers_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `kimai2_customers_comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_customers_meta`
--

DROP TABLE IF EXISTS `kimai2_customers_meta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_customers_meta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `value` text COLLATE utf8mb4_unicode_ci,
  `visible` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQ_A48A760F9395C3F35E237E06` (`customer_id`,`name`),
  KEY `IDX_A48A760F9395C3F3` (`customer_id`),
  CONSTRAINT `FK_A48A760F9395C3F3` FOREIGN KEY (`customer_id`) REFERENCES `kimai2_customers` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_customers_meta`
--

LOCK TABLES `kimai2_customers_meta` WRITE;
/*!40000 ALTER TABLE `kimai2_customers_meta` DISABLE KEYS */;
/*!40000 ALTER TABLE `kimai2_customers_meta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_customers_rates`
--

DROP TABLE IF EXISTS `kimai2_customers_rates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_customers_rates` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `customer_id` int DEFAULT NULL,
  `rate` double NOT NULL,
  `fixed` tinyint(1) NOT NULL,
  `internal_rate` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQ_82AB0AECA76ED3959395C3F3` (`user_id`,`customer_id`),
  KEY `IDX_82AB0AECA76ED395` (`user_id`),
  KEY `IDX_82AB0AEC9395C3F3` (`customer_id`),
  CONSTRAINT `FK_82AB0AEC9395C3F3` FOREIGN KEY (`customer_id`) REFERENCES `kimai2_customers` (`id`) ON DELETE CASCADE,
  CONSTRAINT `FK_82AB0AECA76ED395` FOREIGN KEY (`user_id`) REFERENCES `kimai2_users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_customers_rates`
--

LOCK TABLES `kimai2_customers_rates` WRITE;
/*!40000 ALTER TABLE `kimai2_customers_rates` DISABLE KEYS */;
/*!40000 ALTER TABLE `kimai2_customers_rates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_customers_teams`
--

DROP TABLE IF EXISTS `kimai2_customers_teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_customers_teams` (
  `customer_id` int NOT NULL,
  `team_id` int NOT NULL,
  PRIMARY KEY (`customer_id`,`team_id`),
  KEY `IDX_50BD83889395C3F3` (`customer_id`),
  KEY `IDX_50BD8388296CD8AE` (`team_id`),
  CONSTRAINT `FK_50BD8388296CD8AE` FOREIGN KEY (`team_id`) REFERENCES `kimai2_teams` (`id`) ON DELETE CASCADE,
  CONSTRAINT `FK_50BD83889395C3F3` FOREIGN KEY (`customer_id`) REFERENCES `kimai2_customers` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_customers_teams`
--

LOCK TABLES `kimai2_customers_teams` WRITE;
/*!40000 ALTER TABLE `kimai2_customers_teams` DISABLE KEYS */;
/*!40000 ALTER TABLE `kimai2_customers_teams` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_export_templates`
--

DROP TABLE IF EXISTS `kimai2_export_templates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_export_templates` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `renderer` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `language` varchar(6) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `columns` json NOT NULL,
  `options` json NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQ_2F0CA26F2B36786B` (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_export_templates`
--

LOCK TABLES `kimai2_export_templates` WRITE;
/*!40000 ALTER TABLE `kimai2_export_templates` DISABLE KEYS */;
/*!40000 ALTER TABLE `kimai2_export_templates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_invoice_templates`
--

DROP TABLE IF EXISTS `kimai2_invoice_templates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_invoice_templates` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `company` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address` text COLLATE utf8mb4_unicode_ci,
  `due_days` int NOT NULL,
  `vat` double DEFAULT '0',
  `calculator` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `number_generator` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `renderer` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `payment_terms` text COLLATE utf8mb4_unicode_ci,
  `vat_id` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `contact` longtext COLLATE utf8mb4_unicode_ci,
  `payment_details` longtext COLLATE utf8mb4_unicode_ci,
  `language` varchar(6) COLLATE utf8mb4_unicode_ci NOT NULL,
  `customer_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQ_1626CFE95E237E06` (`name`),
  KEY `IDX_1626CFE99395C3F3` (`customer_id`),
  CONSTRAINT `FK_1626CFE99395C3F3` FOREIGN KEY (`customer_id`) REFERENCES `kimai2_customers` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_invoice_templates`
--

LOCK TABLES `kimai2_invoice_templates` WRITE;
/*!40000 ALTER TABLE `kimai2_invoice_templates` DISABLE KEYS */;
/*!40000 ALTER TABLE `kimai2_invoice_templates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_invoice_templates_meta`
--

DROP TABLE IF EXISTS `kimai2_invoice_templates_meta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_invoice_templates_meta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `template_id` int NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `value` text COLLATE utf8mb4_unicode_ci,
  `visible` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQ_A165B0555DA0FB85E237E06` (`template_id`,`name`),
  KEY `IDX_A165B0555DA0FB8` (`template_id`),
  CONSTRAINT `FK_A165B0555DA0FB8` FOREIGN KEY (`template_id`) REFERENCES `kimai2_invoice_templates` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_invoice_templates_meta`
--

LOCK TABLES `kimai2_invoice_templates_meta` WRITE;
/*!40000 ALTER TABLE `kimai2_invoice_templates_meta` DISABLE KEYS */;
/*!40000 ALTER TABLE `kimai2_invoice_templates_meta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_invoices`
--

DROP TABLE IF EXISTS `kimai2_invoices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_invoices` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `user_id` int NOT NULL,
  `invoice_number` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL,
  `timezone` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `total` double NOT NULL,
  `tax` double NOT NULL,
  `currency` varchar(3) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `due_days` int NOT NULL,
  `vat` double NOT NULL,
  `invoice_filename` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `payment_date` date DEFAULT NULL,
  `comment` longtext COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQ_76C38E372DA68207` (`invoice_number`),
  UNIQUE KEY `UNIQ_76C38E372323B33D` (`invoice_filename`),
  KEY `IDX_76C38E37A76ED395` (`user_id`),
  KEY `IDX_76C38E379395C3F3` (`customer_id`),
  CONSTRAINT `FK_76C38E379395C3F3` FOREIGN KEY (`customer_id`) REFERENCES `kimai2_customers` (`id`) ON DELETE CASCADE,
  CONSTRAINT `FK_76C38E37A76ED395` FOREIGN KEY (`user_id`) REFERENCES `kimai2_users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_invoices`
--

LOCK TABLES `kimai2_invoices` WRITE;
/*!40000 ALTER TABLE `kimai2_invoices` DISABLE KEYS */;
/*!40000 ALTER TABLE `kimai2_invoices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_invoices_meta`
--

DROP TABLE IF EXISTS `kimai2_invoices_meta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_invoices_meta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `invoice_id` int NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `value` text COLLATE utf8mb4_unicode_ci,
  `visible` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQ_7EDC37D92989F1FD5E237E06` (`invoice_id`,`name`),
  KEY `IDX_7EDC37D92989F1FD` (`invoice_id`),
  CONSTRAINT `FK_7EDC37D92989F1FD` FOREIGN KEY (`invoice_id`) REFERENCES `kimai2_invoices` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_invoices_meta`
--

LOCK TABLES `kimai2_invoices_meta` WRITE;
/*!40000 ALTER TABLE `kimai2_invoices_meta` DISABLE KEYS */;
/*!40000 ALTER TABLE `kimai2_invoices_meta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_projects`
--

DROP TABLE IF EXISTS `kimai2_projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_projects` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `order_number` tinytext COLLATE utf8mb4_unicode_ci,
  `comment` text COLLATE utf8mb4_unicode_ci,
  `visible` tinyint(1) NOT NULL,
  `budget` double NOT NULL DEFAULT '0',
  `color` varchar(7) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `time_budget` int NOT NULL DEFAULT '0',
  `order_date` datetime DEFAULT NULL,
  `start` datetime DEFAULT NULL,
  `end` datetime DEFAULT NULL,
  `timezone` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `budget_type` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `billable` tinyint(1) NOT NULL DEFAULT '1',
  `invoice_text` longtext COLLATE utf8mb4_unicode_ci,
  `global_activities` tinyint(1) NOT NULL DEFAULT '1',
  `number` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT NULL COMMENT '(DC2Type:datetime_immutable)',
  PRIMARY KEY (`id`),
  KEY `IDX_407F12069395C3F3` (`customer_id`),
  KEY `IDX_407F12069395C3F37AB0E8595E237E06` (`customer_id`,`visible`,`name`),
  KEY `IDX_407F12069395C3F37AB0E859BF396750` (`customer_id`,`visible`,`id`),
  CONSTRAINT `FK_407F12069395C3F3` FOREIGN KEY (`customer_id`) REFERENCES `kimai2_customers` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_projects`
--

LOCK TABLES `kimai2_projects` WRITE;
/*!40000 ALTER TABLE `kimai2_projects` DISABLE KEYS */;
INSERT INTO `kimai2_projects` VALUES (1,1,'Présence',NULL,NULL,1,0,NULL,0,NULL,NULL,NULL,'UTC',NULL,1,NULL,1,'0002','2026-04-24 14:59:57'),(2,1,'Absences',NULL,NULL,1,0,'#1e90ff',0,NULL,NULL,NULL,'UTC',NULL,1,NULL,1,'0003','2026-04-24 15:03:11');
/*!40000 ALTER TABLE `kimai2_projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_projects_comments`
--

DROP TABLE IF EXISTS `kimai2_projects_comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_projects_comments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL,
  `created_by_id` int NOT NULL,
  `message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL,
  `pinned` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `IDX_29A23638166D1F9C` (`project_id`),
  KEY `IDX_29A23638B03A8386` (`created_by_id`),
  CONSTRAINT `FK_29A23638166D1F9C` FOREIGN KEY (`project_id`) REFERENCES `kimai2_projects` (`id`) ON DELETE CASCADE,
  CONSTRAINT `FK_29A23638B03A8386` FOREIGN KEY (`created_by_id`) REFERENCES `kimai2_users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_projects_comments`
--

LOCK TABLES `kimai2_projects_comments` WRITE;
/*!40000 ALTER TABLE `kimai2_projects_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `kimai2_projects_comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_projects_meta`
--

DROP TABLE IF EXISTS `kimai2_projects_meta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_projects_meta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `value` text COLLATE utf8mb4_unicode_ci,
  `visible` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQ_50536EF2166D1F9C5E237E06` (`project_id`,`name`),
  KEY `IDX_50536EF2166D1F9C` (`project_id`),
  CONSTRAINT `FK_50536EF2166D1F9C` FOREIGN KEY (`project_id`) REFERENCES `kimai2_projects` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_projects_meta`
--

LOCK TABLES `kimai2_projects_meta` WRITE;
/*!40000 ALTER TABLE `kimai2_projects_meta` DISABLE KEYS */;
/*!40000 ALTER TABLE `kimai2_projects_meta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_projects_rates`
--

DROP TABLE IF EXISTS `kimai2_projects_rates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_projects_rates` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `project_id` int DEFAULT NULL,
  `rate` double NOT NULL,
  `fixed` tinyint(1) NOT NULL,
  `internal_rate` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQ_41535D55A76ED395166D1F9C` (`user_id`,`project_id`),
  KEY `IDX_41535D55A76ED395` (`user_id`),
  KEY `IDX_41535D55166D1F9C` (`project_id`),
  CONSTRAINT `FK_41535D55166D1F9C` FOREIGN KEY (`project_id`) REFERENCES `kimai2_projects` (`id`) ON DELETE CASCADE,
  CONSTRAINT `FK_41535D55A76ED395` FOREIGN KEY (`user_id`) REFERENCES `kimai2_users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_projects_rates`
--

LOCK TABLES `kimai2_projects_rates` WRITE;
/*!40000 ALTER TABLE `kimai2_projects_rates` DISABLE KEYS */;
/*!40000 ALTER TABLE `kimai2_projects_rates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_projects_teams`
--

DROP TABLE IF EXISTS `kimai2_projects_teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_projects_teams` (
  `project_id` int NOT NULL,
  `team_id` int NOT NULL,
  PRIMARY KEY (`project_id`,`team_id`),
  KEY `IDX_9345D431166D1F9C` (`project_id`),
  KEY `IDX_9345D431296CD8AE` (`team_id`),
  CONSTRAINT `FK_9345D431166D1F9C` FOREIGN KEY (`project_id`) REFERENCES `kimai2_projects` (`id`) ON DELETE CASCADE,
  CONSTRAINT `FK_9345D431296CD8AE` FOREIGN KEY (`team_id`) REFERENCES `kimai2_teams` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_projects_teams`
--

LOCK TABLES `kimai2_projects_teams` WRITE;
/*!40000 ALTER TABLE `kimai2_projects_teams` DISABLE KEYS */;
/*!40000 ALTER TABLE `kimai2_projects_teams` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_roles`
--

DROP TABLE IF EXISTS `kimai2_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `roles_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_roles`
--

LOCK TABLES `kimai2_roles` WRITE;
/*!40000 ALTER TABLE `kimai2_roles` DISABLE KEYS */;
INSERT INTO `kimai2_roles` VALUES (3,'ROLE_ADMIN'),(4,'ROLE_SUPER_ADMIN'),(2,'ROLE_TEAMLEAD'),(1,'ROLE_USER');
/*!40000 ALTER TABLE `kimai2_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_roles_permissions`
--

DROP TABLE IF EXISTS `kimai2_roles_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_roles_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `role_id` int NOT NULL,
  `permission` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `allowed` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `role_permission` (`role_id`,`permission`),
  KEY `IDX_D263A3B8D60322AC` (`role_id`),
  CONSTRAINT `FK_D263A3B8D60322AC` FOREIGN KEY (`role_id`) REFERENCES `kimai2_roles` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_roles_permissions`
--

LOCK TABLES `kimai2_roles_permissions` WRITE;
/*!40000 ALTER TABLE `kimai2_roles_permissions` DISABLE KEYS */;
INSERT INTO `kimai2_roles_permissions` VALUES (1,4,'budget_team_activity',0),(2,4,'budget_customer',0),(3,4,'comments_customer',0),(4,4,'create_customer',0),(5,4,'delete_customer',0),(6,4,'details_customer',0),(7,4,'edit_customer',0),(8,4,'permissions_customer',0),(9,4,'time_customer',0),(10,4,'view_customer',0),(11,3,'view_customer',0),(12,3,'permissions_customer',0),(13,3,'edit_customer',0),(14,3,'time_customer',0),(15,3,'details_customer',0),(16,3,'delete_customer',0),(17,3,'create_customer',0),(18,3,'comments_customer',0),(19,3,'budget_customer',0);
/*!40000 ALTER TABLE `kimai2_roles_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_sessions`
--

DROP TABLE IF EXISTS `kimai2_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_sessions` (
  `id` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `data` blob NOT NULL,
  `time` int unsigned NOT NULL,
  `lifetime` int unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_sessions`
--

LOCK TABLES `kimai2_sessions` WRITE;
/*!40000 ALTER TABLE `kimai2_sessions` DISABLE KEYS */;
INSERT INTO `kimai2_sessions` VALUES ('dm88uq4o827u2id6se5ug8vlrk',_binary '_sf2_attributes|a:4:{s:34:\"_security.secured_area.target_path\";s:36:\"http://192.168.1.15:8055/fr/homepage\";s:18:\"_csrf/authenticate\";s:43:\"eSEQEgnkGH1F9Kxfcz774VnBT5jTAAtTUEUYBomYJAA\";s:23:\"_security.last_username\";s:9:\"cbtitalia\";s:20:\"_csrf/password_reset\";s:43:\"3xBsGWHh5gywBm500t3wiuNDGFqNjyN2aZ0Lkxpor98\";}_sf2_meta|a:3:{s:1:\"u\";i:1777058289;s:1:\"c\";i:1777057832;s:1:\"l\";i:0;}',1777058289,1777663089),('l4i03uudbi84tlakala8r838fe',_binary '_sf2_attributes|a:25:{s:23:\"_security.last_username\";s:20:\"admin@pointage.local\";s:22:\"_security_secured_area\";s:419:\"O:74:\"Symfony\\Component\\Security\\Core\\Authentication\\Token\\UsernamePasswordToken\":3:{i:0;N;i:1;s:12:\"secured_area\";i:2;a:5:{i:0;O:15:\"App\\Entity\\User\":5:{s:2:\"id\";i:1;s:8:\"username\";s:5:\"admin\";s:7:\"enabled\";b:1;s:5:\"email\";s:19:\"cbtitalia@gmail.com\";s:8:\"password\";s:60:\"$2y$13$H04kyBOJk/6V24GsbTGGD.k3v0Fh4NbVRgVIcUsXkNlfsSEkg3UKq\";}i:1;b:1;i:2;N;i:3;a:0:{}i:4;a:2:{i:0;s:16:\"ROLE_SUPER_ADMIN\";i:1;s:9:\"ROLE_USER\";}}}\";s:10:\"_csrf/form\";s:43:\"n037_izbbyHl0XnfAC9FoqU4s3nm_XCAEIL8dH5rCSU\";s:12:\"_csrf/search\";s:43:\"pGUFjHaZyT7CYJkgHTvjsAjIqNyoBLoUp6tHefw4Qiw\";s:22:\"_csrf/datatable_update\";s:43:\"ayZ5FW75d8Xm_yU5QB6JxAd_400Kxwqc93mEK3O-e3w\";s:23:\"_csrf/edit_user_profile\";s:43:\"t9iRiFCvw8Jid32KtJfa0PqBQGnDFbWqR45NbMyHrnY\";s:24:\"_csrf/edit_user_password\";s:43:\"bgw2UojDQgbXoJGohZs9MsBNOnXeOQqcT9UWLmP6I3Y\";s:27:\"_csrf/edit_user_preferences\";s:43:\"wGjeIugEfIvlj5fndhpDWDeXu5-mq0iYmF5j3ExyD-U\";s:19:\"_csrf/edit_user_2fa\";s:43:\"-iXVmDAHIRxosfczqLgp5r3ttJELAy1ohKHlN6t_sA4\";s:30:\"_csrf/edit_user_password_token\";s:43:\"f0yyFqdZdnWJa9JNzbqvyaFDQ5UI1rd4nzci5wiyLro\";s:21:\"_csrf/edit_user_teams\";s:43:\"IiEuRrHaOiYYO2z4dph5005OaKrwB1Vk7MK-C0dElZU\";s:21:\"_csrf/edit_user_roles\";s:43:\"YjW-Sm1v7c3XKgbQ3EZ_7D7wHZLCjyL5osFvWBCoJTI\";s:24:\"_csrf/admin_project_edit\";s:43:\"d4saNph6R6pbf_xt3BCmZ3-7QkAqAF-B_slh9m4N_Dg\";s:25:\"_csrf/admin_customer_edit\";s:43:\"OfQM8vULzHGCEtHXhqedoghbBrlkqWMEzz5lzz5m7tA\";s:28:\"_csrf/admin_customer_comment\";s:43:\"EfSqEFnX8n7C0JBF55A3C7l3dlMlXJg2A6ZsUhAc5As\";s:27:\"_csrf/admin_project_comment\";s:43:\"H-hV21CHPln3qMk1DgQ5lEC6Z5dRpHpktrbmkYdtEdY\";s:23:\"_csrf/project.duplicate\";s:43:\"jbu6CNIhf1KRFit9Up_SE13cmDdu1C4zHRsUru29PBI\";s:25:\"_csrf/admin_activity_edit\";s:43:\"JxTuIp1gPNtuj1CBUvRvAhiRoPMvmbMAR89pyMzXycQ\";s:23:\"_csrf/access_token_form\";s:43:\"HOFXz3kq2bzABhOO9ZjHRoAjBSlfUzet42LWinP9f8I\";s:26:\"_csrf/entities_multiupdate\";s:43:\"K_hfyP90_6S1sXWkiR0FJfH1oqMDRuNbib_tEEvXf04\";s:26:\"_csrf/timesheet_quick_edit\";s:43:\"f5R_HLapi6ETrOa82SiJNnjAgJaFIQr7fhXPjaGRCVg\";s:32:\"_csrf/edit_system_configurations\";s:43:\"UCj1M9yANyB6ueK49CSjeYzUKw5qvK1u4549N1N_rzw\";s:20:\"_csrf/timesheet_edit\";s:43:\"F7-NUO7SGKah5ILY_MGWnMMy53eXldgXOSuxsdbb4Xs\";s:24:\"_csrf/edit_user_contract\";s:43:\"cH5Nw2F0uXlfJwpU-ruMTavKQQy7pcNlWlVBd7ndReI\";s:27:\"_csrf/user_role_permissions\";s:43:\"z5C9EJanBVUl2NjgrD6-vQAOyG9dXrVaOk7H3yP1JFU\";}_sf2_meta|a:3:{s:1:\"u\";i:1777063045;s:1:\"c\";i:1777042117;s:1:\"l\";i:0;}',1777063045,1777667845);
/*!40000 ALTER TABLE `kimai2_sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_tags`
--

DROP TABLE IF EXISTS `kimai2_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_tags` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `color` varchar(7) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `visible` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQ_27CAF54C5E237E06` (`name`),
  KEY `IDX_27CAF54C7AB0E859` (`visible`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_tags`
--

LOCK TABLES `kimai2_tags` WRITE;
/*!40000 ALTER TABLE `kimai2_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `kimai2_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_teams`
--

DROP TABLE IF EXISTS `kimai2_teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_teams` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `color` varchar(7) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQ_3BEDDC7F5E237E06` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_teams`
--

LOCK TABLES `kimai2_teams` WRITE;
/*!40000 ALTER TABLE `kimai2_teams` DISABLE KEYS */;
/*!40000 ALTER TABLE `kimai2_teams` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_timesheet`
--

DROP TABLE IF EXISTS `kimai2_timesheet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_timesheet` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user` int NOT NULL,
  `activity_id` int NOT NULL,
  `project_id` int NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime DEFAULT NULL,
  `duration` int DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `rate` double NOT NULL,
  `fixed_rate` double DEFAULT NULL,
  `hourly_rate` double DEFAULT NULL,
  `exported` tinyint(1) NOT NULL DEFAULT '0',
  `timezone` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `internal_rate` double DEFAULT NULL,
  `billable` tinyint(1) DEFAULT '1',
  `category` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'work',
  `modified_at` datetime DEFAULT NULL,
  `date_tz` date NOT NULL,
  `break` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `IDX_4F60C6B18D93D649` (`user`),
  KEY `IDX_4F60C6B181C06096` (`activity_id`),
  KEY `IDX_4F60C6B1166D1F9C` (`project_id`),
  KEY `IDX_4F60C6B18D93D649502DF587` (`user`,`start_time`),
  KEY `IDX_4F60C6B1502DF587` (`start_time`),
  KEY `IDX_4F60C6B1502DF58741561401` (`start_time`,`end_time`),
  KEY `IDX_4F60C6B1502DF587415614018D93D649` (`start_time`,`end_time`,`user`),
  KEY `IDX_4F60C6B1BDF467148D93D649` (`date_tz`,`user`),
  KEY `IDX_4F60C6B1415614018D93D649` (`end_time`,`user`),
  KEY `IDX_TIMESHEET_TICKTAC` (`end_time`,`user`,`start_time`),
  KEY `IDX_TIMESHEET_RECENT_ACTIVITIES` (`user`,`project_id`,`activity_id`),
  KEY `IDX_TIMESHEET_RESULT_STATS` (`user`,`id`,`duration`),
  CONSTRAINT `FK_4F60C6B1166D1F9C` FOREIGN KEY (`project_id`) REFERENCES `kimai2_projects` (`id`) ON DELETE CASCADE,
  CONSTRAINT `FK_4F60C6B181C06096` FOREIGN KEY (`activity_id`) REFERENCES `kimai2_activities` (`id`) ON DELETE CASCADE,
  CONSTRAINT `FK_4F60C6B18D93D649` FOREIGN KEY (`user`) REFERENCES `kimai2_users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_timesheet`
--

LOCK TABLES `kimai2_timesheet` WRITE;
/*!40000 ALTER TABLE `kimai2_timesheet` DISABLE KEYS */;
INSERT INTO `kimai2_timesheet` VALUES (8,1,1,1,'2026-04-24 19:22:00','2026-04-24 19:27:00',300,NULL,0,NULL,0,0,'Europe/Paris',0,1,'work','2026-04-24 19:26:38','2026-04-24',0),(9,1,1,1,'2026-04-24 05:30:00','2026-04-24 10:00:00',16200,NULL,0,NULL,0,0,'Europe/Paris',0,1,'work','2026-04-24 19:28:18','2026-04-24',0),(10,1,1,1,'2026-04-24 19:29:00','2026-04-24 19:33:00',240,NULL,0,NULL,0,0,'Europe/Paris',0,1,'work','2026-04-24 19:32:04','2026-04-24',0),(11,1,1,1,'2026-04-24 19:32:00','2026-04-24 19:48:00',960,NULL,0,NULL,0,0,'Europe/Paris',0,1,'work','2026-04-24 19:47:16','2026-04-24',0);
/*!40000 ALTER TABLE `kimai2_timesheet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_timesheet_meta`
--

DROP TABLE IF EXISTS `kimai2_timesheet_meta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_timesheet_meta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `timesheet_id` int NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `value` text COLLATE utf8mb4_unicode_ci,
  `visible` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQ_CB606CBAABDD46BE5E237E06` (`timesheet_id`,`name`),
  KEY `IDX_CB606CBAABDD46BE` (`timesheet_id`),
  CONSTRAINT `FK_CB606CBAABDD46BE` FOREIGN KEY (`timesheet_id`) REFERENCES `kimai2_timesheet` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_timesheet_meta`
--

LOCK TABLES `kimai2_timesheet_meta` WRITE;
/*!40000 ALTER TABLE `kimai2_timesheet_meta` DISABLE KEYS */;
/*!40000 ALTER TABLE `kimai2_timesheet_meta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_timesheet_tags`
--

DROP TABLE IF EXISTS `kimai2_timesheet_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_timesheet_tags` (
  `timesheet_id` int NOT NULL,
  `tag_id` int NOT NULL,
  PRIMARY KEY (`timesheet_id`,`tag_id`),
  KEY `IDX_E3284EFEABDD46BE` (`timesheet_id`),
  KEY `IDX_E3284EFEBAD26311` (`tag_id`),
  CONSTRAINT `FK_732EECA9ABDD46BE` FOREIGN KEY (`timesheet_id`) REFERENCES `kimai2_timesheet` (`id`) ON DELETE CASCADE,
  CONSTRAINT `FK_732EECA9BAD26311` FOREIGN KEY (`tag_id`) REFERENCES `kimai2_tags` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_timesheet_tags`
--

LOCK TABLES `kimai2_timesheet_tags` WRITE;
/*!40000 ALTER TABLE `kimai2_timesheet_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `kimai2_timesheet_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_user_preferences`
--

DROP TABLE IF EXISTS `kimai2_user_preferences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_user_preferences` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `value` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQ_8D08F631A76ED3955E237E06` (`user_id`,`name`),
  KEY `IDX_8D08F631A76ED395` (`user_id`),
  CONSTRAINT `FK_8D08F631A76ED395` FOREIGN KEY (`user_id`) REFERENCES `kimai2_users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_user_preferences`
--

LOCK TABLES `kimai2_user_preferences` WRITE;
/*!40000 ALTER TABLE `kimai2_user_preferences` DISABLE KEYS */;
INSERT INTO `kimai2_user_preferences` VALUES (1,1,'timezone','Europe/Paris'),(2,1,'language','fr'),(3,1,'skin','dark'),(4,1,'hourly_rate','0'),(5,1,'internal_rate',NULL),(6,1,'locale','fr'),(7,1,'first_weekday','monday'),(8,1,'update_browser_title','1'),(9,1,'calendar_initial_view','month'),(10,1,'login_initial_view','timesheet'),(11,1,'favorite_routes',''),(12,1,'daily_stats','0'),(13,1,'export_decimal','0'),(14,1,'__wizards__','intro,profile'),(15,1,'_latest_approval',NULL),(16,1,'__pw_reset__','0'),(17,1,'work_contract_type','day'),(18,1,'work_monday','27000'),(19,1,'work_tuesday','27000'),(20,1,'work_wednesday','27000'),(21,1,'work_thursday','27000'),(22,1,'work_friday','27000');
/*!40000 ALTER TABLE `kimai2_user_preferences` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_users`
--

DROP TABLE IF EXISTS `kimai2_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(180) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(180) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `alias` varchar(60) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `enabled` tinyint(1) NOT NULL,
  `registration_date` datetime DEFAULT NULL,
  `title` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `avatar` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `roles` longtext COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '(DC2Type:array)',
  `last_login` datetime DEFAULT NULL,
  `confirmation_token` varchar(180) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `password_requested_at` datetime DEFAULT NULL,
  `api_token` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `auth` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `color` varchar(7) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `account` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `totp_secret` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `totp_enabled` tinyint(1) NOT NULL DEFAULT '0',
  `system_account` tinyint(1) NOT NULL DEFAULT '0',
  `supervisor_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQ_B9AC5BCEF85E0677` (`username`),
  UNIQUE KEY `UNIQ_B9AC5BCEE7927C74` (`email`),
  UNIQUE KEY `UNIQ_B9AC5BCEC05FB297` (`confirmation_token`),
  KEY `IDX_B9AC5BCE19E9AC5F` (`supervisor_id`),
  CONSTRAINT `FK_B9AC5BCE19E9AC5F` FOREIGN KEY (`supervisor_id`) REFERENCES `kimai2_users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_users`
--

LOCK TABLES `kimai2_users` WRITE;
/*!40000 ALTER TABLE `kimai2_users` DISABLE KEYS */;
INSERT INTO `kimai2_users` VALUES (1,'admin','cbtitalia@gmail.com','$2y$13$H04kyBOJk/6V24GsbTGGD.k3v0Fh4NbVRgVIcUsXkNlfsSEkg3UKq','Stan',1,'2026-04-24 14:46:47',NULL,NULL,'a:2:{i:0;s:16:\"ROLE_SUPER_ADMIN\";i:1;s:10:\"ROLE_ADMIN\";}','2026-04-24 20:30:46',NULL,NULL,NULL,'kimai',NULL,NULL,'IRFXQM3NEFNLWNU7RIVPZ5Y64XCLMQIHL6Y3PDRLK2ZOKYDRCVHQ',0,0,NULL);
/*!40000 ALTER TABLE `kimai2_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_users_teams`
--

DROP TABLE IF EXISTS `kimai2_users_teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_users_teams` (
  `user_id` int NOT NULL,
  `team_id` int NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `teamlead` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQ_B5E92CF8A76ED395296CD8AE` (`user_id`,`team_id`),
  KEY `IDX_B5E92CF8A76ED395` (`user_id`),
  KEY `IDX_B5E92CF8296CD8AE` (`team_id`),
  CONSTRAINT `FK_B5E92CF8296CD8AE` FOREIGN KEY (`team_id`) REFERENCES `kimai2_teams` (`id`) ON DELETE CASCADE,
  CONSTRAINT `FK_B5E92CF8A76ED395` FOREIGN KEY (`user_id`) REFERENCES `kimai2_users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_users_teams`
--

LOCK TABLES `kimai2_users_teams` WRITE;
/*!40000 ALTER TABLE `kimai2_users_teams` DISABLE KEYS */;
/*!40000 ALTER TABLE `kimai2_users_teams` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kimai2_working_times`
--

DROP TABLE IF EXISTS `kimai2_working_times`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kimai2_working_times` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `approved_by` int DEFAULT NULL,
  `date` date NOT NULL,
  `expected` int NOT NULL,
  `actual` int NOT NULL,
  `approved_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQ_F95E4933A76ED395AA9E377A` (`user_id`,`date`),
  KEY `IDX_F95E4933A76ED395` (`user_id`),
  KEY `IDX_F95E49334EA3CB3D` (`approved_by`),
  CONSTRAINT `FK_F95E49334EA3CB3D` FOREIGN KEY (`approved_by`) REFERENCES `kimai2_users` (`id`) ON DELETE SET NULL,
  CONSTRAINT `FK_F95E4933A76ED395` FOREIGN KEY (`user_id`) REFERENCES `kimai2_users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kimai2_working_times`
--

LOCK TABLES `kimai2_working_times` WRITE;
/*!40000 ALTER TABLE `kimai2_working_times` DISABLE KEYS */;
/*!40000 ALTER TABLE `kimai2_working_times` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `migration_versions`
--

DROP TABLE IF EXISTS `migration_versions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `migration_versions` (
  `version` varchar(191) COLLATE utf8mb3_unicode_ci NOT NULL,
  `executed_at` datetime DEFAULT NULL,
  `execution_time` int DEFAULT NULL,
  PRIMARY KEY (`version`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `migration_versions`
--

LOCK TABLES `migration_versions` WRITE;
/*!40000 ALTER TABLE `migration_versions` DISABLE KEYS */;
INSERT INTO `migration_versions` VALUES ('DoctrineMigrations\\Version20180701120000','2026-04-24 14:45:41',2753),('DoctrineMigrations\\Version20180715160326','2026-04-24 14:45:44',1142),('DoctrineMigrations\\Version20180730044139','2026-04-24 14:45:45',389),('DoctrineMigrations\\Version20180805183527','2026-04-24 14:45:45',117),('DoctrineMigrations\\Version20180903202256','2026-04-24 14:45:45',136),('DoctrineMigrations\\Version20180905190737','2026-04-24 14:45:45',471),('DoctrineMigrations\\Version20180924111853','2026-04-24 14:45:46',255),('DoctrineMigrations\\Version20181031220003','2026-04-24 14:45:46',2214),('DoctrineMigrations\\Version20190124004014','2026-04-24 14:45:48',112),('DoctrineMigrations\\Version20190201150324','2026-04-24 14:45:49',116),('DoctrineMigrations\\Version20190219200020','2026-04-24 14:45:49',2),('DoctrineMigrations\\Version20190305152308','2026-04-24 14:45:49',1326),('DoctrineMigrations\\Version20190321181243','2026-04-24 14:45:50',144),('DoctrineMigrations\\Version20190502161758','2026-04-24 14:45:50',355),('DoctrineMigrations\\Version20190510205245','2026-04-24 14:45:51',288),('DoctrineMigrations\\Version20190605171157','2026-04-24 14:45:51',347),('DoctrineMigrations\\Version20190617100845','2026-04-24 14:45:51',2233),('DoctrineMigrations\\Version20190706224211','2026-04-24 14:45:54',1517),('DoctrineMigrations\\Version20190706224219','2026-04-24 14:45:55',1040),('DoctrineMigrations\\Version20190729162655','2026-04-24 14:45:56',587),('DoctrineMigrations\\Version20190730123324','2026-04-24 14:45:57',2787),('DoctrineMigrations\\Version20190813162649','2026-04-24 14:46:00',513),('DoctrineMigrations\\Version20191024100951','2026-04-24 14:46:00',152),('DoctrineMigrations\\Version20191108151534','2026-04-24 14:46:00',690),('DoctrineMigrations\\Version20191113132640','2026-04-24 14:46:01',128),('DoctrineMigrations\\Version20191116110124','2026-04-24 14:46:01',217),('DoctrineMigrations\\Version20191204120823','2026-04-24 14:46:01',173),('DoctrineMigrations\\Version20200109102138','2026-04-24 14:46:02',1569),('DoctrineMigrations\\Version20200125123942','2026-04-24 14:46:03',230),('DoctrineMigrations\\Version20200204124425','2026-04-24 14:46:03',129),('DoctrineMigrations\\Version20200205115243','2026-04-24 14:46:04',3668),('DoctrineMigrations\\Version20200205115244','2026-04-24 14:46:07',409),('DoctrineMigrations\\Version20200308171950','2026-04-24 14:46:08',1265),('DoctrineMigrations\\Version20200323163038','2026-04-24 14:46:09',552),('DoctrineMigrations\\Version20200323163039','2026-04-24 14:46:10',0),('DoctrineMigrations\\Version20200413133226','2026-04-24 14:46:10',178),('DoctrineMigrations\\Version20200524142042','2026-04-24 14:46:10',185),('DoctrineMigrations\\Version20200705152310','2026-04-24 14:46:10',279),('DoctrineMigrations\\Version20200725213424','2026-04-24 14:46:10',777),('DoctrineMigrations\\Version20210316224358','2026-04-24 14:46:11',526),('DoctrineMigrations\\Version20210320162820','2026-04-24 14:46:12',179),('DoctrineMigrations\\Version20210405105611','2026-04-24 14:46:12',117),('DoctrineMigrations\\Version20210605154245','2026-04-24 14:46:12',466),('DoctrineMigrations\\Version20210704111542','2026-04-24 14:46:12',306),('DoctrineMigrations\\Version20210717211144','2026-04-24 14:46:13',206),('DoctrineMigrations\\Version20210719123928','2026-04-24 14:46:13',491),('DoctrineMigrations\\Version20210727104955','2026-04-24 14:46:14',1678),('DoctrineMigrations\\Version20210802152259','2026-04-24 14:46:15',173),('DoctrineMigrations\\Version20210802152814','2026-04-24 14:46:15',66),('DoctrineMigrations\\Version20210802160837','2026-04-24 14:46:15',614),('DoctrineMigrations\\Version20210802174318','2026-04-24 14:46:16',416),('DoctrineMigrations\\Version20210802174319','2026-04-24 14:46:17',1),('DoctrineMigrations\\Version20210802174320','2026-04-24 14:46:17',368),('DoctrineMigrations\\Version20211008092010','2026-04-24 14:46:17',73),('DoctrineMigrations\\Version20211230163612','2026-04-24 14:46:17',162),('DoctrineMigrations\\Version20220101204501','2026-04-24 14:46:17',529),('DoctrineMigrations\\Version20220315224645','2026-04-24 14:46:18',460),('DoctrineMigrations\\Version20220404150236','2026-04-24 14:46:18',409),('DoctrineMigrations\\Version20220531145920','2026-04-24 14:46:19',516),('DoctrineMigrations\\Version20220722125847','2026-04-24 14:46:19',264),('DoctrineMigrations\\Version20230126002049','2026-04-24 14:46:20',2666),('DoctrineMigrations\\Version20230126002050','2026-04-24 14:46:22',411),('DoctrineMigrations\\Version20230327143628','2026-04-24 14:46:23',1013),('DoctrineMigrations\\Version20230606125948','2026-04-24 14:46:24',150),('DoctrineMigrations\\Version20230819090536','2026-04-24 14:46:24',970),('DoctrineMigrations\\Version20231130000719','2026-04-24 14:46:25',15),('DoctrineMigrations\\Version20240214061246','2026-04-24 14:46:25',784),('DoctrineMigrations\\Version20240326125247','2026-04-24 14:46:26',244),('DoctrineMigrations\\Version20240920105524','2026-04-24 14:46:26',1),('DoctrineMigrations\\Version20240926111739','2026-04-24 14:46:26',632),('DoctrineMigrations\\Version20250608143244','2026-04-24 14:46:27',239),('DoctrineMigrations\\Version20251031142000','2026-04-24 14:46:27',1706),('DoctrineMigrations\\Version20251031143000','2026-04-24 14:46:29',585),('DoctrineMigrations\\Version20251214160001','2026-04-24 14:46:29',235);
/*!40000 ALTER TABLE `migration_versions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-24 20:47:51
