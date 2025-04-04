CREATE TABLE `abono` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `numero_abonos` enum('Pago inicial','Pago final') NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `estado` enum('Abono Pendiente','Abono confirmado') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `monto` decimal(10,0) NOT NULL,
  `abono_final` decimal(10,0) DEFAULT NULL,
  `pedido_id` bigint unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_abono_pedido1_idx` (`pedido_id`),
  CONSTRAINT `fk_abono_pedido1` FOREIGN KEY (`pedido_id`) REFERENCES `pedido` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `abono` (`id`, `numero_abonos`, `fecha`, `estado`, `monto`, `abono_final`, `pedido_id`) VALUES (1, 'Pago final', '2025-04-02 20:51:24', 'Abono Pendiente', 56000, 89, 2);
INSERT INTO `abono` (`id`, `numero_abonos`, `fecha`, `estado`, `monto`, `abono_final`, `pedido_id`) VALUES (2, 'Pago inicial', '2025-04-03 12:58:45', 'Abono Pendiente', 56777, NULL, 2);
INSERT INTO `abono` (`id`, `numero_abonos`, `fecha`, `estado`, `monto`, `abono_final`, `pedido_id`) VALUES (3, 'Pago inicial', '2025-04-03 12:59:04', 'Abono Pendiente', 677, 56, 1);

CREATE TABLE `carrito_compras` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `cantidad` int NOT NULL,
  `fecha_creacion` date NOT NULL,
  `producto_id` bigint unsigned NOT NULL,
  `users_id` bigint unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_carrito_compras_producto1_idx` (`producto_id`),
  KEY `fk_carrito_compras_users1_idx` (`users_id`),
  CONSTRAINT `fk_carrito_compras_producto1` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`),
  CONSTRAINT `fk_carrito_compras_users1` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=161 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `carrito_compras` (`id`, `cantidad`, `fecha_creacion`, `producto_id`, `users_id`) VALUES (159, 2, 2025-04-03, 3, 4);

CREATE TABLE `departamento` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `codigo` varchar(3) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `estado` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (1, '05', 'Antioquia ', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (2, '08', 'Atlántico ', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (3, '11', 'Bogotá', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (4, '13', 'Bolívar', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (5, '15', 'Boyacá', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (6, '17', 'Caldas', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (7, '18', 'Caquetá', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (8, '19', 'Cauca', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (9, '20', 'Cesar', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (10, '23', 'Córdoba', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (11, '25', 'Cundinamarca', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (12, '27', 'Chocó', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (13, '41', 'Huila', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (14, '44', 'La Guajira', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (15, '47', 'Magdalena', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (16, '50', 'Meta', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (17, '52', 'Nariño', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (18, '54', 'Norte de Santander', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (19, '63', 'Quindío', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (20, '66', 'Risaralda', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (21, '68', 'Santander', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (22, '70', 'Sucre', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (23, '73', 'Tolima', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (24, '76', 'Valle del Cauca', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (25, '81', 'Arauca', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (26, '85', 'Casanare', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (27, '86', 'Putumayo', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (28, '88', 'San Andrés y Providencia', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (29, '91', 'Amazonas', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (30, '94', 'Guainía', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (31, '95', 'Guaviare', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (32, '97', 'Vaupés', 1);
INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES (33, '99', 'Vichada', 1);

CREATE TABLE `detalle_pedido` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `precio_unitario` decimal(10,2) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `cantidad` bigint NOT NULL,
  `pedido_id` bigint unsigned NOT NULL,
  `producto_id` bigint unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_detalle_pedido_pedido1_idx` (`pedido_id`),
  KEY `fk_detalle_pedido_producto1_idx` (`producto_id`),
  CONSTRAINT `fk_detalle_pedido_pedido1` FOREIGN KEY (`pedido_id`) REFERENCES `pedido` (`id`),
  CONSTRAINT `fk_detalle_pedido_producto1` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=238 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `detalle_pedido` (`id`, `precio_unitario`, `total`, `cantidad`, `pedido_id`, `producto_id`) VALUES (229, 26.00, 52.00, 2, 1, 1);
INSERT INTO `detalle_pedido` (`id`, `precio_unitario`, `total`, `cantidad`, `pedido_id`, `producto_id`) VALUES (230, 26.00, 130.00, 5, 2, 1);
INSERT INTO `detalle_pedido` (`id`, `precio_unitario`, `total`, `cantidad`, `pedido_id`, `producto_id`) VALUES (231, 26.00, 104.00, 4, 3, 1);
INSERT INTO `detalle_pedido` (`id`, `precio_unitario`, `total`, `cantidad`, `pedido_id`, `producto_id`) VALUES (232, 26.00, 104.00, 4, 4, 1);
INSERT INTO `detalle_pedido` (`id`, `precio_unitario`, `total`, `cantidad`, `pedido_id`, `producto_id`) VALUES (233, 23.00, 207.00, 9, 5, 3);
INSERT INTO `detalle_pedido` (`id`, `precio_unitario`, `total`, `cantidad`, `pedido_id`, `producto_id`) VALUES (234, 26.00, 26.00, 1, 6, 1);
INSERT INTO `detalle_pedido` (`id`, `precio_unitario`, `total`, `cantidad`, `pedido_id`, `producto_id`) VALUES (235, 45.00, 45.00, 1, 6, 2);
INSERT INTO `detalle_pedido` (`id`, `precio_unitario`, `total`, `cantidad`, `pedido_id`, `producto_id`) VALUES (236, 23.00, 23.00, 1, 6, 3);
INSERT INTO `detalle_pedido` (`id`, `precio_unitario`, `total`, `cantidad`, `pedido_id`, `producto_id`) VALUES (237, 234.00, 468.00, 2, 7, 5);

CREATE TABLE `direccion` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `nombre_completo` varchar(160) NOT NULL,
  `barrio` text NOT NULL,
  `domicilio` text NOT NULL,
  `referencias` text,
  `telefono` varchar(15) NOT NULL,
  `estado` enum('Activo','Inactivo') NOT NULL,
  `costo_domicilio` bigint DEFAULT NULL,
  `users_id` bigint unsigned NOT NULL,
  `municipio_id` bigint NOT NULL,
  `departamento_id` bigint unsigned NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_direccion_municipio1_idx` (`municipio_id`),
  KEY `fk_direccion_users1_idx` (`users_id`),
  KEY `fk_direccion_departamento1_idx` (`departamento_id`),
  CONSTRAINT `fk_direccion_departamento1_idx` FOREIGN KEY (`departamento_id`) REFERENCES `departamento` (`id`),
  CONSTRAINT `fk_direccion_municipio1` FOREIGN KEY (`municipio_id`) REFERENCES `municipio` (`id`),
  CONSTRAINT `fk_direccion_users1_idx` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `direccion` (`id`, `nombre_completo`, `barrio`, `domicilio`, `referencias`, `telefono`, `estado`, `costo_domicilio`, `users_id`, `municipio_id`, `departamento_id`, `created_at`) VALUES (1, 'JUAN SEBASTIAN MORENO OLMOS', 'lagos', 'carrera 10 2-23', 'CASA VERDE CON AZUL', '3214412444', 'Activo', NULL, 1, 26, 1, '2025-04-02 20:48:08');
INSERT INTO `direccion` (`id`, `nombre_completo`, `barrio`, `domicilio`, `referencias`, `telefono`, `estado`, `costo_domicilio`, `users_id`, `municipio_id`, `departamento_id`, `created_at`) VALUES (2, 'JUAN SEBASTIAN MORENO OLMOS', 'LAGOS', 'CASA VERDE', 'CASA VERDE', '34555675786', 'Activo', 1, 1, 756, 16, '2025-04-02 20:52:31');
INSERT INTO `direccion` (`id`, `nombre_completo`, `barrio`, `domicilio`, `referencias`, `telefono`, `estado`, `costo_domicilio`, `users_id`, `municipio_id`, `departamento_id`, `created_at`) VALUES (3, 'brandon', 'lagos', 'carrera 10 2-23', 'casa verde', '3214412444', 'Activo', 5000, 2, 482, 12, '2025-04-02 20:56:19');
INSERT INTO `direccion` (`id`, `nombre_completo`, `barrio`, `domicilio`, `referencias`, `telefono`, `estado`, `costo_domicilio`, `users_id`, `municipio_id`, `departamento_id`, `created_at`) VALUES (4, 'brandon', 'asd', 'carrera 10 2-23-89', 'dasdas', '32144124446', 'Activo', NULL, 2, 162, 2, '2025-04-02 20:57:14');
INSERT INTO `direccion` (`id`, `nombre_completo`, `barrio`, `domicilio`, `referencias`, `telefono`, `estado`, `costo_domicilio`, `users_id`, `municipio_id`, `departamento_id`, `created_at`) VALUES (5, 'brandon', 'lagos', 'carrera 10 2-23', 'casa verde', '3214412444', 'Activo', 5000, 4, 255, 5, '2025-04-02 22:09:00');
INSERT INTO `direccion` (`id`, `nombre_completo`, `barrio`, `domicilio`, `referencias`, `telefono`, `estado`, `costo_domicilio`, `users_id`, `municipio_id`, `departamento_id`, `created_at`) VALUES (6, 'brandony', 'cumaral', 'carrera 10 2-23-6', 'asjkdhaskjd123das2', '321441244455', 'Activo', 4555, 4, 781, 17, '2025-04-02 22:10:38');
INSERT INTO `direccion` (`id`, `nombre_completo`, `barrio`, `domicilio`, `referencias`, `telefono`, `estado`, `costo_domicilio`, `users_id`, `municipio_id`, `departamento_id`, `created_at`) VALUES (7, 'el olmos jujas', 'adasd', '213das-123', 'dsaasd', '3265465464', 'Activo', 5000, 4, 740, 16, '2025-04-02 23:06:03');
INSERT INTO `direccion` (`id`, `nombre_completo`, `barrio`, `domicilio`, `referencias`, `telefono`, `estado`, `costo_domicilio`, `users_id`, `municipio_id`, `departamento_id`, `created_at`) VALUES (8, 'alexandra olmos', 'esmeralda', 'calle10 2-23', 'pedrito y su amor', '1048847238', 'Activo', NULL, 4, 484, 12, '2025-04-02 23:08:47');
INSERT INTO `direccion` (`id`, `nombre_completo`, `barrio`, `domicilio`, `referencias`, `telefono`, `estado`, `costo_domicilio`, `users_id`, `municipio_id`, `departamento_id`, `created_at`) VALUES (9, 'mi mai', 'la verdadera rata olmos', 'carretera olmos', 'asdasd', '9891234566', 'Activo', 2333, 4, 481, 12, '2025-04-02 23:10:33');
INSERT INTO `direccion` (`id`, `nombre_completo`, `barrio`, `domicilio`, `referencias`, `telefono`, `estado`, `costo_domicilio`, `users_id`, `municipio_id`, `departamento_id`, `created_at`) VALUES (10, '45', '45', '45', '45', '455657676', 'Inactivo', 1, 1, 754, 16, '2025-04-03 13:10:50');
INSERT INTO `direccion` (`id`, `nombre_completo`, `barrio`, `domicilio`, `referencias`, `telefono`, `estado`, `costo_domicilio`, `users_id`, `municipio_id`, `departamento_id`, `created_at`) VALUES (11, 'lina marcela', 'asdasd', 'asdasd-4234', 'asd23123', '3456312345', 'Activo', NULL, 1, 16, 1, '2025-04-03 14:42:37');

CREATE TABLE `entrega` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `tipo` enum('Domicilio','Presencial') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `fecha_hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `estado` enum('Pendiente','En Proceso','En camino','Entregado') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `costo_domicilio` decimal(10,2) DEFAULT '0.00',
  `direccion_id` bigint unsigned DEFAULT NULL,
  `users_id` bigint unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_entrega_direccion1_idx` (`direccion_id`),
  KEY `fk_entrega_users` (`users_id`),
  CONSTRAINT `fk_entrega_direccion1` FOREIGN KEY (`direccion_id`) REFERENCES `direccion` (`id`),
  CONSTRAINT `fk_entrega_users` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `entrega` (`id`, `tipo`, `fecha_hora`, `estado`, `costo_domicilio`, `direccion_id`, `users_id`) VALUES (1, 'Domicilio', '2025-04-02 20:48:14', 'En camino', 56000.00, 1, 1);
INSERT INTO `entrega` (`id`, `tipo`, `fecha_hora`, `estado`, `costo_domicilio`, `direccion_id`, `users_id`) VALUES (2, 'Presencial', '2025-04-02 20:48:54', 'Entregado', 0.00, NULL, 1);
INSERT INTO `entrega` (`id`, `tipo`, `fecha_hora`, `estado`, `costo_domicilio`, `direccion_id`, `users_id`) VALUES (3, 'Domicilio', '2025-04-02 20:57:22', 'Pendiente', 0.00, 4, 2);
INSERT INTO `entrega` (`id`, `tipo`, `fecha_hora`, `estado`, `costo_domicilio`, `direccion_id`, `users_id`) VALUES (4, 'Domicilio', '2025-04-02 22:11:01', 'En camino', 45000.00, 6, 4);
INSERT INTO `entrega` (`id`, `tipo`, `fecha_hora`, `estado`, `costo_domicilio`, `direccion_id`, `users_id`) VALUES (5, 'Domicilio', '2025-04-02 23:10:45', 'Pendiente', 0.00, 9, 4);
INSERT INTO `entrega` (`id`, `tipo`, `fecha_hora`, `estado`, `costo_domicilio`, `direccion_id`, `users_id`) VALUES (6, 'Presencial', '2025-04-02 23:11:44', 'Entregado', 0.00, NULL, 4);
INSERT INTO `entrega` (`id`, `tipo`, `fecha_hora`, `estado`, `costo_domicilio`, `direccion_id`, `users_id`) VALUES (7, 'Domicilio', '2025-04-03 14:42:42', 'Pendiente', 0.00, 11, 1);

CREATE TABLE `factura` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `estado` enum('Pendiente','Facturado') NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `pedido_id` bigint unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_factura_pedido1_idx` (`pedido_id`) USING BTREE,
  CONSTRAINT `fk_factura_pedido1` FOREIGN KEY (`pedido_id`) REFERENCES `pedido` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `factura` (`id`, `estado`, `fecha`, `pedido_id`) VALUES (1, 'Pendiente', '2025-04-02 20:50:43', 2);
