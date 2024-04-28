import openpyxl
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as Bs
from concurrent.futures import ThreadPoolExecutor

header = {
    'User-Agent': str(UserAgent().random)  # 使用 fake_useragent 生成随机 User-Agent
}

cities = {
    1: 'beijing', 2: 'shanghai', 3: 'tianjin', 4: 'chongqing', 5: 'haerbin', 6: 'changchun', 7: 'shenyang',
    8: 'huhehaote', 9: 'shijiazhuang', 10: 'taiyuan', 11: 'xian', 12: 'jinan', 13: 'wulumuqi', 14: 'lasa',
    15: 'xining', 16: 'lanzhou', 17: 'yinchuan', 18: 'zhengzhou', 19: 'nanjing', 20: 'wuhan', 21: 'hangzhou',
    22: 'hefei', 23: 'fuzhou', 24: 'nanchang', 25: 'changsha', 26: 'guiyang', 27: 'chengdu', 28: 'guangzhou',
    29: 'kunming', 30: 'nanning', 31: 'haikou', 32: 'xianggang', 33: 'aomen', 34: 'taibei'
}


def single_city(city, start_year, end_year):
    weather_data = []
    high_temp_count = 0  # 记录高温天气的数量

    # 遍历指定年份范围内的每一年
    for year in range(start_year, end_year + 1):
        # 遍历4月到6月的每一个月份
        for month in range(4, 7):
            try:
                url = f"http://www.tianqihoubao.com/lishi/{city}/month/{year}{month:02d}.html"
                res = requests.request("GET", url, headers=header)
                html = Bs(res.text, 'html.parser')
                rows = html.select('tr')[1:]
                for row in rows:
                    date = row.select('td')[0].text.strip()
                    temperature = row.select('td')[2].text.strip().replace('℃', '')
                    low_temp, high_temp = temperature.split('/')
                    low_temp = low_temp.strip()
                    high_temp = high_temp.strip()
                    avg_temp = (int(low_temp) + int(high_temp)) / 2

                    if int(high_temp) >= 35:
                        high_temp_count += 1

                print(f"已爬取成功：{city} {year}年{month}月")
            except Exception:
                break

    return high_temp_count


def main():
    wb = openpyxl.Workbook()
    ws = wb.active  # 获取默认工作表

    # 写入表头
    ws.append(['省份', '高温天气数量'])

    with ThreadPoolExecutor(max_workers=10) as executor:
        for city_id, city_name in cities.items():
            high_temp_count = single_city(city_name, 2023, 2023)  # 获取高温天气数量
            ws.append([city_name, high_temp_count])

    wb.save("./全国各省高温天气数量（35℃）.xlsx")


if __name__ == "__main__":
    main()
