create database bumblebee;

create user admin with encrypted password admin;

grant all privileges on database bumblebee to "admin";

ALTER ROLE admin
SET
    client_encoding TO 'utf8';

ALTER ROLE admin
SET
    default_transaction_isolation TO 'read committed';

ALTER ROLE admin
SET
    timezone TO 'UTC';