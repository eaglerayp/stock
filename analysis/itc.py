# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.svm import NuSVR
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn import metrics

## try get correlation of ITC and stock price, only on ITC had traded
def NonZeroCorrelation(s1,s2,dayAfter):
    diff1 = []
    diff2 = []
    for i in range(0, len(s1)-dayAfter, 1):
        if s1[i] != 0:
            diff1.append(s1[i])
            diff2.append(s2[i+dayAfter])
    return pd.Series(diff1).corr(pd.Series(diff2))

def FindMaxCorrelation(s1,s2):
    indexList = [1,2,5,10,20,40]
    maxCor = -1
    resultIndex = 0
    for i in indexList:
        cor = NonZeroCorrelation(s1, s2, i)
        if cor > maxCor:
            maxCor = cor
            resultIndex = i
    return resultIndex, maxCor

# find diff similar to ITC's volume??
def ITCTradeBank(datas, top):
    ITCBankCount = {}
    for i in range(0, len(datas), 1):
        sell = datas['賣張'][i]
        buy = datas['買張'][i]
        ITCBuy = datas['ITC BUY'][i]
        ITCSell = datas['ITC SELL'][i]
        if (buy > ITCBuy and ITCBuy>0) or (sell > ITCSell and ITCSell>0):
            name = datas['券商名稱'][i]
            #print(name)
            if name in ITCBankCount:
                ITCBankCount[name] = ITCBankCount[name] + 1
            else:
                ITCBankCount[name] = 1
    sortedResult = sorted(ITCBankCount.items(), key=lambda d: d[1],reverse=True)
    return sortedResult[:top]

def DayTradeBank(datas, top):
    dayTradeBankCount = {}
    for i in range(0, len(datas), 1):
        sell = datas['賣張'][i]
        if sell==0:
            continue
        dayTradeRate = datas['買張'][i]/sell
        if dayTradeRate > 0.7 and dayTradeRate < 1.3 and sell > 50:
            name = datas['券商名稱'][i]
            #print(name)
            if name in dayTradeBankCount:
                dayTradeBankCount[name] = dayTradeBankCount[name] + 1
            else:
                dayTradeBankCount[name] = 1
    sortedResult = sorted(dayTradeBankCount.items(), key=lambda d: d[1],reverse=True)
    return sortedResult[:top]


def DayTradePriceCor(datas, price, dayAfter):
    # find stock price
    dayTrade={}
    incRate={}
    timeDiff = len(price)- len(datas)
    price = price[timeDiff-1:-1].reset_index(drop=True)
    for i in range(0, len(datas)-dayAfter, 1):
        sell = datas['賣張'][i]
        if sell==0:
            continue
        dayTradeRate = datas['買張'][i]/sell
        if dayAfter == 0:
            incRate[i] = datas['漲幅(%)'][i]
        else:
            incRate[i] = price[i+dayAfter] - price[i]
        if dayTradeRate > 0.7 and dayTradeRate < 1.3 and sell > 50:
            dayTrade[i]=1
        else:
            dayTrade[i]=0

    cor = pd.Series(dayTrade).corr(pd.Series(incRate))
    return cor


# def main():
xl = pd.ExcelFile('./data/yuan_20180302.xlsx')
writer = pd.ExcelWriter('result.xlsx')

# get ITC meta
itc = xl.parse("Sheet1")
itc = itc.sort_values(by='日期')
# get Stock Meta Data
stock = xl.parse("Sheet4")
stock = stock.sort_values(by='日期')


# tradeInc = {}
# tradeInc[5]= NonZeroCorrelation(itc['投信買賣超'],stock['收盤價'], 5)
# tradeInc[1]= NonZeroCorrelation(itc['投信買賣超'],stock['收盤價'], 1)
# tradeInc[0]= NonZeroCorrelation(itc['投信買賣超'],stock['收盤價'], 0)

# tradeVol = {}
# tradeVol[5]= NonZeroCorrelation(itc['投信買賣超'],stock['成交量'], 5)
# tradeVol[1]= NonZeroCorrelation(itc['投信買賣超'],stock['成交量'], 1)
# tradeVol[0]= NonZeroCorrelation(itc['投信買賣超'],stock['成交量'], 0)

# invHigh = {}
# invHigh[5]= NonZeroCorrelation(itc['投信庫存'],stock['最高價'], 5)
# invHigh[1]= NonZeroCorrelation(itc['投信庫存'],stock['最高價'], 1)
# invHigh[0]= NonZeroCorrelation(itc['投信庫存'],stock['最高價'], 0)

# invEnd = {}
# invEnd[5]= NonZeroCorrelation(itc['投信庫存'],stock['收盤價'], 5)
# invEnd[1]= NonZeroCorrelation(itc['投信庫存'],stock['收盤價'], 1)
# invEnd[0]= NonZeroCorrelation(itc['投信庫存'],stock['收盤價'], 0)

# corResult = {}
# corResult['投信買賣超&漲幅 (whole)'] = itc['投信買賣超'].corr(itc['漲幅(%)'])
# corResult["投信買賣超&收盤價 cor"]= tradeInc
# corResult["投信買賣超&成交量 cor"]= tradeVol
# corResult["投信庫存&最高價 cor"]= invHigh
# corResult["投信庫存&收盤價 cor"]= invEnd
# corResult["DayTrade&漲幅 cor"]= dayTrade
# pd.DataFrame(data=corResult).to_excel(writer, 'Cor Result')

