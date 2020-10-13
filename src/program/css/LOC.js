const fse = require('fs-extra')
const os = require('os')
const path = require('path')
const stylelint = require('stylelint')
const globby = require('globby')
const { once } = require('events')
const { createReadStream } = require('fs')
const { createInterface } = require('readline')

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

const getCSSLOC = async (mpDir) => {
  let CSSLOC = 0

  const tmpMpdir = copy2Tmp(mpDir)

  const globbyPatterns = [
    '**/*.wxss'
  ]
  const globbyOptions = {
    cwd: tmpMpdir
  }
  let files = globby.sync(globbyPatterns, globbyOptions)
  files = files.map(file => path.join(tmpMpdir, file))

  const stylelintConfig = require(path.join(__dirname, '../../config/stylelint/stylelint.config.js'))
  await stylelint.lint({
    config: stylelintConfig,
    fix: true,
    files,
    globbyOptions
  })

  CSSLOC = await files.reduce(async (acc, cur) => {
    const locOfFile = await getLOC(cur)
    let accLoc = await acc
    accLoc += locOfFile
    return accLoc
  }, CSSLOC)

  return CSSLOC
}

module.exports = getCSSLOC
