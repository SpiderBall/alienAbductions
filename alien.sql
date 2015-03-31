DROP DATABASE IF EXISTS alien;
CREATE DATABASE  alien;
\c alien;
DROP TABLE IF EXISTS abductions;
CREATE TABLE abductions (
    id serial NOT NULL,
    first varchar(40) NOT NULL default '',
    last varchar(40) NOT NULL default '',
    handle varchar(40), 
    month int,
    day int, 
    year int, 
    city varchar(40), 
    state varchar(5), 
    scary int, 
    attributes varchar(100));