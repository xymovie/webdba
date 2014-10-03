create or replace  view test_v
as

with total_cpu as (
    select member, cast (sum(
        agent_usr_cpu_time_s + (agent_usr_cpu_time_ms/1000000.0)
        + agent_sys_cpu_time_s + (agent_sys_cpu_time_ms/1000000.0)) as float) as total_cpu_s
    from sysibmadm.snapappl
    group by member
)

select 
i.snapshot_timestamp
, i.agent_id as handle, i.primary_auth_id as auth_id, i.appl_status as AppState, i.appl_name as prog_name
, (agent_usr_cpu_time_s + (agent_usr_cpu_time_ms/1000000.0)
    + agent_sys_cpu_time_s + (agent_sys_cpu_time_ms/1000000.0)) as cpu_s
, a.rows_read as rr, a.rows_written as rw
, total_cpu_s
from sysibmadm.snapappl_info i, sysibmadm.snapappl a, total_cpu c
where i.agent_id = a.agent_id
and i.member = a.member
and a.member = c.member
and c.total_cpu_s > 0
;
