def check_rowcolrange(row, col, res):
    resolution_info = {
      250: {"max_row": 43968, "max_col": 43968, "error_msg": "错误：行列号均不在查询范围内，正确为[0-43967]"},
      500: {"max_row": 21984, "max_col": 21984, "error_msg": "错误：行列号均不在查询范围内，正确为[0-21983]"},
      1000: {"max_row": 10992, "max_col": 10992, "error_msg": "错误：行列号均不在查询范围内，正确为[0-10991]"},
      2000: {"max_row": 5496, "max_col": 5496, "error_msg": "错误：行列号均不在查询范围内，正确为[0-5495]"},
      4000: {"max_row": 2748, "max_col": 2748, "error_msg": "错误：行列号均不在查询范围内，正确为[0-2747]"}
  }

    max_row = resolution_info.get(res, {}).get("max_row")
    max_col = resolution_info.get(res, {}).get("max_col")

    if max_row and max_col:
        if row < 0 or row >= max_row:
            if col < 0 or col >= max_col:
                return resolution_info[res]["error_msg"], False
            else:
                return "错误：行号不在查询范围内，正确为[0-{}]".format(max_row - 1), False
        elif col < 0 or col >= max_col:
            return "错误：列号不在查询范围内，正确为[0-{}]".format(max_col - 1), False
        else:
            return "正确：行列号均在查询范围内", True
    else:
        return "找不到分辨率：分辨率当前有250、500、1000、2000、4000", False
    
def check_latlonrange(lat, lon):
    if lat < -90 or lat > 90:
        if lon < -180 or lon > 180:
            return "错误：纬度经度均不在查询范围内，正确为[-90~90、-180~180]",False
        else:
            return "错误：纬度不在查询范围内，正确为[-90~90]",False
    elif lon < -180 or lon > 180:
        return "错误：经度不在查询范围内，正确为[-180~180]",False
    else:
        return "正确：经度纬度均在查询范围内",True
    
# if __name__ == '__main__':
#     # 这部分代码会在主程序直接执行时运行
#     pass