#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   rednote.py
@Time    :   2025/04/24 10:55:50
@Author  :   zjp 
@Desc    :   小红书爬虫
'''


# 请求地址
url = 'https://edith.xiaohongshu.com/api/sns/web/v1/feed'

# 请求头
h1 = {
	'Accept': 'application/json, text/plain, */*',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
	'Content-Type': 'application/json;charset=UTF-8',
	'Cookie': '换成自己的cookie值',
	'Origin': 'https://www.xiaohongshu.com',
	'Referer': 'https://www.xiaohongshu.com/',
	'Sec-Ch-Ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
	'Sec-Ch-Ua-Mobile': '?0',
	'Sec-Ch-Ua-Platform': '"macOS"',
	'Sec-Fetch-Dest': 'empty',
	'Sec-Fetch-Mode': 'cors',
	'Sec-Fetch-Site': 'same-site',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
}


# 请求参数
post_data = {
	"source_note_id": note_id,
	"image_formats": ["jpg", "webp", "avif"],
	"extra": {"need_body_topic": "1"}
}


# 发送请求
r = requests.post(url, headers=h1, data=data_json)
# 接收数据
json_data = r.json()



# 笔记标题
try:
	title = json_data['data']['items'][0]['note_card']['title']
except:
	title = ''


# 返回数据
data_row = note_id, title, desc, create_time, update_time, ip_location, like_count, collected_count, comment_count, share_count, nickname, user_id, user_url
# 保存到csv文件
with open(self.result_file, 'a+', encoding='utf_8_sig', newline='') as f:
	writer = csv.writer(f)
	writer.writerow(data_row)
