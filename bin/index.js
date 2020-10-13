#!/usr/bin/env node

const { program } = require('commander')
const { inspect } = require('../src/program')
const pkgJSON = require('../package.json')

program
  .version(pkgJSON.version)
  .name(pkgJSON.name)

program
  .command('analyze [mpDir]')
  .option('-i, --input [mp directory]', 'miniprogram directory path')
  .option('-o, --output [report directory]', 'report directory path')
  .action(async (mpDir, options) => {
    mpDir = mpDir || options.input || process.cwd()
    const reportDir = options.output
    await inspect(mpDir, reportDir)
  })

program.parse(process.argv)
