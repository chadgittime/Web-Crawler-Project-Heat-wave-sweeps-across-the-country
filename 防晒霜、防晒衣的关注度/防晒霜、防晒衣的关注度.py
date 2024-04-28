import pandas as pd  # 导入pandas库，用于处理数据
import requests  # 导入requests库，用于发送网络请求
from fake_useragent import UserAgent  # 导入fake_useragent库，用于生成随机的User-Agent

# 保存登录百度指数所需的Cookie信息
cookies = 'BDUSS=kyeG1JZDRMTDBERDd4NHNjVGp0RTNvam1lTUF0T0s1eExOb0VpU21zeU9GTFprRVFBQUFBJCQAAAAAAAAAAAEAAACdO5GP6K-25Zi~5Zi~8J-YAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI6HjmSOh45kZz'

# 设置搜索参数
search_param = {'area': '0',
                'word': '[[{"name": "防晒霜", "wordType": 1}],[{"name": "防晒衣", "wordType": 1}]]',
                'startDate': '2023-04-20', 'endDate': '2023-6-20'}

search_url = 'https://index.baidu.com/api/SearchApi/index?'  # 百度指数搜索接口的URL地址

# 设置HTTP请求头信息
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cipher-Text': '1672733200884_1672792253933_1NLQa+cgc5N2JSNoinHAaMmrDrPtwqHL6D2NHONACx//1P+9YXcg/erBma8ucj43shvH2VsAi3Dzlo9cFfqA3k/PmqixjXJEslJCwNzCzNCVHs+/y7su33mGAxAtFWXrl55rYxzEJNGi4xM6jb4UUibTrVbOl46gKWq/7PVKAIzRyrJbxQP9pKmxECIpO12JbXFrA3leOj8xDZk69P1O/tNU6lD8eMPylUrgCp5k89c9EAD+Q4lgHhsZpTktcKTzKSbrJ5/l0GYNxNS96gEpS/0BnesBc6X52rqE7K4fNzrxm5cfgwbCJx/2+1ayhkI2gUMNDabQ1dnR0hr/NyWxeh7nYvxqarQHsZ+cu3XCt5uEHE4aAPgcXTfDgMsCQOrtMfDGKuxX5PiMDzDODjxSn8cDFRnJ+RMvfPjIIfq2P4k=',
    'Connection': 'keep-alive',
    'Cookie': cookies,
    'Host': 'index.baidu.com',
    'Referer': 'https://index.baidu.com/v2/main/index.html',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': str(UserAgent().random)  # 使用随机生成的User-Agent作为请求头信息的一部分
}

# 发送GET请求获取搜索结果数据
res = requests.get(search_url, params=search_param, headers=headers)
encrypted_data = res.json()['data']  # 提取返回结果中的加密数据
uniqid = encrypted_data['uniqid']  # 提取唯一ID

ptbk_url = f'http://index.baidu.com/Interface/ptbk?uniqid={uniqid}'  # 解密参数URL地址
ptbk_response = requests.get(ptbk_url, headers=headers)
ptbk = ptbk_response.json()['data']  # 获取解密参数


# 解密函数
def decrypt(ptbk, encrypted_data):
    """
    :param ptbk: 解密参数
    :param encrypted_data: 加密数据
    :return: 解密后的数据
    """
    if not ptbk:
        return ""
    n = len(ptbk) // 2
    d = {ptbk[o]: ptbk[n + o] for o in range(n)}
    decrypted_data = [d[data] for data in encrypted_data]
    return ''.join(decrypted_data)


# 填充零值的函数
def fill_zero(data):
    """
    :param data: 字符串格式的数据
    :return: 如果data为空则返回0，否则返回原数据
    """
    if data == '':
        return 0
    else:
        return data


result = pd.DataFrame(columns=['关键词', '日期', '整体日均值'])  # 创建一个空的DataFrame用于存储结果数据

# 遍历加密数据中的用户指数数据
for userIndexes_data in encrypted_data['userIndexes']:
    word = userIndexes_data['word'][0]['name']  # 提取关键词

    start_date = userIndexes_data['all']['startDate']  # 提取开始日期
    end_date = userIndexes_data['all']['endDate']  # 提取结束日期
    timestamp_list = pd.date_range(start_date, end_date).to_list()  # 生成日期范围的时间戳列表
    date_list = [timestamp.strftime('%Y-%m-%d') for timestamp in timestamp_list]  # 将时间戳转换为字符串格式的日期列表
    encrypted_data_all = userIndexes_data['all']['data']  # 提取整体日均值的加密数据
    decrypted_data_all = [int(fill_zero(data)) for data in decrypt(ptbk, encrypted_data_all).split(',')]  # 解密整体日均值数据
    '''
    encrypted_data_pc = userIndexes_data['pc']['data']
    decrypted_data_pc = [int(fill_zero(data)) for data in decrypt(ptbk, encrypted_data_pc).split(',')]
    encrypted_data_wise = userIndexes_data['wise']['data']
    decrypted_data_wise = [int(fill_zero(data)) for data in decrypt(ptbk, encrypted_data_wise).split(',')]
    '''
    df = pd.DataFrame({'关键词': word, '日期': date_list, '整体日均值': decrypted_data_all})  # 创建DataFrame存储解密后的数据
    result = pd.concat([result, df])  # 将解密后的数据添加到结果DataFrame中

result.to_csv('./防晒霜、防晒衣的关注度.csv', index=False)  # 将结果数据保存为CSV文件
