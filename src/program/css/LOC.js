const fse = require('fs-extra')
const os = require('os')
const path = require('path')
const stylelint = require('stylelint')
const globby = require('globby')
const { once } = require('events')
const { createReadStream } = require('fs')
const { createInterface } = require('readline')
const { ignoreRegex } = require('../../config/ignore/index')

const copy2Tmp = (mpDir) => {
  const tmpDir = os.tmpdir()
  const tmpMpdir = fse.mkdtempSync(path.join(tmpDir, 'mpAnalyzer-'))
  fse.copySync(mpDir, tmpMpdir)
  return tmpMpdir
}

// line of code
async function getLOC (fd) {
  let loc = 0
  try {
    const rl = createInterface({
      input: createReadStream(fd),
      crlfDelay: Infinity
    })

    rl.on('line', (line) => {
      loc++
    })

    await once(rl, 'close')

    return loc
  } catch (err) {
    console.error(err)
  }
}

// 剔除异常值：代码超过 1000 行
const MAX_LOC = 1000
const getCSSLOC = async (mpDir) => {
  let CSSLOC = 0

  const tmpMpdir = copy2Tmp(mpDir)

  const globbyPatterns = [
    '**/*.wxss'
  ]
  const globbyOptions = {
    cwd: tmpMpdir
  }
  let CSSFiles = globby.sync(globbyPatterns, globbyOptions)
  CSSFiles = CSSFiles.map(file => path.join(tmpMpdir, file))
  CSSFiles = CSSFiles.filter(CSSFile => !ignoreRegex.test(CSSFile))

  const stylelintConfig = require(path.join(__dirname, '../../config/stylelint/stylelint.config.js'))
  await stylelint.lint({
    config: stylelintConfig,
    fix: true,
    files: CSSFiles,
    globbyOptions
  })

  CSSLOC = await CSSFiles.reduce(async (acc, cur) => {
    let locOfFile = await getLOC(cur)
    // 剔除异常值
    if (locOfFile >= MAX_LOC) {
      locOfFile = 0
      console.warn('CSSLOC: 剔除异常值', cur)
    }
    let accLoc = await acc
    accLoc += locOfFile
    return accLoc
  }, CSSLOC)

  return CSSLOC
}

module.exports = getCSSLOC
