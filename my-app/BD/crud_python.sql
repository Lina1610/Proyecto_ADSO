-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         8.0.30 - MySQL Community Server - GPL
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para crud_python
CREATE DATABASE IF NOT EXISTS crud_python /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_genral_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE crud_python;

-- Volcando estructura para tabla crud_python.persona
CREATE TABLE IF NOT EXISTS `persona` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,  
  `nombre` VARCHAR(80) NULL,  
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

-- Volcando estructura para tabla crud_python.administrador
CREATE TABLE IF NOT EXISTS `administrador` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `tipo_documento` ENUM("Tarjeta identidad", "cedula ciudadia", "cedula extranjeria", "NIT") NOT NULL,
  `documento` BIGINT NOT NULL,
  `nombre` VARCHAR(80) NULL,
  `apellido` VARCHAR(80) NULL,
  `codigo_pais` VARCHAR(8) NOT NULL,
  `telefono` BIGINT NOT NULL,
  `correo_electronico` VARCHAR(80) NOT NULL,
  `contrasena` VARCHAR(128) NULL,  
  `estado` ENUM("Activo", "Inactivo") NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

-- Volcando estructura para tabla crud_python.clientes
CREATE TABLE IF NOT EXISTS `cliente` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `tipo_documento` ENUM("Tarjeta identidad", "cedula ciudadia", "cedula extranjeria", "NIT") NOT NULL,
  `documento` BIGINT NOT NULL,
  `nombre` VARCHAR(80) NULL,
  `apellido` VARCHAR(80) NULL,
  `codigo_pais` VARCHAR(8) NOT NULL,
  `telefono` BIGINT NOT NULL,
  `correo_electronico` VARCHAR(80) NOT NULL,
  `contrasena` VARCHAR(128) NULL,  
  `estado` ENUM("Activo", "Inactivo") NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

-- Volcando datos para la tabla crud_python.cliente: ~5 rows (aproximadamente)
INSERT INTO `cliente` (`id`, `tipo_documento`, `documento`, `nombre`, `apellido`, `codigo_pais`, `telefono`, `correo_electronico`, `contrasena`, `estado`) 
VALUES
  (1, 'cedula ciudadania', 12345678, 'Juan', 'Pérez', '+57', 3123456789, 'juan.perez@gmail.com', 'hashed_password_1', 'Activo'),
  (2, 'cedula ciudadania', 87654321, 'María', 'Gómez', '+57', 3129876543, 'maria.gomez@gmail.com', 'hashed_password_2', 'Activo'),
  (3, 'NIT', 900123456, 'Comercializadora', 'XYZ', '+57', 3101234567, 'contacto@comercialxyz.com', 'hashed_password_3', 'Activo'),
  (4, 'cedula extranjeria', 45678901, 'James', 'Smith', '+1', 1234567890, 'james.smith@gmail.com', 'hashed_password_4', 'Inactivo'),
  (5, 'Tarjeta identidad', 11223344, 'Laura', 'Martínez', '+57', 3145678901, 'laura.martinez@gmail.com', 'hashed_password_5', 'Activo');

-- Volcando estructura para tabla crud_python.tbl_empleados
CREATE TABLE IF NOT EXISTS tbl_empleados (
  id_empleado int NOT NULL AUTO_INCREMENT,
  nombre_empleado varchar(50) DEFAULT NULL,
  apellido_empleado varchar(50) DEFAULT NULL,
  sexo_empleado int DEFAULT NULL,
  telefono_empleado varchar(50) DEFAULT NULL,
  email_empleado varchar(50) DEFAULT NULL,
  profesion_empleado varchar(50) DEFAULT NULL,
  foto_empleado mediumtext,
  salario_empleado bigint DEFAULT NULL,
  fecha_registro timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_empleado)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

