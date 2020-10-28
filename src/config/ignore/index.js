// 根据关键字忽略文件
const ignoreTokens = [
  // wxss 样式类
  'weui', // UI/组件库 weui
  'colorui', // UI 库 colorui
  'vant', // 组件库 vant
  'animate', // 动画样式库
  // js 工具类
  'wxParse', // 富文本解析工具
  'towxml', // 富文本解析工具
  // 第三方包
  'miniprogram_npm', // 微信小程序 npm 构建包
  'node_modules', // 第三方包
  'dist' // 第三方构建包
]

const ignoreString = ignoreTokens.join('|')
const ignoreRegex = new RegExp(ignoreString, 'i')

module.exports = {
  ignoreRegex
}
