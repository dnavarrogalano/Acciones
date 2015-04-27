# -*- coding: cp1252 -*-
import urllib2
import urllib
import codecs
import numpy as np
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import talib as ta
folder='D:\\DEV\\stocks\\'
folderReportes='D:\\DNG\\'

RSILOW=5

if datetime.today().weekday()<5:
        fechahoy = datetime.now().strftime("%Y%m%d")
else:
        fechahoy = '19000101' # no acutalizar sabados y domingos (weekday = 5 y 6)
def traeStock(stockName):

        u = {'Symbol' : stockName}
        u = urllib.urlencode(u)
        print "u : " , u

        url = 'http://www.bolsadesantiago.cl/Theme/Data/Historico.aspx?' + u + '&dividendo=S'

        print url

        f = urllib2.urlopen(url)

        guarda = codecs.decode(f.read(),'utf-16').replace(',','.')

        output = codecs.open(folder + stockName + '.stk','w', 'utf-8')

        output.write(guarda)
        output.close()

'''function linkNemo()
	{
		var url = '/theme/resumenInstrumento.aspx?nemo=';
		var texto = document.getElementById('buscadorNemo');
		window.location.href = url + texto.value.toString();
	}
'''

def verificaArchivoStock(stockName):
    fileInput  = codecs.open(folder + stockName + '.stk','rb')
    print fileInput.read()


def abreArchivo(stockName):
    archivoDatos = codecs.open(folder + stockName + '.stk','r' )

    #data = np.genfromtxt(archivoDatos,skiprows=3)
    #data = np.fromfile(archivoDatos.read())

    stockFile =[]
    try:
            sourceCode = codecs.open(folder + stockName + '.stk','rb').read()
            splitSource = sourceCode.split('\n')
            for eachLine in splitSource[4:]:
                splitLine = eachLine.split(';')
                if len(splitLine)==6:
                    if 'values' not in eachLine:
                        stockFile.append(eachLine)
    except Exception, e:
            print str(e), 'failed to organize pulled data.'

    #date, openp, highp, lowp, closep,  volume = np.loadtxt(stockFile,delimiter=';', unpack=True
                                                               #   converters={ 0: mdates.strpdate2num('%Y%m%d')})

    return pd.read_csv(folder + stockName + ".stk", skiprows=2, delimiter=';')

    #variation = closep - openp

    #pronostico(closep, date )

'''    newAr = []
    while x < y:
        appendLine = date[x],openp[x],closep[x],highp[x],lowp[x],volume[x]
        newAr.append(appendLine)
        x+=1
    '''



def conectaDB():
    return  sqlite3.connect("d:/dev/stocks/stocks.sqlite")

def grabaRegistros(t):

    con = conectaDB()
    pd.io.sql.to_sql(t, "t_ohlcv", con, if_exists="append")


def fechaUltCarga():
        con = conectaDB()# sqlite3.connect("d:/dev/stocks/stocks.sqlite")
        q = "select max(Fecha) from t_ohlcv"
        try:
                cursor  = con.execute(q)
                aux = cursor.fetchall()
                fechaCarga = aux[0][0]
        except:
                fechaCarga = 19000101
                pass
        return int(fechaCarga)

def cargaArchivoAtablaOHLCV(forzarActualizacionDatos=False):
        con = conectaDB()# sqlite3.connect("d:/dev/stocks/stocks.sqlite")
        fechaCarga = fechaUltCarga()
        print 'ultima carga de datos : ' , fechaCarga , fechahoy
        if int(fechaCarga) < int(fechahoy) or forzarActualizacionDatos:
                print "TRAE ACCIONES DE LA BOLSA"
                con.execute("DROP TABLE IF EXISTS t_ohlcv")
                con.close()
                archivoStock = open(folder + 'listadoIGPA.dat')
                splitLines = archivoStock.read().split('\n')
                archivoStock.close
                for x in splitLines:
                        print x
                        traeStock(x)
                        f = abreArchivo(x)
                        f['NANO']=x
                        grabaRegistros(f)
                print 'crea Indice'
            #    con = conectaDB()
            #    con.execute ('create  index main.ix_fecha_nano on t_ohlcv (Fecha ASC, NANO ASC);')
            #   con.close()
        print "DATOS ACTUALIZADOS ", fechaCarga , fechahoy





def consultaOHLCV(nemo, fechaini, fechafin=0):
        q = """select NANO, Fecha, Close, Volume from t_ohlcv
                where NANO = '%s' and Fecha >= '%s'""" % (nemo, fechaini)
        con = conectaDB()
        cursor = con.execute(q)
        return cursor.fetchall()


