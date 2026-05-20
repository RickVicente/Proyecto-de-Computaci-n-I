-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         10.4.32-MariaDB - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.15.0.7171
-- MADRIVE — Script de inicialización de base de datos
-- Se ejecuta automáticamente al primer arranque del contenedor MariaDB
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para pc2
CREATE DATABASE IF NOT EXISTS `pc2` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `pc2`;

-- ─── TABLA: usuarios ─────────────────────────────────────────────
-- (se crea antes que predicciones porque predicciones tiene FK a usuarios)
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `rol` enum('admin','usuario','invitado') NOT NULL DEFAULT 'usuario',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla pc2.usuarios
INSERT INTO `usuarios` (`id`, `username`, `email`, `password`, `rol`) VALUES
	(2, 'rick', 'ricky@test.com', 'bcb15f821479b4d5772bd0ca866c00ad5f926e3580720659cc80d39c9d09802a', 'admin'),
	(3, 'ricky', 'rick@test.com', 'bcb15f821479b4d5772bd0ca866c00ad5f926e3580720659cc80d39c9d09802a', 'usuario'),
	(4, 'mama', 'mama@hotmail.com', '9e965e5ba418e202fa94472150057b28dc6c7ac8293b181f936ff5febd86170e', 'usuario'),
	(5, 'leo', 'leo@test.com', 'bcb15f821479b4d5772bd0ca866c00ad5f926e3580720659cc80d39c9d09802a', 'usuario'),
	(9, 'usuario', 'usuario@test.com', 'bcb15f821479b4d5772bd0ca866c00ad5f926e3580720659cc80d39c9d09802a', 'usuario');

