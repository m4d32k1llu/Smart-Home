drop table users cascade;

create table users(
	username	varchar(80) not null unique,
	password	varchar(60) not null
);

insert into users values ('super', '$2b$12$hyx1Z83DP9vyaOYvdbz3GO7tPX5BtQ/qA9aoOThrrjYO9JkbZ0MFC');

