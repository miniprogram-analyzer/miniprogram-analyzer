const { detectClones } = require('jscpd')
const path = require('path')

async function getDuplications (mpDir, outputDir) {
  return detectClones({
    path: [mpDir],
    output: path.join(outputDir, 'jscpd-report'),
    reporters: ['json'],
    silent: true
  })
}

module.exports = getDuplications
