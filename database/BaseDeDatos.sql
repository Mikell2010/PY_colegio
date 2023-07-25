-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema db_prestamos
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema db_prestamos
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `db_prestamos` ;
USE `db_prestamos` ;

-- -----------------------------------------------------
-- Table `db_prestamos`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_prestamos`.`usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(245) NOT NULL,
  `password` VARCHAR(245) NOT NULL,
  `rut` VARCHAR(145) NOT NULL,
  `nombres` VARCHAR(145) NULL,
  `apellido_p` VARCHAR(145) NULL,
  `apellido_m` VARCHAR(145) NULL,
  `curso` VARCHAR(45) NULL,
  `status` VARCHAR(45) NULL,
  `bloqueo` VARCHAR(45) NULL,
  `es_alumno` VARCHAR(45) NULL,
  `fotografia` VARCHAR(245) NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db_prestamos`.`familia`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_prestamos`.`familias` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updeate_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db_prestamos`.`activos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_prestamos`.`activos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `codigo` VARCHAR(45) NOT NULL,
  `nombre` VARCHAR(245) NULL,
  `modelo` VARCHAR(245) NULL,
  `operativo` VARCHAR(45) NULL,
  `estado` VARCHAR(45) NULL,
  `familia_id` INT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW(),
  PRIMARY KEY (`id`),
  INDEX `fk_activos_familia_idx` (`familia_id` ASC) VISIBLE,
  CONSTRAINT `fk_activos_familia`
    FOREIGN KEY (`familia_id`)
    REFERENCES `db_prestamos`.`familia` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db_prestamos`.`prestamos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_prestamos`.`prestamos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `activos_id` INT NOT NULL,
  `usuario_id` INT NOT NULL,
  `admin_entrega_id` INT NOT NULL,
  `admin_recibe_id` INT NOT NULL,
  `vigente` VARCHAR(45) NULL,
  `observacion` VARCHAR(45) NULL,
  `fecha_entrega` DATETIME NULL,
  `fecha_recepcion` DATETIME NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW(),
  PRIMARY KEY (`id`),
  INDEX `fk_prestamos_activos1_idx` (`activos_id` ASC) VISIBLE,
  INDEX `fk_prestamos_usuarios1_idx` (`admin_entrega_id` ASC) VISIBLE,
  INDEX `fk_prestamos_usuarios2_idx` (`admin_recibe_id` ASC) VISIBLE,
  INDEX `fk_prestamos_usuarios3_idx` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_prestamos_activos1`
    FOREIGN KEY (`activos_id`)
    REFERENCES `db_prestamos`.`activos` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_prestamos_usuarios1`
    FOREIGN KEY (`admin_entrega_id`)
    REFERENCES `db_prestamos`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_prestamos_usuarios2`
    FOREIGN KEY (`admin_recibe_id`)
    REFERENCES `db_prestamos`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_prestamos_usuarios3`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `db_prestamos`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
