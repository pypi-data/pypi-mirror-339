
import json

from check_range import check_rowcolrange, check_latlonrange
from calcu_row_lat import lat_to_row, row_to_lat

# 输入row和col得到经纬度
def get_latlon(row,col,res,sat):
    # ####如果row col超出最大行了，要提示不在查询范围内
    # row = int(data.get("row", 0))760g
    # col = int(data.get("col", 0))
    # res = int(data.get("res", 0))
    # sat = data.get("sat", 0)
    if sat.find('A')>0  and res == 250:
        response = "FY4A成像仪AGRI有500m、1000m、2000m、4000m分辨率，无250m"
        return response
    else:
        forward_checkinfo, forward_checkflag = check_rowcolrange(row, col, res)
        if forward_checkflag:
            latitude, longitude = row_to_lat(row, col, res, sat)
            if latitude == 65535.0 or longitude == 65535.0:
                data = {"latitude": "65535.0", "longitude": "65535.0"}
            else:
                data = {"latitude": round(latitude, 8), "longitude": round(longitude, 8)}
            response = json.dumps(data)
        else:
            response = forward_checkinfo
        return response

# 反查；经度Lat纬度lon分辨率res，输入经纬度得到row和col
def get_rowcol(lat,lon,res,sat):
    if sat.find('A')>0 and res == 250:
        response = "FY4A成像仪AGRI有500m、1000m、2000m、4000m分辨率，无250m"
        return response
    else:
        reverse_checkinfo, reverse_checkflag = check_latlonrange(lat, lon)
        if reverse_checkflag:
            row, column = lat_to_row(lat, lon, res, sat)
            data = {"row": int(row) ,"column": int(column)}
            response = json.dumps(data)
        else:
            response = reverse_checkinfo
        return response
    


# 启动服务
if __name__ == "__main__":
    
    # # 获取当前脚本的绝对路径
    # script_dir = os.path.dirname(os.path.abspath(__file__))
    # # 拼接配置文件路径
    # config_file_path = os.path.join(script_dir, 'config.yml')
    # # 读取YAML文件
    # with open(config_file_path, 'r') as file:
    #     data = yaml.safe_load(file)

    # print(get_latlon(621, 2764, 2000, 'FY4A'))
    print(get_rowcol(30,156,2000,'FY4B'))