-- Volcando datos para la tabla crud_python.tbl_empleados: ~3 rows (aproximadamente)
INSERT INTO `tbl_empleados` VALUES (4,'Urian','Viera',1,'54544454','programadorphp2017@gmail.com','Ingeniero de Sistemas','fda30f83ebbc4fb1a2ce2609b2b1e34c6614c1dff6e44460b9ba27ed5bb8e927.png',3500000,'2023-08-23 17:04:49'),(5,'Brenda','Viera',2,'323543543','brenda@gmail.com','Dev','22c055aeec314572a0046ec50b84f21719270dac6ea34c91b8380ac289fff9e5.png',1200000,'2023-08-23 17:05:34'),(6,'Alejandro','Torres',1,'324242342','alejandro@gmail.com','Tecnico','7b84aceb56534d27aa2e8b727a245dca9f60156a070a47c491ff2d21da1742e5.png',2100,'2023-08-23 17:06:13'),(7,'Karla','Ramos',2,'345678','karla@gmail.com','Ingeniera','248cc9c38cfb494bb2300d7cbf4a3b317522f295338b4639a8e025e6b203291c.png',2300,'2023-08-23 17:07:28'),(8,'hojas','Ramos',2,'345678','karla@gmail.com','Ingeniera','248cc9c38cfb494bb2300d7cbf4a3b317522f295338b4639a8e025e6b203291c.png',2300,'2023-08-23 17:07:28');



