module.exports = {
  extends: 'stylelint-config-standard',
  rules: {
    'unit-no-unknown': [true, { ignoreUnits: ['rpx'] }],
    'selector-type-no-unknown': [true, { ignoreTypes: ['page'] }]
  }
}
