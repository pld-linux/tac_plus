# This file created by Devrim SERAL<devrim@gazi.edu.tr>
# For creating tac_plus related database and tables

CREATE DATABASE tacacs;
USE tacacs;

# id table fields are:
# name | surname | usern | tel | address 
# name : Real name
# surname : Surname
# usern : Account name 
# tel: Tel number
# address: Address

CREATE TABLE id ( name char(40) NOT NULL, surname char(40) NOT NULL,usern char(15) NOT NULL,tel char(20), address char(50) ,PRIMARY KEY(usern));

# auth tables fields are:
# usern | passwd | exp_time | time_limit | lck
# usern : Account name
# passwd : usern password
# exp_time : Expire date 
# time_limit : Time limiting
# lck : Adminstrative lock 

CREATE TABLE auth( usern CHAR(15) NOT NULL, passwd CHAR(15) NOT NULL, exp_time TIMESTAMP(8) NOT NULL ,time_limit CHAR(30) DEFAULT "*",lck ENUM("T","F") DEFAULT "F",PRIMARY KEY(usern) ); 

# acct tables fields are:
# usern | s_name | c_name | elapsed_time | bytes_in | bytes_out | fin_t
# usern : Account name
# s_name : Server name(RAS)
# c_name : Client Name
# elapsed_time : How much the user spent on router
# bytes_in : Incoming bytes to port
# bytes_out : Outgoing bytes from port
# fin_t :  When the accounting is finished
 
CREATE TABLE acct( usern CHAR(15) NOT NULL, s_name CHAR(30) NOT NULL, c_name CHAR(30) NOT NULL, elapsed_time INT NOT NULL, bytes_in INT DEFAULT 0, bytes_out INT  DEFAULT 0,fin_t TIMESTAMP(14) NOT NULL,INDEX acct_index(usern(10)));
