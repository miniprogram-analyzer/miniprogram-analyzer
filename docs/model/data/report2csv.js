// miniprogram-analyzer 生成的 report
// =>
// 多元线性回归模型可分析的数据
const fse = require('fs-extra')
const path = require('path')
const os = require('os')

const saveReport = (fd, report, index) => {
  const { pages, components, hasCloudFunction, wxAPIs, CSSLOC } = report

  const componentsCount = Object.values(components).reduce((acc, cur) => {
    acc += cur
    return acc
  }, 0)

  const uniqueComponentsCount = Object.keys(components).length

  const wxAPIsCount = Object.values(wxAPIs).reduce((acc, cur) => {
    acc += cur
    return acc
  }, 0)

  const uniqueWxAPIsCount = Object.keys(wxAPIs).length

  const formatedReport = [
    index, // 索引
    pages.length, // 页面个数
    componentsCount, // 组件个数，可对 组件进行难度分级
    uniqueComponentsCount, // 组件类型个数
    hasCloudFunction ? 1 : 0, // 是否启用云开发
    wxAPIsCount, // wx API 个数
    uniqueWxAPIsCount, // wx API 类型个数
    CSSLOC,
    100 - 5 * (Math.ceil((index + 1) / 41))
  ]
  fse.appendFileSync(fd, formatedReport.join(','))
  fse.appendFileSync(fd, os.EOL)
}

// const miniprograms = fse.readdirSync(path.join(__dirname, 'miniprograms'))
const miniprograms = Array.from({ length: 164 }).map((_, index) => {
  return index + 1
})

const reportFile = `report.csv`

for (let i = 0; i < miniprograms.length; ++i) {
  const miniprogram = miniprograms[i]
  const reportPath = path.join(__dirname, 'miniprograms', String(miniprogram), 'report', 'report.json')
  console.log(reportPath, fse.existsSync(reportPath))

  if (!fse.existsSync(reportPath)) {
    continue
  }

  const report = fse.readJSONSync(reportPath)
  saveReport(path.join(__dirname, reportFile), report, Number(miniprogram))
}
