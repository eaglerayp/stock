# -*- coding: utf-8 -*-


import pandas as pd

xl = pd.ExcelFile('./data/yuan_20180302.xlsx')
writer = pd.ExcelWriter('result.xlsx')
# get ITC meta

itc = xl.parse("Sheet1")
itc = itc.sort_values(by='日期')

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

tradeInc = {}
tradeInc[5]= NonZeroCorrelation(itc['投信買賣超'],stock['收盤價'], 5)
tradeInc[1]= NonZeroCorrelation(itc['投信買賣超'],stock['收盤價'], 1)
tradeInc[0]= NonZeroCorrelation(itc['投信買賣超'],stock['收盤價'], 0)

tradeVol = {}
tradeVol[5]= NonZeroCorrelation(itc['投信買賣超'],stock['成交量'], 5)
tradeVol[1]= NonZeroCorrelation(itc['投信買賣超'],stock['成交量'], 1)
tradeVol[0]= NonZeroCorrelation(itc['投信買賣超'],stock['成交量'], 0)

invHigh = {}
invHigh[5]= NonZeroCorrelation(itc['投信庫存'],stock['最高價'], 5)
invHigh[1]= NonZeroCorrelation(itc['投信庫存'],stock['最高價'], 1)
invHigh[0]= NonZeroCorrelation(itc['投信庫存'],stock['最高價'], 0)

invEnd = {}
invEnd[5]= NonZeroCorrelation(itc['投信庫存'],stock['收盤價'], 5)
invEnd[1]= NonZeroCorrelation(itc['投信庫存'],stock['收盤價'], 1)
invEnd[0]= NonZeroCorrelation(itc['投信庫存'],stock['收盤價'], 0)

corResult = {}
corResult['投信買賣超&漲幅 (whole)'] = itc['投信買賣超'].corr(itc['漲幅(%)'])
corResult["投信買賣超&收盤價 cor"]= tradeInc
corResult["投信買賣超&成交量 cor"]= tradeVol
corResult["投信庫存&最高價 cor"]= invHigh
corResult["投信庫存&收盤價 cor"]= invEnd


stock = stock.join(itc['投信庫存'])
stock = stock.join(itc['投信買賣超'])

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
oneBank = datas.loc[datas['券商名稱'] == '新光'].reset_index(drop=True)

dayTrade = {}
dayTrade[5]= DayTradePriceCor(oneBank,stock['收盤價'],5)
dayTrade[1]= DayTradePriceCor(oneBank,stock['收盤價'],1)
dayTrade[0]= DayTradePriceCor(oneBank,stock['收盤價'],0)

corResult["DayTrade&漲幅 cor"]= dayTrade

pd.DataFrame(data=corResult).to_excel(writer, 'Cor Result')
pd.DataFrame(data=DayTradeBank(datas,30),columns=['bank','count']).to_excel(writer, 'Day Trade')
pd.DataFrame(data=ITCTradeBank(datas,30),columns=['bank','count']).to_excel(writer, 'ITC Trade')
writer.save()
# print()
# print("ITCBank:")
# print(ITCTradeBank(datas,10))


