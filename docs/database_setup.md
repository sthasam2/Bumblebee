# POSTGRES SETUP

**System: Linux**
**OS: UBUNTU 20.10**
 
[Digital Ocean Setup POstgres]([https://link](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-16-04))

## Steps

Follow the given steps to setup postgresql with django on your ubuntu machine

### Install components from ubuntu repositories

The following components are required for setting up postgresql with django

**Pre-Requirements**: python3, pip3, libpq

``` BASH
sudo apt install python3-pip python3-dev libpq-dev
```

**PostgreSQl componenets**: postgresql, postgresql-contrib

``` BASH
sudo apt install postgresql postgresql-contrib
```

### Create a Database and User

We need to setup a database ourselves. repeat the given steps to do so

* #### **Database**

1. Open postgres session

``` BASH
sudo -u postgres psql
```

2. Create database

``` SQL
CREATE DATABASE <name_of_database>;
```

*Note: Angular brackets <> denotes custom naming. DO NOT USE ANGULAR BRACKETS*

* #### **User**

``` SQL
CREATE USER <user_name> WITH PASSWORD 'password'; 
```

**Give permission to the user**

``` SQL
GRANT ALL PRIVILEGES ON DATABASE <db> TO <user>;
```

**Now we need to perform some additional steps to customize postgres according to Django preferences.**

``` SQL
ALTER ROLE user_name SET client_encoding TO 'utf8';
ALTER ROLE user_name SET default_transaction_isolation TO 'read committed';
ALTER ROLE user_name SET timezone TO 'UTC';
```

With this your database is setup on your linux machine

## Check created database

1. open postgres

``` BASH
sudo -u postgres psql
```

or 

``` BASH
bash$: sudo -i -u postgres
postgres$: psql
```

2. List Databases on the postgres server

 `\l`

**Output**:

``` 

                                  List of databases
   Name    |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges   
-----------+----------+----------+-------------+-------------+-----------------------
 bumblebee | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =Tc/postgres         +
           |          |          |             |             | postgres=CTc/postgres+
           |          |          |             |             | admin=CTc/postgres
 postgres  | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | 
 template0 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
           |          |          |             |             | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
           |          |          |             |             | postgres=CTc/postgres
(4 rows)
```
