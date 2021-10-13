import time
import rrdtool
from Notify import *
from getSNMP import consultaSNMP
import threading

class HandlerSNMP:

    def __init__(self, path_rrd, name_rrd):
        self.path_rrd = path_rrd
        self.name_rrd = name_rrd

    def create(self, type):
        ret = rrdtool.create(self.path_rrd + type+self.name_rrd,
                       "--start", 'N',
                       "--step", '60',
                       "DS:"+ type +":GAUGE:600:U:U",
                       "RRA:AVERAGE:0.5:1:24")
        if ret:
            print(rrdtool.error())

    def update(self, community, ip, OID = '1.3.6.1.2.1.25.3.3.1.2.196608', total = 100, type ="CPUload"):
        carga_CPU = 0
        i = 0
        she_doesnt_love_you = 1

        while i < total:
            carga_CPU = int(consultaSNMP(community, ip, OID))
            valor = "N:" + str(carga_CPU)
            print(str(i) + "-> " + valor)
            ret = rrdtool.update(self.path_rrd + type + self.name_rrd, valor)
            rrdtool.dump(self.path_rrd + type+self.name_rrd, 'trend.xml')
            time.sleep(1)
            i += 1

        if ret:
            print(rrdtool.error())
            time.sleep(300)

    def create_image(self, path_png, threshold_lower, threshold_upper, threshold_breakpoint, type):

        ultima_lectura = int(rrdtool.last(self.path_rrd + self.name_rrd))
        tiempo_final = ultima_lectura
        tiempo_inicial = tiempo_final - 3600

        ret = rrdtool.graph(path_png + type+ "trend.png",
                            "--start", str(tiempo_inicial),
                            "--end", str(tiempo_final),
                            "--vertical-label="+type,
                            "--title=Uso de " + type,
                            "--color", "ARROW#009900",
                            '--vertical-label', "Uso de CPU (%)",
                            '--lower-limit', threshold_lower,
                            '--upper-limit', threshold_upper,
                            "DEF:carga=" + self.path_rrd + self.name_rrd + ":CPUload:AVERAGE",
                            "AREA:carga#00FF00:Carga CPU",
                            "LINE1:30",
                            "AREA:5#ff000022:stack",
                            "VDEF:CPUlast=carga,LAST",
                            "VDEF:CPUmin=carga,MINIMUM",
                            "VDEF:CPUavg=carga,AVERAGE",
                            "VDEF:CPUmax=carga,MAXIMUM",
                            "LINE2:" + threshold_breakpoint + "#FF0000",
                            "LINE2:" + threshold_upper      + "#0D76FF",
                            "LINE2:" + threshold_lower      + "#00FF00",
                            "COMMENT:Now          Min             Avg             Max",
                            "GPRINT:CPUlast:%12.0lf%s",
                            "GPRINT:CPUmin:%10.0lf%s",
                            "GPRINT:CPUavg:%13.0lf%s",
                            "GPRINT:CPUmax:%13.0lf%s",
                            "VDEF:m=carga,LSLSLOPE",
                            "VDEF:b=carga,LSLINT",
                            'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
                            "LINE2:tendencia#FFBB00")

    def deteccion(self, umbrales, type = "CPUload"):
        print(type)
        ultima_lectura = int(rrdtool.last(self.path_rrd +type+ self.name_rrd))
        tiempo_final = ultima_lectura
        tiempo_inicial = tiempo_final - 3600

        if type == "CPUload":

            ret = rrdtool.graphv(self.path_rrd + type + "deteccion.png",
                                 "--start", str(tiempo_inicial),
                                 "--end", str(tiempo_final),
                                 "--title", type,
                                 "--vertical-label=Uso de "+ type+"(%)",
                                 '--lower-limit', '0',
                                 '--upper-limit', '100',
                                 "DEF:carga=" + self.path_rrd +type+ self.name_rrd + ":"+type+":AVERAGE",
                                 "CDEF:umbral25=carga,25,LT,0,carga,IF",
                                 "VDEF:cargaMAX=carga,MAXIMUM",
                                 "VDEF:cargaMIN=carga,MINIMUM",
                                 "VDEF:cargaSTDEV=carga,STDEV",
                                 "VDEF:cargaLAST=carga,LAST",
                                 "AREA:carga#00FF00:"+type,
                                 "AREA:umbral25#FF9F00:Tráfico de carga mayor que 25",
                                 "HRULE:25#FF0000:Umbral 1 - 25%",
                                 "LINE2:" + umbrales['breakpoint'] + "#FF0000",
                                 "LINE2:" + umbrales['set'] + "#0D76FF",
                                 "LINE2:" + umbrales['go'] + "#00FF00",
                                 "PRINT:cargaMAX:%6.2lf %S",
                                 "GPRINT:cargaMIN:%6.2lf %SMIN",
                                 "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                                 "GPRINT:cargaLAST:%6.2lf %SLAST",
                                 "VDEF:m=carga,LSLSLOPE",
                                 "VDEF:b=carga,LSLINT",
                                 'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
                                 "LINE2:tendencia#FFBB00",
                                 "PRINT:m:%6.2lf %S",
                                 "PRINT:b:%6.2lf %S")
        elif type == "RAM":

            ret = rrdtool.graphv(self.path_rrd + type + "deteccion.png",
                                 "--start", str(tiempo_inicial),
                                 "--end", str(tiempo_final),
                                 "--title", type,
                                 "--vertical-label=Uso de "+ type+"(%)",
                                 '--lower-limit', '0',
                                 '--upper-limit', '100',
                                 "DEF:carga=" + self.path_rrd +type+ self.name_rrd + ":"+type+":AVERAGE",
                                 "CDEF:umbral25=carga,25,LT,0,carga,IF",
                                 "VDEF:cargaMAX=carga,MAXIMUM",
                                 "VDEF:cargaMIN=carga,MINIMUM",
                                 "VDEF:cargaSTDEV=carga,STDEV",
                                 "VDEF:cargaLAST=carga,LAST",
                                 "AREA:carga#00FF00:"+type,
                                 "AREA:umbral25#FF9F00:Tráfico de carga mayor que 25",
                                 "HRULE:25#FF0000:Umbral 1 - 25%",
                                 "LINE2:" + umbrales['breakpoint'] + "#FF0000",
                                 "LINE2:" + umbrales['set'] + "#0D76FF",
                                 "LINE2:" + umbrales['go'] + "#00FF00",
                                 "PRINT:cargaMAX:%6.2lf %S",
                                 "GPRINT:cargaMIN:%6.2lf %SMIN",
                                 "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                                 "GPRINT:cargaLAST:%6.2lf %SLAST",
                                 "VDEF:m=carga,LSLSLOPE",
                                 "VDEF:b=carga,LSLINT",
                                 'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
                                 "LINE2:tendencia#FFBB00",
                                 "PRINT:m:%6.2lf %S",
                                 "PRINT:b:%6.2lf %S")
        print (ret)
        # print(ret.keys())
        # print(ret.items())

        value = ret['print[0]']
        res = formatNumber(value)
        ultimo_valor = float(res)

        slope = float(formatNumber(ret['print[1]'].replace(" ","").replace("k", "")))
        B = float(formatNumber(ret['print[2]']))
        print(slope)
        print(B)
        pre = Prediction(slope, B)

        if ultimo_valor > float(umbrales['breakpoint']):
            nombre_asunto = "Prac2 - "
            send_alert_attached(nombre_asunto + "Sobrepasa Umbral línea base", self.path_rrd, type+"deteccion.png", type+self.name_rrd)


def formatNumber(value):
    print("val: " + value)
    res = 0
    j = 0
    neg = False
    for i in range(0, len(value)):
        if value[i].isdigit() == True:
            res = res + (int(value[i]) * (10 ** (j)))
            j = j + 1
        elif value[i] == '-':
            neg = True
    res = int(str(res)[::-1])
    if neg:
        res = res * -1
    return res / 100
class Prediction:
    def __init__(self, m, b):
        self.m = m
        self.b = b
    def predict(self, val):
        return (val - self.b) / self.m