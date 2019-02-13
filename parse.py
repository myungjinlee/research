#!/usr/bin/env python2

inp_file='lj.lib'

import sqlite3

connection=sqlite3.connect(':memory:')
cursor=connection.cursor()

query='CREATE TABLE lj(atom_name TXT, res_name TXT, a FLOAT, b FLOAT )'
cursor.execute(query)

query='CREATE INDEX lj_a_indx ON lj(atom_name,res_name,a,b)'
cursor.execute(query)

with open(inp_file,'r') as f_obj:
   for line in f_obj:
      tmp=line.rstrip().split()
      if len(tmp)==6:
         query='INSERT INTO lj VALUES(?,?,?,?)'
         cursor.execute(query,(tmp[0],tmp[2],float(tmp[3]),float(tmp[4]),))


pdb_in='CLOSED_membrane.pdb'

with open(pdb_in,'r') as f_obj:
   for line in f_obj:
      if line[0:6]=='ATOM  ':
         if line[17:20].split()[0]!='MEB':
            query='SELECT a,b FROM lj WHERE atom_name=? AND res_name=?'
            cursor.execute(query,(line[12:16].split()[0],line[17:20].split()[0],))
            for i in cursor.fetchall():
                  print i


query='UPDATE lj SET a=0.0 WHERE atom_name="N"'
cursor.execute(query)

query='SELECT * FROM (SELECT * FROM lj WHERE res_name="A*2") WHERE atom_name LIKE "%N" AND res_name LIKE "%*2"'
cursor.execute(query)
for i in cursor.fetchall():
    print i


connection.close()
