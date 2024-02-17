# Taxi telegram bot 

***
## Описание

Бот, который выполняет функции диспетчера такси.

## Установка

Для установки зависимостей лучше использовать Poetry, так как это более современный и удобный инструмент для управления зависимостями.

```
pip install poetry
poetry install
```

Если вы используете `pip` напрямую, можно воспользоваться командой:

`pip install -r poetry.lock`

Создайте файл .env и задайте значения следующим переменным:
  1. TOKEN - токен телеграм бота
  2. CHAT_ID - id чата, который будет использоваться для получения заказов
  3. DB_NAME - название базы данных
  4. HOST
  5. PORT
  6. USER 
  7. PASS

Дамп бд:
```sql
-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Версия сервера: 10.4.21-MariaDB
-- Версия PHP: 8.0.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `taxi`
--

-- --------------------------------------------------------

--
-- Структура таблицы `drivers`
--

CREATE TABLE `drivers` (
  `id` bigint(20) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL,
  `number` varchar(15) DEFAULT NULL,
  `car_model` varchar(20) DEFAULT NULL,
  `car_color` varchar(20) DEFAULT NULL,
  `car_number` varchar(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `address_from` varchar(50) NOT NULL,
  `address_to` varchar(50) NOT NULL,
  `date` varchar(30) NOT NULL,
  `id_user` bigint(11) NOT NULL,
  `status` enum('active','inactive','cancel') NOT NULL,
  `id_order_message` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` bigint(11) NOT NULL,
  `number` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `drivers`
--
ALTER TABLE `drivers`
  ADD UNIQUE KEY `id` (`id`);

--
-- Индексы таблицы `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=116;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
```

## Использование

Добавьте бота в выбранный чат, в нём должны находиться только водители.

Используйте команду `/start` в телеграм боте, чтобы начать использовать бота.

Команда ```/driver``` используется для регистрации водителей.

Пользователь сначала должен пройти регистрацию и после может создавать заказ.
Водитель, чтобы принимать заказ, тоже должен пройти регистрацию.

Заказ отсылается в чат, где водители могут принять его. После взятия заказа, бот присылает пользователю оповещение о водителе (нмя, номер телефона, данные автомобиля)

Пользователь может отменить заказ в любой момент и подтвердить его по завершении
