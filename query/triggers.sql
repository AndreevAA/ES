/* Deleting connected elements (Citizen only with passport.) */
create trigger delete_passport
after delete
on w_dir.passports
for each row execute function delete_citizen(get_citizen_id_by_passport_id(passport_id));

/* Deleting Education information while citizen deleting */
create trigger delete_citizen
    after delete on w_dir."Citizens"
    for each row execute function delete_education("educationsLevelsID");