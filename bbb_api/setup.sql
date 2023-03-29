-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema bbb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema bbb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `bbb` DEFAULT CHARACTER SET utf8 ;
USE `bbb` ;

-- -----------------------------------------------------
-- Table `bbb`.`candidates`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bbb`.`candidates` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `cpf` VARCHAR(11) NOT NULL COMMENT 'CPF',
  `full_name` VARCHAR(100) NOT NULL COMMENT 'Nome completo',
  `birth_date` DATE NOT NULL COMMENT 'Data de nascimento',
  `father_name` VARCHAR(100) NULL COMMENT 'Nome do pai',
  `mother_name` VARCHAR(100) NULL COMMENT 'Nome da mãe',
  `gender` ENUM('M', 'F', 'OUTRO') NOT NULL COMMENT 'Sexo',
  `height` FLOAT(3) NOT NULL COMMENT 'Altura',
  `religion` VARCHAR(45) NULL COMMENT 'Religião',
  `email` VARCHAR(100) NOT NULL COMMENT 'E-mail',
  `password` VARCHAR(45) NOT NULL COMMENT 'Senha',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Data de criação do registro',
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Data de atualização do registro',
  `deleted_at` DATETIME NULL COMMENT 'Data de remoção do registro',
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bbb`.`applications`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bbb`.`applications` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `candidate_id` INT NOT NULL,
  `program_season` ENUM('BBB24') NOT NULL,
  `country_region` ENUM('NORTE', 'NORDESTE', 'CENTROOESTE', 'SUDESTE', 'SUL') NOT NULL,
  `video_uuid` VARCHAR(255) NULL,
  `photo1_uuid` VARCHAR(255) NULL,
  `photo2_uuid` VARCHAR(255) NULL,
  `photo3_uuid` VARCHAR(255) NULL,
  `status` ENUM('PENDENTE', 'ENTREGUE', 'REJEITADO', 'APROVADO') NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` DATETIME NULL,
  PRIMARY KEY (`id`, `candidate_id`),
  INDEX `fk_applications_candidate_idx` (`candidate_id` ASC) VISIBLE,
  INDEX `program_season_INDEX` (`program_season` ASC) INVISIBLE,
  INDEX `country_region_INDEX` (`country_region` ASC) VISIBLE,
  CONSTRAINT `fk_applications_candidates`
    FOREIGN KEY (`candidate_id`)
    REFERENCES `bbb`.`candidates` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bbb`.`questions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bbb`.`questions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `program_season` ENUM('BBB24') NOT NULL,
  `form_section` ENUM('BASICO', 'PESSOAL', 'FAMILIA', 'ESTILODEVIDA', 'DESEJOS', 'MEDICO', 'BBB') NOT NULL,
  `question_text` VARCHAR(255) NOT NULL,
  `is_active` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  INDEX `is_active_INDEX` (`is_active` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bbb`.`answers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bbb`.`answers` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `application_id` INT NOT NULL,
  `question_id` INT NOT NULL,
  `answer_text` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`, `application_id`, `question_id`),
  INDEX `fk_answers_application_idx` (`application_id` ASC) VISIBLE,
  INDEX `fk_answers_question_idx` (`question_id` ASC) INVISIBLE,
  CONSTRAINT `fk_answers_applications`
    FOREIGN KEY (`application_id`)
    REFERENCES `bbb`.`applications` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_answers_questions`
    FOREIGN KEY (`question_id`)
    REFERENCES `bbb`.`questions` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