-- ─── TABLA: zonas ────────────────────────────────────────────────
-- (se crea antes que predicciones porque predicciones tiene FK a zonas)
CREATE TABLE IF NOT EXISTS `zonas` (
  `id_zona` int(11) NOT NULL,
  `latitud` decimal(10,8) DEFAULT NULL,
  `longitud` decimal(11,8) DEFAULT NULL,
  `carretera` varchar(50) DEFAULT NULL,
  `pk` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id_zona`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla pc2.zonas: 53 cámaras reales de la DGT
INSERT INTO `zonas` (`id_zona`, `latitud`, `longitud`, `carretera`, `pk`) VALUES
	(4, 41.92270000, -4.50630000, 'A-62', '87.9'),
	(22, 41.53600000, -5.06400000, 'A-6', '188.55'),
	(28, 42.05810000, -5.68060000, 'A-6', '268.37'),
	(598, 40.52156500, -3.65140800, 'A-1', '14.3'),
	(634, 40.44939400, -3.64811400, 'A-2', '5.5'),
	(651, 40.48071565, -3.64387716, 'M-40', '3.6'),
	(660, 40.45033300, -3.60013200, 'A-2', '9.6'),
	(668, 40.46768900, -3.43970900, 'A-2', '23.6'),
	(673, 40.51249100, -3.31930200, 'A-2', '35.4'),
	(677, 40.47255345, -3.41822320, 'A-2', '37.0'),
	(696, 40.38546900, -3.60533400, 'A-3', '8.0'),
	(705, 40.32476200, -3.51818500, 'A-3', '12.0'),
	(726, 40.22625000, -3.33500800, 'A-3', '18.5'),
	(731, 40.34245796, -3.67245840, 'A-4', '24.0'),
	(762, 38.41132200, -3.49883400, 'A-4', '244.25'),
	(771, 40.27263700, -3.75309600, 'A-42', '8.5'),
	(773, 40.29565500, -3.73738400, 'A-42', '10.5'),
	(782, 39.88015900, -4.02099700, 'A-42', '68.0'),
	(791, 40.38056000, -3.78959900, 'A-5', '18.0'),
	(798, 40.40342100, -3.75584300, 'A-5', '22.0'),
	(799, 40.35510400, -3.83062800, 'A-5', '22.5'),
	(821, 40.39620700, -3.83256600, 'M-40', '36.4'),
	(826, 40.45863519, -3.81353934, 'M-40', '7.0'),
	(864, 40.45344800, -3.74311700, 'A-6', '14.0'),
	(866, 40.43493400, -3.71918100, 'A-6', '17.0'),
	(868, 40.47483500, -3.84200200, 'A-6', '18.5'),
	(872, 40.47449000, -3.83037300, 'A-6', '21.0'),
	(873, 40.47976700, -3.84865400, 'A-6', '22.0'),
	(877, 40.44790200, -3.73577400, 'A-6', '25.0'),
	(897, 40.62242000, -3.98954200, 'A-6', '5.0'),
	(926, 40.36480500, -3.69490200, 'M-40', '3.0'),
	(967, 40.30568500, -3.78326800, 'M-50', '8.0'),
	(971, 40.30691600, -3.65389900, 'M-50', '5.5'),
	(972, 40.29226800, -3.67510900, 'M-50', '4.5'),
	(1004, 40.50733900, -3.70979100, 'M-40', '40.0'),
	(1010, 40.49159171, -3.73758792, 'M-40', '6.0'),
	(1097, 40.53925200, -3.28073500, 'A-2', '40.0'),
	(1125, 40.40830500, -3.74309700, 'A-5', '28.0'),
	(1158, 40.45867900, -3.74766300, 'A-6', '20.0'),
	(1160, 40.45967500, -3.75061300, 'A-6', '22.0'),
	(1161, 40.48247100, -3.85581500, 'A-6', '22.5'),
	(1162, 40.50818300, -3.87816700, 'A-6', '23.0'),
	(1676, 40.25770900, -3.69004000, 'A-4', '12.0'),
	(1690, 40.01423000, -3.63239400, 'A-4', '11.0'),
	(167781, 40.35371980, -3.63772440, 'M-31', '2.5'),
	(169372, 40.34946110, -3.72301110, 'A-42', '6.5'),
	(169708, 40.73328860, -4.02400260, 'M-614', '28.0'),
	(169709, 40.73150000, -4.03265000, 'M-614', '28.5'),
	(169741, 40.44712800, -3.73450800, 'A-6', '30.0'),
	(174942, 40.46722500, -3.81260100, 'A-6', '4.0'),
	(174943, 40.47554500, -3.83884100, 'A-6', '4.5'),
	(174945, 40.49299940, -3.86812540, 'A-6', '5.0'),
	(175471, 40.66590900, -4.07948910, 'N-6', '7.5');

-- ─── TABLA: predicciones ─────────────────────────────────────────
-- (se crea al final porque tiene FK tanto a usuarios como a zonas)
CREATE TABLE IF NOT EXISTS `predicciones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) NOT NULL,
  `zona_id` int(11) DEFAULT NULL,
  `fecha_hora_prediccion` datetime DEFAULT NULL,
  `valor_ocupacion` int(11) DEFAULT NULL,
  `fecha_calculo` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  KEY `zona_id` (`zona_id`),
  CONSTRAINT `predicciones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  CONSTRAINT `predicciones_ibfk_2` FOREIGN KEY (`zona_id`) REFERENCES `zonas` (`id_zona`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla pc2.predicciones
INSERT INTO `predicciones` (`id`, `usuario_id`, `zona_id`, `fecha_hora_prediccion`, `valor_ocupacion`, `fecha_calculo`) VALUES
	(3, 2, 660, '2026-04-23 11:53:00', 1, '2026-04-23 09:53:14'),
	(4, 2, 169709, '2026-04-24 08:00:00', 0, '2026-04-24 20:04:19'),
	(5, 4, 866, '2026-05-11 08:00:00', 2, '2026-05-10 14:29:02'),
	(6, 3, 866, '2026-05-14 08:00:00', 2, '2026-05-13 20:58:09'),
	(7, 3, 1676, '2026-05-14 08:00:00', 1, '2026-05-13 21:24:46'),
	(14, 9, 926, '2026-05-21 08:00:00', 2, '2026-05-20 15:01:53'),
	(15, 9, 1097, '2026-05-21 08:00:00', 1, '2026-05-20 15:02:01'),
	(16, 9, 1097, '2026-05-21 08:00:00', 1, '2026-05-20 15:02:07'),
	(17, 9, 668, '2026-05-20 08:00:00', 2, '2026-05-20 16:33:25'),
	(18, 9, 660, '2026-05-20 08:00:00', 2, '2026-05-20 16:33:34');


/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
