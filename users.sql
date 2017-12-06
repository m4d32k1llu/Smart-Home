drop table if exists users;

create table users(
	username	varchar(80) not null unique,
	password	varchar(60) not null
);

insert into users values ('super', '$2b$12$/lwyGZ0vbfEL7t0d35fMOObqjFkALtN7zekV2shSU05Ik2BJHGc9W');

