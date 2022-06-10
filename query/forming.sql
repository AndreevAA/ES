
drop table w_dir.passports;

create table w_dir.passports  (
    passport_ID int,
    name text,
    surname text,
    patronymic text,
    registration text,
    children_Number int,
    is_Married_Now bool,
    birth_Date date,
    is_Depth bool,
    depth_Date date,
    primary key (passport_ID)
);
