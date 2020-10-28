import requests
import re
import xlwt

write_content = ''
regex1 = r'<a href="https://www\.oursparkspace\.cn/\?p=([\w./?%&=])*" target="_blank"><img'

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36' }
			   
cookies = {
    "cookie: _ga":"GA1.2.120972614.1597323898",
    "wordpress_logged_in_bcf1d3efe0b9914465a555c6dbdce649":"13151.258.41d51b315412a87c321c1cc7cf0b78ed%7C1602748124%7CVsSQS8jumGgCCmMh6K7MIJfx3AhUSkJALJ2BWRebdCN%7C24c693cc9754b0b49ffd4bfdf41fe075557807fe15dbc4a1e185a545d231e85e",
    "wp_xh_session_bcf1d3efe0b9914465a555c6dbdce649":"eccdc2552c1a8e1f8523c8503a876e59%7C%7C1602657059%7C%7C1602653459%7C%7Cc2f3d749fec6a9dfe57d6fae8fac552d",
    "wp-settings-time-13151":"1602579942",
    "wp-settings-13151":"editor%3Dtinymce",
    "PHPSESSID":"923vtf7p9518004pghi8dgr8v3"
}


# 创建 xls 文件对象
wb = xlwt.Workbook()

# 新增两个表单页
sh1 = wb.add_sheet('爬虫')

# 然后按照位置来添加数据,第一个参数是行，第二个参数是列
# 写入第一个sheet
sh1.write(0, 0, '火花链接')
sh1.write(0, 1, '待访问链接')

index=1
list = []
while index<45:
	url='https://www.oursparkspace.cn/?page_id=432&category_name=web&paged='+str(index)
	html=requests.get(url, cookies = cookies, headers = headers)
	if html.status_code != 200:
		index+=1
		continue
	html_bytes=html.content
	html_str=html_bytes.decode()
	i = 1
	string = ''
	all_items1 = re.finditer(regex1,html_str)
	for match in all_items1: 
		string+=match.group()
	all_items2 = re.finditer(r'\d+',string)
	for match in all_items2: 
		sh1.write(index, i, match.group())
		i+=1
		list.append(match.group())
	sh1.write(index, 0, url)
	index+=1

# 最后保存文件即可
wb.save('select.xls')
print(list)
