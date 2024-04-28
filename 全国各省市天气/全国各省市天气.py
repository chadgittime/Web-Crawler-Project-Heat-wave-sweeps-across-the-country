import openpyxl
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as Bs
from concurrent.futures import ThreadPoolExecutor

header = {
    'User-Agent': str(UserAgent().random)
}

cities = {
    1: 'beijing', 2: 'shanghai', 3: 'tianjin', 4: 'chongqing', 5: 'haerbin', 6: 'changchun', 7: 'shenyang',
    8: 'huhehaote',
    9: 'shijiazhuang', 10: 'taiyuan', 11: 'xian', 12: 'jinan', 13: 'wulumuqi', 14: 'lasa', 15: 'xining',
    16: 'lanzhou', 17: 'yinchuan', 18: 'zhengzhou', 19: 'nanjing', 20: 'wuhan', 21: 'hangzhou', 22: 'hefei',
    23: 'fuzhou', 24: 'nanchang', 25: 'changsha', 26: 'guiyang', 27: 'chengdu', 28: 'guangzhou', 29: 'kunming',
    30: 'nanning', 31: 'haikou', 32: 'xianggang', 33: 'aomen', 34: 'taibei'
}


def single_city(city, start_year, end_year):
    """
    爬取单个城市的天气数据
    :param city: 城市名称
    :param start_year: 开始年份
    :param end_year: 结束年份
    :return: 天气数据列表
    """
    weather_data = []
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
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
                    weather_data.append([date, low_temp, high_temp, avg_temp])
                print(f"已爬取成功：{city} {year}年{month}月")
            except Exception:
                break

    return weather_data


def crawl_weather(_, city_name, wb):
    """
    爬取指定城市的天气数据，并写入Excel工作簿
    :param _: 无关参数，用于与ThreadPoolExecutor的接口兼容
    :param city_name: 城市名称
    :param wb: Excel工作簿
    """
    weather_data = single_city(city_name, 2019, 2023)
    ws = wb.create_sheet(city_name)
    ws.append(['日期', '最低温(℃)', '最高温(℃)', '平均温(℃)'])
    for i in weather_data:
        ws.append(i)


def main():
    """
    主函数，用于执行爬取操作
    """
    wb = openpyxl.Workbook()
    with ThreadPoolExecutor(max_workers=10) as executor:
        for city_id, city_name in cities.items():
            executor.submit(crawl_weather, city_id, city_name, wb)
    del wb['Sheet']
    wb.save("./全国各省市天气.xlsx")


if __name__ == "__main__":
    main()
