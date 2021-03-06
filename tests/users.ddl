-- This CLP file was created using DB2LOOK Version "10.5" 
-- Timestamp: Sun 28 Sep 2014 12:42:01 PM EDT
-- Database Name: SAMPLE         
-- Database Manager Version: DB2/LINUXX8664 Version 10.5.4 
-- Database Codepage: 1208
-- Database Collating Sequence is: IDENTITY
-- Alternate collating sequence(alt_collate): null
-- varchar2 compatibility(varchar2_compat): OFF


CONNECT TO SAMPLE;

------------------------------------------------
-- DDL Statements for Table "ASIF    "."USERS"
------------------------------------------------
 

CREATE TABLE "ASIF    "."USERS"  (
		  "ID" INTEGER NOT NULL GENERATED BY DEFAULT AS IDENTITY (  
		    START WITH +1  
		    INCREMENT BY +1  
		    MINVALUE +1  
		    MAXVALUE +2147483647  
		    NO CYCLE  
		    CACHE 20  
		    NO ORDER ) , 
		  "EMAIL" VARCHAR(64 OCTETS) , 
		  "USERNAME" VARCHAR(64 OCTETS) , 
		  "ROLE_ID" INTEGER , 
		  "PASSWORD_HASH" VARCHAR(128 OCTETS) , 
		  "CONFIRMED" SMALLINT )   
		 IN "IBMDB2SAMPLEREL"  
		 ORGANIZE BY ROW; 


-- DDL Statements for Primary Key on Table "ASIF    "."USERS"

ALTER TABLE "ASIF    "."USERS" 
	ADD PRIMARY KEY
		("ID");



-- DDL Statements for Indexes on Table "ASIF    "."USERS"

SET NLS_STRING_UNITS = 'SYSTEM';

CREATE UNIQUE INDEX "ASIF    "."IX_USERS_EMAIL" ON "ASIF    "."USERS" 
		("EMAIL" ASC)
		
		COMPRESS NO 
		INCLUDE NULL KEYS ALLOW REVERSE SCANS;

-- DDL Statements for Indexes on Table "ASIF    "."USERS"

SET NLS_STRING_UNITS = 'SYSTEM';

CREATE UNIQUE INDEX "ASIF    "."IX_USERS_USERNAME" ON "ASIF    "."USERS" 
		("USERNAME" ASC)
		
		COMPRESS NO 
		INCLUDE NULL KEYS ALLOW REVERSE SCANS;

-- DDL Statements for Foreign Keys on Table "ASIF    "."USERS"

ALTER TABLE "ASIF    "."USERS" 
	ADD CONSTRAINT "SQL140928124121740" FOREIGN KEY
		("ROLE_ID")
	REFERENCES "ASIF    "."ROLES"
		("ID")
	ON DELETE NO ACTION
	ON UPDATE NO ACTION
	ENFORCED
	ENABLE QUERY OPTIMIZATION;

-- DDL Statements for Check Constraints on Table "ASIF    "."USERS"

SET NLS_STRING_UNITS = 'SYSTEM';

ALTER TABLE "ASIF    "."USERS" 
	ADD CONSTRAINT "SQL140928124121750" CHECK 
		(CONFIRMED IN (0, 1))
	ENFORCED
	ENABLE QUERY OPTIMIZATION;







COMMIT WORK;

CONNECT RESET;

TERMINATE;

