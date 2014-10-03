-- This CLP file was created using DB2LOOK Version "10.5" 
-- Timestamp: Thu 02 Oct 2014 12:31:26 PM EDT
-- Database Name: SAMPLE         
-- Database Manager Version: DB2/LINUXX8664 Version 10.5.4 
-- Database Codepage: 1208
-- Database Collating Sequence is: IDENTITY
-- Alternate collating sequence(alt_collate): null
-- varchar2 compatibility(varchar2_compat): OFF


CONNECT TO SAMPLE;

----------------------------

-- DDL Statements for Views

----------------------------
SET CURRENT SCHEMA = "ASIF    ";
SET CURRENT PATH = "SYSIBM","SYSFUN","SYSPROC","SYSIBMADM","ASIF";
CREATE  view test_v as with total_cpu as ( select member, cast
(sum( agent_usr_cpu_time_s + (agent_usr_cpu_time_ms/1000000.0) + agent_sys_cpu_time_s
+ (agent_sys_cpu_time_ms/1000000.0)) as float) as total_cpu_s from sysibmadm.snapappl
group by member ) select i.snapshot_timestamp , i.agent_id as handle, i.primary_auth_id
as auth_id, i.appl_status as AppState, i.appl_name as prog_name , (agent_usr_cpu_time_s
+ (agent_usr_cpu_time_ms/1000000.0) + agent_sys_cpu_time_s + (agent_sys_cpu_time_ms/1000000.0))
as cpu_s , a.rows_read as rr, a.rows_written as rw , total_cpu_s from sysibmadm.snapappl_info
i, sysibmadm.snapappl a, total_cpu c where i.agent_id = a.agent_id and
i.member = a.member and a.member = c.member and c.total_cpu_s > 0;




COMMIT WORK;

CONNECT RESET;

TERMINATE;

