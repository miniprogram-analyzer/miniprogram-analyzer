const parser = require('@babel/parser')
const traverse = require('@babel/traverse').default
const types = require('@babel/types')
const globby = require('globby')
const path = require('path')
const fs = require('fs')
const { ignoreRegex } = require('../../config/ignore/index')

const getASTInfo = (mpDir) => {
  const APIs = {}
  let LOC = 0
  let commentLOC = 0

  const globbyOptions = {
    cwd: mpDir || process.cwd()
  }
  const filePattern = '**/*.js'
  let jsFiles = globby.sync([filePattern], globbyOptions)
  jsFiles = jsFiles.filter(jsFile => !ignoreRegex.test(jsFile))

  const next = fileIndex => {
    if (fileIndex >= jsFiles.length) {
      return {
        APIs,
        LOC,
        commentLOC
      }
    }

    const filePath = path.join(mpDir, jsFiles[fileIndex])

    const jsString = fs.readFileSync(filePath, {
      encoding: 'utf8'
    })

    const ast = parser.parse(jsString, {
      sourceType: 'unambiguous'
    })

    const { loc, comments } = ast
    LOC += (loc.end.line - loc.start.line + 1)
    commentLOC += comments.reduce((acc, cur) => {
      acc += cur.loc.end.line - cur.loc.start.line + 1
      return acc
    }, 0)

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

  return {
    APIs,
    LOC,
    commentLOC
  }
}

module.exports = getASTInfo
