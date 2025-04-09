import os
import math
import numpy as np

import os
import yaml

def calcu_factor(res_param, sat_apram):
    # 获取当前脚本的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 拼接配置文件路径
    config_file_path = os.path.join(script_dir, 'config.yml')
    # 读取YAML文件
    with open(config_file_path, 'r') as file:
        data = yaml.safe_load(file)
    # 获取计算因子
    coefficients = data['res'][res_param][0]
    COFF = coefficients['COFF']
    CFAC = coefficients['CFAC']
    LOFF = coefficients['LOFF']
    LFAC = coefficients['LFAC']
    PI = data['common']['PI']
    ea = data['common']['ea']
    eb = data['common']['eb']
    h = data['common']['h']
    if sat_apram == 'A':
        D = data['common']['DA']
    else:
        D = data['common']['DB']
    print("COFF, CFAC, LOFF, LFAC, PI, ea, eb, h, D:",COFF, CFAC, LOFF, LFAC, PI, ea, eb, h, D)

    return COFF, CFAC, LOFF, LFAC, PI, ea, eb, h, D

# 正向查询函数
def row_to_lat(l, c, res, sat):
    COFF, CFAC, LOFF, LFAC, PI, ea, eb, h, D, = calcu_factor(res, sat)
    x = PI*(c-COFF)/(180*math.pow(2,-16)*CFAC)
    y = PI*(l-LOFF)/(180*math.pow(2,-16)*LFAC)
    sd = math.pow(h*math.cos(x)*math.cos(y),2)-(math.pow(math.cos(y),2)+math.pow(ea, 2)/math.pow(eb, 2)*math.pow(math.sin(y),2))*(math.pow(h,2)-math.pow(ea,2))
    if sd < 0:
        return 65535.0, 65535.0
    else:
        sd = math.sqrt(sd) 
    sn = (h*math.cos(x)*math.cos(y)-sd)/(math.pow(math.cos(y),2)+math.pow(ea, 2)/math.pow(eb, 2)*math.pow(math.sin(y),2))
    s1 = h - sn*math.cos(x)*math.cos(y)
    s2 = sn*math.sin(x)*math.cos(y)
    s3 = -sn*math.sin(y) 
    sxy = math.sqrt(math.pow(s1,2)+math.pow(s2,2))
    lat = 180/PI*math.atan(math.pow(ea,2)/math.pow(eb,2)*s3/sxy)
    lon = 180/PI*math.atan(s2/s1)+D
    
    if lon > 180:
        lon -= 360
    if lon < -180:
        lon += 360
    
    # print("---------------------x----------------------",x,type(x))
    # print("---------------------y----------------------",y,type(y))
    # print("---------------------sd----------------------",sd,type(sd))
    # print("---------------------sn----------------------",sn,type(sn))
    # print("---------------------s1----------------------",s1,type(s1))
    # print("---------------------s2----------------------",s2,type(s2))
    # print("---------------------s3----------------------",s3,type(s3))
    # print("---------------------sxy----------------------",sxy,type(sxy))
    # print("---------------------lat----------------------",lat,type(lat))
    # print("---------------------lon----------------------",lon,type(lon))

    return lat, lon
        
# 反向查询函数
def lat_to_row(lat, lon, res, sat):
    COFF, CFAC, LOFF, LFAC, PI, ea, eb, h, D, = calcu_factor(res, sat)
    lat = lat*PI/180
    lon = lon*PI/180
    late = math.atan(math.pow(eb, 2)/math.pow(ea, 2)*math.tan(lat))
    re = eb / math.sqrt(1- (math.pow(ea, 2) - math.pow(eb, 2))/math.pow(ea, 2)*math.pow(math.cos(late), 2))
    D = D * PI / 180
    r1 = h - re*math.cos(late)*math.cos(lon-D)
    r2 = - re*math.cos(late)*math.sin(lon-D)
    r3 = re*math.sin(late)
    rn = math.sqrt(math.pow(r1, 2)+math.pow(r2, 2)+math.pow(r3, 2))
    x = math.atan(-r2/r1)*180/PI
    y = math.asin(-r3/rn)*180/PI
    # l 行号  c 列号
    l = LOFF+y*math.pow(2, -16)*LFAC
    c = COFF+x*math.pow(2, -16)*CFAC

    # print("---------------------lat----------------------",lat)
    # print("---------------------lon----------------------",lon)
    # print("---------------------late----------------------",late)
    # print("---------------------re----------------------",re)
    # print("---------------------r1----------------------",r1)
    # print("---------------------r2----------------------",r2)
    # print("---------------------r3----------------------",r3)
    # print("---------------------rn----------------------",rn)
    # print("---------------------l----------------------",l)
    # print("---------------------c----------------------",c)

    return l, c
        
# if __name__ == '__main__':
#     # 这部分代码会在主程序直接执行时运行
#     pass