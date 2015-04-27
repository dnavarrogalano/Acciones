#-------------------------------------------------------------------------------
# Name:        Se?ales
# Purpose:
#
# Author:      DNG
#
# Created:     18/11/2014
# Copyright:   (c) Administrador2 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from trae_stocks import estrategiaMACD
import talib as ta
class Senales():
    def __init__(self):
       pass


    def stg_2RSI(self, stockValues):
        rsi2=ta.RSI(stockValues['Close'],2)
        
        
        
if __name__ == '__main__':
    f = estrategiaMACD('LAN')


