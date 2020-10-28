// 微信小程序
// =>
// miniprogram-analyzer 生成的 report
const fse = require('fs-extra')
const path = require('path')
const { inspect: mpAnalyzer } = require('../../../src/program/index')

// const miniprograms = fse.readdirSync(path.join(__dirname, 'miniprograms'))
let miniprograms = Array.from({ length: 164 }).map((_, index) => {
  return index + 1
});

(async () => {
  for (let i = 0; i < miniprograms.length; ++i) {
    const miniprogram = miniprograms[i]
    const mpDir = path.join(__dirname, 'miniprograms', String(miniprogram), 'miniprogram')
    const reportDir = path.join(__dirname, 'miniprograms', String(miniprogram), 'report')

    if (
      !fse.existsSync(mpDir) ||
      (fse.existsSync(mpDir) && fse.readdirSync(mpDir).length === 0)
    ) {
      continue
    }
    try {
      console.log(`=> analyze ${mpDir}, report ${reportDir}`)
      await mpAnalyzer(mpDir, reportDir)
    } catch (err) {
      console.error(err)
    }
  }
})()
