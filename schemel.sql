-- schema.sql

drop database if exists awesome;

create database awesome;

use awesome;

grant select, insert, update, delete on awesome.* to 'www-data'@'localhost' identified by 'www-data';

create table users (
    `id` varchar(50) not null,
    `email` varchar(50) not null,
    `passwd` varchar(50) not null,
    `admin` bool not null,
    `name` varchar(50) not null,
    `image` varchar(500) not null,
    `created_at` real not null,
    unique key `idx_email` (`email`),
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table blogs (
    `id` varchar(50) not null,
    `user_id` varchar(50) not null,
    `user_name` varchar(50) not null,
    `user_image` varchar(500) not null,
    `name` varchar(50) not null,
    `summary` varchar(200) not null,
    `content` mediumtext not null,
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table comments (
    `id` varchar(50) not null,
    `blog_id` varchar(50) not null,
    `user_id` varchar(50) not null,
    `user_name` varchar(50) not null,
    `user_image` varchar(500) not null,
    `content` mediumtext not null,
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table usdt (
    `acceptOrder` bool not null,
    `availableAmount` real not null,
    `availableFromTime` varchar(20) not null,
    `availableToTime` varchar(20) not null,
    `best` int not null,
    `blacker` bool not null,
    `canPlaceOrder` bool not null,
    `clientAvgCompletedTime` varchar(20) not null,
    `clientAvgPaidTime` varchar(20) not null,
    `clientCancelledOrderQuantity` int not null,
    `clientCompletedOrderQuantity` int not null,
    `clientCompletionSecondsAvg` varchar(20) not null,
    `clientId` int not null,
    `clientKycLevel` varchar(20) not null,
    `clientName` varchar(50) not null,
    `clientPaymentSecondsAvg` varchar(20) not null,
    `completedAmount` real not null,
    `completedOrderQuantity` int not null,
    `completedOrderTotal` real not null,
    `createdDate` int not null,
    `digitalCurrencySymbol` varchar(20) not null,
    `exchangeRate` real not null,
    `exchangeRateDeviateTooFar` bool not null,
    `existPhone` bool not null,
    `floatRate` int not null,
    `frozenAmount` int not null,
    `index` int not null,
    `isBuy` bool not null,
    `legalCurrencySymbol` varchar(20) not null,
    `maxPlacePrice` int not null,
    `minKycLevel` int not null,
    `minPlacePrice` real not null,
    `publicTradingOrderId` int not null,
    `type` int not null
) engine=innodb default charset=utf8;