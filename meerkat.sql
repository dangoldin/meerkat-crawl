create table meerkat (
  source varchar(24) not null,
  target varchar(24) not null
);

LOAD DATA INFILE '/Users/danielgoldin/data/meerkat-out/network.csv'
into table meerkat
fields terminated by ','
enclosed by ''
lines terminated by '\n'
ignore 1 rows;

create index idx_source on meerkat(source);
create index idx_target on meerkat(target);

create table meerkat_users (
  userid varchar(24) not null,
  username varchar(100) not null,
  primary key (`userid`)
);

LOAD DATA INFILE '/Users/danielgoldin/data/meerkat-out/user_map.csv'
into table meerkat_users
fields terminated by ','
enclosed by ''
lines terminated by '\n';

select coalesce(u.username, m.source) as username, count(1) as num_following
from meerkat m
left join meerkat_users u on m.source = u.userid
group by source
order by num_following desc;

select coalesce(u.username, m.target) as username, count(1) as num_followers
from meerkat m
left join meerkat_users u on m.target = u.userid
group by target
order by num_followers desc;