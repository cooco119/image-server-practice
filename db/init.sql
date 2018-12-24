-- To initialize db, use following command
-- psql -h 192.168.99.100 -p 5432 -U postgres -f ./db/init.sql

CREATE DATABASE practicedb;
\c practicedb;
CREATE TABLE USERS (
    ID      SERIAL  PRIMARY KEY     NOT NULL,
    NAME    VARCHAR(50)             NOT NULL,
    ISMEM   BOOLEAN                 NOT NULL
);
CREATE TABLE IMAGE (
    ID      SERIAL  PRIMARY KEY     NOT NULL,
    NAME    VARCHAR(50)             NOT NULL,
    IMG_OID OID                             ,
    UID     INTEGER REFERENCES USERS(ID)     ,
    ISPRIVATE   BOOLEAN             NOT NULL
);