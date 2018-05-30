-- schema.sql

drop database if exists awesome;

create database awesome;

use awesome;

grant select, insert, update, delete on awesome.* to 'www-data'@'localhost' identified by 'www-data';

create table coinProfit (
    `id` varchar(50) not null,
    `fromType` varchar(10) not null,
    `toType` varchar(10) not null,
    `fromMinSalePrice` real not null,
    `fromMaxBuyPrice` real not null,
    `toMinSalePrice` real not null,
    `toMaxBuyPrice` real not null,
    `lastVs` real not null,
    `buy` real not null,
    `sell` real not null,
    `fromJson` varchar(200) not null,
    `toJson` varchar(200) not null,
    `vsJson` varchar(200) not null,
    `fromToProfit` real not null,
    `toFromProfit` real not null,
    `createdTime` real not null
) engine=innodb default charset=utf8;