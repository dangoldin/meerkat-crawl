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

select num_following, count(1) as num_in_bucket
from (
  select coalesce(u.username, m.source) as username, count(1) as num_following
  from meerkat m
  left join meerkat_users u on m.source = u.userid
  group by source
  order by num_following desc
) d
group by num_following
order by num_following asc;

select coalesce(u.username, m.target) as username, count(1) as num_followers
from meerkat m
left join meerkat_users u on m.target = u.userid
group by target
order by num_followers desc;

select num_followers, count(1) as num_in_bucket
from (
  select coalesce(u.username, m.target) as username, count(1) as num_followers
  from meerkat m
  left join meerkat_users u on m.target = u.userid
  group by target
  order by num_followers desc
) d
group by num_followers
order by num_followers asc;

-- High volume investigation
select u1.username as source, u2.username as target
from meerkat m
join meerkat_users u1 on m.source = u1.userid
join meerkat_users u2 on m.target = u2.userid
join (
  select target
  from meerkat m
  group by target
  having count(1) > 100
) high_vol_target on high_vol_target.target = m.target
join (
  select source
  from meerkat m
  group by source
  having count(1) > 10
) high_vol_source on high_vol_source.source = m.source;

-- High volume into a file
select *
  from (
  select u1.username as source, u2.username as target
  from meerkat m
  join meerkat_users u1 on m.source = u1.userid
  join meerkat_users u2 on m.target = u2.userid
  join (
    select target
    from meerkat m
    group by target
    having count(1) > 100
  ) high_vol_target on high_vol_target.target = m.target
  join (
    select source
    from meerkat m
    group by source
    having count(1) > 100
  ) high_vol_source on high_vol_source.source = m.source
) d into outfile '/tmp/meerkat_high.csv'
fields terminated by ','
enclosed by ''
lines terminated by '\n';

select *
from (
  select u1.username as source, u2.username as target
  from meerkat m
  join meerkat_users u1 on m.source = u1.userid
  join meerkat_users u2 on m.target = u2.userid
  where m.source not in (
    select target
    from meerkat m
    group by target
    having count(1) > 500
    union
    select source
    from meerkat m
    group by source
    having count(1) > 500
  ) and m.target not in (
    select target
    from meerkat m
    group by target
    having count(1) > 500
    union
    select source
    from meerkat m
    group by source
    having count(1) > 500
  )
) d into outfile '/tmp/meerkat_500.csv'
fields terminated by ','
enclosed by ''
lines terminated by '\n';

create table meerkat_high_vol as
    select target as userid
    from meerkat m
    group by target
    having count(1) > 500
    union
    select source as userid
    from meerkat m
    group by source
    having count(1) > 500;

create index idx_userid on meerkat_high_vol(userid);

select *
from (
  select u1.username as source, u2.username as target
  from meerkat m
  join meerkat_users u1 on m.source = u1.userid
  join meerkat_users u2 on m.target = u2.userid
  join meerkat_high_vol mh1 on m.source = mh1.userid
  join meerkat_high_vol mh2 on m.target = mh2.userid
) d into outfile '/tmp/meerkat_500.csv'
fields terminated by ','
enclosed by ''
lines terminated by '\n';