INSERT INTO `factura` (`id`, `estado`, `fecha`, `pedido_id`) VALUES (2, 'Facturado', '2025-04-03 12:58:24', 4);

CREATE TABLE `metodo_pago` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `metodo` enum('Nequi','Daviplata','Cuenta bancaria','Efectivo') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `metodo_pago` (`id`, `metodo`) VALUES (1, 'Nequi');
INSERT INTO `metodo_pago` (`id`, `metodo`) VALUES (2, 'Daviplata');
INSERT INTO `metodo_pago` (`id`, `metodo`) VALUES (3, 'Cuenta bancaria');
INSERT INTO `metodo_pago` (`id`, `metodo`) VALUES (4, 'Efectivo');

CREATE TABLE `migraciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `registros_afectados` int NOT NULL,
  `fecha_ejecucion` datetime NOT NULL,
  `detalles` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `municipio` (
  `id` bigint NOT NULL,
  `codigo` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `nombre` varchar(80) NOT NULL,
  `departamento_id` varchar(3) NOT NULL,
  `estado` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `codigo` (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1, '91001', 'LETICIA', '29', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (2, '91263', 'EL ENCANTO', '29', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (3, '91405', 'LA CHORRERA', '29', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (4, '91407', 'LA PEDRERA', '29', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (5, '91430', 'LA VICTORIA', '29', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (6, '91460', 'MIRITÍ – PARANÁ', '29', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (7, '91530', 'PUERTO ALEGRÍA', '29', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (8, '91536', 'PUERTO ARICA', '29', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (9, '91540', 'PUERTO NARIÑO', '29', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (10, '91669', 'PUERTO SANTANDER', '29', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (11, '91798', 'TARAPACÁ', '29', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (12, '05001', 'MEDELLÍN', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (13, '05002', 'ABEJORRAL', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (14, '05004', 'ABRIAQUÍ', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (15, '05021', 'ALEJANDRÍA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (16, '05030', 'AMAGÁ', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (17, '05031', 'AMALFI', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (18, '05034', 'ANDES', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (19, '05036', 'ANGELÓPOLIS', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (20, '05038', 'ANGOSTURA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (21, '05040', 'ANORÍ', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (22, '05042', 'SANTA FÉ DE ANTIOQUIA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (23, '05044', 'ANZÁ', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (24, '05045', 'APARTADÓ', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (25, '05051', 'ARBOLETES', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (26, '05055', 'ARGELIA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (27, '05059', 'ARMENIA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (28, '05079', 'BARBOSA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (29, '05086', 'BELMIRA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (30, '05088', 'BELLO', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (31, '05091', 'BETANIA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (32, '05093', 'BETULIA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (33, '05101', 'CIUDAD BOLÍVAR', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (34, '05107', 'BRICEÑO', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (35, '05113', 'BURITICÁ', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (36, '05120', 'CÁCERES', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (37, '05125', 'CAICEDO', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (38, '05129', 'CALDAS', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (39, '05134', 'CAMPAMENTO', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (40, '05138', 'CAÑASGORDAS', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (41, '05142', 'CARACOLÍ', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (42, '05145', 'CARAMANTA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (43, '05147', 'CAREPA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (44, '05148', 'EL CARMEN DE VIBORAL', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (45, '05150', 'CAROLINA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (46, '05154', 'CAUCASIA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (47, '05172', 'CHIGORODÓ', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (48, '05190', 'CISNEROS', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (49, '05197', 'COCORNÁ', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (50, '05206', 'CONCEPCIÓN', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (51, '05209', 'CONCORDIA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (52, '05212', 'COPACABANA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (53, '05234', 'DABEIBA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (54, '05237', 'DONMATÍAS', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (55, '05240', 'EBÉJICO', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (56, '05250', 'EL BAGRE', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (57, '05264', 'ENTRERRÍOS', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (58, '05266', 'ENVIGADO', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (59, '05282', 'FREDONIA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (60, '05284', 'FRONTINO', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (61, '05306', 'GIRALDO', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (62, '05308', 'GIRARDOTA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (63, '05310', 'GÓMEZ PLATA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (64, '05313', 'GRANADA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (65, '05315', 'GUADALUPE', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (66, '05318', 'GUARNE', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (67, '05321', 'GUATAPÉ', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (68, '05347', 'HELICONIA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (69, '05353', 'HISPANIA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (70, '05360', 'ITAGÜÍ', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (71, '05361', 'ITUANGO', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (72, '05364', 'JARDÍN', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (73, '05368', 'JERICÓ', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (74, '05376', 'LA CEJA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (75, '05380', 'LA ESTRELLA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (76, '05390', 'LA PINTADA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (77, '05400', 'LA UNIÓN', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (78, '05411', 'LIBORINA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (79, '05425', 'MACEO', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (80, '05440', 'MARINILLA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (81, '05467', 'MONTEBELLO', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (82, '05475', 'MURINDÓ', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (83, '05480', 'MUTATÁ', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (84, '05483', 'NARIÑO', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (85, '05490', 'NECOCLÍ', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (86, '05495', 'NECHÍ', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (87, '05501', 'OLAYA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (88, '05541', 'PEÑOL', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (89, '05543', 'PEQUE', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (90, '05576', 'PUEBLORRICO', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (91, '05579', 'PUERTO BERRÍO', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (92, '05585', 'PUERTO NARE', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (93, '05591', 'PUERTO TRIUNFO', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (94, '05604', 'REMEDIOS', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (95, '05607', 'RETIRO', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (96, '05615', 'RIONEGRO', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (97, '05628', 'SABANALARGA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (98, '05631', 'SABANETA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (99, '05642', 'SALGAR', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (100, '05647', 'SAN ANDRÉS DE CUERQUÍA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (101, '05649', 'SAN CARLOS', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (102, '05652', 'SAN FRANCISCO', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (103, '05656', 'SAN JERÓNIMO', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (104, '05658', 'SAN JOSÉ DE LA MONTAÑA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (105, '05659', 'SAN JUAN DE URABÁ', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (106, '05660', 'SAN LUIS', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (107, '05664', 'SAN PEDRO DE LOS MILAGROS', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (108, '05665', 'SAN PEDRO DE URABÁ', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (109, '05667', 'SAN RAFAEL', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (110, '05670', 'SAN ROQUE', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (111, '05674', 'SAN VICENTE FERRER', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (112, '05679', 'SANTA BÁRBARA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (113, '05686', 'SANTA ROSA DE OSOS', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (114, '05690', 'SANTO DOMINGO', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (115, '05697', 'EL SANTUARIO', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (116, '05736', 'SEGOVIA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (117, '05756', 'SONSÓN', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (118, '05761', 'SOPETRÁN', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (119, '05789', 'TÁMESIS', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (120, '05790', 'TARAZÁ', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (121, '05792', 'TARSO', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (122, '05809', 'TITIRIBÍ', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (123, '05819', 'TOLEDO', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (124, '05837', 'TURBO', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (125, '05842', 'URAMITA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (126, '05847', 'URRAO', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (127, '05854', 'VALDIVIA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (128, '05856', 'VALPARAÍSO', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (129, '05858', 'VEGACHÍ', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (130, '05861', 'VENECIA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (131, '05873', 'VIGÍA DEL FUERTE', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (132, '05885', 'YALÍ', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (133, '05887', 'YARUMAL', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (134, '05890', 'YOLOMBÓ', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (135, '05893', 'YONDÓ', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (136, '05895', 'ZARAGOZA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (137, '05861', 'VENECIA', '1', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (138, '81001', 'ARAUCA', '25', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (139, '81065', 'ARAUQUITA', '25', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (140, '81220', 'CRAVO NORTE', '25', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (141, '81300', 'FORTUL', '25', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (142, '81591', 'PUERTO RONDÓN', '25', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (143, '81736', 'SARAVENA', '25', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (144, '81794', 'TAME', '25', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (145, '88001', 'SAN ANDRÉS', '28', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (146, '88564', 'PROVIDENCIA', '28', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (147, '08001', 'BARRANQUILLA', '2', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (148, '08078', 'BARANOA', '2', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (149, '08137', 'CAMPO DE LA CRUZ', '2', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (150, '08141', 'CANDELARIA', '2', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (151, '08296', 'GALAPA', '2', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (152, '08372', 'JUAN DE ACOSTA', '2', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (153, '08421', 'LURUACO', '2', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (154, '08433', 'MALAMBO', '2', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (155, '08436', 'MANATÍ', '2', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (156, '08520', 'PALMAR DE VARELA', '2', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (157, '08549', 'PIOJÓ', '2', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (158, '08558', 'POLONUEVO', '2', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (159, '08560', 'PONEDERA', '2', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (160, '08573', 'PUERTO COLOMBIA', '2', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (161, '08606', 'REPELÓN', '2', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (162, '08634', 'SABANAGRANDE', '2', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (163, '08638', 'SABANALARGA', '2', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (164, '08675', 'SANTA LUCÍA', '2', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (165, '08685', 'SANTO TOMÁS', '2', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (166, '08758', 'SOLEDAD', '2', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (167, '08770', 'SUAN', '2', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (168, '08832', 'TUBARÁ', '2', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (169, '08849', 'USIACURÍ', '2', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (170, '11001', 'BOGOTÁ, D.C.', '3', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (171, '13001', 'CARTAGENA DE INDIAS', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (172, '13006', 'ACHÍ', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (173, '13030', 'ALTOS DEL ROSARIO', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (174, '13042', 'ARENAL', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (175, '13052', 'ARJONA', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (176, '13062', 'ARROYOHONDO', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (177, '13074', 'BARRANCO DE LOBA', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (178, '13140', 'CALAMAR', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (179, '13160', 'CANTAGALLO', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (180, '13188', 'CICUCO', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (181, '13212', 'CÓRDOBA', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (182, '13222', 'CLEMENCIA', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (183, '13244', 'EL CARMEN DE BOLÍVAR', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (184, '13248', 'EL GUAMO', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (185, '13268', 'EL PEÑÓN', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (186, '13300', 'HATILLO DE LOBA', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (187, '13430', 'MAGANGUÉ', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (188, '13433', 'MAHATES', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (189, '13440', 'MARGARITA', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (190, '13442', 'MARÍA LA BAJA', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (191, '13458', 'MONTECRISTO', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (192, '13468', 'MOMPÓS', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (193, '13473', 'MORALES', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (194, '13490', 'NOROSÍ', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (195, '13549', 'PINILLOS', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (196, '13580', 'REGIDOR', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (197, '13600', 'RÍO VIEJO', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (198, '13620', 'SAN CRISTÓBAL', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (199, '13647', 'SAN ESTANISLAO', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (200, '13650', 'SAN FERNANDO', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (201, '13654', 'SAN JACINTO', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (202, '13655', 'SAN JACINTO DEL CAUCA', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (203, '13657', 'SAN JUAN NEPOMUCENO', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (204, '13667', 'SAN MARTÍN DE LOBA', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (205, '13670', 'SAN PABLO SUR', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (206, '13673', 'SANTA CATALINA', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (207, '13683', 'SANTA ROSA DE LIMA', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (208, '13688', 'SANTA ROSA DEL SUR', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (209, '13744', 'SIMITÍ', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (210, '13760', 'SOPLAVIENTO', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (211, '13780', 'TALAIGUA NUEVO', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (212, '13810', 'TIQUISIO', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (213, '13836', 'TURBACO', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (214, '13838', 'TURBANÁ', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (215, '13873', 'VILLANUEVA', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (216, '13894', 'ZAMBRANO', '4', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (217, '15001', 'TUNJA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (218, '15022', 'ALMEIDA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (219, '15047', 'AQUITANIA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (220, '15051', 'ARCABUCO', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (221, '15087', 'BELÉN', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (222, '15090', 'BERBEO', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (223, '15092', 'BETÉITIVA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (224, '15097', 'BOAVITA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (225, '15104', 'BOYACÁ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (226, '15106', 'BRICEÑO', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (227, '15109', 'BUENAVISTA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (228, '15114', 'BUSBANZÁ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (229, '15131', 'CALDAS', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (230, '15135', 'CAMPOHERMOSO', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (231, '15162', 'CERINZA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (232, '15172', 'CHINAVITA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (233, '15176', 'CHIQUINQUIRÁ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (234, '15180', 'CHISCAS', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (235, '15183', 'CHITA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (236, '15185', 'CHITARAQUE', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (237, '15187', 'CHIVATÁ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (238, '15189', 'CIÉNEGA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (239, '15204', 'CÓMBITA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (240, '15212', 'COPER', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (241, '15215', 'CORRALES', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (242, '15218', 'COVARACHÍA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (243, '15223', 'CUBARÁ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (244, '15224', 'CUCAITA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (245, '15226', 'CUÍTIVA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (246, '15232', 'CHÍQUIZA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (247, '15236', 'CHIVOR', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (248, '15238', 'DUITAMA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (249, '15244', 'EL COCUY', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (250, '15248', 'EL ESPINO', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (251, '15272', 'FIRAVITOBA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (252, '15276', 'FLORESTA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (253, '15293', 'GACHANTIVÁ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (254, '15296', 'GÁMEZA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (255, '15299', 'GARAGOA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (256, '15317', 'GUACAMAYAS', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (257, '15322', 'GUATEQUE', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (258, '15325', 'GUAYATÁ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (259, '15332', 'GÜICÁN DE LA SIERRA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (260, '15362', 'IZA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (261, '15367', 'JENESANO', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (262, '15368', 'JERICÓ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (263, '15377', 'LABRANZAGRANDE', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (264, '15380', 'LA CAPILLA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (265, '15401', 'LA VICTORIA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (266, '15403', 'LA UVITA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (267, '15407', 'VILLA DE LEYVA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (268, '15425', 'MACANAL', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (269, '15442', 'MARIPÍ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (270, '15455', 'MIRAFLORES', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (271, '15464', 'MONGUA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (272, '15466', 'MONGUÍ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (273, '15469', 'MONIQUIRÁ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (274, '15476', 'MOTAVITA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (275, '15480', 'MUZO', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (276, '15491', 'NOBSA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (277, '15494', 'NUEVO COLÓN', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (278, '15500', 'OICATÁ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (279, '15507', 'OTANCHE', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (280, '15511', 'PACHAVITA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (281, '15514', 'PÁEZ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (282, '15516', 'PAIPA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (283, '15518', 'PAJARITO', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (284, '15522', 'PANQUEBA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (285, '15531', 'PAUNA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (286, '15533', 'PAYA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (287, '15537', 'PAZ DE RÍO', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (288, '15542', 'PESCA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (289, '15550', 'PISBA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (290, '15572', 'PUERTO BOYACÁ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (291, '15580', 'QUÍPAMA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (292, '15599', 'RAMIRIQUÍ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (293, '15600', 'RÁQUIRA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (294, '15621', 'RONDÓN', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (295, '15632', 'SABOYÁ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (296, '15638', 'SÁCHICA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (297, '15646', 'SAMACÁ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (298, '15660', 'SAN EDUARDO', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (299, '15664', 'SAN JOSÉ DE PARE', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (300, '15667', 'SAN LUIS DE GACENO', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (301, '15673', 'SAN MATEO', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (302, '15676', 'SAN MIGUEL DE SEMA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (303, '15681', 'SAN PABLO DE BORBUR', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (304, '15686', 'SANTANA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (305, '15690', 'SANTA MARÍA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (306, '15693', 'SANTA ROSA DE VITERBO', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (307, '15696', 'SANTA SOFÍA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (308, '15720', 'SATIVANORTE', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (309, '15723', 'SATIVASUR', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (310, '15740', 'SIACHOQUE', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (311, '15753', 'SOATÁ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (312, '15755', 'SOCOTÁ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (313, '15757', 'SOCHA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (314, '15759', 'SOGAMOSO', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (315, '15761', 'SOMONDOCO', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (316, '15762', 'SORA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (317, '15763', 'SOTAQUIRÁ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (318, '15764', 'SORACÁ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (319, '15774', 'SUSACÓN', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (320, '15776', 'SUTAMARCHÁN', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (321, '15778', 'SUTATENZA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (322, '15790', 'TASCO', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (323, '15798', 'TENZA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (324, '15804', 'TIBANÁ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (325, '15806', 'TIBASOSA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (326, '15808', 'TINJACÁ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (327, '15810', 'TIPACOQUE', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (328, '15814', 'TOCA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (329, '15816', 'TOGÜÍ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (330, '15820', 'TÓPAGA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (331, '15822', 'TOTA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (332, '15832', 'TUNUNGUÁ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (333, '15835', 'TURMEQUÉ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (334, '15837', 'TUTA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (335, '15839', 'TUTAZÁ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (336, '15842', 'ÚMBITA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (337, '15861', 'VENTAQUEMADA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (338, '15879', 'VIRACACHÁ', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (339, '15897', 'ZETAQUIRA', '5', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (340, '17001', 'MANIZALES', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (341, '17013', 'AGUADAS', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (342, '17042', 'ANSERMA', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (343, '17050', 'ARANZAZU', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (344, '17088', 'BELALCÁZAR', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (345, '17174', 'CHINCHINÁ', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (346, '17272', 'FILADELFIA', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (347, '17380', 'LA DORADA', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (348, '17388', 'LA MERCED', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (349, '17433', 'MANZANARES', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (350, '17442', 'MARMATO', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (351, '17444', 'MARQUETALIA', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (352, '17446', 'MARULANDA', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (353, '17486', 'NEIRA', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (354, '17495', 'NORCASIA', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (355, '17513', 'PÁCORA', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (356, '17524', 'PALESTINA', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (357, '17541', 'PENSILVANIA', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (358, '17614', 'RIOSUCIO', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (359, '17616', 'RISARALDA', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (360, '17653', 'SALAMINA', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (361, '17662', 'SAMANÁ', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (362, '17665', 'SAN JOSÉ', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (363, '17777', 'SUPÍA', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (364, '17867', 'VICTORIA', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (365, '17873', 'VILLAMARÍA', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (366, '17877', 'VITERBO', '6', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (367, '18001', 'FLORENCIA', '7', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (368, '18029', 'ALBANIA', '7', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (369, '18094', 'BELÉN DE LOS ANDAQUÍES', '7', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (370, '18150', 'CARTAGENA DEL CHAIRÁ', '7', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (371, '18205', 'CURILLO', '7', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (372, '18247', 'EL DONCELLO', '7', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (373, '18256', 'EL PAUJÍL', '7', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (374, '18410', 'LA MONTAÑITA', '7', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (375, '18460', 'MILÁN', '7', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (376, '18479', 'MORELIA', '7', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (377, '18592', 'PUERTO RICO', '7', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (378, '18610', 'SAN JOSÉ DEL FRAGUA', '7', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (379, '18753', 'SAN VICENTE DEL CAGUÁN', '7', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (380, '18756', 'SOLANO', '7', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (381, '18785', 'SOLITA', '7', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (382, '18860', 'VALPARAÍSO', '7', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (383, '85001', 'YOPAL', '26', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (384, '85010', 'AGUAZUL', '26', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (385, '85015', 'CHÁMEZA', '26', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (386, '85125', 'HATO COROZAL', '26', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (387, '85136', 'LA SALINA', '26', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (388, '85139', 'MANÍ', '26', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (389, '85162', 'MONTERREY', '26', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (390, '85225', 'NUNCHÍA', '26', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (391, '85230', 'OROCUÉ', '26', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (392, '85250', 'PAZ DE ARIPORO', '26', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (393, '85263', 'PORE', '26', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (394, '85279', 'RECETOR', '26', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (395, '85300', 'SABANALARGA', '26', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (396, '85315', 'SÁCAMA', '26', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (397, '85325', 'SAN LUIS DE PALENQUE', '26', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (398, '85400', 'TÁMARA', '26', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (399, '85410', 'TAURAMENA', '26', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (400, '85430', 'TRINIDAD', '26', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (401, '85440', 'VILLANUEVA', '26', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (402, '19001', 'POPAYÁN', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (403, '19022', 'ALMAGUER', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (404, '19050', 'ARGELIA', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (405, '19075', 'BALBOA', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (406, '19100', 'BOLÍVAR', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (407, '19110', 'BUENOS AIRES', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (408, '19130', 'CAJIBÍO', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (409, '19137', 'CALDONO', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (410, '19142', 'CALOTO', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (411, '19212', 'CORINTO', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (412, '19256', 'EL TAMBO', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (413, '19290', 'FLORENCIA', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (414, '19300', 'GUACHENÉ', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (415, '19318', 'GUAPÍ', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (416, '19355', 'INZÁ', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (417, '19364', 'JAMBALÓ', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (418, '19392', 'LA SIERRA', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (419, '19397', 'LA VEGA', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (420, '19418', 'LÓPEZ DE MICAY', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (421, '19450', 'MERCADERES', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (422, '19455', 'MIRANDA', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (423, '19473', 'MORALES', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (424, '19513', 'PADILLA', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (425, '19517', 'PÁEZ - BELALCAZAR', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (426, '19532', 'PATÍA – EL BORDO', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (427, '19533', 'PIAMONTE', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (428, '19548', 'PIENDAMÓ – TUNÍA', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (429, '19573', 'PUERTO TEJADA', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (430, '19585', 'PURACÉ - COCONUCO', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (431, '19622', 'ROSAS', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (432, '19693', 'SAN SEBASTIÁN', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (433, '19698', 'SANTANDER DE QUILICHAO', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (434, '19701', 'SANTA ROSA', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (435, '19743', 'SILVIA', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (436, '19760', 'SOTARA', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (437, '19780', 'SUÁREZ', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (438, '19785', 'SUCRE', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (439, '19807', 'TIMBÍO', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (440, '19809', 'TIMBIQUÍ', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (441, '19821', 'TORIBÍO', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (442, '19824', 'TOTORÓ', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (443, '19845', 'VILLA RICA', '8', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (444, '20001', 'VALLEDUPAR', '9', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (445, '20011', 'AGUACHICA', '9', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (446, '20013', 'AGUSTÍN CODAZZI', '9', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (447, '20032', 'ASTREA', '9', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (448, '20045', 'BECERRIL', '9', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (449, '20060', 'BOSCONIA', '9', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (450, '20175', 'CHIMICHAGUA', '9', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (451, '20178', 'CHIRIGUANÁ', '9', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (452, '20228', 'CURUMANÍ', '9', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (453, '20238', 'EL COPEY', '9', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (454, '20250', 'EL PASO', '9', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (455, '20295', 'GAMARRA', '9', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (456, '20310', 'GONZÁLEZ', '9', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (457, '20383', 'LA GLORIA', '9', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (458, '20400', 'LA JAGUA DE IBIRICO', '9', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (459, '20443', 'MANAURE BALCÓN DEL CESAR', '9', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (460, '20517', 'PAILITAS', '9', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (461, '20550', 'PELAYA', '9', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (462, '20570', 'PUEBLO BELLO', '9', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (463, '20614', 'RÍO DE ORO', '9', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (464, '20621', 'LA PAZ', '9', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (465, '20710', 'SAN ALBERTO', '9', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (466, '20750', 'SAN DIEGO', '9', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (467, '20770', 'SAN MARTÍN', '9', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (468, '20787', 'TAMALAMEQUE', '9', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (469, '27001', 'QUIBDÓ', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (470, '27006', 'ACANDÍ', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (471, '27025', 'ALTO BAUDÓ (PIE DE PATÓ)', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (472, '27050', 'ATRATO (YUTO)', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (473, '27073', 'BAGADÓ', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (474, '27075', 'BAHÍA SOLANO (MUTIS)', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (475, '27077', 'BAJO BAUDÓ (PIZARRO)', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (476, '27099', 'BOJAYÁ (BELLA VISTA)', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (477, '27135', 'EL CANTÓN DEL SAN PABLO', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (478, '27150', 'CARMEN DEL DARIÉN', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (479, '27160', 'CÉRTEGUI', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (480, '27205', 'CONDOTO', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (481, '27245', 'EL CARMEN DE ATRATO', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (482, '27250', 'EL LITORAL DEL SAN JUAN', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (483, '27361', 'ISTMINA', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (484, '27372', 'JURADÓ', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (485, '27413', 'LLORÓ', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (486, '27425', 'MEDIO ATRATO (BETÉ)', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (487, '27430', 'MEDIO BAUDÓ', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (488, '27450', 'MEDIO SAN JUAN (ANDAGOYA)', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (489, '27491', 'NÓVITA', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (490, '27495', 'NUQUÍ', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (491, '27580', 'RÍO IRÓ (SANTA RITA)', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (492, '27600', 'RÍO QUITO (PAIMADÓ)', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (493, '27615', 'RIOSUCIO', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (494, '27660', 'SAN JOSÉ DEL PALMAR', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (495, '27745', 'SIPÍ', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (496, '27787', 'TADÓ', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (497, '27800', 'UNGUÍA', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (498, '27810', 'UNIÓN PANAMERICANA (LAS ÁNIMAS)', '12', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (499, '23001', 'MONTERÍA', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (500, '23068', 'AYAPEL', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (501, '23079', 'BUENAVISTA', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (502, '23090', 'CANALETE', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (503, '23162', 'CERETÉ', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (504, '23168', 'CHIMÁ', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (505, '23182', 'CHINÚ', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (506, '23189', 'CIÉNAGA DE ORO', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (507, '23300', 'COTORRA', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (508, '23350', 'LA APARTADA', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (509, '23417', 'LORICA', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (510, '23419', 'LOS CÓRDOBAS', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (511, '23464', 'MOMIL', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (512, '23466', 'MONTELÍBANO', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (513, '23500', 'MOÑITOS', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (514, '23555', 'PLANETA RICA', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (515, '23570', 'PUEBLO NUEVO', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (516, '23574', 'PUERTO ESCONDIDO', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (517, '23580', 'PUERTO LIBERTADOR', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (518, '23586', 'PURÍSIMA DE LA CONCEPCIÓN', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (519, '23660', 'SAHAGÚN', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (520, '23670', 'SAN ANDRÉS DE SOTAVENTO', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (521, '23672', 'SAN ANTERO', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (522, '23675', 'SAN BERNARDO DEL VIENTO', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (523, '23678', 'SAN CARLOS', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (524, '23682', 'SAN JOSÉ DE URÉ', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (525, '23686', 'SAN PELAYO', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (526, '23807', 'TIERRALTA', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (527, '23815', 'TUCHÍN', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (528, '23855', 'VALENCIA', '10', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (529, '25001', 'AGUA DE DIOS', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (530, '25019', 'ALBÁN', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (531, '25035', 'ANAPOIMA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (532, '25040', 'ANOLAIMA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (533, '25053', 'ARBELÁEZ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (534, '25086', 'BELTRÁN', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (535, '25095', 'BITUIMA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (536, '25099', 'BOJACÁ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (537, '25120', 'CABRERA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (538, '25123', 'CACHIPAY', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (539, '25126', 'CAJICÁ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (540, '25148', 'CAPARRAPÍ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (541, '25151', 'CÁQUEZA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (542, '25154', 'CARMEN DE CARUPA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (543, '25168', 'CHAGUANÍ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (544, '25175', 'CHÍA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (545, '25178', 'CHIPAQUE', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (546, '25181', 'CHOACHÍ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (547, '25183', 'CHOCONTÁ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (548, '25200', 'COGUA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (549, '25214', 'COTA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (550, '25224', 'CUCUNUBÁ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (551, '25245', 'EL COLEGIO', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (552, '25258', 'EL PEÑÓN', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (553, '25260', 'EL ROSAL', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (554, '25269', 'FACATATIVÁ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (555, '25279', 'FÓMEQUE', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (556, '25281', 'FOSCA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (557, '25286', 'FUNZA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (558, '25288', 'FÚQUENE', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (559, '25290', 'FUSAGASUGÁ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (560, '25293', 'GACHALÁ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (561, '25295', 'GACHANCIPÁ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (562, '25297', 'GACHETÁ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (563, '25299', 'GAMA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (564, '25307', 'GIRARDOT', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (565, '25312', 'GRANADA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (566, '25317', 'GUACHETÁ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (567, '25320', 'GUADUAS', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (568, '25322', 'GUASCA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (569, '25324', 'GUATAQUÍ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (570, '25326', 'GUATAVITA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (571, '25328', 'GUAYABAL DE SÍQUIMA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (572, '25335', 'GUAYABETAL', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (573, '25339', 'GUTIÉRREZ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (574, '25368', 'JERUSALÉN', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (575, '25372', 'JUNÍN', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (576, '25377', 'LA CALERA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (577, '25386', 'LA MESA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (578, '25394', 'LA PALMA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (579, '25398', 'LA PEÑA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (580, '25402', 'LA VEGA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (581, '25407', 'LENGUAZAQUE', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (582, '25426', 'MACHETÁ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (583, '25430', 'MADRID', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (584, '25436', 'MANTA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (585, '25438', 'MEDINA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (586, '25473', 'MOSQUERA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (587, '25483', 'NARIÑO', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (588, '25486', 'NEMOCÓN', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (589, '25488', 'NILO', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (590, '25489', 'NIMAIMA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (591, '25491', 'NOCAIMA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (592, '25506', 'VENECIA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (593, '25513', 'PACHO', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (594, '25518', 'PAIME', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (595, '25524', 'PANDI', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (596, '25530', 'PARATEBUENO', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (597, '25535', 'PASCA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (598, '25572', 'PUERTO SALGAR', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (599, '25580', 'PULÍ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (600, '25592', 'QUEBRADANEGRA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (601, '25594', 'QUETAME', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (602, '25596', 'QUIPILE', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (603, '25599', 'APULO', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (604, '25612', 'RICAURTE', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (605, '25645', 'SAN ANTONIO DEL TEQUENDAMA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (606, '25649', 'SAN BERNARDO', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (607, '25653', 'SAN CAYETANO', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (608, '25658', 'SAN FRANCISCO', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (609, '25662', 'SAN JUAN DE RIOSECO', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (610, '25718', 'SASAIMA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (611, '25736', 'SESQUILÉ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (612, '25740', 'SIBATÉ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (613, '25743', 'SILVANIA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (614, '25745', 'SIMIJACA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (615, '25754', 'SOACHA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (616, '25758', 'SOPÓ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (617, '25769', 'SUBACHOQUE', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (618, '25772', 'SUESCA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (619, '25777', 'SUPATÁ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (620, '25779', 'SUSA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (621, '25781', 'SUTATAUSA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (622, '25785', 'TABIO', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (623, '25793', 'TAUSA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (624, '25797', 'TENA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (625, '25799', 'TENJO', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (626, '25805', 'TIBACUY', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (627, '25807', 'TIBIRITA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (628, '25815', 'TOCAIMA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (629, '25817', 'TOCANCIPÁ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (630, '25823', 'TOPAIPÍ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (631, '25839', 'UBALÁ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (632, '25841', 'UBAQUE', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (633, '25843', 'VILLA DE SAN DIEGO DE UBATÉ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (634, '25845', 'UNE', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (635, '25851', 'ÚTICA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (636, '25862', 'VERGARA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (637, '25867', 'VIANÍ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (638, '25871', 'VILLAGÓMEZ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (639, '25873', 'VILLAPINZÓN', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (640, '25875', 'VILLETA', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (641, '25878', 'VIOTÁ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (642, '25885', 'YACOPÍ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (643, '25898', 'ZIPACÓN', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (644, '25899', 'ZIPAQUIRÁ', '11', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (645, '94001', 'INÍRIDA', '30', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (646, '94343', 'BARRANCOMINAS', '30', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (647, '94663', 'MAPIRIPANA', '30', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (648, '94883', 'SAN FELIPE', '30', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (649, '94884', 'PUERTO COLOMBIA', '30', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (650, '94885', 'LA GUADALUPE', '30', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (651, '94886', 'CACAHUAL', '30', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (652, '94887', 'PANA PANA', '30', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (653, '94888', 'MORICHAL NUEVO', '30', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (654, '95001', 'SAN JOSÉ DEL GUAVIARE', '31', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (655, '95015', 'CALAMAR', '31', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (656, '95025', 'EL RETORNO', '31', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (657, '95200', 'MIRAFLORES', '31', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (658, '41001', 'NEIVA', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (659, '41006', 'ACEVEDO', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (660, '41013', 'AGRADO', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (661, '41016', 'AIPE', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (662, '41020', 'ALGECIRAS', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (663, '41026', 'ALTAMIRA', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (664, '41078', 'BARAYA', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (665, '41132', 'CAMPOALEGRE', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (666, '41206', 'COLOMBIA', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (667, '41244', 'ELÍAS', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (668, '41298', 'GARZÓN', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (669, '41306', 'GIGANTE', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (670, '41319', 'GUADALUPE', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (671, '41349', 'HOBO', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (672, '41357', 'ÍQUIRA', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (673, '41359', 'ISNOS', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (674, '41378', 'LA ARGENTINA (LA PLATA VIEJA)', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (675, '41396', 'LA PLATA', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (676, '41483', 'NÁTAGA', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (677, '41503', 'OPORAPA', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (678, '41518', 'PAICOL', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (679, '41524', 'PALERMO', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (680, '41530', 'PALESTINA', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (681, '41548', 'PITAL', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (682, '41551', 'PITALITO', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (683, '41615', 'RIVERA', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (684, '41660', 'SALADOBLANCO', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (685, '41668', 'SAN AGUSTÍN', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (686, '41676', 'SANTA MARÍA', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (687, '41770', 'SUAZA', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (688, '41791', 'TARQUI', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (689, '41797', 'TESALIA (CARNICERÍAS)', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (690, '41799', 'TELLO', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (691, '41801', 'TERUEL', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (692, '41807', 'TIMANÁ', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (693, '41872', 'VILLAVIEJA', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (694, '41885', 'YAGUARÁ', '13', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (695, '44001', 'RIOHACHA', '14', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (696, '44035', 'ALBANIA', '14', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (697, '44078', 'BARRANCAS', '14', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (698, '44090', 'DIBULLA', '14', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (699, '44098', 'DISTRACCIÓN', '14', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (700, '44110', 'EL MOLINO', '14', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (701, '44279', 'FONSECA', '14', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (702, '44378', 'HATONUEVO', '14', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (703, '44420', 'LA JAGUA DEL PILAR', '14', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (704, '44430', 'MAICAO', '14', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (705, '44560', 'MANAURE', '14', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (706, '44650', 'SAN JUAN DEL CESAR', '14', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (707, '44847', 'URIBIA', '14', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (708, '44855', 'URUMITA', '14', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (709, '44874', 'VILLANUEVA', '14', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (710, '47001', 'SANTA MARTA', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (711, '47030', 'ALGARROBO', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (712, '47053', 'ARACATACA', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (713, '47058', 'ARIGUANÍ', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (714, '47161', 'CERRO DE SAN ANTONIO', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (715, '47170', 'CHIBOLO', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (716, '47189', 'CIÉNAGA', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (717, '47205', 'CONCORDIA', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (718, '47245', 'EL BANCO', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (719, '47258', 'EL PIÑÓN', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (720, '47268', 'EL RETÉN', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (721, '47288', 'FUNDACIÓN', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (722, '47318', 'GUAMAL', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (723, '47460', 'NUEVA GRANADA', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (724, '47541', 'PEDRAZA', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (725, '47545', 'PIJIÑO DEL CARMEN', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (726, '47551', 'PIVIJAY', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (727, '47555', 'PLATO', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (728, '47570', 'PUEBLOVIEJO', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (729, '47605', 'REMOLINO', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (730, '47660', 'SABANAS DE SAN ÁNGEL', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (731, '47675', 'SALAMINA', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (732, '47692', 'SAN SEBASTIÁN DE BUENAVISTA', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (733, '47703', 'SAN ZENÓN', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (734, '47707', 'SANTA ANA', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (735, '47720', 'SANTA BÁRBARA DE PINTO', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (736, '47745', 'SITIONUEVO', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (737, '47798', 'TENERIFE', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (738, '47960', 'ZAPAYÁN', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (739, '47980', 'ZONA BANANERA', '15', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (740, '50001', 'VILLAVICENCIO', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (741, '50006', 'ACACÍAS', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (742, '50110', 'BARRANCA DE UPÍA', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (743, '50124', 'CABUYARO', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (744, '50150', 'CASTILLA LA NUEVA', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (745, '50223', 'CUBARRAL', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (746, '50226', 'CUMARAL', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (747, '50245', 'EL CALVARIO', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (748, '50251', 'EL CASTILLO', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (749, '50270', 'EL DORADO', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (750, '50287', 'FUENTEDEORO', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (751, '50313', 'GRANADA', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (752, '50318', 'GUAMAL', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (753, '50325', 'MAPIRIPÁN', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (754, '50330', 'MESETAS', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (755, '50350', 'LA MACARENA', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (756, '50370', 'URIBE', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (757, '50400', 'LEJANÍAS', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (758, '50450', 'PUERTO CONCORDIA', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (759, '50568', 'PUERTO GAITÁN', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (760, '50573', 'PUERTO LÓPEZ', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (761, '50577', 'PUERTO LLERAS', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (762, '50590', 'PUERTO RICO', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (763, '50606', 'RESTREPO', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (764, '50680', 'SAN CARLOS DE GUAROA', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (765, '50683', 'SAN JUAN DE ARAMA', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (766, '50686', 'SAN JUANITO', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (767, '50689', 'SAN MARTÍN DE LOS LLANOS', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (768, '50711', 'VISTAHERMOSA', '16', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (769, '52001', 'PASTO', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (770, '52019', 'ALBÁN (SAN JOSÉ)', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (771, '52022', 'ALDANA', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (772, '52036', 'ANCUYÁ', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (773, '52051', 'ARBOLEDA', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (774, '52079', 'BARBACOAS', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (775, '52083', 'BELÉN', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (776, '52110', 'BUESACO', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (777, '52203', 'COLÓN (GÉNOVA)', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (778, '52207', 'CONSACÁ', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (779, '52210', 'CONTADERO', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (780, '52215', 'CÓRDOBA', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (781, '52224', 'CUASPÚD', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (782, '52227', 'CUMBAL', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (783, '52233', 'CUMBITARA', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (784, '52240', 'CHACHAGÜÍ', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (785, '52250', 'EL CHARCO', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (786, '52254', 'EL PEÑOL', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (787, '52256', 'EL ROSARIO', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (788, '52258', 'EL TABLÓN DE GÓMEZ', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (789, '52260', 'EL TAMBO', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (790, '52287', 'FUNES', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (791, '52317', 'GUACHUCAL', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (792, '52320', 'GUAITARILLA', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (793, '52323', 'GUALMATÁN', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (794, '52352', 'ILES', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (795, '52354', 'IMUÉS', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (796, '52356', 'IPIALES', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (797, '52378', 'LA CRUZ', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (798, '52381', 'LA FLORIDA', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (799, '52385', 'LA LLANADA', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (800, '52390', 'LA TOLA', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (801, '52399', 'LA UNIÓN', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (802, '52405', 'LEIVA', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (803, '52411', 'LINARES', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (804, '52418', 'LOS ANDES (SOTOMAYOR)', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (805, '52427', 'MAGÜÍ (PAYÁN)', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (806, '52435', 'MALLAMA (PIEDRANCHA)', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (807, '52473', 'MOSQUERA', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (808, '52480', 'NARIÑO', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (809, '52490', 'OLAYA HERRERA', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (810, '52506', 'OSPINA', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (811, '52520', 'FRANCISCO PIZARRO', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (812, '52540', 'POLICARPA', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (813, '52560', 'POTOSÍ', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (814, '52565', 'PROVIDENCIA', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (815, '52573', 'PUERRES', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (816, '52585', 'PUPIALES', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (817, '52612', 'RICAURTE', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (818, '52621', 'ROBERTO PAYÁN (SAN JOSÉ)', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (819, '52678', 'SAMANIEGO', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (820, '52683', 'SANDONÁ', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (821, '52685', 'SAN BERNARDO', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (822, '52687', 'SAN LORENZO', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (823, '52693', 'SAN PABLO', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (824, '52694', 'SAN PEDRO DE CARTAGO', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (825, '52696', 'SANTA BÁRBARA', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (826, '52699', 'SANTACRUZ', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (827, '52720', 'SAPUYES', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (828, '52786', 'TAMINANGO', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (829, '52788', 'TANGUA', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (830, '52835', 'SAN ANDRÉS DE TUMACO', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (831, '52838', 'TÚQUERRES', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (832, '52885', 'YACUANQUER', '17', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (833, '54001', 'CÚCUTA', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (834, '54003', 'ÁBREGO', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (835, '54051', 'ARBOLEDAS', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (836, '54099', 'BOCHALEMA', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (837, '54109', 'BUCARASICA', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (838, '54125', 'CÁCOTA DE VELASCO', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (839, '54128', 'CÁCHIRA', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (840, '54172', 'CHINÁCOTA', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (841, '54174', 'CHITAGÁ', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (842, '54206', 'CONVENCIÓN', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (843, '54223', 'CUCUTILLA', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (844, '54239', 'DURANIA', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (845, '54245', 'EL CARMEN', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (846, '54250', 'EL TARRA', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (847, '54261', 'EL ZULIA', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (848, '54313', 'GRAMALOTE', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (849, '54344', 'HACARÍ', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (850, '54347', 'HERRÁN', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (851, '54377', 'LABATECA', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (852, '54385', 'LA ESPERANZA', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (853, '54398', 'LA PLAYA DE BELÉN', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (854, '54405', 'LOS PATIOS', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (855, '54418', 'LOURDES', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (856, '54480', 'MUTISCUA', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (857, '54498', 'OCAÑA', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (858, '54518', 'PAMPLONA', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (859, '54520', 'PAMPLONITA', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (860, '54553', 'PUERTO SANTANDER', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (861, '54599', 'RAGONVALIA', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (862, '54660', 'SALAZAR DE LAS PALMAS', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (863, '54670', 'SAN CALIXTO', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (864, '54673', 'SAN CAYETANO', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (865, '54680', 'SANTIAGO', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (866, '54720', 'SARDINATA', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (867, '54743', 'SANTO DOMINGO DE SILOS', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (868, '54800', 'TEORAMA', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (869, '54810', 'TIBÚ', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (870, '54820', 'TOLEDO', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (871, '54871', 'VILLA CARO', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (872, '54874', 'VILLA DEL ROSARIO', '18', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (873, '86001', 'MOCOA', '27', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (874, '86219', 'COLÓN', '27', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (875, '86320', 'ORITO', '27', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (876, '86568', 'PUERTO ASÍS', '27', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (877, '86569', 'PUERTO CAICEDO', '27', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (878, '86571', 'PUERTO GUZMÁN', '27', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (879, '86573', 'PUERTO LEGUÍZAMO', '27', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (880, '86749', 'SIBUNDOY', '27', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (881, '86755', 'SAN FRANCISCO', '27', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (882, '86757', 'SAN MIGUEL', '27', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (883, '86760', 'SANTIAGO', '27', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (884, '86865', 'VALLE DEL GUAMUEZ', '27', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (885, '86885', 'VILLAGARZÓN', '27', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (886, '63001', 'ARMENIA', '19', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (887, '63111', 'BUENAVISTA', '19', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (888, '63130', 'CALARCÁ', '19', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (889, '63190', 'CIRCASIA', '19', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (890, '63212', 'CÓRDOBA', '19', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (891, '63272', 'FILANDIA', '19', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (892, '63302', 'GÉNOVA', '19', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (893, '63401', 'LA TEBAIDA', '19', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (894, '63470', 'MONTENEGRO', '19', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (895, '63548', 'PIJAO', '19', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (896, '63594', 'QUIMBAYA', '19', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (897, '63690', 'SALENTO', '19', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (898, '66001', 'PEREIRA', '20', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (899, '66045', 'APÍA', '20', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (900, '66075', 'BALBOA', '20', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (901, '66088', 'BELÉN DE UMBRÍA', '20', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (902, '66170', 'DOSQUEBRADAS', '20', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (903, '66318', 'GUÁTICA', '20', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (904, '66383', 'LA CELIA', '20', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (905, '66400', 'LA VIRGINIA', '20', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (906, '66440', 'MARSELLA', '20', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (907, '66456', 'MISTRATÓ', '20', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (908, '66572', 'PUEBLO RICO', '20', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (909, '66594', 'QUINCHÍA', '20', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (910, '66682', 'SANTA ROSA DE CABAL', '20', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (911, '66687', 'SANTUARIO', '20', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (912, '68001', 'BUCARAMANGA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (913, '68013', 'AGUADA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (914, '68020', 'ALBANIA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (915, '68051', 'ARATOCA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (916, '68077', 'BARBOSA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (917, '68079', 'BARICHARA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (918, '68081', 'BARRANCABERMEJA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (919, '68092', 'BETULIA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (920, '68101', 'BOLÍVAR', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (921, '68121', 'CABRERA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (922, '68132', 'CALIFORNIA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (923, '68147', 'CAPITANEJO', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (924, '68152', 'CARCASÍ', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (925, '68160', 'CEPITÁ', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (926, '68162', 'CERRITO', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (927, '68167', 'CHARALÁ', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (928, '68169', 'CHARTA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (929, '68176', 'CHIMA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (930, '68179', 'CHIPATÁ', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (931, '68190', 'CIMITARRA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (932, '68207', 'CONCEPCIÓN', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (933, '68209', 'CONFINES', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (934, '68211', 'CONTRATACIÓN', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (935, '68217', 'COROMORO', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (936, '68229', 'CURITÍ', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (937, '68235', 'EL CARMEN DE CHUCURÍ', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (938, '68245', 'EL GUACAMAYO', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (939, '68250', 'EL PEÑÓN', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (940, '68255', 'EL PLAYÓN', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (941, '68264', 'ENCINO', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (942, '68266', 'ENCISO', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (943, '68271', 'FLORIÁN', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (944, '68276', 'FLORIDABLANCA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (945, '68296', 'GALÁN', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (946, '68298', 'GÁMBITA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (947, '68307', 'GIRÓN', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (948, '68318', 'GUACA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (949, '68320', 'GUADALUPE', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (950, '68322', 'GUAPOTÁ', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (951, '68324', 'GUAVATÁ', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (952, '68327', 'GÜEPSA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (953, '68344', 'HATO', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (954, '68368', 'JESÚS MARÍA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (955, '68370', 'JORDÁN', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (956, '68377', 'LA BELLEZA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (957, '68385', 'LANDÁZURI', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (958, '68397', 'LA PAZ', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (959, '68406', 'LEBRIJA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (960, '68418', 'LOS SANTOS', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (961, '68425', 'MACARAVITA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (962, '68432', 'MÁLAGA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (963, '68444', 'MATANZA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (964, '68464', 'MOGOTES', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (965, '68468', 'MOLAGAVITA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (966, '68498', 'OCAMONTE', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (967, '68500', 'OIBA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (968, '68502', 'ONZAGA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (969, '68522', 'PALMAR', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (970, '68524', 'PALMAS DEL SOCORRO', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (971, '68533', 'PÁRAMO', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (972, '68547', 'PIEDECUESTA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (973, '68549', 'PINCHOTE', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (974, '68572', 'PUENTE NACIONAL', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (975, '68573', 'PUERTO PARRA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (976, '68575', 'PUERTO WILCHES', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (977, '68615', 'RIONEGRO', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (978, '68655', 'SABANA DE TORRES', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (979, '68669', 'SAN ANDRÉS', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (980, '68673', 'SAN BENITO', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (981, '68679', 'SAN GIL', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (982, '68682', 'SAN JOAQUÍN', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (983, '68684', 'SAN JOSÉ DE MIRANDA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (984, '68686', 'SAN MIGUEL', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (985, '68689', 'SAN VICENTE DE CHUCURÍ', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (986, '68705', 'SANTA BÁRBARA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (987, '68720', 'SANTA HELENA DEL OPÓN', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (988, '68745', 'SIMACOTA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (989, '68755', 'SOCORRO', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (990, '68770', 'SUAITA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (991, '68773', 'SUCRE', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (992, '68780', 'SURATÁ', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (993, '68820', 'TONA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (994, '68855', 'VALLE DE SAN JOSÉ', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (995, '68861', 'VÉLEZ', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (996, '68867', 'VETAS', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (997, '68872', 'VILLANUEVA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (998, '68895', 'ZAPATOCA', '21', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (999, '70001', 'SINCELEJO', '22', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1000, '70110', 'BUENAVISTA', '22', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1001, '70124', 'CAIMITO', '22', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1002, '70204', 'COLOSÓ', '22', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1003, '70215', 'COROZAL', '22', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1004, '70221', 'COVEÑAS', '22', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1005, '70230', 'CHALÁN', '22', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1006, '70233', 'EL ROBLE', '22', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1007, '70235', 'GALERAS', '22', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1008, '70265', 'GUARANDA', '22', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1009, '70400', 'LA UNIÓN', '22', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1010, '70418', 'LOS PALMITOS', '22', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1011, '70429', 'MAJAGUAL', '22', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1012, '70473', 'MORROA', '22', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1013, '70508', 'OVEJAS', '22', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1014, '70523', 'PALMITO', '22', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1015, '70670', 'SAMPUÉS', '22', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1016, '70678', 'SAN BENITO ABAD', '22', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1017, '70702', 'SAN JUAN DE BETULIA', '22', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1018, '70708', 'SAN MARCOS', '22', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1019, '70713', 'SAN ONOFRE', '22', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1020, '70717', 'SAN PEDRO', '22', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1021, '70742', 'SAN LUIS DE SINCÉ', '22', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1022, '70771', 'SUCRE', '22', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1023, '70820', 'SANTIAGO DE TOLÚ', '22', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1024, '70823', 'TOLÚ VIEJO', '22', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1025, '73001', 'IBAGUÉ', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1026, '73024', 'ALPUJARRA', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1027, '73026', 'ALVARADO', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1028, '73030', 'AMBALEMA', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1029, '73043', 'ANZOÁTEGUI', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1030, '73055', 'ARMERO (GUAYABAL)', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1031, '73067', 'ATACO', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1032, '73124', 'CAJAMARCA', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1033, '73148', 'CARMEN DE APICALÁ', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1034, '73152', 'CASABIANCA', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1035, '73168', 'CHAPARRAL', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1036, '73200', 'COELLO', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1037, '73217', 'COYAIMA', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1038, '73226', 'CUNDAY', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1039, '73236', 'DOLORES', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1040, '73268', 'ESPINAL', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1041, '73270', 'FALAN', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1042, '73275', 'FLANDES', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1043, '73283', 'FRESNO', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1044, '73319', 'GUAMO', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1045, '73347', 'HERVEO', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1046, '73349', 'HONDA', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1047, '73352', 'ICONONZO', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1048, '73408', 'LÉRIDA', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1049, '73411', 'LÍBANO', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1050, '73443', 'SAN SEBASTIÁN DE MARIQUITA', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1051, '73449', 'MELGAR', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1052, '73461', 'MURILLO', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1053, '73483', 'NATAGAIMA', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1054, '73504', 'ORTEGA', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1055, '73520', 'PALOCABILDO', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1056, '73547', 'PIEDRAS', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1057, '73555', 'PLANADAS', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1058, '73563', 'PRADO', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1059, '73585', 'PURIFICACIÓN', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1060, '73616', 'RIOBLANCO', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1061, '73622', 'RONCESVALLES', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1062, '73624', 'ROVIRA', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1063, '73671', 'SALDAÑA', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1064, '73675', 'SAN ANTONIO', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1065, '73678', 'SAN LUIS', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1066, '73686', 'SANTA ISABEL', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1067, '73770', 'SUÁREZ', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1068, '73854', 'VALLE DE SAN JUAN', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1069, '73861', 'VENADILLO', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1070, '73870', 'VILLAHERMOSA', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1071, '73873', 'VILLARRICA', '23', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1072, '76001', 'CALI', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1073, '76020', 'ALCALÁ', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1074, '76036', 'ANDALUCÍA', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1075, '76041', 'ANSERMANUEVO', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1076, '76054', 'ARGELIA', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1077, '76100', 'BOLÍVAR', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1078, '76109', 'BUENAVENTURA', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1079, '76111', 'GUADALAJARA DE BUGA', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1080, '76113', 'BUGALAGRANDE', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1081, '76122', 'CAICEDONIA', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1082, '76126', 'CALIMA (DARIEN)', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1083, '76130', 'CANDELARIA', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1084, '76147', 'CARTAGO', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1085, '76233', 'DAGUA', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1086, '76243', 'EL ÁGUILA', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1087, '76246', 'EL CAIRO', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1088, '76248', 'EL CERRITO', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1089, '76250', 'EL DOVIO', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1090, '76275', 'FLORIDA', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1091, '76306', 'GINEBRA', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1092, '76318', 'GUACARÍ', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1093, '76364', 'JAMUNDÍ', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1094, '76377', 'LA CUMBRE', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1095, '76400', 'LA UNIÓN', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1096, '76403', 'LA VICTORIA', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1097, '76497', 'OBANDO', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1098, '76520', 'PALMIRA', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1099, '76563', 'PRADERA', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1100, '76606', 'RESTREPO', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1101, '76616', 'RIOFRÍO', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1102, '76622', 'ROLDANILLO', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1103, '76670', 'SAN PEDRO', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1104, '76736', 'SEVILLA', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1105, '76823', 'TORO', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1106, '76828', 'TRUJILLO', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1107, '76834', 'TULUÁ', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1108, '76845', 'ULLOA', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1109, '76863', 'VERSALLES', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1110, '76869', 'VIJES', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1111, '76890', 'YOTOCO', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1112, '76892', 'YUMBO', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1113, '76895', 'ZARZAL', '24', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1114, '97001', 'MITÚ', '32', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1115, '97161', 'CARURÚ', '32', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1116, '97511', 'PACOA', '32', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1117, '97666', 'TARAIRA', '32', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1118, '97777', 'PAPUNAHUA', '32', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1119, '97889', 'YAVARATÉ', '32', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1120, '99001', 'PUERTO CARREÑO', '33', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1121, '99524', 'LA PRIMAVERA', '33', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1122, '99624', 'SANTA ROSALÍA', '33', 1);
INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES (1123, '99773', 'CUMARIBO', '33', 1);

CREATE TABLE `pedido` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `fecha` timestamp NULL DEFAULT NULL,
  `fechaEntrega` date DEFAULT NULL,
  `horaEntrega` time DEFAULT NULL,
  `estado` enum('Pendiente','En Proceso','En camino','Entregado') NOT NULL,
  `total` decimal(10,2) unsigned NOT NULL,
  `entrega_id` bigint unsigned NOT NULL,
  `users_id` bigint unsigned NOT NULL,
  `producto_id` bigint unsigned NOT NULL,
  `metodo_pago_id` bigint unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_pedido_entrega1_idx` (`entrega_id`),
  KEY `fk_pedido_users1_idx` (`users_id`),
  KEY `fk_pedido_producto1_idx` (`producto_id`),
  KEY `fk_pedido_metodo_pago1_idx` (`metodo_pago_id`) USING BTREE,
  CONSTRAINT `fk_pedido_entrega1` FOREIGN KEY (`entrega_id`) REFERENCES `entrega` (`id`),
  CONSTRAINT `fk_pedido_metodo_pago1` FOREIGN KEY (`metodo_pago_id`) REFERENCES `metodo_pago` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_pedido_producto1` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_pedido_users1` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `pedido` (`id`, `fecha`, `fechaEntrega`, `horaEntrega`, `estado`, `total`, `entrega_id`, `users_id`, `producto_id`, `metodo_pago_id`) VALUES (1, '2025-04-02 20:48:14', NULL, NULL, 'Pendiente', 52.00, 1, 1, 1, 3);
