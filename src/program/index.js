const plato = require('plato')
const fse = require('fs-extra')
const path = require('path')

const getUsedComponents = require('./html/component')

const inspect = async (mpDir, reportDir, options = {}) => {
  const projectConfigJSONPath = path.join(mpDir, './project.config.json')
  let appJSONPath = path.join(mpDir, 'app.json')
  let miniprogramRoot = mpDir
  let cloudfunctionRoot = path.join(mpDir, 'cloudfunctions')

  if (!fse.existsSync(projectConfigJSONPath)) {
    if (!fse.existsSync(appJSONPath)) {
      console.warn('Error: project.config.json & app.json are not exist!')
      console.warn(`  mpDir: ${mpDir}`)
      return
    }
  } else {
    const projectConfigJSON = fse.readJsonSync(projectConfigJSONPath)
    miniprogramRoot = path.join(mpDir, projectConfigJSON.miniprogramRoot || '')
    cloudfunctionRoot = path.join(mpDir, projectConfigJSON.cloudfunctionRoot || 'cloudfunctions')
  }

  appJSONPath = path.join(miniprogramRoot, 'app.json')
  if (!fse.existsSync(appJSONPath)) {
    console.warn('Error: app.json is not exist!')
    console.warn(`  miniprogramRoot: ${miniprogramRoot}`)
    return
  }

  const appJSON = fse.readJSONSync(appJSONPath)
  const mpPages = appJSON.pages

  const hasCloudFunction = fse.existsSync(cloudfunctionRoot)

  const outputDir = reportDir || path.join(process.cwd(), 'report', path.basename(mpDir))

  fse.ensureDirSync(outputDir)
  fse.emptyDirSync(outputDir)

  const { platoOptions = {
    recurse: true
  } } = options

  const platoReport = await new Promise((resolve, reject) => {
    const files = [mpDir]
    const platoOutputDir = path.join(outputDir, 'plato')
    plato.inspect(files, platoOutputDir, platoOptions, report => {
      resolve(report)
    })
  })

  const usedComponents = await getUsedComponents(miniprogramRoot)

  const report = {
    pages: mpPages,
    hasCloudFunction,
    components: usedComponents,
    plato: platoReport
  }

  fse.writeFileSync(path.join(outputDir, 'report.json'), JSON.stringify(report, null, 2))

  console.log(`报告输出至：${outputDir}`)

  return report
}

module.exports = {
  inspect
}
