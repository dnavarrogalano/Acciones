
#x = open ("D:\marketing\FILES\INPUT\TARGET_NEW.OUT" ,'r')
x = open ("\\\\bchapp430\d$\Marketing\FILES\INPUT\TARGET_NEW.OUT" ,'r')


o = open ("d:\salidaCompara.txt2" , 'wb')
o.write (x.readline())
o.write (x.readline())
o.write (x.readline())
o.write (x.readline())
o.write (x.readline())
o.write (x.readline())
o.write (x.readline())
o.write (x.readline())

o.close()
x.close()
    
print "termino"
