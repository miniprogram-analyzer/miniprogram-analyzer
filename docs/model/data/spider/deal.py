import xlwt
import xlrd

# 打开 xls 文件对象
wb = xlrd.open_workbook('collect.xls')
i = 1
bs = wb.sheet_by_index(0)   
cols = bs.col_values(1)

# 创建 xls 文件对象
wbb = xlwt.Workbook()

# 新增两个表单页
sh1 = wbb.add_sheet('爬虫')
i=0

for index in cols :
    sh1.write(i,0,index[7:-9])
    i+=1

# 最后保存文件即可
wbb.save('collect.xls')