def traeStockIntraDay(stockName):

        u = {'Symbol' : stockName}
        u = urllib.urlencode(u)
        print "u : " , u

        url = 'http://www.bolsadesantiago.com/Theme/Data/Intraday.aspx?' + u + '&dividendo=S'
        #  url='http://www.bolsadesantiago.com/Theme/Data/Intraday.aspx?Symbol=AZUL%20AZUL&dividendo=S'
        #urldia = 'http://www.bolsadesantiago.com/Theme/Data/Intraday.aspx?Symbol='+ u + 'dividendo=S'
        print url

        f = urllib2.urlopen(url)
        cols = ['Fecha','Open','High','Low','Close','Volume']
        guarda = codecs.decode(f.read(),'utf-16').replace(',','.').replace(';',',').split('\n')
        #data = pd.DataFrame(guarda)
        #return data
        return guarda[2:]

        output = codecs.open(folder + stockName + '.stk','w', 'utf-8')

        output.write(guarda)
        output.close()

'''function linkNemo()
	{
		var url = '/theme/resumenInstrumento.aspx?nemo=';
		var texto = document.getElementById('buscadorNemo');
		window.location.href = url + texto.value.toString();
	}
'''
def log(text):
        archivoOrdenes = open( folderReportes + 'ordenes_RSI2_' + fechahoy + '.csv','a')
        archivoOrdenes.write(text + '\n')
        archivoOrdenes.close()



def estrategiaRSI2():
        archivoStock = open(folder + 'listadoIGPA.dat')
        splitLines = archivoStock.read().split('\n')
        archivoStock.close
        encontrados = 0
        #log ('INICIO ==> estrategiaRSI2')
        log('INSTRUMENTO;MAX 40;MIN 40;MAXRATIO 40;MAX 20;MIN 20;MAXRATIO 20;HOY;RATIO HOY;')
        for x in splitLines:
                try:
                
                        if x<>'':
                                d =consultaOHLCV(x,"20040101",0)
                                data = pd.DataFrame (d, columns=['symbol','fecha','close','volume'])
                                f = data['fecha']
                                data.index = f
                                close = data['close']
                                bbands,bu,bd = ta.BBANDS(close.values)
                                rsi2 = ta.RSI(close.values,2)
                                data['SMA5'] = ta.SMA(close.values,5)
                                data['SMALONG'] = ta.SMA(close.values,100)
                                #data['bu'] = bu
                                #data['bd'] = bd
                                data['rsi2'] = rsi2

                               
                                
                               
                                indice = 0
                                for i in data.index:
                                        if indice > 10 :#and data.iloc[indice].close > data.iloc[indice].SMALONG:
                                                        if data.iloc[indice].rsi2 < RSILOW :
                                                                if i == int(fechahoy):
                                                                        maxClose = max(data.iloc[-20:-1].close.values)
                                                                        minClose = min(data.iloc[-20:-1].close.values)
                                                                        maxClose40 = max(data.iloc[-40:-1].close.values)
                                                                        minClose40 = min(data.iloc[-40:-1].close.values)
                                                                        maxVar =  minClose/maxClose
                                                                        maxVar40 =  minClose40/maxClose40
                                                                        bollingerDown = min(bbands[:-20])
                                                                        bollingerDownMax = max(bd[:-20])

                                                                        if bollingerDown <= bollingerDownMax:
                                                                                print x
                                                                        
                                                                        if maxVar < .95 or maxVar40 < .95:
                                                                                if data.iloc[indice].close == maxClose:
                                                                                        msjMaximo = ';hoy'
                                                                                else:
                                                                                        msjMaximo = ';'
                                                                                log( x + ';' + str(maxClose40) + ';' + str(minClose40) + ';' + str(round(100- maxVar40 *100,2))  + '%;'
                                                                                 + str(maxClose) + ';' + str(minClose) + ';' + str(round(100- maxVar *100,2))  + '%;' +  str(data.iloc[indice].close) + ';' + str(round(100-data.iloc[indice].close/maxClose*100,2)) + '%' + msjMaximo)
                                                                                                                                                 
                                                                        grabaestrategiaProc("estrategiaRSI2",fechahoy,x,"C",data.iloc[indice].close)
                                                                        encontrados+=1
                                                                        print "Encontrados : " , str(encontrados)
                                        indice+=1
                except Exception, e:
                        print str(e), 'Error en datos ' , x
                        pass

        #log ('FIN ==> Estrategia')


