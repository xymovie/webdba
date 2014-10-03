"""
db2.py
=========

This module provides DB2 interface.

:copyright: (c) 2014 by Asif Jalil.
:license:   BSD, see LICENSE for more details.
"""

from __future__ import print_function
import logging
import pprint
import ibm_db
import re

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

def _date_handler(o):
    return o.isoformat() if hasattr(o, 'isoformat') else 0

class DB2(object):
    
    #app = current_app._get_current_object()

    def __init__(self, app):
        self._conn = None
        self.app = app._get_current_object()

    def __enter__(self):
        try:
            self._conn = ibm_db.pconnect(self.app.config['DBNAME']
                    , self.app.config['DBUSER']
                    , self.app.config['DBPW'])
        except:
            log.error("Database connection failed.")
            log.error(ibm_db.conn_errormsg())
            raise
        else:
            log.debug("Connected to {dbname} user {dbuser} using ****".format(dbname = self.app.config['DBNAME']
                , dbuser = self.app.config['DBUSER']))
        
        return self

    def __exit__(self, exc_type, exc_val, exc_tb): 
        if self._conn:
            ibm_db.close(self._conn) 
            log.debug("Closed {dbname} connection.".format(dbname = self.app.config['DBNAME']))


    def _create_table(self, ddl):
        result = ibm_db.exec_immediate(self._conn, ddl)

    def query_db(self, query, args=()):
        """Submits database query.
    
        Examples:
    
        for user in query_db('select * from users'):
            print user['username'], 'has the id', user['user_id']
        
        for user in query_db('select * from users where username = ?', [the_username]):
            print user['username'], 'has the id', user['user_id']

        Returns list
        list = list of rows, where each row is represented using tuple
        """
        rows = []
        if self._conn:
            log.debug("Running query\n" + query)
            log.debug("Query params: " + pprint.pformat(args))
            stmt = ibm_db.prepare(self._conn, query)
    
            for i, param in enumerate(args):
                ibm_db.bind_param(stmt, i, param)
    
            ibm_db.execute(stmt)
            if re.search('create|insert|update|delete', query, re.I):
                return rows

            row = ibm_db.fetch_tuple(stmt)
            while (row):
                rows.append(row)
                row = ibm_db.fetch_tuple(stmt)

        return rows


    def _check_table(self, tabschema, tabname):
        """ Checks if a table is defined.
            Returns True if defined, False otherwise.
        """
        cols = []
        rows = []
        log.debug("Checking if {tabschema}.{tabname} exist".format(tabschema = tabschema, tabname = tabname))
        try:
            self.query_db("select 1 from {tabschema}.{tabname}".format(tabschema = tabschema, tabname = tabname))
            log.debug("Exist.")
            return True
        except:
            if 'is an undefined name' in ibm_db.stmt_errormsg(): 
                return False
            else:
                raise

    def snapappl(self, member = None):
        """Returns DB2 application snapshot.
        """
        cols = []
        rows = []
        dgt_schema = "session"
        dgt_name = "snapappl"
        dgt_ddl = """
        declare global temporary table session.snapappl (
                SNAPSHOT_TIMESTAMP TIMESTAMP
                ,  MEMBER SMALLINT
                ,  HANDLE BIGINT
                ,  APPL_ID VARCHAR(128)
                ,  SEQUENCE_NO VARCHAR(4)
                ,  AUTH_ID VARCHAR(128)
                ,  APPSTATE VARCHAR(22)
                ,  PROG_NAME VARCHAR(256)
                ,  CPU_S DEC(31,11)
                ,  RR BIGINT
                ,  RW BIGINT
                ,  TOTAL_CPU_S DOUBLE
                ) on commit preserve rows
                  not logged

        """

        snapappl_delete = """
        delete from {dgt_schema}.{dgt_name}
        where snapshot_timestamp not in ( select max(snapshot_timestamp)
                                          from {dgt_schema}.{dgt_name})
        """.format(dgt_schema = dgt_schema, dgt_name = dgt_name)

        snapappl_insert = """
        insert into {dgt_schema}.{dgt_name}
            with total_cpu as (
            select member, cast (sum(
            agent_usr_cpu_time_s + (agent_usr_cpu_time_ms/1000000.0)
                + agent_sys_cpu_time_s + (agent_sys_cpu_time_ms/1000000.0)) as float) as total_cpu_s
            from sysibmadm.snapappl
            group by member
        )

        select
        i.snapshot_timestamp
        , i.member
        , i.agent_id as handle
        , i.appl_id
        , i.sequence_no
        , i.primary_auth_id as auth_id
        , i.appl_status as AppState
        , i.appl_name as prog_name
        , (agent_usr_cpu_time_s + (agent_usr_cpu_time_ms/1000000.0)
        + agent_sys_cpu_time_s + (agent_sys_cpu_time_ms/1000000.0)) as cpu_s
        , a.rows_read as rr, a.rows_written as rw
        , total_cpu_s
        from sysibmadm.snapappl_info i, sysibmadm.snapappl a, total_cpu c
        where i.agent_id = a.agent_id
        and i.member = a.member
        and a.member = c.member
        and c.total_cpu_s > 0
        """.format(dgt_schema = dgt_schema, dgt_name = dgt_name)

        member_clause = ""
        if member:
            member_clause = " where member = {member} ".format(member = member)

        snapappl_delta = """
        select handle, auth_id, appstate, prog_name
        , cast (100 * (sum(cpu_s) / sum(total_cpu_s)) as dec(5,2)) as "CPU%"
        , int(sum(rr)/max(tm_s)) as "RR/s"
        , int(sum(rw)/max(tm_s)) as "RW/s"
        from (
            select handle, auth_id, appstate, prog_name
            , cpu_s - lag(cpu_s) over(partition by appl_id, sequence_no, member order by snapshot_timestamp) as cpu_s
            , rr - lag(rr) over (partition by appl_id, sequence_no, member order by snapshot_timestamp) as rr
            , rw - lag(rw) over (partition by appl_id, sequence_no, member order by snapshot_timestamp) as rw
            , total_cpu_s - lag(total_cpu_s) over (partition by appl_id, sequence_no, member order by snapshot_timestamp) as total_cpu_s
            , timestampdiff(2, CHAR(snapshot_timestamp - lag(snapshot_timestamp) 
                over (partition by appl_id, sequence_no, member order by snapshot_timestamp))) as tm_s
            from {dgt_schema}.{dgt_name}
            {member_clause}
            ) x
        where x.total_cpu_s > 0
        and x.tm_s > 0
        group by handle, auth_id, appstate, prog_name
        order by "CPU%" desc
        """.format(dgt_schema = dgt_schema, dgt_name = dgt_name, member_clause = member_clause)

        if not self._check_table(dgt_schema, dgt_name):
            self._create_table(dgt_ddl)
            self.query_db(snapappl_insert)

        self.query_db(snapappl_insert)
        cols = ['Handle', 'AuthID', 'AppState', 'ProgNm', 'CPU%', 'RR/s', 'RW/s']
        rows = self.query_db(snapappl_delta)
        self.query_db(snapappl_delete)

        return cols, rows
