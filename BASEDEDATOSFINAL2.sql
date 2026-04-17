-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         10.4.32-MariaDB - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.10.0.7000
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

-- Volcando estructura para tabla pc2.predicciones
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla pc2.predicciones: ~0 rows (aproximadamente)

-- Volcando estructura para tabla pc2.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `rol` enum('admin','usuario') NOT NULL DEFAULT 'usuario',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla pc2.usuarios: ~1 rows (aproximadamente)
INSERT INTO `usuarios` (`id`, `username`, `email`, `password`, `rol`) VALUES
	(1, 'test', 'test@test.com', '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244', 'usuario');

-- Volcando estructura para tabla pc2.zonas
CREATE TABLE IF NOT EXISTS `zonas` (
  `id_zona` int(11) NOT NULL,
  `latitud` decimal(10,8) DEFAULT NULL,
  `longitud` decimal(11,8) DEFAULT NULL,
  `carretera` varchar(50) DEFAULT NULL,
  `pk` varchar(20) DEFAULT NULL,
  `imagen_url` varchar(255) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  PRIMARY KEY (`id_zona`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla pc2.zonas: ~45 rows (aproximadamente)
INSERT IGNORE INTO `zonas` (`id_zona`, `latitud`, `longitud`, `carretera`, `pk`) VALUES
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
(771, 40.27263700, -3.75309600, 'A-42', '8.5'),
(773, 40.29565500, -3.73738400, 'A-42', '10.5'),
(791, 40.38056000, -3.78959900, 'A-5', '18.0'),
(798, 40.40342100, -3.75584300, 'A-5', '22.0'),
(799, 40.35510400, -3.83062800, 'A-5', '22.5'),
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
(169372, 40.34946110, -3.72301110, 'A-42', '6.5'),
(169708, 40.73328860, -4.02400260, 'M-614', '28.0'),
(169709, 40.73150000, -4.03265000, 'M-614', '28.5'),
(169741, 40.44712800, -3.73450800, 'A-6', '30.0'),
(174942, 40.46722500, -3.81260100, 'A-6', '4.0'),
(174943, 40.47554500, -3.83884100, 'A-6', '4.5'),
(174945, 40.49299940, -3.86812540, 'A-6', '5.0'),
(175471, 40.66590900, -4.07948910, 'N-6', '7.5');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