def estrategiaBBANDS():
        archivoStock = open(folder + 'listadoIGPA.dat')
        splitLines = archivoStock.read().split('\n')
        archivoStock.close
        encontrados = 0
        #log ('estrategiaBBANDS')
        #con = conectaDB()# sqlite3.connect("d:/dev/stocks/stocks.sqlite")
        #con.execute("DROP TABLE IF EXISTS t_indicadoresTA")
        for x in splitLines:
                try:
                        if x<>'':
                                d =consultaOHLCV(x,"20010101",0)
                                data = pd.DataFrame (d, columns=['symbol','fecha','close','volume'])
                                f = data['fecha']
                                data.index = f
                                close = data['close']
                                bbands,bu,bd = ta.BBANDS(close.values,9)
                                data['SMA5'] = ta.SMA(close.values,5)
                                data['SMA20'] = ta.SMA(close.values,20)
                                data['SMA50'] = ta.SMA(close.values,50)
                                data['SMA200'] = ta.SMA(close.values,200)
                                data['bu'] = bu
                                data['bd'] = bd
                                #data['bb'] = bbands
                                data['rsi'] = ta.RSI(close.values,5)
                                
                                del(data['fecha'])
                                grabaRegistrosTA(data)
                                indice = 0
                                
                                for i in data.index:
                                        if indice > 14 :
                                                if data.iloc[indice].SMA5 > data.iloc[indice-1].SMA5 :
                                                        if data.iloc[indice].rsi < 30  or data.iloc[indice - 1].rsi < 30:
                                                                if i == int(fechahoy):
                                                                      
                                                                        log(x + ';' + str(data.iloc[indice].close))
                                                                        grabaestrategiaProc("estrategiaBBANDS",fechahoy,x,"C",data.iloc[indice].close)
                                                                        encontrados+=1
                                                                       



                                        indice+=1
                                         
                except Exception, e:
                        print str(e), 'Error en datos ' , x
                        pass                
        #log ('FIN Estrategia')
        print "Encontrados : " , str(encontrados)

def estrategiaMACD(X):
                        d =consultaOHLCV(X,"20010101",0)
                        data = pd.DataFrame (d, columns=['symbol','fecha','close','volume'])
                        f = data['fecha']
                        data.index = f
                        return data

def grabaRegistrosTA(t):

    con = sqlite3.connect("d:/dev/stocks/stocks.sqlite")
    pd.io.sql.to_sql(t, "t_indicadoresTA", con, if_exists="append")

def grabaestrategiaProc(nom_estrategia, fecha, symbol,tipo_orden,valor_accion, comentario=''):
    fechaProceso = datetime.now()
    q = "insert into proc_estrategia(estrategia,fec_proc,fec_senal,Symbol,tipo_orden,valor_accion,Comentario) values (?,?,?,?,?,?,?)"
    conn = conectaDB()
    cur = conn.cursor()
    cur.execute(q, (nom_estrategia,fechaProceso, fecha,symbol,tipo_orden, valor_accion, comentario))
    conn.commit()
    lid = cur.lastrowid
    #print "The last Id of the inserted row is %d" % lid


def runBenchMark():
    
    
    fechahoy = datetime(2014,11,01)
    while int(fechahoy.strftime("%Y%m%d")) <= 20141120:
            print fechahoy
            cargaArchivoAtablaOHLCV()
            estrategiaRSI2()
            estrategiaBBANDS()
            fechahoy += timedelta(days=1)
    return


if __name__ == '__main__':

       
        #data = estrategiaMACD('HABITAT')
        #con = conectaDB()
        #con.execute ('create  index main.ix_fecha_nano on t_ohlcv (Fecha ASC, NANO ASC);')
        #con.close()
        #runBenchMark()
        #grabaestrategiaProc("prueba", 20141118,"PRUBEA","C",100,"")
        #fechahoy = '20141120'        
        cargaArchivoAtablaOHLCV()
        estrategiaRSI2()
        estrategiaBBANDS()
        
        print "FIN"
        #nemo = 'CENCOSUD'
        #fechaini = 20140101
        #q = """select Fecha, Close
        #from
        #t_ohlcv
        #      where NANO = '""" + nemo + """'  and Fecha >= """ + str(fechaini)
        #print q
        #con = conectaDB()
        #cursor = con.execute(q)
        #cursor = con.cursor()
        #json_string = json.dumps(dict(cursor.fetchall()))
        #records =  cursor.fetchall()
        #print json_string

        #datos = traeStockIntraDay('LAN')


        #cargaArchivoAtablaOHLCV()


        #archivoOrdenes = open('D:\DNG\ordenes_' + datatime.now() + '.txt','wb')

