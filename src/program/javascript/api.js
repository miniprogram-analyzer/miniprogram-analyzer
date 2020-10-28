const parser = require('@babel/parser')
const traverse = require('@babel/traverse').default
const types = require('@babel/types')
const globby = require('globby')
const path = require('path')
const fs = require('fs')
const { ignoreRegex } = require('../../config/ignore/index')

const getUsedWxAPIs = (mpDir) => {
  const APIs = {}

  const globbyOptions = {
    cwd: mpDir || process.cwd()
  }
  const filePattern = '**/*.js'
  let jsFiles = globby.sync([filePattern], globbyOptions)
  jsFiles = jsFiles.filter(jsFile => !ignoreRegex.test(jsFile))

  const next = fileIndex => {
    if (fileIndex >= jsFiles.length) {
      return APIs
    }

    const filePath = path.join(mpDir, jsFiles[fileIndex])

    const jsString = fs.readFileSync(filePath, {
      encoding: 'utf8'
    })

    const ast = parser.parse(jsString, {
      sourceType: 'unambiguous'
    })

    traverse(ast, {
      CallExpression (path) {
        const callee = path.node.callee
        if (types.isMemberExpression(callee)) {
          const object = callee.object
          const property = callee.property
          if (types.isIdentifier(object) && object.name === 'wx') {
            const API = `wx.${property.name}`
            APIs[API] = APIs[API] ? ++APIs[API] : 1
          }
        }
      }
    })

    next(++fileIndex)
  }

  next(0)

  return APIs
}

module.exports = getUsedWxAPIs
