-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 20-02-2025 a las 21:44:25
-- Versión del servidor: 8.0.30
-- Versión de PHP: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `crud_python`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `abono`
--

CREATE TABLE `abono` (
  `id` bigint UNSIGNED NOT NULL,
  `numero_abonos` enum('Pago inicial','Pago final') NOT NULL,
  `fecha` date NOT NULL,
  `estado` enum('Abono confirmado') NOT NULL,
  `pedido_id` bigint UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carrito_compras`
--

CREATE TABLE `carrito_compras` (
  `id` bigint UNSIGNED NOT NULL,
  `cantidad` int NOT NULL,
  `fecha_creacion` date NOT NULL,
  `producto_id` bigint UNSIGNED NOT NULL,
  `users_id` bigint UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `departamento`
--

CREATE TABLE `departamento` (
  `id` bigint UNSIGNED NOT NULL,
  `codigo` varchar(3) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `estado` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `departamento`
--

INSERT INTO `departamento` (`id`, `codigo`, `nombre`, `estado`) VALUES
(1, '05', 'Antioquia ', 1),
(2, '08', 'Atlántico ', 1),
(3, '11', 'Bogotá', 1),
(4, '13', 'Bolívar', 1),
(5, '15', 'Boyacá', 1),
(6, '17', 'Caldas', 1),
(7, '18', 'Caquetá', 1),
(8, '19', 'Cauca', 1),
(9, '20', 'Cesar', 1),
(10, '23', 'Córdoba', 1),
(11, '25', 'Cundinamarca', 1),
(12, '27', 'Chocó', 1),
(13, '41', 'Huila', 1),
(14, '44', 'La Guajira', 1),
(15, '47', 'Magdalena', 1),
(16, '50', 'Meta', 1),
(17, '52', 'Nariño', 1),
(18, '54', 'Norte de Santander', 1),
(19, '63', 'Quindío', 1),
(20, '66', 'Risaralda', 1),
(21, '68', 'Santander', 1),
(22, '70', 'Sucre', 1),
(23, '73', 'Tolima', 1),
(24, '76', 'Valle del Cauca', 1),
(25, '81', 'Arauca', 1),
(26, '85', 'Casanare', 1),
(27, '86', 'Putumayo', 1),
(28, '88', 'San Andrés y Providencia', 1),
(29, '91', 'Amazonas', 1),
(30, '94', 'Guainía', 1),
(31, '95', 'Guaviare', 1),
(32, '97', 'Vaupés', 1),
(33, '99', 'Vichada', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_pedido`
--

CREATE TABLE `detalle_pedido` (
  `id` bigint UNSIGNED NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `cantidad` bigint NOT NULL,
  `pedido_id` bigint UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `direccion`
--

CREATE TABLE `direccion` (
  `id` bigint UNSIGNED NOT NULL,
  `nombre_completo` varchar(160) NOT NULL,
  `barrio` text NOT NULL,
  `domicilio` text NOT NULL,
  `referencias` text,
  `telefono` varchar(15) NOT NULL,
  `estado` enum('Activo','Inactivo') NOT NULL,
  `costo_domicilio` bigint NOT NULL,
  `users_id` bigint UNSIGNED NOT NULL,
  `municipio_id` bigint NOT NULL,
  `departamento_id` bigint UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entrega`
--

CREATE TABLE `entrega` (
  `id` bigint UNSIGNED NOT NULL,
  `tipo` enum('Domicilio','Establecimiento fisico') NOT NULL,
  `fecha_hora` datetime NOT NULL,
  `estado` enum('Pendiente','En camino','Entregado') NOT NULL,
  `costo_domicilio` decimal(10,0) NOT NULL,
  `direccion_id` bigint UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `factura`
--

CREATE TABLE `factura` (
  `id` bigint UNSIGNED NOT NULL,
  `estado` enum('Pendiente','Facturado') NOT NULL,
  `fecha` date NOT NULL,
  `valor_total` decimal(10,0) NOT NULL,
  `pedido_id` bigint UNSIGNED NOT NULL,
  `metodo_pago_id` bigint UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario`
--

CREATE TABLE `inventario` (
  `id` bigint UNSIGNED NOT NULL,
  `cantidad_disponible` int NOT NULL,
  `fecha_actualizacion` date NOT NULL,
  `fecha_registro` datetime NOT NULL,
  `producto_id` bigint UNSIGNED NOT NULL,
  `users_id` bigint UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `metodo_pago`
--

CREATE TABLE `metodo_pago` (
  `id` bigint UNSIGNED NOT NULL,
  `metodo` enum('billeteras electrónicas','Cuenta bancaria','Efectivo') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `municipio`
--

CREATE TABLE `municipio` (
  `id` bigint NOT NULL,
  `codigo` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `nombre` varchar(80) NOT NULL,
  `departamento_id` varchar(3) NOT NULL,
  `estado` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `municipio`
--

INSERT INTO `municipio` (`id`, `codigo`, `nombre`, `departamento_id`, `estado`) VALUES
(1, '91001', 'LETICIA', '91', 1),
(2, '91263', 'EL ENCANTO', '91', 1),
(3, '91405', 'LA CHORRERA', '91', 1),
(4, '91407', 'LA PEDRERA', '91', 1),
(5, '91430', 'LA VICTORIA', '91', 1),
(6, '91460', 'MIRITÍ – PARANÁ', '91', 1),
(7, '91530', 'PUERTO ALEGRÍA', '91', 1),
(8, '91536', 'PUERTO ARICA', '91', 1),
(9, '91540', 'PUERTO NARIÑO', '91', 1),
(10, '91669', 'PUERTO SANTANDER', '91', 1),
(11, '91798', 'TARAPACÁ', '91', 1),
(12, '05001', 'MEDELLÍN', '05', 1),
(13, '05002', 'ABEJORRAL', '05', 1),
(14, '05004', 'ABRIAQUÍ', '05', 1),
(15, '05021', 'ALEJANDRÍA', '05', 1),
(16, '05030', 'AMAGÁ', '05', 1),
(17, '05031', 'AMALFI', '05', 1),
(18, '05034', 'ANDES', '05', 1),
(19, '05036', 'ANGELÓPOLIS', '05', 1),
(20, '05038', 'ANGOSTURA', '05', 1),
(21, '05040', 'ANORÍ', '05', 1),
(22, '05042', 'SANTA FÉ DE ANTIOQUIA', '05', 1),
(23, '05044', 'ANZÁ', '05', 1),
(24, '05045', 'APARTADÓ', '05', 1),
(25, '05051', 'ARBOLETES', '05', 1),
(26, '05055', 'ARGELIA', '05', 1),
(27, '05059', 'ARMENIA', '05', 1),
(28, '05079', 'BARBOSA', '05', 1),
(29, '05086', 'BELMIRA', '05', 1),
(30, '05088', 'BELLO', '05', 1),
(31, '05091', 'BETANIA', '05', 1),
(32, '05093', 'BETULIA', '05', 1),
(33, '05101', 'CIUDAD BOLÍVAR', '05', 1),
(34, '05107', 'BRICEÑO', '05', 1),
(35, '05113', 'BURITICÁ', '05', 1),
(36, '05120', 'CÁCERES', '05', 1),
(37, '05125', 'CAICEDO', '05', 1),
(38, '05129', 'CALDAS', '05', 1),
(39, '05134', 'CAMPAMENTO', '05', 1),
(40, '05138', 'CAÑASGORDAS', '05', 1),
(41, '05142', 'CARACOLÍ', '05', 1),
(42, '05145', 'CARAMANTA', '05', 1),
(43, '05147', 'CAREPA', '05', 1),
(44, '05148', 'EL CARMEN DE VIBORAL', '05', 1),
(45, '05150', 'CAROLINA', '05', 1),
(46, '05154', 'CAUCASIA', '05', 1),
(47, '05172', 'CHIGORODÓ', '05', 1),
(48, '05190', 'CISNEROS', '05', 1),
(49, '05197', 'COCORNÁ', '05', 1),
(50, '05206', 'CONCEPCIÓN', '05', 1),
(51, '05209', 'CONCORDIA', '05', 1),
(52, '05212', 'COPACABANA', '05', 1),
(53, '05234', 'DABEIBA', '05', 1),
(54, '05237', 'DONMATÍAS', '05', 1),
(55, '05240', 'EBÉJICO', '05', 1),
(56, '05250', 'EL BAGRE', '05', 1),
(57, '05264', 'ENTRERRÍOS', '05', 1),
(58, '05266', 'ENVIGADO', '05', 1),
(59, '05282', 'FREDONIA', '05', 1),
(60, '05284', 'FRONTINO', '05', 1),
(61, '05306', 'GIRALDO', '05', 1),
(62, '05308', 'GIRARDOTA', '05', 1),
(63, '05310', 'GÓMEZ PLATA', '05', 1),
(64, '05313', 'GRANADA', '05', 1),
(65, '05315', 'GUADALUPE', '05', 1),
(66, '05318', 'GUARNE', '05', 1),
(67, '05321', 'GUATAPÉ', '05', 1),
(68, '05347', 'HELICONIA', '05', 1),
(69, '05353', 'HISPANIA', '05', 1),
(70, '05360', 'ITAGÜÍ', '05', 1),
(71, '05361', 'ITUANGO', '05', 1),
(72, '05364', 'JARDÍN', '05', 1),
(73, '05368', 'JERICÓ', '05', 1),
(74, '05376', 'LA CEJA', '05', 1),
(75, '05380', 'LA ESTRELLA', '05', 1),
(76, '05390', 'LA PINTADA', '05', 1),
(77, '05400', 'LA UNIÓN', '05', 1),
(78, '05411', 'LIBORINA', '05', 1),
(79, '05425', 'MACEO', '05', 1),
(80, '05440', 'MARINILLA', '05', 1),
(81, '05467', 'MONTEBELLO', '05', 1),
(82, '05475', 'MURINDÓ', '05', 1),
(83, '05480', 'MUTATÁ', '05', 1),
(84, '05483', 'NARIÑO', '05', 1),
(85, '05490', 'NECOCLÍ', '05', 1),
(86, '05495', 'NECHÍ', '05', 1),
(87, '05501', 'OLAYA', '05', 1),
(88, '05541', 'PEÑOL', '05', 1),
(89, '05543', 'PEQUE', '05', 1),
(90, '05576', 'PUEBLORRICO', '05', 1),
(91, '05579', 'PUERTO BERRÍO', '05', 1),
(92, '05585', 'PUERTO NARE', '05', 1),
(93, '05591', 'PUERTO TRIUNFO', '05', 1),
(94, '05604', 'REMEDIOS', '05', 1),
(95, '05607', 'RETIRO', '05', 1),
(96, '05615', 'RIONEGRO', '05', 1),
(97, '05628', 'SABANALARGA', '05', 1),
(98, '05631', 'SABANETA', '05', 1),
(99, '05642', 'SALGAR', '05', 1),
(100, '05647', 'SAN ANDRÉS DE CUERQUÍA', '05', 1),
(101, '05649', 'SAN CARLOS', '05', 1),
(102, '05652', 'SAN FRANCISCO', '05', 1),
(103, '05656', 'SAN JERÓNIMO', '05', 1),
(104, '05658', 'SAN JOSÉ DE LA MONTAÑA', '05', 1),
(105, '05659', 'SAN JUAN DE URABÁ', '05', 1),
(106, '05660', 'SAN LUIS', '05', 1),
(107, '05664', 'SAN PEDRO DE LOS MILAGROS', '05', 1),
(108, '05665', 'SAN PEDRO DE URABÁ', '05', 1),
(109, '05667', 'SAN RAFAEL', '05', 1),
(110, '05670', 'SAN ROQUE', '05', 1),
(111, '05674', 'SAN VICENTE FERRER', '05', 1),
(112, '05679', 'SANTA BÁRBARA', '05', 1),
(113, '05686', 'SANTA ROSA DE OSOS', '05', 1),
(114, '05690', 'SANTO DOMINGO', '05', 1),
(115, '05697', 'EL SANTUARIO', '05', 1),
(116, '05736', 'SEGOVIA', '05', 1),
(117, '05756', 'SONSÓN', '05', 1),
(118, '05761', 'SOPETRÁN', '05', 1),
(119, '05789', 'TÁMESIS', '05', 1),
(120, '05790', 'TARAZÁ', '05', 1),
(121, '05792', 'TARSO', '05', 1),
(122, '05809', 'TITIRIBÍ', '05', 1),
(123, '05819', 'TOLEDO', '05', 1),
(124, '05837', 'TURBO', '05', 1),
(125, '05842', 'URAMITA', '05', 1),
(126, '05847', 'URRAO', '05', 1),
(127, '05854', 'VALDIVIA', '05', 1),
(128, '05856', 'VALPARAÍSO', '05', 1),
(129, '05858', 'VEGACHÍ', '05', 1),
(130, '05861', 'VENECIA', '05', 1),
(131, '05873', 'VIGÍA DEL FUERTE', '05', 1),
(132, '05885', 'YALÍ', '05', 1),
(133, '05887', 'YARUMAL', '05', 1),
(134, '05890', 'YOLOMBÓ', '05', 1),
(135, '05893', 'YONDÓ', '05', 1),
(136, '05895', 'ZARAGOZA', '05', 1),
(137, '05861', 'VENECIA', '05', 1),
(138, '81001', 'ARAUCA', '81', 1),
(139, '81065', 'ARAUQUITA', '81', 1),
(140, '81220', 'CRAVO NORTE', '81', 1),
(141, '81300', 'FORTUL', '81', 1),
(142, '81591', 'PUERTO RONDÓN', '81', 1),
(143, '81736', 'SARAVENA', '81', 1),
(144, '81794', 'TAME', '81', 1),
(145, '88001', 'SAN ANDRÉS', '88', 1),
(146, '88564', 'PROVIDENCIA', '88', 1),
(147, '08001', 'BARRANQUILLA', '08', 1),
(148, '08078', 'BARANOA', '08', 1),
(149, '08137', 'CAMPO DE LA CRUZ', '08', 1),
(150, '08141', 'CANDELARIA', '08', 1),
(151, '08296', 'GALAPA', '08', 1),
(152, '08372', 'JUAN DE ACOSTA', '08', 1),
(153, '08421', 'LURUACO', '08', 1),
(154, '08433', 'MALAMBO', '08', 1),
(155, '08436', 'MANATÍ', '08', 1),
(156, '08520', 'PALMAR DE VARELA', '08', 1),
(157, '08549', 'PIOJÓ', '08', 1),
(158, '08558', 'POLONUEVO', '08', 1),
(159, '08560', 'PONEDERA', '08', 1),
(160, '08573', 'PUERTO COLOMBIA', '08', 1),
(161, '08606', 'REPELÓN', '08', 1),
(162, '08634', 'SABANAGRANDE', '08', 1),
(163, '08638', 'SABANALARGA', '08', 1),
(164, '08675', 'SANTA LUCÍA', '08', 1),
(165, '08685', 'SANTO TOMÁS', '08', 1),
(166, '08758', 'SOLEDAD', '08', 1),
(167, '08770', 'SUAN', '08', 1),
(168, '08832', 'TUBARÁ', '08', 1),
(169, '08849', 'USIACURÍ', '08', 1),
(170, '11001', 'BOGOTÁ, D.C.', '11', 1),
(171, '13001', 'CARTAGENA DE INDIAS', '13', 1),
(172, '13006', 'ACHÍ', '13', 1),
(173, '13030', 'ALTOS DEL ROSARIO', '13', 1),
(174, '13042', 'ARENAL', '13', 1),
(175, '13052', 'ARJONA', '13', 1),
(176, '13062', 'ARROYOHONDO', '13', 1),
(177, '13074', 'BARRANCO DE LOBA', '13', 1),
(178, '13140', 'CALAMAR', '13', 1),
(179, '13160', 'CANTAGALLO', '13', 1),
(180, '13188', 'CICUCO', '13', 1),
(181, '13212', 'CÓRDOBA', '13', 1),
(182, '13222', 'CLEMENCIA', '13', 1),
(183, '13244', 'EL CARMEN DE BOLÍVAR', '13', 1),
(184, '13248', 'EL GUAMO', '13', 1),
(185, '13268', 'EL PEÑÓN', '13', 1),
(186, '13300', 'HATILLO DE LOBA', '13', 1),
(187, '13430', 'MAGANGUÉ', '13', 1),
(188, '13433', 'MAHATES', '13', 1),
(189, '13440', 'MARGARITA', '13', 1),
(190, '13442', 'MARÍA LA BAJA', '13', 1),
(191, '13458', 'MONTECRISTO', '13', 1),
(192, '13468', 'MOMPÓS', '13', 1),
(193, '13473', 'MORALES', '13', 1),
(194, '13490', 'NOROSÍ', '13', 1),
(195, '13549', 'PINILLOS', '13', 1),
(196, '13580', 'REGIDOR', '13', 1),
(197, '13600', 'RÍO VIEJO', '13', 1),
(198, '13620', 'SAN CRISTÓBAL', '13', 1),
(199, '13647', 'SAN ESTANISLAO', '13', 1),
(200, '13650', 'SAN FERNANDO', '13', 1),
(201, '13654', 'SAN JACINTO', '13', 1),
(202, '13655', 'SAN JACINTO DEL CAUCA', '13', 1),
(203, '13657', 'SAN JUAN NEPOMUCENO', '13', 1),
(204, '13667', 'SAN MARTÍN DE LOBA', '13', 1),
(205, '13670', 'SAN PABLO SUR', '13', 1),
(206, '13673', 'SANTA CATALINA', '13', 1),
(207, '13683', 'SANTA ROSA DE LIMA', '13', 1),
(208, '13688', 'SANTA ROSA DEL SUR', '13', 1),
(209, '13744', 'SIMITÍ', '13', 1),
(210, '13760', 'SOPLAVIENTO', '13', 1),
(211, '13780', 'TALAIGUA NUEVO', '13', 1),
(212, '13810', 'TIQUISIO', '13', 1),
(213, '13836', 'TURBACO', '13', 1),
(214, '13838', 'TURBANÁ', '13', 1),
(215, '13873', 'VILLANUEVA', '13', 1),
(216, '13894', 'ZAMBRANO', '13', 1),
(217, '15001', 'TUNJA', '15', 1),
(218, '15022', 'ALMEIDA', '15', 1),
(219, '15047', 'AQUITANIA', '15', 1),
(220, '15051', 'ARCABUCO', '15', 1),
(221, '15087', 'BELÉN', '15', 1),
(222, '15090', 'BERBEO', '15', 1),
(223, '15092', 'BETÉITIVA', '15', 1),
(224, '15097', 'BOAVITA', '15', 1),
(225, '15104', 'BOYACÁ', '15', 1),
(226, '15106', 'BRICEÑO', '15', 1),
(227, '15109', 'BUENAVISTA', '15', 1),
(228, '15114', 'BUSBANZÁ', '15', 1),
(229, '15131', 'CALDAS', '15', 1),
(230, '15135', 'CAMPOHERMOSO', '15', 1),
(231, '15162', 'CERINZA', '15', 1),
(232, '15172', 'CHINAVITA', '15', 1),
(233, '15176', 'CHIQUINQUIRÁ', '15', 1),
(234, '15180', 'CHISCAS', '15', 1),
(235, '15183', 'CHITA', '15', 1),
(236, '15185', 'CHITARAQUE', '15', 1),
(237, '15187', 'CHIVATÁ', '15', 1),
(238, '15189', 'CIÉNEGA', '15', 1),
(239, '15204', 'CÓMBITA', '15', 1),
(240, '15212', 'COPER', '15', 1),
(241, '15215', 'CORRALES', '15', 1),
(242, '15218', 'COVARACHÍA', '15', 1),
(243, '15223', 'CUBARÁ', '15', 1),
(244, '15224', 'CUCAITA', '15', 1),
(245, '15226', 'CUÍTIVA', '15', 1),
(246, '15232', 'CHÍQUIZA', '15', 1),
(247, '15236', 'CHIVOR', '15', 1),
(248, '15238', 'DUITAMA', '15', 1),
(249, '15244', 'EL COCUY', '15', 1),
(250, '15248', 'EL ESPINO', '15', 1),
(251, '15272', 'FIRAVITOBA', '15', 1),
(252, '15276', 'FLORESTA', '15', 1),
(253, '15293', 'GACHANTIVÁ', '15', 1),
(254, '15296', 'GÁMEZA', '15', 1),
(255, '15299', 'GARAGOA', '15', 1),
(256, '15317', 'GUACAMAYAS', '15', 1),
(257, '15322', 'GUATEQUE', '15', 1),
(258, '15325', 'GUAYATÁ', '15', 1),
(259, '15332', 'GÜICÁN DE LA SIERRA', '15', 1),
(260, '15362', 'IZA', '15', 1),
(261, '15367', 'JENESANO', '15', 1),
(262, '15368', 'JERICÓ', '15', 1),
(263, '15377', 'LABRANZAGRANDE', '15', 1),
(264, '15380', 'LA CAPILLA', '15', 1),
(265, '15401', 'LA VICTORIA', '15', 1),
(266, '15403', 'LA UVITA', '15', 1),
(267, '15407', 'VILLA DE LEYVA', '15', 1),
(268, '15425', 'MACANAL', '15', 1),
(269, '15442', 'MARIPÍ', '15', 1),
(270, '15455', 'MIRAFLORES', '15', 1),
(271, '15464', 'MONGUA', '15', 1),
(272, '15466', 'MONGUÍ', '15', 1),
(273, '15469', 'MONIQUIRÁ', '15', 1),
(274, '15476', 'MOTAVITA', '15', 1),
(275, '15480', 'MUZO', '15', 1),
(276, '15491', 'NOBSA', '15', 1),
(277, '15494', 'NUEVO COLÓN', '15', 1),
(278, '15500', 'OICATÁ', '15', 1),
(279, '15507', 'OTANCHE', '15', 1),
(280, '15511', 'PACHAVITA', '15', 1),
(281, '15514', 'PÁEZ', '15', 1),
(282, '15516', 'PAIPA', '15', 1),
(283, '15518', 'PAJARITO', '15', 1),
(284, '15522', 'PANQUEBA', '15', 1),
(285, '15531', 'PAUNA', '15', 1),
(286, '15533', 'PAYA', '15', 1),
(287, '15537', 'PAZ DE RÍO', '15', 1),
(288, '15542', 'PESCA', '15', 1),
(289, '15550', 'PISBA', '15', 1),
(290, '15572', 'PUERTO BOYACÁ', '15', 1),
(291, '15580', 'QUÍPAMA', '15', 1),
(292, '15599', 'RAMIRIQUÍ', '15', 1),
(293, '15600', 'RÁQUIRA', '15', 1),
(294, '15621', 'RONDÓN', '15', 1),
(295, '15632', 'SABOYÁ', '15', 1),
(296, '15638', 'SÁCHICA', '15', 1),
(297, '15646', 'SAMACÁ', '15', 1),
(298, '15660', 'SAN EDUARDO', '15', 1),
(299, '15664', 'SAN JOSÉ DE PARE', '15', 1),
(300, '15667', 'SAN LUIS DE GACENO', '15', 1),
(301, '15673', 'SAN MATEO', '15', 1),
(302, '15676', 'SAN MIGUEL DE SEMA', '15', 1),
(303, '15681', 'SAN PABLO DE BORBUR', '15', 1),
(304, '15686', 'SANTANA', '15', 1),
(305, '15690', 'SANTA MARÍA', '15', 1),
(306, '15693', 'SANTA ROSA DE VITERBO', '15', 1),
(307, '15696', 'SANTA SOFÍA', '15', 1),
(308, '15720', 'SATIVANORTE', '15', 1),
(309, '15723', 'SATIVASUR', '15', 1),
(310, '15740', 'SIACHOQUE', '15', 1),
(311, '15753', 'SOATÁ', '15', 1),
(312, '15755', 'SOCOTÁ', '15', 1),
(313, '15757', 'SOCHA', '15', 1),
(314, '15759', 'SOGAMOSO', '15', 1),
(315, '15761', 'SOMONDOCO', '15', 1),
(316, '15762', 'SORA', '15', 1),
(317, '15763', 'SOTAQUIRÁ', '15', 1),
(318, '15764', 'SORACÁ', '15', 1),
(319, '15774', 'SUSACÓN', '15', 1),
(320, '15776', 'SUTAMARCHÁN', '15', 1),
(321, '15778', 'SUTATENZA', '15', 1),
(322, '15790', 'TASCO', '15', 1),
(323, '15798', 'TENZA', '15', 1),
(324, '15804', 'TIBANÁ', '15', 1),
(325, '15806', 'TIBASOSA', '15', 1),
(326, '15808', 'TINJACÁ', '15', 1),
(327, '15810', 'TIPACOQUE', '15', 1),
(328, '15814', 'TOCA', '15', 1),
(329, '15816', 'TOGÜÍ', '15', 1),
(330, '15820', 'TÓPAGA', '15', 1),
(331, '15822', 'TOTA', '15', 1),
(332, '15832', 'TUNUNGUÁ', '15', 1),
(333, '15835', 'TURMEQUÉ', '15', 1),
(334, '15837', 'TUTA', '15', 1),
(335, '15839', 'TUTAZÁ', '15', 1),
(336, '15842', 'ÚMBITA', '15', 1),
(337, '15861', 'VENTAQUEMADA', '15', 1),
(338, '15879', 'VIRACACHÁ', '15', 1),
(339, '15897', 'ZETAQUIRA', '15', 1),
(340, '17001', 'MANIZALES', '17', 1),
(341, '17013', 'AGUADAS', '17', 1),
(342, '17042', 'ANSERMA', '17', 1),
(343, '17050', 'ARANZAZU', '17', 1),
(344, '17088', 'BELALCÁZAR', '17', 1),
(345, '17174', 'CHINCHINÁ', '17', 1),
(346, '17272', 'FILADELFIA', '17', 1),
(347, '17380', 'LA DORADA', '17', 1),
(348, '17388', 'LA MERCED', '17', 1),
(349, '17433', 'MANZANARES', '17', 1),
(350, '17442', 'MARMATO', '17', 1),
(351, '17444', 'MARQUETALIA', '17', 1),
(352, '17446', 'MARULANDA', '17', 1),
(353, '17486', 'NEIRA', '17', 1),
(354, '17495', 'NORCASIA', '17', 1),
(355, '17513', 'PÁCORA', '17', 1),
(356, '17524', 'PALESTINA', '17', 1),
(357, '17541', 'PENSILVANIA', '17', 1),
(358, '17614', 'RIOSUCIO', '17', 1),
(359, '17616', 'RISARALDA', '17', 1),
(360, '17653', 'SALAMINA', '17', 1),
(361, '17662', 'SAMANÁ', '17', 1),
(362, '17665', 'SAN JOSÉ', '17', 1),
(363, '17777', 'SUPÍA', '17', 1),
(364, '17867', 'VICTORIA', '17', 1),
(365, '17873', 'VILLAMARÍA', '17', 1),
(366, '17877', 'VITERBO', '17', 1),
(367, '18001', 'FLORENCIA', '18', 1),
(368, '18029', 'ALBANIA', '18', 1),
(369, '18094', 'BELÉN DE LOS ANDAQUÍES', '18', 1),
(370, '18150', 'CARTAGENA DEL CHAIRÁ', '18', 1),
(371, '18205', 'CURILLO', '18', 1),
(372, '18247', 'EL DONCELLO', '18', 1),
(373, '18256', 'EL PAUJÍL', '18', 1),
(374, '18410', 'LA MONTAÑITA', '18', 1),
(375, '18460', 'MILÁN', '18', 1),
(376, '18479', 'MORELIA', '18', 1),
(377, '18592', 'PUERTO RICO', '18', 1),
(378, '18610', 'SAN JOSÉ DEL FRAGUA', '18', 1),
(379, '18753', 'SAN VICENTE DEL CAGUÁN', '18', 1),
(380, '18756', 'SOLANO', '18', 1),
(381, '18785', 'SOLITA', '18', 1),
(382, '18860', 'VALPARAÍSO', '18', 1),
(383, '85001', 'YOPAL', '85', 1),
(384, '85010', 'AGUAZUL', '85', 1),
(385, '85015', 'CHÁMEZA', '85', 1),
(386, '85125', 'HATO COROZAL', '85', 1),
(387, '85136', 'LA SALINA', '85', 1),
(388, '85139', 'MANÍ', '85', 1),
(389, '85162', 'MONTERREY', '85', 1),
(390, '85225', 'NUNCHÍA', '85', 1),
(391, '85230', 'OROCUÉ', '85', 1),
(392, '85250', 'PAZ DE ARIPORO', '85', 1),
(393, '85263', 'PORE', '85', 1),
(394, '85279', 'RECETOR', '85', 1),
(395, '85300', 'SABANALARGA', '85', 1),
(396, '85315', 'SÁCAMA', '85', 1),
(397, '85325', 'SAN LUIS DE PALENQUE', '85', 1),
(398, '85400', 'TÁMARA', '85', 1),
(399, '85410', 'TAURAMENA', '85', 1),
(400, '85430', 'TRINIDAD', '85', 1),
(401, '85440', 'VILLANUEVA', '85', 1),
(402, '19001', 'POPAYÁN', '19', 1),
(403, '19022', 'ALMAGUER', '19', 1),
(404, '19050', 'ARGELIA', '19', 1),
(405, '19075', 'BALBOA', '19', 1),
(406, '19100', 'BOLÍVAR', '19', 1),
(407, '19110', 'BUENOS AIRES', '19', 1),
(408, '19130', 'CAJIBÍO', '19', 1),
(409, '19137', 'CALDONO', '19', 1),
(410, '19142', 'CALOTO', '19', 1),
(411, '19212', 'CORINTO', '19', 1),
(412, '19256', 'EL TAMBO', '19', 1),
(413, '19290', 'FLORENCIA', '19', 1),
(414, '19300', 'GUACHENÉ', '19', 1),
(415, '19318', 'GUAPÍ', '19', 1),
(416, '19355', 'INZÁ', '19', 1),
(417, '19364', 'JAMBALÓ', '19', 1),
(418, '19392', 'LA SIERRA', '19', 1),
(419, '19397', 'LA VEGA', '19', 1),
(420, '19418', 'LÓPEZ DE MICAY', '19', 1),
(421, '19450', 'MERCADERES', '19', 1),
(422, '19455', 'MIRANDA', '19', 1),
(423, '19473', 'MORALES', '19', 1),
(424, '19513', 'PADILLA', '19', 1),
(425, '19517', 'PÁEZ - BELALCAZAR', '19', 1),
(426, '19532', 'PATÍA – EL BORDO', '19', 1),
(427, '19533', 'PIAMONTE', '19', 1),
(428, '19548', 'PIENDAMÓ – TUNÍA', '19', 1),
(429, '19573', 'PUERTO TEJADA', '19', 1),
(430, '19585', 'PURACÉ - COCONUCO', '19', 1),
(431, '19622', 'ROSAS', '19', 1),
(432, '19693', 'SAN SEBASTIÁN', '19', 1),
(433, '19698', 'SANTANDER DE QUILICHAO', '19', 1),
(434, '19701', 'SANTA ROSA', '19', 1),
(435, '19743', 'SILVIA', '19', 1),
(436, '19760', 'SOTARA', '19', 1),
(437, '19780', 'SUÁREZ', '19', 1),
(438, '19785', 'SUCRE', '19', 1),
(439, '19807', 'TIMBÍO', '19', 1),
(440, '19809', 'TIMBIQUÍ', '19', 1),
(441, '19821', 'TORIBÍO', '19', 1),
(442, '19824', 'TOTORÓ', '19', 1),
(443, '19845', 'VILLA RICA', '19', 1),
(444, '20001', 'VALLEDUPAR', '20', 1),
(445, '20011', 'AGUACHICA', '20', 1),
(446, '20013', 'AGUSTÍN CODAZZI', '20', 1),
(447, '20032', 'ASTREA', '20', 1),
(448, '20045', 'BECERRIL', '20', 1),
(449, '20060', 'BOSCONIA', '20', 1),
(450, '20175', 'CHIMICHAGUA', '20', 1),
(451, '20178', 'CHIRIGUANÁ', '20', 1),
(452, '20228', 'CURUMANÍ', '20', 1),
(453, '20238', 'EL COPEY', '20', 1),
(454, '20250', 'EL PASO', '20', 1),
(455, '20295', 'GAMARRA', '20', 1),
(456, '20310', 'GONZÁLEZ', '20', 1),
(457, '20383', 'LA GLORIA', '20', 1),
(458, '20400', 'LA JAGUA DE IBIRICO', '20', 1),
(459, '20443', 'MANAURE BALCÓN DEL CESAR', '20', 1),
(460, '20517', 'PAILITAS', '20', 1),
(461, '20550', 'PELAYA', '20', 1),
(462, '20570', 'PUEBLO BELLO', '20', 1),
(463, '20614', 'RÍO DE ORO', '20', 1),
(464, '20621', 'LA PAZ', '20', 1),
(465, '20710', 'SAN ALBERTO', '20', 1),
(466, '20750', 'SAN DIEGO', '20', 1),
(467, '20770', 'SAN MARTÍN', '20', 1),
(468, '20787', 'TAMALAMEQUE', '20', 1),
(469, '27001', 'QUIBDÓ', '27', 1),
(470, '27006', 'ACANDÍ', '27', 1),
(471, '27025', 'ALTO BAUDÓ (PIE DE PATÓ)', '27', 1),
(472, '27050', 'ATRATO (YUTO)', '27', 1),
(473, '27073', 'BAGADÓ', '27', 1),
(474, '27075', 'BAHÍA SOLANO (MUTIS)', '27', 1),
(475, '27077', 'BAJO BAUDÓ (PIZARRO)', '27', 1),
(476, '27099', 'BOJAYÁ (BELLA VISTA)', '27', 1),
(477, '27135', 'EL CANTÓN DEL SAN PABLO', '27', 1),
(478, '27150', 'CARMEN DEL DARIÉN', '27', 1),
(479, '27160', 'CÉRTEGUI', '27', 1),
(480, '27205', 'CONDOTO', '27', 1),
(481, '27245', 'EL CARMEN DE ATRATO', '27', 1),
(482, '27250', 'EL LITORAL DEL SAN JUAN', '27', 1),
(483, '27361', 'ISTMINA', '27', 1),
(484, '27372', 'JURADÓ', '27', 1),
(485, '27413', 'LLORÓ', '27', 1),
(486, '27425', 'MEDIO ATRATO (BETÉ)', '27', 1),
(487, '27430', 'MEDIO BAUDÓ', '27', 1),
(488, '27450', 'MEDIO SAN JUAN (ANDAGOYA)', '27', 1),
(489, '27491', 'NÓVITA', '27', 1),
(490, '27495', 'NUQUÍ', '27', 1),
(491, '27580', 'RÍO IRÓ (SANTA RITA)', '27', 1),
(492, '27600', 'RÍO QUITO (PAIMADÓ)', '27', 1),
(493, '27615', 'RIOSUCIO', '27', 1),
(494, '27660', 'SAN JOSÉ DEL PALMAR', '27', 1),
(495, '27745', 'SIPÍ', '27', 1),
(496, '27787', 'TADÓ', '27', 1),
(497, '27800', 'UNGUÍA', '27', 1),
(498, '27810', 'UNIÓN PANAMERICANA (LAS ÁNIMAS)', '27', 1),
(499, '23001', 'MONTERÍA', '23', 1),
(500, '23068', 'AYAPEL', '23', 1),
(501, '23079', 'BUENAVISTA', '23', 1),
(502, '23090', 'CANALETE', '23', 1),
(503, '23162', 'CERETÉ', '23', 1),
(504, '23168', 'CHIMÁ', '23', 1),
(505, '23182', 'CHINÚ', '23', 1),
(506, '23189', 'CIÉNAGA DE ORO', '23', 1),
(507, '23300', 'COTORRA', '23', 1),
(508, '23350', 'LA APARTADA', '23', 1),
(509, '23417', 'LORICA', '23', 1),
(510, '23419', 'LOS CÓRDOBAS', '23', 1),
(511, '23464', 'MOMIL', '23', 1),
(512, '23466', 'MONTELÍBANO', '23', 1),
(513, '23500', 'MOÑITOS', '23', 1),
(514, '23555', 'PLANETA RICA', '23', 1),
(515, '23570', 'PUEBLO NUEVO', '23', 1),
(516, '23574', 'PUERTO ESCONDIDO', '23', 1),
(517, '23580', 'PUERTO LIBERTADOR', '23', 1),
(518, '23586', 'PURÍSIMA DE LA CONCEPCIÓN', '23', 1),
(519, '23660', 'SAHAGÚN', '23', 1),
(520, '23670', 'SAN ANDRÉS DE SOTAVENTO', '23', 1),
(521, '23672', 'SAN ANTERO', '23', 1),
(522, '23675', 'SAN BERNARDO DEL VIENTO', '23', 1),
(523, '23678', 'SAN CARLOS', '23', 1),
(524, '23682', 'SAN JOSÉ DE URÉ', '23', 1),
(525, '23686', 'SAN PELAYO', '23', 1),
(526, '23807', 'TIERRALTA', '23', 1),
(527, '23815', 'TUCHÍN', '23', 1),
(528, '23855', 'VALENCIA', '23', 1),
(529, '25001', 'AGUA DE DIOS', '25', 1),
(530, '25019', 'ALBÁN', '25', 1),
(531, '25035', 'ANAPOIMA', '25', 1),
(532, '25040', 'ANOLAIMA', '25', 1),
(533, '25053', 'ARBELÁEZ', '25', 1),
(534, '25086', 'BELTRÁN', '25', 1),
(535, '25095', 'BITUIMA', '25', 1),
(536, '25099', 'BOJACÁ', '25', 1),
(537, '25120', 'CABRERA', '25', 1),
(538, '25123', 'CACHIPAY', '25', 1),
(539, '25126', 'CAJICÁ', '25', 1),
(540, '25148', 'CAPARRAPÍ', '25', 1),
(541, '25151', 'CÁQUEZA', '25', 1),
(542, '25154', 'CARMEN DE CARUPA', '25', 1),
(543, '25168', 'CHAGUANÍ', '25', 1),
(544, '25175', 'CHÍA', '25', 1),
(545, '25178', 'CHIPAQUE', '25', 1),
(546, '25181', 'CHOACHÍ', '25', 1),
(547, '25183', 'CHOCONTÁ', '25', 1),
(548, '25200', 'COGUA', '25', 1),
(549, '25214', 'COTA', '25', 1),
(550, '25224', 'CUCUNUBÁ', '25', 1),
(551, '25245', 'EL COLEGIO', '25', 1),
(552, '25258', 'EL PEÑÓN', '25', 1),
(553, '25260', 'EL ROSAL', '25', 1),
(554, '25269', 'FACATATIVÁ', '25', 1),
(555, '25279', 'FÓMEQUE', '25', 1),
(556, '25281', 'FOSCA', '25', 1),
(557, '25286', 'FUNZA', '25', 1),
(558, '25288', 'FÚQUENE', '25', 1),
(559, '25290', 'FUSAGASUGÁ', '25', 1),
(560, '25293', 'GACHALÁ', '25', 1),
(561, '25295', 'GACHANCIPÁ', '25', 1),
(562, '25297', 'GACHETÁ', '25', 1),
(563, '25299', 'GAMA', '25', 1),
(564, '25307', 'GIRARDOT', '25', 1),
(565, '25312', 'GRANADA', '25', 1),
(566, '25317', 'GUACHETÁ', '25', 1),
(567, '25320', 'GUADUAS', '25', 1),
(568, '25322', 'GUASCA', '25', 1),
(569, '25324', 'GUATAQUÍ', '25', 1),
(570, '25326', 'GUATAVITA', '25', 1),
(571, '25328', 'GUAYABAL DE SÍQUIMA', '25', 1),
(572, '25335', 'GUAYABETAL', '25', 1),
(573, '25339', 'GUTIÉRREZ', '25', 1),
(574, '25368', 'JERUSALÉN', '25', 1),
(575, '25372', 'JUNÍN', '25', 1),
(576, '25377', 'LA CALERA', '25', 1),
(577, '25386', 'LA MESA', '25', 1),
(578, '25394', 'LA PALMA', '25', 1),
(579, '25398', 'LA PEÑA', '25', 1),
(580, '25402', 'LA VEGA', '25', 1),
(581, '25407', 'LENGUAZAQUE', '25', 1),
(582, '25426', 'MACHETÁ', '25', 1),
(583, '25430', 'MADRID', '25', 1),
(584, '25436', 'MANTA', '25', 1),
(585, '25438', 'MEDINA', '25', 1),
(586, '25473', 'MOSQUERA', '25', 1),
(587, '25483', 'NARIÑO', '25', 1),
(588, '25486', 'NEMOCÓN', '25', 1),
(589, '25488', 'NILO', '25', 1),
(590, '25489', 'NIMAIMA', '25', 1),
(591, '25491', 'NOCAIMA', '25', 1),
(592, '25506', 'VENECIA', '25', 1),
(593, '25513', 'PACHO', '25', 1),
(594, '25518', 'PAIME', '25', 1),
(595, '25524', 'PANDI', '25', 1),
(596, '25530', 'PARATEBUENO', '25', 1),
(597, '25535', 'PASCA', '25', 1),
(598, '25572', 'PUERTO SALGAR', '25', 1),
(599, '25580', 'PULÍ', '25', 1),
(600, '25592', 'QUEBRADANEGRA', '25', 1),
(601, '25594', 'QUETAME', '25', 1),
(602, '25596', 'QUIPILE', '25', 1),
(603, '25599', 'APULO', '25', 1),
(604, '25612', 'RICAURTE', '25', 1),
(605, '25645', 'SAN ANTONIO DEL TEQUENDAMA', '25', 1),
(606, '25649', 'SAN BERNARDO', '25', 1),
(607, '25653', 'SAN CAYETANO', '25', 1),
(608, '25658', 'SAN FRANCISCO', '25', 1),
(609, '25662', 'SAN JUAN DE RIOSECO', '25', 1),
(610, '25718', 'SASAIMA', '25', 1),
(611, '25736', 'SESQUILÉ', '25', 1),
(612, '25740', 'SIBATÉ', '25', 1),
(613, '25743', 'SILVANIA', '25', 1),
(614, '25745', 'SIMIJACA', '25', 1),
(615, '25754', 'SOACHA', '25', 1),
(616, '25758', 'SOPÓ', '25', 1),
(617, '25769', 'SUBACHOQUE', '25', 1),
(618, '25772', 'SUESCA', '25', 1),
(619, '25777', 'SUPATÁ', '25', 1),
(620, '25779', 'SUSA', '25', 1),
(621, '25781', 'SUTATAUSA', '25', 1),
(622, '25785', 'TABIO', '25', 1),
(623, '25793', 'TAUSA', '25', 1),
(624, '25797', 'TENA', '25', 1),
(625, '25799', 'TENJO', '25', 1),
(626, '25805', 'TIBACUY', '25', 1),
(627, '25807', 'TIBIRITA', '25', 1),
(628, '25815', 'TOCAIMA', '25', 1),
(629, '25817', 'TOCANCIPÁ', '25', 1),
(630, '25823', 'TOPAIPÍ', '25', 1),
(631, '25839', 'UBALÁ', '25', 1),
(632, '25841', 'UBAQUE', '25', 1),
(633, '25843', 'VILLA DE SAN DIEGO DE UBATÉ', '25', 1),
(634, '25845', 'UNE', '25', 1),
(635, '25851', 'ÚTICA', '25', 1),
(636, '25862', 'VERGARA', '25', 1),
(637, '25867', 'VIANÍ', '25', 1),
(638, '25871', 'VILLAGÓMEZ', '25', 1),
(639, '25873', 'VILLAPINZÓN', '25', 1),
(640, '25875', 'VILLETA', '25', 1),
(641, '25878', 'VIOTÁ', '25', 1),
(642, '25885', 'YACOPÍ', '25', 1),
(643, '25898', 'ZIPACÓN', '25', 1),
(644, '25899', 'ZIPAQUIRÁ', '25', 1),
(645, '94001', 'INÍRIDA', '94', 1),
(646, '94343', 'BARRANCOMINAS', '94', 1),
(647, '94663', 'MAPIRIPANA', '94', 1),
(648, '94883', 'SAN FELIPE', '94', 1),
(649, '94884', 'PUERTO COLOMBIA', '94', 1),
(650, '94885', 'LA GUADALUPE', '94', 1),
(651, '94886', 'CACAHUAL', '94', 1),
(652, '94887', 'PANA PANA', '94', 1),
(653, '94888', 'MORICHAL NUEVO', '94', 1),
(654, '95001', 'SAN JOSÉ DEL GUAVIARE', '95', 1),
(655, '95015', 'CALAMAR', '95', 1),
(656, '95025', 'EL RETORNO', '95', 1),
(657, '95200', 'MIRAFLORES', '95', 1),
(658, '41001', 'NEIVA', '41', 1),
(659, '41006', 'ACEVEDO', '41', 1),
(660, '41013', 'AGRADO', '41', 1),
(661, '41016', 'AIPE', '41', 1),
(662, '41020', 'ALGECIRAS', '41', 1),
(663, '41026', 'ALTAMIRA', '41', 1),
(664, '41078', 'BARAYA', '41', 1),
(665, '41132', 'CAMPOALEGRE', '41', 1),
(666, '41206', 'COLOMBIA', '41', 1),
(667, '41244', 'ELÍAS', '41', 1),
(668, '41298', 'GARZÓN', '41', 1),
(669, '41306', 'GIGANTE', '41', 1),
(670, '41319', 'GUADALUPE', '41', 1),
(671, '41349', 'HOBO', '41', 1),
(672, '41357', 'ÍQUIRA', '41', 1),
(673, '41359', 'ISNOS', '41', 1),
(674, '41378', 'LA ARGENTINA (LA PLATA VIEJA)', '41', 1),
(675, '41396', 'LA PLATA', '41', 1),
(676, '41483', 'NÁTAGA', '41', 1),
(677, '41503', 'OPORAPA', '41', 1),
(678, '41518', 'PAICOL', '41', 1),
(679, '41524', 'PALERMO', '41', 1),
(680, '41530', 'PALESTINA', '41', 1),
(681, '41548', 'PITAL', '41', 1),
(682, '41551', 'PITALITO', '41', 1),
(683, '41615', 'RIVERA', '41', 1),
(684, '41660', 'SALADOBLANCO', '41', 1),
(685, '41668', 'SAN AGUSTÍN', '41', 1),
(686, '41676', 'SANTA MARÍA', '41', 1),
(687, '41770', 'SUAZA', '41', 1),
(688, '41791', 'TARQUI', '41', 1),
(689, '41797', 'TESALIA (CARNICERÍAS)', '41', 1),
(690, '41799', 'TELLO', '41', 1),
(691, '41801', 'TERUEL', '41', 1),
(692, '41807', 'TIMANÁ', '41', 1),
(693, '41872', 'VILLAVIEJA', '41', 1),
(694, '41885', 'YAGUARÁ', '41', 1),
(695, '44001', 'RIOHACHA', '44', 1),
(696, '44035', 'ALBANIA', '44', 1),
(697, '44078', 'BARRANCAS', '44', 1),
(698, '44090', 'DIBULLA', '44', 1),
(699, '44098', 'DISTRACCIÓN', '44', 1),
(700, '44110', 'EL MOLINO', '44', 1),
(701, '44279', 'FONSECA', '44', 1),
(702, '44378', 'HATONUEVO', '44', 1),
(703, '44420', 'LA JAGUA DEL PILAR', '44', 1),
(704, '44430', 'MAICAO', '44', 1),
(705, '44560', 'MANAURE', '44', 1),
(706, '44650', 'SAN JUAN DEL CESAR', '44', 1),
(707, '44847', 'URIBIA', '44', 1),
(708, '44855', 'URUMITA', '44', 1),
(709, '44874', 'VILLANUEVA', '44', 1),
(710, '47001', 'SANTA MARTA', '47', 1),
(711, '47030', 'ALGARROBO', '47', 1),
(712, '47053', 'ARACATACA', '47', 1),
(713, '47058', 'ARIGUANÍ', '47', 1),
(714, '47161', 'CERRO DE SAN ANTONIO', '47', 1),
(715, '47170', 'CHIBOLO', '47', 1),
(716, '47189', 'CIÉNAGA', '47', 1),
(717, '47205', 'CONCORDIA', '47', 1),
(718, '47245', 'EL BANCO', '47', 1),
(719, '47258', 'EL PIÑÓN', '47', 1),
(720, '47268', 'EL RETÉN', '47', 1),
(721, '47288', 'FUNDACIÓN', '47', 1),
(722, '47318', 'GUAMAL', '47', 1),
(723, '47460', 'NUEVA GRANADA', '47', 1),
(724, '47541', 'PEDRAZA', '47', 1),
(725, '47545', 'PIJIÑO DEL CARMEN', '47', 1),
(726, '47551', 'PIVIJAY', '47', 1),
(727, '47555', 'PLATO', '47', 1),
(728, '47570', 'PUEBLOVIEJO', '47', 1),
(729, '47605', 'REMOLINO', '47', 1),
(730, '47660', 'SABANAS DE SAN ÁNGEL', '47', 1),
(731, '47675', 'SALAMINA', '47', 1),
(732, '47692', 'SAN SEBASTIÁN DE BUENAVISTA', '47', 1),
(733, '47703', 'SAN ZENÓN', '47', 1),
(734, '47707', 'SANTA ANA', '47', 1),
(735, '47720', 'SANTA BÁRBARA DE PINTO', '47', 1),
(736, '47745', 'SITIONUEVO', '47', 1),
(737, '47798', 'TENERIFE', '47', 1),
(738, '47960', 'ZAPAYÁN', '47', 1),
(739, '47980', 'ZONA BANANERA', '47', 1),
(740, '50001', 'VILLAVICENCIO', '50', 1),
(741, '50006', 'ACACÍAS', '50', 1),
(742, '50110', 'BARRANCA DE UPÍA', '50', 1),
(743, '50124', 'CABUYARO', '50', 1),
(744, '50150', 'CASTILLA LA NUEVA', '50', 1),
(745, '50223', 'CUBARRAL', '50', 1),
(746, '50226', 'CUMARAL', '50', 1),
(747, '50245', 'EL CALVARIO', '50', 1),
(748, '50251', 'EL CASTILLO', '50', 1),
(749, '50270', 'EL DORADO', '50', 1),
(750, '50287', 'FUENTEDEORO', '50', 1),
(751, '50313', 'GRANADA', '50', 1),
(752, '50318', 'GUAMAL', '50', 1),
(753, '50325', 'MAPIRIPÁN', '50', 1),
(754, '50330', 'MESETAS', '50', 1),
(755, '50350', 'LA MACARENA', '50', 1),
(756, '50370', 'URIBE', '50', 1),
(757, '50400', 'LEJANÍAS', '50', 1),
(758, '50450', 'PUERTO CONCORDIA', '50', 1),
(759, '50568', 'PUERTO GAITÁN', '50', 1),
(760, '50573', 'PUERTO LÓPEZ', '50', 1),
(761, '50577', 'PUERTO LLERAS', '50', 1),
(762, '50590', 'PUERTO RICO', '50', 1),
(763, '50606', 'RESTREPO', '50', 1),
(764, '50680', 'SAN CARLOS DE GUAROA', '50', 1),
(765, '50683', 'SAN JUAN DE ARAMA', '50', 1),
(766, '50686', 'SAN JUANITO', '50', 1),
(767, '50689', 'SAN MARTÍN DE LOS LLANOS', '50', 1),
(768, '50711', 'VISTAHERMOSA', '50', 1),
(769, '52001', 'PASTO', '52', 1),
(770, '52019', 'ALBÁN (SAN JOSÉ)', '52', 1),
(771, '52022', 'ALDANA', '52', 1),
(772, '52036', 'ANCUYÁ', '52', 1),
(773, '52051', 'ARBOLEDA', '52', 1),
(774, '52079', 'BARBACOAS', '52', 1),
(775, '52083', 'BELÉN', '52', 1),
(776, '52110', 'BUESACO', '52', 1),
(777, '52203', 'COLÓN (GÉNOVA)', '52', 1),
(778, '52207', 'CONSACÁ', '52', 1),
(779, '52210', 'CONTADERO', '52', 1),
(780, '52215', 'CÓRDOBA', '52', 1),
(781, '52224', 'CUASPÚD', '52', 1),
(782, '52227', 'CUMBAL', '52', 1),
(783, '52233', 'CUMBITARA', '52', 1),
(784, '52240', 'CHACHAGÜÍ', '52', 1),
(785, '52250', 'EL CHARCO', '52', 1),
(786, '52254', 'EL PEÑOL', '52', 1),
(787, '52256', 'EL ROSARIO', '52', 1),
(788, '52258', 'EL TABLÓN DE GÓMEZ', '52', 1),
(789, '52260', 'EL TAMBO', '52', 1),
(790, '52287', 'FUNES', '52', 1),
(791, '52317', 'GUACHUCAL', '52', 1),
(792, '52320', 'GUAITARILLA', '52', 1),
(793, '52323', 'GUALMATÁN', '52', 1),
(794, '52352', 'ILES', '52', 1),
(795, '52354', 'IMUÉS', '52', 1),
(796, '52356', 'IPIALES', '52', 1),
(797, '52378', 'LA CRUZ', '52', 1),
(798, '52381', 'LA FLORIDA', '52', 1),
(799, '52385', 'LA LLANADA', '52', 1),
(800, '52390', 'LA TOLA', '52', 1),
(801, '52399', 'LA UNIÓN', '52', 1),
(802, '52405', 'LEIVA', '52', 1),
(803, '52411', 'LINARES', '52', 1),
(804, '52418', 'LOS ANDES (SOTOMAYOR)', '52', 1),
(805, '52427', 'MAGÜÍ (PAYÁN)', '52', 1),
(806, '52435', 'MALLAMA (PIEDRANCHA)', '52', 1),
(807, '52473', 'MOSQUERA', '52', 1),
(808, '52480', 'NARIÑO', '52', 1),
(809, '52490', 'OLAYA HERRERA', '52', 1),
(810, '52506', 'OSPINA', '52', 1),
(811, '52520', 'FRANCISCO PIZARRO', '52', 1),
(812, '52540', 'POLICARPA', '52', 1),
(813, '52560', 'POTOSÍ', '52', 1),
(814, '52565', 'PROVIDENCIA', '52', 1),
(815, '52573', 'PUERRES', '52', 1),
(816, '52585', 'PUPIALES', '52', 1),
(817, '52612', 'RICAURTE', '52', 1),
(818, '52621', 'ROBERTO PAYÁN (SAN JOSÉ)', '52', 1),
(819, '52678', 'SAMANIEGO', '52', 1),
(820, '52683', 'SANDONÁ', '52', 1),
(821, '52685', 'SAN BERNARDO', '52', 1),
(822, '52687', 'SAN LORENZO', '52', 1),
(823, '52693', 'SAN PABLO', '52', 1),
(824, '52694', 'SAN PEDRO DE CARTAGO', '52', 1),
(825, '52696', 'SANTA BÁRBARA', '52', 1),
(826, '52699', 'SANTACRUZ', '52', 1),
(827, '52720', 'SAPUYES', '52', 1),
(828, '52786', 'TAMINANGO', '52', 1),
(829, '52788', 'TANGUA', '52', 1),
(830, '52835', 'SAN ANDRÉS DE TUMACO', '52', 1),
(831, '52838', 'TÚQUERRES', '52', 1),
(832, '52885', 'YACUANQUER', '52', 1),
(833, '54001', 'CÚCUTA', '54', 1),
(834, '54003', 'ÁBREGO', '54', 1),
(835, '54051', 'ARBOLEDAS', '54', 1),
(836, '54099', 'BOCHALEMA', '54', 1),
(837, '54109', 'BUCARASICA', '54', 1),
(838, '54125', 'CÁCOTA DE VELASCO', '54', 1),
(839, '54128', 'CÁCHIRA', '54', 1),
(840, '54172', 'CHINÁCOTA', '54', 1),
(841, '54174', 'CHITAGÁ', '54', 1),
(842, '54206', 'CONVENCIÓN', '54', 1),
(843, '54223', 'CUCUTILLA', '54', 1),
(844, '54239', 'DURANIA', '54', 1),
(845, '54245', 'EL CARMEN', '54', 1),
(846, '54250', 'EL TARRA', '54', 1),
(847, '54261', 'EL ZULIA', '54', 1),
(848, '54313', 'GRAMALOTE', '54', 1),
(849, '54344', 'HACARÍ', '54', 1),
(850, '54347', 'HERRÁN', '54', 1),
(851, '54377', 'LABATECA', '54', 1),
(852, '54385', 'LA ESPERANZA', '54', 1),
(853, '54398', 'LA PLAYA DE BELÉN', '54', 1),
(854, '54405', 'LOS PATIOS', '54', 1),
(855, '54418', 'LOURDES', '54', 1),
(856, '54480', 'MUTISCUA', '54', 1),
(857, '54498', 'OCAÑA', '54', 1),
(858, '54518', 'PAMPLONA', '54', 1),
(859, '54520', 'PAMPLONITA', '54', 1),
(860, '54553', 'PUERTO SANTANDER', '54', 1),
(861, '54599', 'RAGONVALIA', '54', 1),
(862, '54660', 'SALAZAR DE LAS PALMAS', '54', 1),
(863, '54670', 'SAN CALIXTO', '54', 1),
(864, '54673', 'SAN CAYETANO', '54', 1),
(865, '54680', 'SANTIAGO', '54', 1),
(866, '54720', 'SARDINATA', '54', 1),
(867, '54743', 'SANTO DOMINGO DE SILOS', '54', 1),
(868, '54800', 'TEORAMA', '54', 1),
(869, '54810', 'TIBÚ', '54', 1),
(870, '54820', 'TOLEDO', '54', 1),
(871, '54871', 'VILLA CARO', '54', 1),
(872, '54874', 'VILLA DEL ROSARIO', '54', 1),
(873, '86001', 'MOCOA', '86', 1),
(874, '86219', 'COLÓN', '86', 1),
(875, '86320', 'ORITO', '86', 1),
(876, '86568', 'PUERTO ASÍS', '86', 1),
(877, '86569', 'PUERTO CAICEDO', '86', 1),
(878, '86571', 'PUERTO GUZMÁN', '86', 1),
(879, '86573', 'PUERTO LEGUÍZAMO', '86', 1),
(880, '86749', 'SIBUNDOY', '86', 1),
(881, '86755', 'SAN FRANCISCO', '86', 1),
(882, '86757', 'SAN MIGUEL', '86', 1),
(883, '86760', 'SANTIAGO', '86', 1),
(884, '86865', 'VALLE DEL GUAMUEZ', '86', 1),
(885, '86885', 'VILLAGARZÓN', '86', 1),
(886, '63001', 'ARMENIA', '63', 1),
(887, '63111', 'BUENAVISTA', '63', 1),
(888, '63130', 'CALARCÁ', '63', 1),
(889, '63190', 'CIRCASIA', '63', 1),
(890, '63212', 'CÓRDOBA', '63', 1),
(891, '63272', 'FILANDIA', '63', 1),
(892, '63302', 'GÉNOVA', '63', 1),
(893, '63401', 'LA TEBAIDA', '63', 1),
(894, '63470', 'MONTENEGRO', '63', 1),
(895, '63548', 'PIJAO', '63', 1),
(896, '63594', 'QUIMBAYA', '63', 1),
(897, '63690', 'SALENTO', '63', 1),
(898, '66001', 'PEREIRA', '66', 1),
(899, '66045', 'APÍA', '66', 1),
(900, '66075', 'BALBOA', '66', 1),
(901, '66088', 'BELÉN DE UMBRÍA', '66', 1),
(902, '66170', 'DOSQUEBRADAS', '66', 1),
(903, '66318', 'GUÁTICA', '66', 1),
(904, '66383', 'LA CELIA', '66', 1),
(905, '66400', 'LA VIRGINIA', '66', 1),
(906, '66440', 'MARSELLA', '66', 1),
(907, '66456', 'MISTRATÓ', '66', 1),
(908, '66572', 'PUEBLO RICO', '66', 1),
(909, '66594', 'QUINCHÍA', '66', 1),
(910, '66682', 'SANTA ROSA DE CABAL', '66', 1),
(911, '66687', 'SANTUARIO', '66', 1),
(912, '68001', 'BUCARAMANGA', '68', 1),
(913, '68013', 'AGUADA', '68', 1),
(914, '68020', 'ALBANIA', '68', 1),
(915, '68051', 'ARATOCA', '68', 1),
(916, '68077', 'BARBOSA', '68', 1),
(917, '68079', 'BARICHARA', '68', 1),
(918, '68081', 'BARRANCABERMEJA', '68', 1),
(919, '68092', 'BETULIA', '68', 1),
(920, '68101', 'BOLÍVAR', '68', 1),
(921, '68121', 'CABRERA', '68', 1),
(922, '68132', 'CALIFORNIA', '68', 1),
(923, '68147', 'CAPITANEJO', '68', 1),
(924, '68152', 'CARCASÍ', '68', 1),
(925, '68160', 'CEPITÁ', '68', 1),
(926, '68162', 'CERRITO', '68', 1),
(927, '68167', 'CHARALÁ', '68', 1),
(928, '68169', 'CHARTA', '68', 1),
(929, '68176', 'CHIMA', '68', 1),
(930, '68179', 'CHIPATÁ', '68', 1),
(931, '68190', 'CIMITARRA', '68', 1),
(932, '68207', 'CONCEPCIÓN', '68', 1),
(933, '68209', 'CONFINES', '68', 1),
(934, '68211', 'CONTRATACIÓN', '68', 1),
(935, '68217', 'COROMORO', '68', 1),
(936, '68229', 'CURITÍ', '68', 1),
(937, '68235', 'EL CARMEN DE CHUCURÍ', '68', 1),
(938, '68245', 'EL GUACAMAYO', '68', 1),
(939, '68250', 'EL PEÑÓN', '68', 1),
(940, '68255', 'EL PLAYÓN', '68', 1),
(941, '68264', 'ENCINO', '68', 1),
(942, '68266', 'ENCISO', '68', 1),
(943, '68271', 'FLORIÁN', '68', 1),
(944, '68276', 'FLORIDABLANCA', '68', 1),
(945, '68296', 'GALÁN', '68', 1),
(946, '68298', 'GÁMBITA', '68', 1),
(947, '68307', 'GIRÓN', '68', 1),
(948, '68318', 'GUACA', '68', 1),
(949, '68320', 'GUADALUPE', '68', 1),
(950, '68322', 'GUAPOTÁ', '68', 1),
(951, '68324', 'GUAVATÁ', '68', 1),
(952, '68327', 'GÜEPSA', '68', 1),
(953, '68344', 'HATO', '68', 1),
(954, '68368', 'JESÚS MARÍA', '68', 1),
(955, '68370', 'JORDÁN', '68', 1),
(956, '68377', 'LA BELLEZA', '68', 1),
(957, '68385', 'LANDÁZURI', '68', 1),
(958, '68397', 'LA PAZ', '68', 1),
(959, '68406', 'LEBRIJA', '68', 1),
(960, '68418', 'LOS SANTOS', '68', 1),
(961, '68425', 'MACARAVITA', '68', 1),
(962, '68432', 'MÁLAGA', '68', 1),
(963, '68444', 'MATANZA', '68', 1),
(964, '68464', 'MOGOTES', '68', 1),
(965, '68468', 'MOLAGAVITA', '68', 1),
(966, '68498', 'OCAMONTE', '68', 1),
(967, '68500', 'OIBA', '68', 1),
(968, '68502', 'ONZAGA', '68', 1),
(969, '68522', 'PALMAR', '68', 1),
(970, '68524', 'PALMAS DEL SOCORRO', '68', 1),
(971, '68533', 'PÁRAMO', '68', 1),
(972, '68547', 'PIEDECUESTA', '68', 1),
(973, '68549', 'PINCHOTE', '68', 1),
(974, '68572', 'PUENTE NACIONAL', '68', 1),
(975, '68573', 'PUERTO PARRA', '68', 1),
(976, '68575', 'PUERTO WILCHES', '68', 1),
(977, '68615', 'RIONEGRO', '68', 1),
(978, '68655', 'SABANA DE TORRES', '68', 1),
(979, '68669', 'SAN ANDRÉS', '68', 1),
(980, '68673', 'SAN BENITO', '68', 1),
(981, '68679', 'SAN GIL', '68', 1),
(982, '68682', 'SAN JOAQUÍN', '68', 1),
(983, '68684', 'SAN JOSÉ DE MIRANDA', '68', 1),
(984, '68686', 'SAN MIGUEL', '68', 1),
(985, '68689', 'SAN VICENTE DE CHUCURÍ', '68', 1),
(986, '68705', 'SANTA BÁRBARA', '68', 1),
(987, '68720', 'SANTA HELENA DEL OPÓN', '68', 1),
(988, '68745', 'SIMACOTA', '68', 1),
(989, '68755', 'SOCORRO', '68', 1),
(990, '68770', 'SUAITA', '68', 1),
(991, '68773', 'SUCRE', '68', 1),
(992, '68780', 'SURATÁ', '68', 1),
(993, '68820', 'TONA', '68', 1),
(994, '68855', 'VALLE DE SAN JOSÉ', '68', 1),
(995, '68861', 'VÉLEZ', '68', 1),
(996, '68867', 'VETAS', '68', 1),
(997, '68872', 'VILLANUEVA', '68', 1),
(998, '68895', 'ZAPATOCA', '68', 1),
(999, '70001', 'SINCELEJO', '70', 1),
(1000, '70110', 'BUENAVISTA', '70', 1),
(1001, '70124', 'CAIMITO', '70', 1),
(1002, '70204', 'COLOSÓ', '70', 1),
(1003, '70215', 'COROZAL', '70', 1),
(1004, '70221', 'COVEÑAS', '70', 1),
(1005, '70230', 'CHALÁN', '70', 1),
(1006, '70233', 'EL ROBLE', '70', 1),
(1007, '70235', 'GALERAS', '70', 1),
(1008, '70265', 'GUARANDA', '70', 1),
(1009, '70400', 'LA UNIÓN', '70', 1),
(1010, '70418', 'LOS PALMITOS', '70', 1),
(1011, '70429', 'MAJAGUAL', '70', 1),
(1012, '70473', 'MORROA', '70', 1),
(1013, '70508', 'OVEJAS', '70', 1),
(1014, '70523', 'PALMITO', '70', 1),
(1015, '70670', 'SAMPUÉS', '70', 1),
(1016, '70678', 'SAN BENITO ABAD', '70', 1),
(1017, '70702', 'SAN JUAN DE BETULIA', '70', 1),
(1018, '70708', 'SAN MARCOS', '70', 1),
(1019, '70713', 'SAN ONOFRE', '70', 1),
(1020, '70717', 'SAN PEDRO', '70', 1),
(1021, '70742', 'SAN LUIS DE SINCÉ', '70', 1),
(1022, '70771', 'SUCRE', '70', 1),
(1023, '70820', 'SANTIAGO DE TOLÚ', '70', 1),
(1024, '70823', 'TOLÚ VIEJO', '70', 1),
(1025, '73001', 'IBAGUÉ', '73', 1),
(1026, '73024', 'ALPUJARRA', '73', 1),
(1027, '73026', 'ALVARADO', '73', 1),
(1028, '73030', 'AMBALEMA', '73', 1),
(1029, '73043', 'ANZOÁTEGUI', '73', 1),
(1030, '73055', 'ARMERO (GUAYABAL)', '73', 1),
(1031, '73067', 'ATACO', '73', 1),
(1032, '73124', 'CAJAMARCA', '73', 1),
(1033, '73148', 'CARMEN DE APICALÁ', '73', 1),
(1034, '73152', 'CASABIANCA', '73', 1),
(1035, '73168', 'CHAPARRAL', '73', 1),
(1036, '73200', 'COELLO', '73', 1),
(1037, '73217', 'COYAIMA', '73', 1),
(1038, '73226', 'CUNDAY', '73', 1),
(1039, '73236', 'DOLORES', '73', 1),
(1040, '73268', 'ESPINAL', '73', 1),
(1041, '73270', 'FALAN', '73', 1),
(1042, '73275', 'FLANDES', '73', 1),
(1043, '73283', 'FRESNO', '73', 1),
(1044, '73319', 'GUAMO', '73', 1),
(1045, '73347', 'HERVEO', '73', 1),
(1046, '73349', 'HONDA', '73', 1),
(1047, '73352', 'ICONONZO', '73', 1),
(1048, '73408', 'LÉRIDA', '73', 1),
(1049, '73411', 'LÍBANO', '73', 1),
(1050, '73443', 'SAN SEBASTIÁN DE MARIQUITA', '73', 1),
(1051, '73449', 'MELGAR', '73', 1),
(1052, '73461', 'MURILLO', '73', 1),
(1053, '73483', 'NATAGAIMA', '73', 1),
(1054, '73504', 'ORTEGA', '73', 1),
(1055, '73520', 'PALOCABILDO', '73', 1),
(1056, '73547', 'PIEDRAS', '73', 1),
(1057, '73555', 'PLANADAS', '73', 1),
(1058, '73563', 'PRADO', '73', 1),
(1059, '73585', 'PURIFICACIÓN', '73', 1),
(1060, '73616', 'RIOBLANCO', '73', 1),
(1061, '73622', 'RONCESVALLES', '73', 1),
(1062, '73624', 'ROVIRA', '73', 1),
(1063, '73671', 'SALDAÑA', '73', 1),
(1064, '73675', 'SAN ANTONIO', '73', 1),
(1065, '73678', 'SAN LUIS', '73', 1),
(1066, '73686', 'SANTA ISABEL', '73', 1),
(1067, '73770', 'SUÁREZ', '73', 1),
(1068, '73854', 'VALLE DE SAN JUAN', '73', 1),
(1069, '73861', 'VENADILLO', '73', 1),
(1070, '73870', 'VILLAHERMOSA', '73', 1),
(1071, '73873', 'VILLARRICA', '73', 1),
(1072, '76001', 'CALI', '76', 1),
(1073, '76020', 'ALCALÁ', '76', 1),
(1074, '76036', 'ANDALUCÍA', '76', 1),
(1075, '76041', 'ANSERMANUEVO', '76', 1),
(1076, '76054', 'ARGELIA', '76', 1),
(1077, '76100', 'BOLÍVAR', '76', 1),
(1078, '76109', 'BUENAVENTURA', '76', 1),
(1079, '76111', 'GUADALAJARA DE BUGA', '76', 1),
(1080, '76113', 'BUGALAGRANDE', '76', 1),
(1081, '76122', 'CAICEDONIA', '76', 1),
(1082, '76126', 'CALIMA (DARIEN)', '76', 1),
(1083, '76130', 'CANDELARIA', '76', 1),
(1084, '76147', 'CARTAGO', '76', 1),
(1085, '76233', 'DAGUA', '76', 1),
(1086, '76243', 'EL ÁGUILA', '76', 1),
(1087, '76246', 'EL CAIRO', '76', 1),
(1088, '76248', 'EL CERRITO', '76', 1),
(1089, '76250', 'EL DOVIO', '76', 1),
(1090, '76275', 'FLORIDA', '76', 1),
(1091, '76306', 'GINEBRA', '76', 1),
(1092, '76318', 'GUACARÍ', '76', 1),
(1093, '76364', 'JAMUNDÍ', '76', 1),
(1094, '76377', 'LA CUMBRE', '76', 1),
(1095, '76400', 'LA UNIÓN', '76', 1),
(1096, '76403', 'LA VICTORIA', '76', 1),
(1097, '76497', 'OBANDO', '76', 1),
(1098, '76520', 'PALMIRA', '76', 1),
(1099, '76563', 'PRADERA', '76', 1),
(1100, '76606', 'RESTREPO', '76', 1),
(1101, '76616', 'RIOFRÍO', '76', 1),
(1102, '76622', 'ROLDANILLO', '76', 1),
(1103, '76670', 'SAN PEDRO', '76', 1),
(1104, '76736', 'SEVILLA', '76', 1),
(1105, '76823', 'TORO', '76', 1),
(1106, '76828', 'TRUJILLO', '76', 1),
(1107, '76834', 'TULUÁ', '76', 1),
(1108, '76845', 'ULLOA', '76', 1),
(1109, '76863', 'VERSALLES', '76', 1),
(1110, '76869', 'VIJES', '76', 1),
(1111, '76890', 'YOTOCO', '76', 1),
(1112, '76892', 'YUMBO', '76', 1),
(1113, '76895', 'ZARZAL', '76', 1),
(1114, '97001', 'MITÚ', '97', 1),
(1115, '97161', 'CARURÚ', '97', 1),
(1116, '97511', 'PACOA', '97', 1),
(1117, '97666', 'TARAIRA', '97', 1),
(1118, '97777', 'PAPUNAHUA', '97', 1),
(1119, '97889', 'YAVARATÉ', '97', 1),
(1120, '99001', 'PUERTO CARREÑO', '99', 1),
(1121, '99524', 'LA PRIMAVERA', '99', 1),
(1122, '99624', 'SANTA ROSALÍA', '99', 1),
(1123, '99773', 'CUMARIBO', '99', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedido`
--

CREATE TABLE `pedido` (
  `id` bigint UNSIGNED NOT NULL,
  `fecha` date NOT NULL,
  `fechaEntrega` date DEFAULT NULL,
  `horaEntrega` time DEFAULT NULL,
  `estado` enum('Pendiente','En Proceso','En camino','Entregado') NOT NULL,
  `entrega_id` bigint UNSIGNED NOT NULL,
  `users_id` bigint UNSIGNED NOT NULL,
  `producto_id` bigint UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto`
--

CREATE TABLE `producto` (
  `id` bigint UNSIGNED NOT NULL,
  `nombre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `descripcion` text NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `estado` enum('Disponible','No disponible') NOT NULL,
  `unidad_medida` decimal(10,2) NOT NULL,
  `cantidad` int NOT NULL,
  `marca` varchar(80) NOT NULL,
  `total` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `producto`
--

INSERT INTO `producto` (`id`, `nombre`, `descripcion`, `precio`, `estado`, `unidad_medida`, `cantidad`, `marca`, `total`) VALUES
(1, 'ww', 'q', 2.00, 'Disponible', 2.00, 2, 'qw', 4.00),
(2, 'q', 'q', 2.00, 'Disponible', 2.00, 2, '2', 4.00),
(3, 'q', 'd', 2.00, 'Disponible', 4.00, 1, 'd', 2.00),
(4, 'q', 'q', 1.00, 'Disponible', 2.00, 1, 'q', 1.00),
(21, 'asdasd', 'jojasss', 1222.00, 'No disponible', 34.00, 2222, '2333', 2715284.00),
(22, 'freimar', 'jojass', 2.00, 'Disponible', 2.00, 2, 'lina', 4.00),
(23, 'HHHHHHHHH', '5FGGGGGG', 5555555.00, 'Disponible', 12.00, 12, 'DDDDDDD', 66666660.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedor`
--

CREATE TABLE `proveedor` (
  `id` bigint UNSIGNED NOT NULL,
  `tipo_persona` enum('Juridica','Natural') NOT NULL,
  `razon_social` varchar(100) NOT NULL,
  `nombre_comercial` varchar(85) NOT NULL,
  `representante_legal` varchar(85) NOT NULL,
  `users_id` bigint UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tbl_empleados`
--

CREATE TABLE `tbl_empleados` (
  `id_empleado` int NOT NULL,
  `nombre_empleado` varchar(50) DEFAULT NULL,
  `apellido_empleado` varchar(50) DEFAULT NULL,
  `sexo_empleado` int DEFAULT NULL,
  `telefono_empleado` varchar(50) DEFAULT NULL,
  `email_empleado` varchar(50) DEFAULT NULL,
  `profesion_empleado` varchar(50) DEFAULT NULL,
  `foto_empleado` mediumtext,
  `salario_empleado` bigint DEFAULT NULL,
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `tbl_empleados`
--

INSERT INTO `tbl_empleados` (`id_empleado`, `nombre_empleado`, `apellido_empleado`, `sexo_empleado`, `telefono_empleado`, `email_empleado`, `profesion_empleado`, `foto_empleado`, `salario_empleado`, `fecha_registro`) VALUES
(5, 'Brenda', 'Viera', 2, '323543543', 'brenda@gmail.com', 'Dev', '22c055aeec314572a0046ec50b84f21719270dac6ea34c91b8380ac289fff9e5.png', 1200000, '2023-08-23 17:05:34'),
(6, 'Alejandro', 'Torres', 1, '324242342', 'alejandro@gmail.com', 'Tecnico', '7b84aceb56534d27aa2e8b727a245dca9f60156a070a47c491ff2d21da1742e5.png', 2100, '2023-08-23 17:06:13'),
(7, 'Karla', 'Ramos', 2, '345678', 'karla@gmail.com', 'Ingeniera', '248cc9c38cfb494bb2300d7cbf4a3b317522f295338b4639a8e025e6b203291c.png', 2300, '2023-08-23 17:07:28'),
(8, 'hojas', 'Ramos', 2, '345678', 'karla@gmail.com', 'Ingeniera', '248cc9c38cfb494bb2300d7cbf4a3b317522f295338b4639a8e025e6b203291c.png', 2300, '2023-08-23 17:07:28'),
(9, 'sdasd', 'asdasd', 1, 'asdasd', 'asdasd@gmail.com', 'asdasd', '0ca183c870b646818fbaf498cda0eb583404c97aa2294bc9851fc6a2cc7ecaa1', 111111, '2024-12-11 21:01:55'),
(12, 'asdasd', 'asdasd', 1, '3214412444', 'samuelmacualo2005@gmail.com', 'asdasd', 'ee745b2a4cdb4d87a2f96776967d2e143c0d2b2946004e10b22fce93f08b45e4', 1222222, '2025-02-14 21:47:07'),
(13, 'freimar', 'sadasd', 2, '3241259', 'juansebastian812005@gamil.com', '2000', 'f3142bfcf3a2409ba3670a67d994fccbd397963d167242eea44d194bbcb93800', 0, '2025-02-14 21:53:52'),
(16, 'Samuel Esteban', 'Macualo Patarroyo', 2, '30057192412', 'samuelmacualo2005@gmail.com', 'jojAS', 'b20d0dceaaa14b20b74ddfa12d4d966daa2746df71fa4d02aecff62fb24d6867', 88888, '2025-02-14 22:13:17');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` bigint UNSIGNED NOT NULL,
  `tipo_documento` enum('Cedula ciudadania','Tarjeta identidad','Cedula extranjeria','NIT') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `documento` bigint NOT NULL,
  `nombre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `apellido` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `telefono` bigint NOT NULL,
  `correo` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `contrasena` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `rol` enum('administrador','cliente','proveedor','empleado','superadmin') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `estado` enum('activo','inactivo') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `created_user` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `tipo_documento`, `documento`, `nombre`, `apellido`, `telefono`, `correo`, `contrasena`, `rol`, `estado`, `created_user`) VALUES
(15, 'NIT', 1048847249, 'juan sebastian ', 'moreno olmos laka', 3244124445, 'juansebastian812005@gmail.com', 'scrypt:32768:8:1$JPM3QEemLqMTQzbF$eb6cdb7379128a4f4da08f4bcaac430525193280d8ac84371b9ed7cfe3eb7fdb839476cbf70ce3637b87817a7163d8be215c77eb61de52d34158de1cd11189d4', 'cliente', 'activo', '2025-02-15 15:39:46'),
(30, 'Tarjeta identidad', 2005, '0000', '0000', 0, '0000@gmasil.cvom', 'scrypt:32768:8:1$AfvkaGOh3ePecqt7$10fe8d5f6fc0647d01692e3dd3bcf1d7144e5570ee98dd2724aaec99c23db63750841a87fb53dcca3c712b7bd844dfe4a0057b42e4f763eb4af7ab60a8ef84d9', 'cliente', 'activo', '2025-02-15 23:51:40'),
(31, 'Tarjeta identidad', 33333, '0000', '0000', 0, '0000@gmail.com', 'scrypt:32768:8:1$6369dlZfT6CosvF7$f82d71f0126665cf8f90f1aed9d07a3a8bd6441dec54918fdb2e0ea0a0e277da6cf210a97ac0121a66a00396e5f966567f680559c063ee39e656d095c7a82f26', 'cliente', 'inactivo', '2025-02-15 23:53:25'),
(32, 'Cedula extranjeria', 9999, '9999', '9999', 9999, '9999@gmail.com', 'scrypt:32768:8:1$9r1ufp8pLgYFVfKH$830d15a335c69269c5426661cca46d394263e0f0a06bfea14a307bfc9c19055216201db673d858b2e5a2f6414a8b397d1929c0a4a253fb5e01d62a0da9774db5', 'cliente', 'activo', '2025-02-16 00:21:29'),
(33, 'NIT', 33675892, 'david', 'olmos', 3187966329, 'juansebas@gmail.com', 'scrypt:32768:8:1$rFoDNyyvLvenR19q$f0fc6e6e10dab17eb2abc7de1d68235abb44defcc569bae9bbc8bb31ea2bc5d3fc97761e8dd3433d255828b8d1db8d8966f36fa97761d90d21790c28f9c8c4b1', 'empleado', 'activo', '2025-02-16 00:33:02'),
(34, 'Tarjeta identidad', 1111, 'ffff', 'ffff', 1222, 'jugfdgdans@gmail.com', 'scrypt:32768:8:1$Ao57BJJbPIPSTH0M$0601234b89a29d9e5a13979bca050b47fc3d6e84d27c95af1226a7e189a5b7c9dda78d2901e5837e5908bf6119b6571dbb138e7a3ea266dc93be7bc6fe451f17', 'cliente', 'activo', '2025-02-16 00:33:40'),
(37, 'Cedula ciudadania', 30272888, 'Super', 'Admin', 3000000000, 'superadmin@example.com', 'scrypt:32768:8:1$MRfRaBKeNzEnXeYj$2388ab4a0af05e4d1dc020b1540b9fce65347cf5c1003924cfd05750b640268f683d342ce685cd2c181525ab66e00222eda055e081033037b8907e7ac0e218aa', 'administrador', 'activo', '2025-02-20 21:34:15');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `abono`
--
ALTER TABLE `abono`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_abono_pedido1_idx` (`pedido_id`);

--
-- Indices de la tabla `carrito_compras`
--
ALTER TABLE `carrito_compras`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_carrito_compras_producto1_idx` (`producto_id`),
  ADD KEY `fk_carrito_compras_users1_idx` (`users_id`);

--
-- Indices de la tabla `departamento`
--
ALTER TABLE `departamento`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_detalle_pedido_pedido1_idx` (`pedido_id`);

--
-- Indices de la tabla `direccion`
--
ALTER TABLE `direccion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_direccion_municipio1_idx` (`municipio_id`),
  ADD KEY `fk_direccion_users1_idx` (`users_id`),
  ADD KEY `fk_direccion_departamento1_idx` (`departamento_id`);

--
-- Indices de la tabla `entrega`
--
ALTER TABLE `entrega`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_entrega_direccion1_idx` (`direccion_id`);

--
-- Indices de la tabla `factura`
--
ALTER TABLE `factura`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_factura_pedido1_idx` (`pedido_id`),
  ADD KEY `fk_factura_metodo_pago1_idx` (`metodo_pago_id`);

--
-- Indices de la tabla `inventario`
--
ALTER TABLE `inventario`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_inventario_producto1_idx` (`producto_id`),
  ADD KEY `fk_inventario_users1_idx` (`users_id`);

--
-- Indices de la tabla `metodo_pago`
--
ALTER TABLE `metodo_pago`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `municipio`
--
ALTER TABLE `municipio`
  ADD PRIMARY KEY (`id`),
  ADD KEY `codigo` (`codigo`);

--
-- Indices de la tabla `pedido`
--
ALTER TABLE `pedido`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_pedido_entrega1_idx` (`entrega_id`),
  ADD KEY `fk_pedido_users1_idx` (`users_id`),
  ADD KEY `fk_pedido_producto1_idx` (`producto_id`);

--
-- Indices de la tabla `producto`
--
ALTER TABLE `producto`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `proveedor`
--
ALTER TABLE `proveedor`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_proveedor_users1_idx` (`users_id`);

--
-- Indices de la tabla `tbl_empleados`
--
ALTER TABLE `tbl_empleados`
  ADD PRIMARY KEY (`id_empleado`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `abono`
--
ALTER TABLE `abono`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `carrito_compras`
--
ALTER TABLE `carrito_compras`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `departamento`
--
ALTER TABLE `departamento`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT de la tabla `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `direccion`
--
ALTER TABLE `direccion`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `entrega`
--
ALTER TABLE `entrega`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `factura`
--
ALTER TABLE `factura`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `inventario`
--
ALTER TABLE `inventario`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `metodo_pago`
--
ALTER TABLE `metodo_pago`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `pedido`
--
ALTER TABLE `pedido`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `producto`
--
ALTER TABLE `producto`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT de la tabla `proveedor`
--
ALTER TABLE `proveedor`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tbl_empleados`
--
ALTER TABLE `tbl_empleados`
  MODIFY `id_empleado` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `abono`
--
ALTER TABLE `abono`
  ADD CONSTRAINT `fk_abono_pedido1` FOREIGN KEY (`pedido_id`) REFERENCES `pedido` (`id`);

--
-- Filtros para la tabla `carrito_compras`
--
ALTER TABLE `carrito_compras`
  ADD CONSTRAINT `fk_carrito_compras_producto1` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`),
  ADD CONSTRAINT `fk_carrito_compras_users1` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Filtros para la tabla `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  ADD CONSTRAINT `fk_detalle_pedido_pedido1` FOREIGN KEY (`pedido_id`) REFERENCES `pedido` (`id`);

--
-- Filtros para la tabla `direccion`
--
ALTER TABLE `direccion`
  ADD CONSTRAINT `fk_direccion_departamento1_idx` FOREIGN KEY (`departamento_id`) REFERENCES `departamento` (`id`),
  ADD CONSTRAINT `fk_direccion_municipio1` FOREIGN KEY (`municipio_id`) REFERENCES `municipio` (`id`),
  ADD CONSTRAINT `fk_direccion_users1_idx` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `entrega`
--
ALTER TABLE `entrega`
  ADD CONSTRAINT `fk_entrega_direccion1` FOREIGN KEY (`direccion_id`) REFERENCES `direccion` (`id`);

--
-- Filtros para la tabla `factura`
--
ALTER TABLE `factura`
  ADD CONSTRAINT `fk_factura_metodo_pago1` FOREIGN KEY (`metodo_pago_id`) REFERENCES `metodo_pago` (`id`),
  ADD CONSTRAINT `fk_factura_pedido1` FOREIGN KEY (`pedido_id`) REFERENCES `pedido` (`id`);

--
-- Filtros para la tabla `inventario`
--
ALTER TABLE `inventario`
  ADD CONSTRAINT `fk_inventario_producto1` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`),
  ADD CONSTRAINT `fk_inventario_users1` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Filtros para la tabla `pedido`
--
ALTER TABLE `pedido`
  ADD CONSTRAINT `fk_pedido_entrega1` FOREIGN KEY (`entrega_id`) REFERENCES `entrega` (`id`),
  ADD CONSTRAINT `fk_pedido_producto1` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `fk_pedido_users1` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Filtros para la tabla `proveedor`
--
ALTER TABLE `proveedor`
  ADD CONSTRAINT `fk_proveedor_users1` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
