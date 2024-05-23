SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `drivers` (
  `id` bigint(20) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL,
  `number` varchar(15) DEFAULT NULL,
  `car_model` varchar(20) DEFAULT NULL,
  `car_color` varchar(20) DEFAULT NULL,
  `car_number` varchar(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `address_from` varchar(50) NOT NULL,
  `address_to` varchar(50) NOT NULL,
  `date` varchar(30) NOT NULL,
  `id_user` bigint(11) NOT NULL,
  `status` enum('active','inactive','cancel') NOT NULL,
  `id_order_message` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `users` (
  `id` bigint(11) NOT NULL,
  `number` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `drivers`
  ADD UNIQUE KEY `id` (`id`);

ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=116;
COMMIT;
