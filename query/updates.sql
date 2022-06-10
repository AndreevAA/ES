create or replace function update_user(id_i int, login_i text, password_i text, acs_level_i int)
returns boolean language plpgsql as $$
    begin
        update inner_s.users
               SET login = login_i,
                   password = password_i,
                   acs_level  = acs_level_i
             WHERE id = id_i;
            RETURN FOUND;
        end;
    $$;

select * from update_user(0, 'andreev@easyguest.ru', 'qwerty', 1);

create or replace function create_user(id_i int, login_i text, password_i text, acs_level_i int)
returns boolean language plpgsql as $$
    begin
        insert into inner_s.users (id, login, password, acs_level) values (id_i, login_i, password_i, acs_level_i);
        return FOUND;
        end;
    $$;


