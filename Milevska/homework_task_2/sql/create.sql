drop table "ship";

create table "ship"
(
    ship_id integer not null,
    ship_number varchar(12) not null,
    ship_date date not null,
    ship_name varchar(40),
    ship_address varchar(100)
)