INSERT INTO `pedido` (`id`, `fecha`, `fechaEntrega`, `horaEntrega`, `estado`, `total`, `entrega_id`, `users_id`, `producto_id`, `metodo_pago_id`) VALUES (2, '2025-04-02 20:48:54', 2025-04-04, 23:55:00, 'En camino', 130.00, 2, 1, 1, 2);
INSERT INTO `pedido` (`id`, `fecha`, `fechaEntrega`, `horaEntrega`, `estado`, `total`, `entrega_id`, `users_id`, `producto_id`, `metodo_pago_id`) VALUES (3, '2025-04-02 20:57:22', 2025-04-10, 21:03:00, 'Entregado', 104.00, 1, 2, 1, 4);
INSERT INTO `pedido` (`id`, `fecha`, `fechaEntrega`, `horaEntrega`, `estado`, `total`, `entrega_id`, `users_id`, `producto_id`, `metodo_pago_id`) VALUES (4, '2025-04-02 22:11:01', 2025-04-03, 15:17:00, 'En camino', 104.00, 1, 4, 1, 3);
INSERT INTO `pedido` (`id`, `fecha`, `fechaEntrega`, `horaEntrega`, `estado`, `total`, `entrega_id`, `users_id`, `producto_id`, `metodo_pago_id`) VALUES (5, '2025-04-02 23:10:45', NULL, NULL, 'Pendiente', 207.00, 5, 4, 3, 3);
INSERT INTO `pedido` (`id`, `fecha`, `fechaEntrega`, `horaEntrega`, `estado`, `total`, `entrega_id`, `users_id`, `producto_id`, `metodo_pago_id`) VALUES (6, '2025-04-02 23:11:44', 2025-04-11, 17:57:00, 'En camino', 94.00, 2, 4, 1, 4);
INSERT INTO `pedido` (`id`, `fecha`, `fechaEntrega`, `horaEntrega`, `estado`, `total`, `entrega_id`, `users_id`, `producto_id`, `metodo_pago_id`) VALUES (7, '2025-04-03 14:42:42', NULL, NULL, 'Pendiente', 468.00, 7, 1, 5, 2);