# find useful feature
# print("投信庫存,收盤價",FindMaxCorrelation(itc['投信庫存'],stock['收盤價']))
# print("投信庫存,最高價",FindMaxCorrelation(itc['投信庫存'],stock['最高價']))
# print("投信買賣超,成交量",FindMaxCorrelation(itc['投信買賣超'],stock['成交量']))
# print("投信買賣超,收盤價",FindMaxCorrelation(itc['投信買賣超'],stock['收盤價']))
# print("投信買賣超,最高價",FindMaxCorrelation(itc['投信買賣超'],stock['最高價']))
# print("投信買張,最高價",FindMaxCorrelation(itc['投信買張'],stock['最高價']))
# print("投信賣張,最高價",FindMaxCorrelation(itc['投信賣張'],stock['最高價']))
# print("投信買賣超,成交量變動(%)",FindMaxCorrelation(itc['投信買賣超'],stock['成交量變動(%)']))
# print("投信庫存,成交量變動(%)",FindMaxCorrelation(itc['投信庫存'],stock['成交量變動(%)']))

# 投信庫存,收盤價 (10, -0.2944036489015487)
# 投信庫存,最高價 (10, -0.29599362567251397)
# 投信買賣超,成交量 (40, 0.32763276593990576)
# 投信買賣超,收盤價 (40, 0.3089239124795162)
# 投信買賣超,最高價 (40, 0.3140942265078386)
# 投信買張,最高價 (40, 0.13562396136450933)
# 投信賣張,最高價 (20, 0.030274366307683324)
# 投信買賣超,成交量變動(%) (10, 0.1355350230725098)
# 投信庫存,成交量變動(%) (2, 0.08520542560138196)
# 小結:
# 投信買賣超對兩個月後股價比較有影響
# 投信買賣超影響兩周內的布局
# 投信買張影響市場程度較高


stock = stock.join(itc['投信庫存'])
stock = stock.join(itc['投信買賣超'])

stock.corr().to_excel(writer, 'COR Matrix')


# Prepare training features, target values
# T-40 投信買賣超
# T-1 投信買賣超
# T-1 成交量
# T-1 振幅(%)
# analysis like KD line?

# Target: stock 最高價/ 漲幅?
f1 = itc['投信買賣超'][:-40].values
f2 = itc['投信買賣超'][39:-1].values
f3 = stock['成交量'][39:-1].values
f4 = stock['振幅(%)'][39:-1].values
f5 = stock['最高價'][39:-1].values
t1 = stock['最高價'][40:].values
t2 = stock['漲幅(%)'][40:].values
Tdate = stock['日期'][40:].values

fDatas = {}
fDatas["投信買賣超-40"] = f1
fDatas["投信買賣超-1"] = f2
fDatas["成交量-1"] = f3
# fDatas["振幅-1"] = f4
fDatas["最高價-1"] = f5

# for validation: it will fit on linear kernel
# fDatas["最高價"] = stock['最高價'][40:].values

# Preprocessing features

raw = pd.DataFrame(data=fDatas)

# scaler = StandardScaler()
scaler = preprocessing.MaxAbsScaler()
scaledFeatures = scaler.fit_transform(raw)
# features = preprocessing.scale(features)

# ITC SVM predict SVR, using 投信買賣超,投信賣張
# How to choose kernel of svm
def SVRPredict(features,target,topic):
    kernels = ["linear","rbf","poly","sigmoid"]
    for k in kernels:
        clf = NuSVR(kernel=k,C=0.5)
        clf = clf.fit(features[:-30],target[:-30])
        print("SVM kernel", k)
        test = features[-30:]
        answer = target[-30:]
        testDate = Tdate[-30:]
        results = clf.predict(X=features[-30:])
        print(topic," score:",clf.score(test,answer))
        graphData = {}
        graphData["RawData"] = answer
        graphData["Prediction"] = results
        graphData["Date"] = testDate
        gd = pd.DataFrame(data=graphData)
        gd.plot(x="Date")
        plt.savefig(topic+"_"+k)

SVRPredict(raw,t1,"RAW_Price")
SVRPredict(scaledFeatures,t1,"MaxAbsScale_Price")

SVRPredict(raw,t2,"RAW_Return")
SVRPredict(scaledFeatures,t2,"MaxAbsScale_Return")

# TODO: with PCA stock
# metadata

# 分行分析

# TODO:大量當沖對股價的關聯性

datas = xl.parse("Sheet7")
datas = datas.sort_values(by='日期')

oneBank = datas.loc[datas['券商名稱'] == '新光'].reset_index(drop=True)

dayTrade = {}
dayTrade[5]= DayTradePriceCor(oneBank,stock['收盤價'],5)
dayTrade[1]= DayTradePriceCor(oneBank,stock['收盤價'],1)
dayTrade[0]= DayTradePriceCor(oneBank,stock['收盤價'],0)

pd.DataFrame(data=DayTradeBank(datas,30),columns=['bank','count']).to_excel(writer, 'Day Trade')
pd.DataFrame(data=ITCTradeBank(datas,30),columns=['bank','count']).to_excel(writer, 'ITC Trade')
writer.save()
# print()
# print("ITCBank:")
# print(ITCTradeBank(datas,10))

# if __name__ == '__main__':
#     main()
