drop function get_user_access_level (usr_id int, usr_login text);

/* Getting access level */
create or replace function get_user_access_level (usr_id int, usr_login text)
	returns table (
	    acs_l int,
	    u_id int
	)
	language plpgsql
as $$
begin
    return query
                select acs_level as acs_l, id as u_id from inner_s.users where id = usr_id and login = usr_login;
end;$$;

select * from inner_s.users;

/* Getting passport ID */
create or replace function get_citizen_id_by_passport_id(passport_id int)
returns int language plpgsql as $$
    declare citizen_id_found boolean;
    begin
        select "CitizenID" into citizen_id_found from w_dir."Citizens" where "passportID"=passport_id;

        return citizen_id_found;
    end;
    $$;

