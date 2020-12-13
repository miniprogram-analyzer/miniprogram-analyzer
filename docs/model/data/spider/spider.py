import requests
import re
import xlwt

write_content = ''
regex1 = r"<h2><b>(.*)</b></h2>"
regex2 = r"https://github\.com/([\w./?%&=])*"

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

# 新增一个表单页
sh1 = wb.add_sheet('爬虫')

# 然后按照位置来添加数据,第一个参数是行，第二个参数是列
# 写入第一个sheet
sh1.write(0, 0, '火花链接')
sh1.write(0, 1, '项目名称')
sh1.write(0, 2, 'github链接')
i = 1
list = ['73734', '20285', '73452', '15411', '15458', '60285', '5088', '73813', '14287', '73604', '14449', '62172', '5033', '66399', '61150', '5035', '13982', '14037', '14322', '14439', '14675', '5081', '14928', '5069', '73653', '5129', '68163', '5109', '14341', '14502', '5149', '14163', '60533', '73746', '14268', '14612', '5117', '14995', '14167', '5104', '15073', '14083', '5053', '10554', '14256', '1054', '14193', '5068', '73', '5052', '1078', '73557', '14272', '5086', '9891', '15043', '5037', '14297', '5085', '5030', '5048', '5008', '14165', '5022', '15406', '15409', '14231', '60336', '5105', '5031', '5059', '14530', '14665', '14395', '15024', '73431', '73739', '1606', '61939', '14552', '14473', '1461', '72', '5148', '14132', '14863', '5118', '5091', '14487', '14202', '14149', '73303', '14889', '14671', '15874', '15045', '5043', '14042', '14352', '60320', '80', '37774', '14693', '39719', '14954', '38159', '14448', '73540', '14410', '14942', '60323', '1124', '14916', '73998', '14288', '1119', '14636', '14479', '79', '1058', '38033', '5054', '14093', '37726', '14874', '14823', '84', '38871', '14709', '37707', '88', '14753', '14843', '14994', '14931', '14429', '14932', '89', '14273', '85', '73525', '15074', '14398', '10633', '60516', '14632', '73446', '14524', '17528', '14940', '37759', '15027', '60888', '73310', '39180', '15075', '18125', '60542', '60775', '19980', '14420', '73725', '15069', '73564', '73536', '18039', '14711', '60399', '37796', '20818', '60406', '38882', '60545', '73656', '60844', '14892', '73712', '14821', '38820', '60677', '60527', '38545', '73778', '39276', '60562', '38537', '60244', '63186', '73748', '60340', '60809', '60628', '71134', '38393', '73516', '39291', '37782', '20176', '60543', '62397', '14992', '71208', '73816', '14946', '60430', '39285', '60574', '60665', '37990', '60688', '14727', '73457', '19496', '60613', '38842', '20821', '20793', '73548', '62175', '20174', '73789', '60577', '39210', '60763', '73798', '73899', '73583', '73855', '61815', '61907', '71357', '60337', '60539', '73373', '82176', '73976', '73851', '73668', '14397', '60771', '73714', '73626', '78596', '61455', '60581', '61077', '73975', '73765', '69301', '73597', '73559', '60276', '73654', '73428', '73434', '73538', '60999', '73546', '73889', '61067', '68795', '60593', '60761', '61259', '73547', '73900', '73562', '73425', '73602', '60700', '61597', '73632', '73361', '73544', '60602', '62079', '73581', '61040', '73732', '61030', '73677', '73574', '73596', '71244', '61224', '62261', '60514', '73809', '60865', '73601', '60935', '60806', '60537', '73672', '73963', '60627', '61106', '61899', '60686', '73593', '61370', '64012', '73529', '83891', '61928', '61618', '74934', '71253', '73686', '62011', '73576', '60894', '73664', '62001', '73958', '61841', '73723', '73836', '62291', '73702', '73439', '73607', '74016', '73650', '61835', '69072', '73934', '61194', '73685', '73962', '73879', '73398', '62165', '73585', '73941', '85702', '71161', '60708', '73377','73839', '71234', '73623', '68577', '73722', '73641', '71169', '73895', '70935', '73566', '47194', '73633', '61180', '61872', '73665', '73651', '69319', '73467', '71127', '37758', '73711', '60704', '73628', '71530', '73691', '73709', '70991', '71185', '70789', '73917', '73775', '73558', '73918', '67642', '73675', '62088', '60740', '70719', '83813', '70958', '73706', '73949', '69359', '61261', '73831', '73716', '65797', '73613', '61249', '70947', '73550', '73640', '69299', '67961', '71144', '73563', '66134', '61929', '73699', '73997', '61059', '73762', '82616', '62110', '73979', '73840', '73852', '70852', '85470', '85470', '73588', '71023', '86443', '70841', '60948', '73636', '73586', '70986', '71155', '73451', '70994', '73740', '61443', '73579', '70802', '70876', '57323', '73614', '61055', '71278', '73829', '71392', '70916', '63500', '70864', '73577', '65174', '70823', '71189', '73727', '70814', '75987', '73662', '71228', '70844', '71148', '69290', '61866', '82853', '69212', '73667', '70979', '70952', '70919', '70977', '71239', '70858', '70862', '71067', '71216', '73779', '61986', '86289', '71959', '70859', '73957', '70820', '73883', '70830', '70918', '69268', '70944', '73747', '73689', '70792', '61470', '73730', '70921', '73629', '70839', '71129', '70803', '60782', '70933', '63660', '71089', '70821', '61134', '73612', '70928', '60840', '68940', '70782', '68959', '60415', '83979', '86261', '70948', '60644', '61604','61211', '73621', '70878', '70950', '71955', '71232', '70828', '89468', '73754', '73534', '63589', '89392', '73458', '73768', '73751', '83976','73749', '73381', '73757', '73750', '73758', '73760', '73761', '73590', '87306']
for index in list[1:20]:
	url='https://www.oursparkspace.cn/?p='+index 
	html=requests.get(url, cookies = cookies, headers = headers)
	if html.status_code != 200:
		continue
	html_bytes=html.content
	html_str=html_bytes.decode()
	all_items1 = re.finditer(regex1,html_str)
	string1 = ''
	for match in all_items1: 
		print(match.group())
		string1+=match.group()
	sh1.write(i, 1, string1)
	string2 = ''
	all_items2 = re.finditer(regex2,html_str)
	for match in all_items2: 
		string2+=match.group()
	sh1.write(i, 2, string2)
	sh1.write(i, 0, url)
	i+=1

# 最后保存文件即可
wb.save('spider.xls')