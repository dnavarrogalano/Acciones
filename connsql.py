import pyodbc
import numpy
import simplejson as json

def connect():
	#conn = pyodbc.connect('Provider={SQL Server};SERVER=bchapp430;UID=mkt;Psw=mktbanco01')
	#conn = pyodbc.connect('Data Source=bchapp430;User ID=mkt;Initial Catalog=BCH;Driver=SQLOLEDB.1;Auto Translate=False;Pwd=mktbanco01;')
	conn = pyodbc.connect('DRIVER={SQL Server};SERVER=bchapp430;DATABASE=ETL_LogAuditDB;UID=mkt;PWD=mktbanco01')
	cur = conn.cursor()
	cur.execute('select top 10 prm_tabla, prm_valor_1  from bch..param ')
	results = cur.fetchall()
	rows=[]
	for x in results:
		t=dict(x.prm_tabla , x.prm_valor_1)
		rows.append (t)
		#print x.prm_tabla , x.prm_valor_1
	#results_as_list = [i[0] for i in results]
	#array = numpy.fromiter(results_as_list, dtype=numpy.int32)
	#print array
	#for i in results:
		#print i[1], i[3], i[5]
	#	print json.dumps([1], i[3], i[5])
	j = json.dumps(rows)
	print j
connect()	




url = 'http://www.bolsadesantiago.cl/Theme/Data/Historico.aspx?Symbol=BANMEDICA&dividendo=S'

import urllib2
mp3file = urllib2.urlopen("http://www.example.com/songs/mp3.mp3")
output = open('test.mp3','wb')
output.write(mp3file.read())
output.close()
