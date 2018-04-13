# -*- coding: utf-8 -*-


import pandas as pd

xl = pd.ExcelFile('./data/yuan_20180302.xlsx')
writer = pd.ExcelWriter('result.xlsx')
# get ITC meta

itc = xl.parse("Sheet1")
itc = itc.sort_values(by='日期')
print(itc.head(5))
print(itc.tail(5))
stock = xl.parse("Sheet4")
stock = stock.sort_values(by='日期')
## try get correlation of ITC and stock price, only on ITC had traded
def NonZeroCorrelation(s1,s2,dayAfter):
    itcDiff = []
    priceDiff = []
    for i in range(0, len(itc)-dayAfter, 1):
        if s1[i] != 0:
            itcDiff.append(s1[i])
            priceDiff.append(s2[i+dayAfter])
    return pd.Series(itcDiff).corr(pd.Series(priceDiff))

corResult = {}
corResult['Cor Of trade&incRate (whole)'] = itc['投信買賣超'].corr(itc['漲幅(%)'])
corResult["trade&incRate day 3 correlation:"]= NonZeroCorrelation(itc['投信買賣超'],itc['漲幅(%)'], 3)
corResult["trade&incRate day 1 correlation:"]= NonZeroCorrelation(itc['投信買賣超'],itc['漲幅(%)'], 1)
corResult["trade&incRate day 0 correlation:"]= NonZeroCorrelation(itc['投信買賣超'],itc['漲幅(%)'], 0)
corResult["trade& vol correlation:"]= NonZeroCorrelation(itc['投信買賣超'],stock['成交量'], 0)
corResult["trade& vol day 1 correlation:"]= NonZeroCorrelation(itc['投信買賣超'],stock['成交量'], 1)
corResult["inv& High price day 1 correlation:"]= NonZeroCorrelation(itc['投信庫存'],stock['最高價'], 1)
corResult["inv& End price day 1 correlation:"]= NonZeroCorrelation(itc['投信庫存'],stock['收盤價'], 1)

pd.DataFrame(data=corResult,index=['cor']).to_excel(writer, 'Cor Result')
stock = stock.join(itc['投信庫存'])
stock = stock.join(itc['投信買賣超'])

print(stock.corr())
stock.corr().to_excel(writer, 'COR Matrix')

datas = xl.parse("Sheet7")
datas = datas.sort_values(by='日期')
#print(datas.head(5))
#print(datas.tail(5))




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

# print("DayTrade:")
pd.DataFrame(data=DayTradeBank(datas,30),columns=['bank','count']).to_excel(writer, 'Day Trade')
pd.DataFrame(data=ITCTradeBank(datas,30),columns=['bank','count']).to_excel(writer, 'ITC Trade')
writer.save()
# print()
# print("ITCBank:")
# print(ITCTradeBank(datas,10))