-- Volcando estructura para tabla crud_python.proveedor
CREATE TABLE IF NOT EXISTS `proveedor` (
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
    REFERENCES `cliente` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

=======
INSERT INTO tbl_empleados VALUES (4,'Urian','Viera',1,'54544454','programadorphp2017@gmail.com','Ingeniero de Sistemas','fda30f83ebbc4fb1a2ce2609b2b1e34c6614c1dff6e44460b9ba27ed5bb8e927.png',3500000,'2023-08-23 17:04:49'),(5,'Brenda','Viera',2,'323543543','brenda@gmail.com','Dev','22c055aeec314572a0046ec50b84f21719270dac6ea34c91b8380ac289fff9e5.png',1200000,'2023-08-23 17:05:34'),(6,'Alejandro','Torres',1,'324242342','alejandro@gmail.com','Tecnico','7b84aceb56534d27aa2e8b727a245dca9f60156a070a47c491ff2d21da1742e5.png',2100,'2023-08-23 17:06:13'),(7,'Karla','Ramos',2,'345678','karla@gmail.com','Ingeniera','248cc9c38cfb494bb2300d7cbf4a3b317522f295338b4639a8e025e6b203291c.png',2300,'2023-08-23 17:07:28');
>>>>>>> 36830dc2cb493114ed80227b97328681b712e4c3

-- Volcando estructura para tabla crud_python.users
CREATE TABLE IF NOT EXISTS users (
  id int NOT NULL AUTO_INCREMENT,
  name_surname varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  email_user varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  pass_user text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  created_user timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

-- Volcando datos para la tabla crud_python.users: ~2 rows (aproximadamente)
INSERT INTO users (id, name_surname, email_user, pass_user, created_user) VALUES
	(1, 'Urian', 'dev@gmail.com', 'scrypt:32768:8:1$ZXqvqovbXYQZdrAB$66758083429739f4f8985992b22cb89fb58c04b99010858e7fb26f73078a23dd3e16019a17bf881108d582a91a635d2c21d26d80da1612c2d9c9bbb9b06452dc', '2023-07-21 20:10:01'),
	(2, 'demo', 'demo@gmail.com', 'scrypt:32768:8:1$Yl2tGU1Ru1Q4Jrzq$d88a0ded538dcfc3a01c8ebf4ea77700576203f6a7cc765f04627464c6047bdcf8eaad84ca3cf0bb5ed058d2dff8ee7a0ba690803538764bedc3ba6173ac6a8a', '2023-07-21 20:29:28');


-- Volcando estructura para tabla crud_python.departamento
CREATE TABLE IF NOT EXISTS `departamento` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `codigo` INT NOT NULL,
  `estado` ENUM("Activo", "Inactivo") NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

-- Volcando estructura para tabla crud_python.municipio
CREATE TABLE IF NOT EXISTS `municipio` (
  `id` BIGINT NOT NULL,
  `nombre` VARCHAR(80) NOT NULL,
  `codigo` INT NOT NULL,
  `estado` ENUM("Activo", "Inactivo") NOT NULL,
  `departamento_id` BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_municipio_departamento1_idx` (`departamento_id` ASC) VISIBLE,
  CONSTRAINT `fk_municipio_departamento1`
    FOREIGN KEY (`departamento_id`)
    REFERENCES `departamento` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- Volcando estructura para tabla crud_python.direccion
CREATE TABLE IF NOT EXISTS `direccion` (
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
    REFERENCES `persona` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_direccion_municipio1`
    FOREIGN KEY (`municipio_id`)
    REFERENCES `municipio` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_direccion_departamento1`
    FOREIGN KEY (`departamento_id`)
    REFERENCES `departamento` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;


-- Volcando estructura para tabla crud_python.entrega
CREATE TABLE IF NOT EXISTS `entrega` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `tipo` ENUM("Domicilio", "Establecimiento fisico") NOT NULL,
  `fecha_hora` DATETIME NOT NULL,
  `estado` ENUM("Pendiente", "En camino", "Entregado") NOT NULL,
  `costo_domicilio` DECIMAL NOT NULL,
  `direccion_id` BIGINT UNSIGNED NOT NULL,  -- Asegurarse de que sea BIGINT UNSIGNED
  PRIMARY KEY (`id`),
  INDEX `fk_entrega_direccion1_idx` (`direccion_id` ASC) VISIBLE,
  CONSTRAINT `fk_entrega_direccion1`
    FOREIGN KEY (`direccion_id`)
    REFERENCES `direccion` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- Volcando estructura para tabla crud_python.pedido
CREATE TABLE IF NOT EXISTS `pedido` (
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
    REFERENCES `persona` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_pedido_entrega1`
    FOREIGN KEY (`entrega_id`)
    REFERENCES `entrega` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- Volcando estructura para tabla crud_python.metodo_pago
CREATE TABLE IF NOT EXISTS `metodo_pago` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `metodo` ENUM("billeteras electrónicas", "Cuenta bancaria", "Efectivo") NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

-- Volcando estructura para tabla crud_python.factura
CREATE TABLE IF NOT EXISTS `factura` (
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
    REFERENCES `pedido` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_factura_metodo_pago1`
    FOREIGN KEY (`metodo_pago_id`)
    REFERENCES `metodo_pago` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- Volcando estructura para tabla crud_python.abono
CREATE TABLE IF NOT EXISTS `abono` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `numero_abonos` ENUM("Pago inicial", "Pago final") NOT NULL,
  `fecha` DATE NOT NULL,
  `estado` ENUM("Abono confirmado") NOT NULL,
  `pedido_id` BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_abono_pedido1_idx` (`pedido_id` ASC) VISIBLE,
  CONSTRAINT `fk_abono_pedido1`
    FOREIGN KEY (`pedido_id`)
    REFERENCES `pedido` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- Volcando estructura para tabla crud_python.promocion
CREATE TABLE IF NOT EXISTS `promocion` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(80) NOT NULL,
  `descripcion` TEXT(200) NOT NULL,
  `descuento_porcentaje` DECIMAL(5,2) NOT NULL,  -- Usamos DECIMAL(5,2) para permitir hasta 3 dígitos enteros y 2 decimales
  `fecha_inicio` DATE NOT NULL,
  `fecha_final` DATE NOT NULL,
  `estado` ENUM("Inicio", "Finalizado") NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE = InnoDB;


-- Volcando estructura para tabla crud_python.producto
CREATE TABLE IF NOT EXISTS `producto` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nombre` ENUM("Tamal clásico") NOT NULL,  -- Esto está bien si solo tienes este valor
  `descripcion` TEXT(200) NOT NULL,
  `precio` DECIMAL(10, 2) NOT NULL,  -- Se recomienda especificar la precisión para DECIMAL
  `estado` ENUM("Disponible", "No disponible") NOT NULL,
  `unidad_medida` DECIMAL(10, 2) NOT NULL,  -- Se recomienda usar DECIMAL para valores exactos
  `cantidad` INT NOT NULL,
  `marca` VARCHAR(80) NOT NULL,
  `tipo` ENUM("Insumo", "Producto") NOT NULL,
  `promocion_id` BIGINT UNSIGNED NOT NULL,
  `total` DECIMAL(10, 2) NOT NULL,  -- Se recomienda especificar la precisión para DECIMAL
  PRIMARY KEY (`id`),
  INDEX `fk_producto_promocion1_idx` (`promocion_id` ASC) VISIBLE,
  CONSTRAINT `fk_producto_promocion1`
    FOREIGN KEY (`promocion_id`)
    REFERENCES `promocion` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

INSERT INTO `producto` 
  (`nombre`, `descripcion`, `precio`, `estado`, `unidad_medida`, `cantidad`, `marca`, `tipo`, `promocion_id`, `total`) 
VALUES
  ('Tamal clásico', 'Delicioso tamal clásico de pollo con arroz y vegetales', 5000.00, 'Disponible', 1.00, 100, 'Marca A', 'Producto', 1, 5000.00),
  ('Tamal clásico', 'Tamal clásico con carne de cerdo, arroz y especias', 5500.00, 'Disponible', 1.00, 50, 'Marca B', 'Producto', 2, 5500.00),
  ('Tamal clásico', 'Tamal clásico con pollo y salsa picante', 6000.00, 'No disponible', 1.00, 0, 'Marca C', 'Producto', 3, 0.00);

-- Volcando estructura para tabla crud_python.producto
CREATE TABLE IF NOT EXISTS `calificacion` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `comentario` TEXT(500) NOT NULL,
  `calificacion` ENUM("1", "2", "3", "4", "5") NOT NULL,
  `fecha` DATE NOT NULL,
  `pedido_id` BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_reseña_pedido1_idx` (`pedido_id` ASC) VISIBLE
  CONSTRAINT `fk_reseña_pedido1`
    FOREIGN KEY (`pedido_id`)
    REFERENCES `pedido` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- Volcando estructura para tabla crud_python.inventario
CREATE TABLE IF NOT EXISTS `inventario` (
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
    REFERENCES `producto` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_inventario_persona1`
    FOREIGN KEY (`persona_id`)
    REFERENCES `persona` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- Volcando estructura para tabla crud_python.carrito_compras
CREATE TABLE IF NOT EXISTS `carrito_compras` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `cantidad` INT NOT NULL,
  `fecha_creacion` DATE NOT NULL,
  `producto_id` BIGINT UNSIGNED NOT NULL,
  `cliente_id` BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_carrito_compras_producto1_idx` (`producto_id` ASC) VISIBLE,  -- Índice para la clave foránea producto_id
  INDEX `fk_carrito_compras_persona1_idx` (`cliente_id` ASC) VISIBLE,  -- Índice para la clave foránea cliente_id
  CONSTRAINT `fk_carrito_compras_producto1`
    FOREIGN KEY (`producto_id`)
    REFERENCES `producto` (`id`)  -- La referencia a la tabla producto
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_carrito_compras_persona1`
    FOREIGN KEY (`cliente_id`)
    REFERENCES `persona` (`id`)  -- La referencia a la tabla persona
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- Volcando estructura para tabla crud_python.persona_has_pedido
CREATE TABLE IF NOT EXISTS `persona_has_pedido` (
  `persona_id` BIGINT UNSIGNED NOT NULL,
  `pedido_id` BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (`persona_id`, `pedido_id`),
  INDEX `fk_persona_has_pedido_pedido1_idx` (`pedido_id` ASC) VISIBLE,
  INDEX `fk_persona_has_pedido_persona_idx` (`persona_id` ASC) VISIBLE,
  CONSTRAINT `fk_persona_has_pedido_persona`
    FOREIGN KEY (`persona_id`)
    REFERENCES `persona` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_persona_has_pedido_pedido1`
    FOREIGN KEY (`pedido_id`)
    REFERENCES `pedido` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- Volcando estructura para tabla crud_python.detalle_pedido
CREATE TABLE IF NOT EXISTS `detalle_pedido` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `precio_unitario` DECIMAL(10, 2) NOT NULL,  
  `total` DECIMAL(10, 2) NOT NULL,            
  `cantidad` BIGINT NOT NULL,
  `pedido_id` BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_detalle_pedido_pedido1_idx` (`pedido_id` ASC) VISIBLE,
  CONSTRAINT `fk_detalle_pedido_pedido1`
    FOREIGN KEY (`pedido_id`)
    REFERENCES `pedido` (`id`)  
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- Volcando estructura para tabla crud_python.compra
CREATE TABLE IF NOT EXISTS `compra` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `total` FLOAT NOT NULL,
  `fecha` DATE NOT NULL,
  `persona_id` BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_compra_persona1_idx` (`persona_id` ASC) VISIBLE,
  CONSTRAINT `fk_compra_persona1`
    FOREIGN KEY (`persona_id`)
    REFERENCES `persona` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- Volcando estructura para tabla crud_python.compra
CREATE TABLE IF NOT EXISTS `detalle_compra` (
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
    REFERENCES `producto` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_detalle_compra_compra1`
    FOREIGN KEY (`compra_id`)
    REFERENCES `compra` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;






/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;