CREATE TABLE `producto` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `codigo` bigint unsigned NOT NULL,
  `nombre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `descripcion` text NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `estado` enum('Disponible','No disponible') NOT NULL,
  `unidad_medida` decimal(10,2) DEFAULT NULL,
  `cantidad` int NOT NULL,
  `marca` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `total` decimal(10,2) NOT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `producto` (`id`, `codigo`, `nombre`, `descripcion`, `precio`, `estado`, `unidad_medida`, `cantidad`, `marca`, `total`, `imagen`) VALUES (1, 26, 'tamal de garagoa', 'es un tamal muy rico', 26.00, 'Disponible', NULL, 26, NULL, 676.00, '/static/assets/img/productos/dabb789b-a46e-4f9c-8510-072f759de89a.jpg');
INSERT INTO `producto` (`id`, `codigo`, `nombre`, `descripcion`, `precio`, `estado`, `unidad_medida`, `cantidad`, `marca`, `total`, `imagen`) VALUES (2, 27, 'hojas 2', 'sads', 45.00, 'Disponible', NULL, 45, NULL, 2025.00, NULL);
INSERT INTO `producto` (`id`, `codigo`, `nombre`, `descripcion`, `precio`, `estado`, `unidad_medida`, `cantidad`, `marca`, `total`, `imagen`) VALUES (3, 1, 'sebastian', 'rere', 67.00, 'Disponible', NULL, 23, NULL, 1541.00, '/static/assets/img/productos/936acc7a-22e4-464d-a23c-1154463e626b.jpg');
INSERT INTO `producto` (`id`, `codigo`, `nombre`, `descripcion`, `precio`, `estado`, `unidad_medida`, `cantidad`, `marca`, `total`, `imagen`) VALUES (4, 45, '45', '45', 67.00, 'Disponible', NULL, 67, NULL, 4489.00, '/static/assets/img/productos/86e3db32-e023-40fd-a4ea-1a99c3053174.jpg');
INSERT INTO `producto` (`id`, `codigo`, `nombre`, `descripcion`, `precio`, `estado`, `unidad_medida`, `cantidad`, `marca`, `total`, `imagen`) VALUES (5, 56, 'brr', 'dsf', 234.00, 'Disponible', NULL, 23, NULL, 5382.00, '/static/assets/img/productos/07e59397-f108-42e7-b344-9ef8d8133db9.jpeg');
INSERT INTO `producto` (`id`, `codigo`, `nombre`, `descripcion`, `precio`, `estado`, `unidad_medida`, `cantidad`, `marca`, `total`, `imagen`) VALUES (6, 566, 'asd', '123ds', 21.00, 'Disponible', NULL, 123, NULL, 2583.00, '/static/assets/img/productos/d029fca2-6def-418c-811e-9ff77f539c88.jpg');

CREATE TABLE `stock` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `cantidad_disponible` bigint NOT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `producto_id` bigint unsigned NOT NULL,
  `users_id` bigint unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_stock_producto1_idx` (`producto_id`),
  KEY `fk_stock_users1_idx` (`users_id`),
  CONSTRAINT `fk_stock_producto1` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_stock_users1` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `tbl_empleados` (
  `id_empleado` int NOT NULL AUTO_INCREMENT,
  `nombre_empleado` varchar(50) DEFAULT NULL,
  `apellido_empleado` varchar(50) DEFAULT NULL,
  `sexo_empleado` int DEFAULT NULL,
  `telefono_empleado` varchar(50) DEFAULT NULL,
  `email_empleado` varchar(50) DEFAULT NULL,
  `profesion_empleado` varchar(50) DEFAULT NULL,
  `foto_empleado` mediumtext,
  `salario_empleado` bigint DEFAULT NULL,
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_empleado`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `users` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `tipo_documento` enum('Cedula ciudadania','Tarjeta identidad','Cedula extranjeria','NIT') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `documento` bigint NOT NULL,
  `nombre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `apellido` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `telefono` bigint NOT NULL,
  `correo` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `contrasena` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `rol` enum('administrador','cliente','proveedor','empleado','superadmin') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `estado` enum('activo','inactivo') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `created_user` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `users` (`id`, `tipo_documento`, `documento`, `nombre`, `apellido`, `telefono`, `correo`, `contrasena`, `rol`, `estado`, `created_user`) VALUES (1, 'Cedula ciudadania', 1048847249, 'Juan Sebastian', 'Moreno Olmos', 3000000000, 'juansebastian812005@gmail.com', 'scrypt:32768:8:1$8F9YE74jHKYRYi6O$6925aa7069f92818d03a1a8eb13eff6f899472b43898eadd5b41c11946eb037e0c59e77b7b833c9a6ee91e09400aede45037eaa7339dad1840a54bf5c7be3943', 'administrador', 'activo', '2025-04-02 20:32:50');
INSERT INTO `users` (`id`, `tipo_documento`, `documento`, `nombre`, `apellido`, `telefono`, `correo`, `contrasena`, `rol`, `estado`, `created_user`) VALUES (2, 'Cedula ciudadania', 23700496123, 'ligia buitrago', 'olmos', 3133583856, 'ligiaas@gmail.com', 'scrypt:32768:8:1$fNLlRCacTvOCEtGD$42f25d2b614ec68196e8b37b189a9ea0a077c483dc2771351f2309d3d9dbb92d80221345caf6e5156eb1723f09052c428fdcc4c23f918e69f9a52fad0cada46f', 'cliente', 'activo', '2025-04-02 20:44:25');
INSERT INTO `users` (`id`, `tipo_documento`, `documento`, `nombre`, `apellido`, `telefono`, `correo`, `contrasena`, `rol`, `estado`, `created_user`) VALUES (3, 'Cedula extranjeria', 12345678909, 'david leonardo ', 'cubides', 32144124448, 'davidleonardo05@gmail.com', 'scrypt:32768:8:1$RexrYmpObbhNdoUl$8f80f16e828f8b2efe2371529bb4c29199bb8abae524769817dd8e2cc7e1f612c6369d8375f6dca11ba48a676480a5b6a488581fe305ae7d60f6dc0a375583de', 'cliente', 'activo', '2025-04-02 21:57:39');
INSERT INTO `users` (`id`, `tipo_documento`, `documento`, `nombre`, `apellido`, `telefono`, `correo`, `contrasena`, `rol`, `estado`, `created_user`) VALUES (4, 'Cedula ciudadania', 1048847238, 'david olmitos', 'buitrago', 3187966329, 'davidolmoSs@gmail.com', 'scrypt:32768:8:1$zrLNwPJVW8cQNHu6$6857d1fe6a274b91c6c69ea709e1a601b5a9794c4c748f0f6ad322e32ff9039add8fc90b885c7891c4cf5574ddd18789d1c313674a698809565a2381c1d95032', 'cliente', 'activo', '2025-04-02 22:05:17');
INSERT INTO `users` (`id`, `tipo_documento`, `documento`, `nombre`, `apellido`, `telefono`, `correo`, `contrasena`, `rol`, `estado`, `created_user`) VALUES (5, 'Tarjeta identidad', 7878789090, 'sad', 'asdasd', 3214412545, 'asdasd23423@gmail.com', 'scrypt:32768:8:1$qCU8GkZ4KVvm1UQw$eda6578ecebe0c4e88f8c51c3504666edebe9502777e8c015c1b3afb1d57f2da72e47fb8072aff2069d51d059167980d50e823cb2475efa7762602eb56cf9fc1', 'cliente', 'activo', '2025-04-03 12:53:31');
INSERT INTO `users` (`id`, `tipo_documento`, `documento`, `nombre`, `apellido`, `telefono`, `correo`, `contrasena`, `rol`, `estado`, `created_user`) VALUES (6, 'Tarjeta identidad', 32144255667, 'dsaadawdsada', 'dsadsdasdasd', 231231235, 'sadasde312@gmail.com', 'scrypt:32768:8:1$TPOfDEwq5hyKKrmq$c3ecc385ae25fac1fc3293406fc53cdb56e354da36dc0bd2cf061f0bbc6290f41bee938ba6a08f52e21a1643064aa97c68a824a85f2b56027947223d8d9f1627', 'cliente', 'inactivo', '2025-04-03 14:45:28');

