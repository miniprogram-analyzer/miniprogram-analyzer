from sklearn.externals import joblib

lr = joblib.load(r'./model/linear_model.pkl')

# wechat-app-mall
# metric = [[
#     39, 1621,
#     23,    0,
#    533,   68,
#   9008
# ]]

# miniprogram-demo
metric = [[
    90, 2161,
    39,    1,
   323,  133,
  2812
]]

print(lr.predict(metric))
