-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`persona`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`persona` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `tipo_documento` ENUM("Tarjeta identidad", "cedula ciudadia", "cedula extranjeria", "NIT") NOT NULL,
  `documento` BIGINT NOT NULL,
  `nombre` VARCHAR(80) NULL,
  `apellido` VARCHAR(80) NULL,
  `codigo_pais` VARCHAR(8) NOT NULL,
  `telefono` BIGINT NOT NULL,
  `correo_electronico` VARCHAR(80) NOT NULL,
  `contrasena` VARCHAR(128) NULL,
  `rol` ENUM("Superadministrador", "Administrador", "Cliente", "Empleado", "Proveedor") NOT NULL,
  `estado` ENUM("Activo", "Inactivo") NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`departamento`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`departamento` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `codigo` INT NOT NULL,
  `estado` ENUM("Activo", "Inactivo") NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`municipio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`municipio` (
  `id` BIGINT NOT NULL,
  `nombre` VARCHAR(80) NOT NULL,
  `codigo` INT NOT NULL,
  `estado` ENUM("Activo", "Inactivo") NOT NULL,
  `departamento_id` BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_municipio_departamento1_idx` (`departamento_id` ASC) VISIBLE,
  CONSTRAINT `fk_municipio_departamento1`
    FOREIGN KEY (`departamento_id`)
    REFERENCES `mydb`.`departamento` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`direccion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`direccion` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nombre_completo` VARCHAR(160) NOT NULL,
  `barrio` TEXT(100) NOT NULL,
  `domicilio` TEXT(200) NOT NULL,
  `referencias` TEXT(200) NULL,
  `telefono` VARCHAR(15) NOT NULL,
  `estado` ENUM("Activo", "Inactivo") NOT NULL,
  `persona_id` BIGINT UNSIGNED NOT NULL,
  `municipio_id` BIGINT NOT NULL,
  `departamento_id` BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_direccion_persona1_idx` (`persona_id` ASC) VISIBLE,
  INDEX `fk_direccion_municipio1_idx` (`municipio_id` ASC) VISIBLE,
  INDEX `fk_direccion_departamento1_idx` (`departamento_id` ASC) VISIBLE,
  CONSTRAINT `fk_direccion_persona1`
    FOREIGN KEY (`persona_id`)
    REFERENCES `mydb`.`persona` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_direccion_municipio1`
    FOREIGN KEY (`municipio_id`)
    REFERENCES `mydb`.`municipio` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_direccion_departamento1`
    FOREIGN KEY (`departamento_id`)
    REFERENCES `mydb`.`departamento` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`entrega`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`entrega` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `tipo` ENUM("Domicilio", "Establecimiento fisico") NOT NULL,
  `fecha_hora` DATETIME NOT NULL,
  `estado` ENUM("Pendiente", "En camino", "Entregado") NOT NULL,
  `costo_domicilio` DECIMAL NOT NULL,
  `direccion_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_entrega_direccion1_idx` (`direccion_id` ASC) VISIBLE,
  CONSTRAINT `fk_entrega_direccion1`
    FOREIGN KEY (`direccion_id`)
    REFERENCES `mydb`.`direccion` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`pedido`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`pedido` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `fecha` DATE NOT NULL,
  `fechaEntrega` DATE NULL,
  `horaEntrega` TIME NULL,
  `estado` ENUM("Pendiente", "En Proceso", "En camino", "Entregado") NOT NULL,
  `persona_id` BIGINT UNSIGNED NOT NULL,
  `entrega_id` BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_pedido_persona1_idx` (`persona_id` ASC) VISIBLE,
  INDEX `fk_pedido_entrega1_idx` (`entrega_id` ASC) VISIBLE,
  CONSTRAINT `fk_pedido_persona1`
    FOREIGN KEY (`persona_id`)
    REFERENCES `mydb`.`persona` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_pedido_entrega1`
    FOREIGN KEY (`entrega_id`)
    REFERENCES `mydb`.`entrega` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`proveedor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`proveedor` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `tipo_persona` ENUM("Juridica", "Natural") NOT NULL,
  `razon_social` VARCHAR(100) NOT NULL,
  `nombre_comercial` VARCHAR(85) NOT NULL,
  `representante_legal` VARCHAR(85) NOT NULL,
  `persona_id` BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`, `persona_id`),
  INDEX `fk_proveedor_persona1_idx` (`persona_id` ASC) VISIBLE,
  CONSTRAINT `fk_proveedor_persona1`
    FOREIGN KEY (`persona_id`)
    REFERENCES `mydb`.`persona` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`metodo_pago`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`metodo_pago` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `metodo` ENUM("billeteras electrónicas", "Cuenta bancaria", "Efectivo") NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`factura`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`factura` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `estado` ENUM("Pendiente", "Facturado") NOT NULL,
  `fecha` DATE NOT NULL,
  `valor_total` DECIMAL NOT NULL,
  `pedido_id` BIGINT UNSIGNED NOT NULL,
  `metodo_pago_id` BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_factura_pedido1_idx` (`pedido_id` ASC) VISIBLE,
  INDEX `fk_factura_metodo_pago1_idx` (`metodo_pago_id` ASC) VISIBLE,
  CONSTRAINT `fk_factura_pedido1`
    FOREIGN KEY (`pedido_id`)
    REFERENCES `mydb`.`pedido` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_factura_metodo_pago1`
    FOREIGN KEY (`metodo_pago_id`)
    REFERENCES `mydb`.`metodo_pago` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`abono`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`abono` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `numero_abonos` ENUM("Pago inicial", "Pago final") NOT NULL,
  `fecha` DATE NOT NULL,
  `estado` ENUM("Abono confirmado") NOT NULL,
  `pedido_id` BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_abono_pedido1_idx` (`pedido_id` ASC) VISIBLE,
  CONSTRAINT `fk_abono_pedido1`
    FOREIGN KEY (`pedido_id`)
    REFERENCES `mydb`.`pedido` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`promocion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`promocion` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(80) NOT NULL,
  `descripcion` TEXT(200) NOT NULL,
  `descuento_porcentaje` DECIMAL NOT NULL,
  `fecha_inicio` DATE NOT NULL,
  `fecha_final` DATE NOT NULL,
  `estado` ENUM("Inicio", "Finalizado") NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`producto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`producto` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nombre` ENUM("Tamal clásico") NOT NULL,
  `descripcion` TEXT(200) NOT NULL,
  `precio` DECIMAL NOT NULL,
  `estado` ENUM("Disponible", "No disponible") NOT NULL,
  `unidad_medida` FLOAT NOT NULL,
  `cantidad` INT NOT NULL,
  `estado` ENUM("Disponible", "No disponible") NOT NULL,
  `marca` VARCHAR(80) NOT NULL,
  `tipo` ENUM("Insumo", "Producto") NOT NULL,
  `promocion_id` BIGINT UNSIGNED NOT NULL,
  `total` DECIMAL NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_producto_promocion1_idx` (`promocion_id` ASC) VISIBLE,
  CONSTRAINT `fk_producto_promocion1`
    FOREIGN KEY (`promocion_id`)
    REFERENCES `mydb`.`promocion` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`calificacion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`calificacion` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `comentario` TEXT(500) NOT NULL,
  `calificacion` ENUM("1", "2", "3", "4", "5") NOT NULL,
  `fecha` DATE NOT NULL,
  `pedido_id` BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_reseña_pedido1_idx` (`pedido_id` ASC) VISIBLE,
  CONSTRAINT `fk_reseña_pedido1`
    FOREIGN KEY (`pedido_id`)
    REFERENCES `mydb`.`pedido` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`inventario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`inventario` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `cantidad_disponible` INT NOT NULL,
  `fecha_actualizacion` DATE NOT NULL,
  `fecha_registro` DATETIME NOT NULL,
  `producto_id` BIGINT UNSIGNED NOT NULL,
  `persona_id` BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_inventario_producto1_idx` (`producto_id` ASC) VISIBLE,
  INDEX `fk_inventario_persona1_idx` (`persona_id` ASC) VISIBLE,
  CONSTRAINT `fk_inventario_producto1`
    FOREIGN KEY (`producto_id`)
    REFERENCES `mydb`.`producto` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_inventario_persona1`
    FOREIGN KEY (`persona_id`)
    REFERENCES `mydb`.`persona` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`carrito_compras`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`carrito_compras` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `cantidad` INT NOT NULL,
  `fecha_creacion` DATE NOT NULL,
  `producto_id` BIGINT UNSIGNED NOT NULL,
  `cliente_id` BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_carrito_compras_producto1_idx` (`producto_id` ASC) VISIBLE,
  INDEX `fk_carrito_compras_persona1_idx` (`cliente_id` ASC) VISIBLE,
  CONSTRAINT `fk_carrito_compras_producto1`
    FOREIGN KEY (`producto_id`)
    REFERENCES `mydb`.`producto` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_carrito_compras_persona1`
    FOREIGN KEY (`cliente_id`)
    REFERENCES `mydb`.`persona` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`persona_has_pedido`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`persona_has_pedido` (
  `persona_id` BIGINT UNSIGNED NOT NULL,
  `pedido_id` BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (`persona_id`, `pedido_id`),
  INDEX `fk_persona_has_pedido_pedido1_idx` (`pedido_id` ASC) VISIBLE,
  INDEX `fk_persona_has_pedido_persona_idx` (`persona_id` ASC) VISIBLE,
  CONSTRAINT `fk_persona_has_pedido_persona`
    FOREIGN KEY (`persona_id`)
    REFERENCES `mydb`.`persona` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_persona_has_pedido_pedido1`
    FOREIGN KEY (`pedido_id`)
    REFERENCES `mydb`.`pedido` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`detalle_pedido`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `detalle_pedido` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `precio_unitario` DECIMAL NOT NULL,
  `total` DECIMAL NOT NULL,
  `cantidad` BIGINT NOT NULL,
  `pedido_id` BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_detalle_pedido_pedido1_idx` (`pedido_id` ASC) VISIBLE,
  CONSTRAINT `fk_detalle_pedido_pedido1`
    FOREIGN KEY (`pedido_id`)
    REFERENCES `mydb`.`pedido` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`compra`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`compra` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `total` FLOAT NOT NULL,
  `fecha` DATE NOT NULL,
  `persona_id` BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_compra_persona1_idx` (`persona_id` ASC) VISIBLE,
  CONSTRAINT `fk_compra_persona1`
    FOREIGN KEY (`persona_id`)
    REFERENCES `mydb`.`persona` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`detalle_compra`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`detalle_compra` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `descripcion` TEXT(200) NOT NULL,
  `precio` DECIMAL NOT NULL,
  `cantidad` DECIMAL NOT NULL,
  `producto_id` BIGINT UNSIGNED NOT NULL,
  `compra_id` BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_detalle_compra_producto1_idx` (`producto_id` ASC) VISIBLE,
  INDEX `fk_detalle_compra_compra1_idx` (`compra_id` ASC) VISIBLE,
  CONSTRAINT `fk_detalle_compra_producto1`
    FOREIGN KEY (`producto_id`)
    REFERENCES `mydb`.`producto` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_detalle_compra_compra1`
    FOREIGN KEY (`compra_id`)
    REFERENCES `mydb`.`compra` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
