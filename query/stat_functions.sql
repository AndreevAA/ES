/* People */
drop function cit_alive_rate_by_year_city(city text);

create or replace function cit_alive_rate_by_year_city (city text)
	returns table (
		year_birth decimal,
		cnt bigint
	)
	language plpgsql
as $$
begin

    if city = 'Not stated' then
            return query
                select extract(year from "birth_date") as year_birth, count(extract(year from "birth_date")) as cnt from w_dir.passports group by year_birth order by year_birth;
        else
            return query
              select extract(year from "birth_date") as year_birth, count(extract(year from "birth_date")) as cnt from w_dir.passports where "is_depth"=false and registration=city group by year_birth order by year_birth;
    end if;
end;$$;

/* Birth */
drop function birth_rate_by_year_city(city text);

create or replace function birth_rate_by_year_city (city text)
	returns table (
		year_birth decimal,
		cnt bigint
	)
	language plpgsql
as $$
begin
    if city = 'Not stated' then return query select extract(year from "birth_date") as year_birth, count(extract(year from "birth_date")) as cnt from w_dir.passports group by year_birth order by year_birth;
        else return query select extract(year from "birth_date") as year_birth, count(extract(year from "birth_date")) as cnt from w_dir.passports where registration=city group by year_birth order by year_birth;
    end if;
end;$$;

/* Depth */
drop function depth_rate_by_year_city(city text);

create or replace function depth_rate_by_year_city (city text)
	returns table (
		year_depth decimal,
		cnt bigint
	)
	language plpgsql
as $$
begin
    if city = 'Not stated' then
        return query
            select extract(year from "depth_date") as year_depth, count(extract(year from "depth_date")) as cnt from w_dir.passports where is_depth=true group by year_depth order by year_depth;
    else
        return query
            select extract(year from "depth_date") as year_depth, count(extract(year from "depth_date")) as cnt from w_dir.passports where is_depth=true and registration=city group by year_depth order by year_depth;
    end if;
end;$$;

select * from depth_rate_by_year_city('Not stated');

/* Life length */
drop function life_length_rate_by_year_city(city text);

create or replace function life_length_rate_by_year_city (city text)
	returns table (
	    ll numeric,
	    cnt bigint
	)
	language plpgsql
as $$
begin
    if city = 'Not stated'
        then
            return query
                select (extract(year from "depth_date") - extract(year from "birth_date")) as ll, count(extract(year from"depth_date") - extract(year from "birth_date")) as cnt from w_dir.passports where is_depth=true group by ll order by ll;
    else
        return query
            select (extract(year from "depth_date") - extract(year from "birth_date")) as ll, count(extract(year from"depth_date") - extract(year from "birth_date")) as cnt from w_dir.passports where is_depth=true and registration=city group by ll order by ll;
        end if;
end;$$;

