create or replace function is_update_user_available(id_i int, login_i text, password_i text)
    returns table
            (
                id_t int
            ) language plpgsql as
    $$
        begin
            return query select id as id_t from inner_s.users where id = id_i or login = login_i or password = password_i;
        end;
    $$;

select * from is_update_user_available(0, 'andreev@easyguest.ru', 'qwerty')