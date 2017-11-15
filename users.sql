drop table users cascade;

create table users(
	username	varchar(80) not null unique,
	password	varchar(80) not null
);

insert into users values ('super', '1ns3cur3');
insert into users values ('user1', '1ns3cur3');

