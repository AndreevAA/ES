/* Deleting citizen */
create or replace function delete_citizen(citizen_id int)
returns boolean as $$
declare not_passed boolean;
begin
        /* Deleting */
        delete from w_dir."Citizens" where "CitizenID" = citizen_id;

        /* Verification */
        SELECT  ("CitizenID" = citizen_id) INTO not_passed
        FROM    w_dir."Citizens"
        WHERE   "CitizenID" = citizen_id;

        RETURN not_passed;
end;
$$  language plpgsql;

/* Deleting education */
create or replace function delete_education(education_level_id int)
returns boolean as $$
declare not_passed boolean;
declare cur_user;
begin
        /* level access */
        select current_user into cur_user;

        /* Deleting */
        delete from w_dir."EducationsLevels" where "EducationLevelID" = education_level_id;

        /* Verification */
        SELECT  ("EducationLevelID" = education_level_id) INTO not_passed
        FROM    w_dir."EducationsLevels"
        WHERE   "EducationLevelID" = education_level_id;

        RETURN not_passed;
end;
$$  language plpgsql
