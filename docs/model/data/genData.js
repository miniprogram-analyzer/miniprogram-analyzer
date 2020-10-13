const fse = require('fs-extra')
const os = require('os')
const path = require('path')
const { inspect: mpAnalyzer } = require('../../../src/program/index')
const { execSync } = require('child_process')
const globby = require('globby')

const collectRepo = (githubRepo, repoDir) => {
  fse.ensureDirSync(repoDir)
  fse.emptyDirSync(repoDir)

  const cmd = `git clone ${githubRepo} ${repoDir}`
  try {
    execSync(cmd)
  } catch (err) {
    console.error(err)
  }
}

const collectMP = (repoDir, mpDir) => {
  fse.ensureDirSync(mpDir)
  fse.emptyDirSync(mpDir)

  const mpRootDir = getMPRootDir(repoDir)
  console.log(mpRootDir, mpDir)
  fse.copySync(mpRootDir, mpDir)
}

const getMPRootDir = (repoDir) => {
  const globbyOptions = {
    cwd: repoDir
  }
  const globbyPatterns = [
    '**/project.config.json',
    '**/app.json'
  ]

  const files = globby.sync(globbyPatterns, globbyOptions)
  if (files.length === 0) {
    throw new Error(`Error: project.config.json or app.json are not exist in ${repoDir}`)
  } else {
    return path.dirname(path.join(repoDir, files[0]))
  }
}

const saveReport = (fd, report, index) => {
  const { pages, components, hasCloudFunction } = report

  const componentsCount = Object.values(components).reduce((acc, cur) => {
    acc += cur
    return acc
  }, 0)

  const formatedReport = [
    index,
    pages.length,
    componentsCount,
    hasCloudFunction ? 1 : 0
  ]
  fse.appendFileSync(fd, formatedReport.join(','))
  fse.appendFileSync(fd, os.EOL)
}

const genData = async (githubRepos, miniprogramsDir, resultPath) => {
  for (let i = 0; i < githubRepos.length; i++) {
    const dataIndex = i + 1

    console.log(`=> genData ${dataIndex}`)

    const dataDir = path.join(miniprogramsDir, String(dataIndex))
    const githubRepo = githubRepos[i]
    const repoDir = path.join(dataDir, 'repo')
    const mpDir = path.join(dataDir, 'miniprogram')
    const reportDir = path.join(dataDir, 'report')
    try {
      console.log(`    > collectRepo ${githubRepo} to ${repoDir}`)
      collectRepo(githubRepo, repoDir)

      console.log(`    > collectMP ${repoDir} to ${mpDir}`)
      collectMP(repoDir, mpDir)

      console.log(`    > analyze ${repoDir}, report ${mpDir}`)
      const report = await mpAnalyzer(mpDir, reportDir)

      saveReport(resultPath, report, dataIndex)
    } catch (err) {
      console.error(err)
    }

    console.log()
    console.log()
    console.log()
  }
}

const githubReposTXT = path.join(path.resolve(__dirname), 'miniprograms.txt')
const miniprogramsDir = path.join(path.resolve(__dirname), 'miniprograms')
const resultPath = path.join(path.resolve(__dirname), 'data.csv')

const githubReposBuffer = fse.readFileSync(githubReposTXT)
const githubRepos = githubReposBuffer.toString('utf8').split(os.EOL);

(async () => {
  fse.ensureDirSync(miniprogramsDir)
  fse.emptyDirSync(miniprogramsDir)
  await genData(githubRepos, miniprogramsDir, resultPath)
})()
