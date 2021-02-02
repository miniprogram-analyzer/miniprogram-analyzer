# miniprogram-analyzer

## Intro

评估小程序代码质量

## 使用

### 项目启动

```bash
$ git clone https://github.com/miniprogram-analyzer/miniprogram-analyzer.git
$ cd miniprogram-analyzer
$ npm install
```

### 代码分析

#### 使用帮助

```bash
$ node bin/index.js analyze -h # 查看使用帮助
```

#### 示例

```bash
$ node bin/index.js analyze example/weiyou
报告输出至：plato-mini-program-zh-CN/report/weiyou
```

分析报告:

```md
report/weiyou
├── plato       # 分析报告 HTML
└── report.json # 详细信息
```

## API

### inspect(mpDir, reportDir, options?):

return `Promise<object>`

**mpDir**

Type: `string`

miniprogram directory

**reportDir**

Type: `string`

report directory

**options**

Type: `object`

```javascript
{
    platoOptions
}
```

- **platoOptions**

  Type: [plato options](https://github.com/es-analysis/plato)

## 代码质量衡量指标说明

- [Introduction to Code Metrics - radon](https://radon.readthedocs.io/en/latest/intro.html)

### Code Metrics

:point_right: 示例： [report/weiyou/reports.json](./report/weiyou/report.json)

| 指标             | 说明                                   |
| ---------------- | -------------------------------------- |
| pages            | 页面列表                               |
| hasCloudFunction | 是否使用云开发                         |
| components       | 使用到的组件                           |
| wxAPIs           | 使用到的小程序 API                     |
| CSSLOC           | wxss 代码行数（经过 stylelint 格式化） |
| plato            | plato 相关                             |
| JSLOC            | js 代码行数                            |
| JSCommentLOC     | js 代码注释行数                        |

### plato 生成页面指标说明

#### 总 Summary

1. Total Lines
   总代码行数，表示文件中的代码总行数。
2. Average Lines
   平均代码行数
3. Maintainability
   代码可维护性指标，[参考说明](https://avandeursen.com/2014/08/29/think-twice-before-using-the-maintainability-index/)
   Maintainability Index = MAX(0,(171 - 5.2 * log(Halstead Volume) - 0.23 * (Cyclomatic Complexity) - 16.2 * log(Lines of Code))*100 /171)
   可维护性指标为0-100之间的数字，数值越大表示越易于维护。
   20-100：易于维护
   10-19：较难维护
   0-9：很难维护
4. Average Maintainability
   平均代码可维护性，依据各文件取平均得出
5. Lines of code
   各文件代码行数
6. Estimated errors in implementation
   潜在bug数估计，依据[Halstead](https://en.wikipedia.org/wiki/Halstead_complexity_measures)模型得出
7. Lint errors
   jsLint错误数，不符合约定编程风格错误数

#### 各文件衡量指标

1. `Difficulty`
   文件中去重操作数越难；重复操作符越多，越难。依据[Halstead](https://en.wikipedia.org/wiki/Halstead_complexity_measures)模型得出
2. `Complexity`
   圈复杂度，表示代码块中所有可能的路径数。圈复杂度越低越好。
   降低圈复杂度的方法：减少分支数。[圈复杂度说明](https://en.wikipedia.org/wiki/Cyclomatic_complexity)
3. `Function weight`
   函数权重。有如下几种分类方式：
   By Complexity：按圈复杂度统计
   BySLOC：按照SLOC/LSLOC（源代码行/逻辑代码行）统计。
   SLOC：物理代码行，统计物理行数，包括注释、空行等。
   LSLOC：逻辑代码行，统计语句数。
