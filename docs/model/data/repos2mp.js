// GitHub 仓库链接
// =>
// 微信小程序代码
const fse = require('fs-extra')
const os = require('os')
const path = require('path')
const { execSync } = require('child_process')
const globby = require('globby')

const collectRepo = (githubRepo, repoDir) => {
  fse.ensureDirSync(repoDir)
  fse.emptyDirSync(repoDir)

  const cmd = `git clone ${githubRepo} ${repoDir} --depth=1`
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

const repos2mp = async (githubRepos, miniprogramsDir) => {
  for (let i = 0; i < githubRepos.length; i++) {
    const dataIndex = i + 1

    // 跳过已知存在问题仓库
    if (
      dataIndex === 77 ||
      dataIndex === 84 ||
      dataIndex === 30 ||
      dataIndex === 100
    ) {
      continue
    }

    console.log(`=> repos2mp ${dataIndex}`)

    const dataDir = path.join(miniprogramsDir, String(dataIndex))
    const githubRepo = githubRepos[i]
    const repoDir = path.join(dataDir, 'repo')
    const mpDir = path.join(dataDir, 'miniprogram')
    try {
      console.log(`    > collectRepo ${githubRepo} to ${repoDir}`)
      collectRepo(githubRepo, repoDir)

      console.log(`    > collectMP ${repoDir} to ${mpDir}`)
      collectMP(repoDir, mpDir)
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

const githubReposBuffer = fse.readFileSync(githubReposTXT)
const githubRepos = githubReposBuffer.toString('utf8').split(os.EOL);

(async () => {
  fse.ensureDirSync(miniprogramsDir)
  await repos2mp(githubRepos, miniprogramsDir)
})()
