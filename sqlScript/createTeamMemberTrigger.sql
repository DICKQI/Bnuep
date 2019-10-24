user Bnuep;
create trigger teamMemberCancel
    after update
    on Contest_Contest
    for each row
begin
    if (NEW.contestStatus = 'RegisterDeadline')
    then
        update contest_teammember
            set is_cancel=true where is_cancel=false;
    end if;
end;