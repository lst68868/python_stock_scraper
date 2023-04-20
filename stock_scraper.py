import csv
import requests
from bs4 import BeautifulSoup


def main():

    URL = "https://finance.yahoo.com/quote/"
    questP = "?p="
    fin = "&.tsrc=fin-srch"
    YTD = "/history?period1=1577836800&period2=1599004800&interval=1mo&filter=history&frequency=1mo"
    # stonks
    # tickers = ["ACBPX", "ANAYX", "BSIIX", "DISRX", "ETILX", "FAGCX", "FCPIX", "FEPIX", "FGBPX", "FHCIX", "FIMKX", "FSCIX", "GLCTX", "GSINX", "HLIEX", "IYW", "JEMSX", "JUESX", "LAUFX", "MAHQX", "MCVIX", "MEIIX", "MPACX", "OTCIX", "PDBZX", "PHYZX", "QISCX", "VIISX"]
    moderateTickers = ["GLCTX", "FAGCX", "MEIIX", "HLIEX", "JUESX", "MCVIX", "OTCIX", "ETILX", "IYW", "FSCIX",
                       "DISRX", "JEMSX", "FIMKX", "GSINX", "MPACX", "LAUFX", "ACBPX", "PDBZX", "MAHQX", "FEPIX", "FGBPX", "PHYZX"]
    modconsTickers = ["GLCTX", "FAGCX", "MEIIX", "HLIEX", "JUESX", "MCVIX", "OTCIX", "ETILX", "IYW", "FSCIX",
                      "DISRX", "JEMSX", "FIMKX", "GSINX", "MPACX", "LAUFX", "ACBPX", "PDBZX", "MAHQX", "FEPIX", "FGBPX", "PHYZX"]
    modaggTickers = ["GLCTX", "FHCIX", "HLIEX", "JUESX", "MCVIX", "QISCX", "ETILX", "FCPIX", "FSCIX", "DISRX",
                     "VIISX", "FIMKX", "GSINX", "MPACX", "LAUFX", "ANAYX", "PDBZX", "MAHQX", "FEPIX", "BSIIX", "PHYZX"]
    stockWatchlistTickers = ["MSFT", "JNJ", "NKE", "JPM", "AMZN", "GOOGL", "AXP", "HD", "MRK", "UNH", "AAPL", "WMT", "DIS",
                             "DAL", "MAR", "SBUX", "BIIB", "REGN", "CRM", "HOLX", "FB", "ATVI", "JDBAX", "CVTRX", "FTCS", "SDSCX", "SEEGX", "OTICX"]

    moderatePortfolio = csv.reader(open('./moderatePortfolio.csv', 'r'))
    modconsPortfolio = csv.reader(open('./modconsPortfolio.csv', 'r'))
    modaggPortfolio = csv.reader(open('./modaggPortfolio.csv', 'r'))

    stockWatchlist = csv.reader(open('./stockWatchlist.csv', 'r'))
    stockWatchlistLines = list(stockWatchlist)

    updateCSV(moderatePortfolio, moderateTickers, './moderatePortfolio.csv')
    updateCSV(modconsPortfolio, modconsTickers, './modconsPortfolio.csv')
    updateCSV(modaggPortfolio, modaggTickers, './modaggPortfolio.csv')

    for i in range(len(stockWatchlistTickers)):
        ticker = stockWatchlistTickers[i]
        line = stockWatchlistLines[i+1]

        tickerURL = (URL + ticker + questP + ticker + fin)
        tickerPage = requests.get(tickerURL)
        tickerSoup = BeautifulSoup(tickerPage.text, 'html.parser')
        stock_price_span = tickerSoup.findAll(
            "span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})
        stock_price = stock_price_span[0].text

        if ("," in stock_price):
            stock_price = stock_price.replace(",", "")

        ytdURL = (URL + ticker + YTD)
        ytdPage = requests.get(ytdURL)
        ytdSoup = BeautifulSoup(ytdPage.text, 'html.parser')
        # ytd_tr = ytdSoup.findAll("tr", {"class": "BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)"})
        ytd_td = ytdSoup.findAll("td", {"class": "Py(10px) Pstart(10px)"})
        jan_price = ytd_td[len(ytd_td)-2].text

        if ("," in jan_price):
            jan_price = jan_price.replace(",", "")

        YTDfinal = ((float(stock_price) - float(jan_price)) /
                    float(jan_price))*100
        YTDfinalrounded = ((YTDfinal*100)//1)/100.0

        line[1] = stock_price_span[0].text
        line[2] = str(YTDfinalrounded) + "%"
        print(line)

        writer = csv.writer(open('./stockWatchlist.csv', 'w'))
        writer.writerows(stockWatchlistLines)


# csv reader object and list version of CSV object
def updateCSV(portfolio, portfolioTickers, csvFilename):

    URL = "https://finance.yahoo.com/quote/"
    questP = "?p="
    fin = "&.tsrc=fin-srch"
    YTD = "/history?period1=1577836800&period2=1599004800&interval=1mo&filter=history&frequency=1mo"

    asset_class_YTDs = {}
    portfolioLines = list(portfolio)

    for i in range(len(portfolioTickers)):
        ticker = portfolioTickers[i]
        line = portfolioLines[i+1]
        tickerURL = (URL + ticker + questP + ticker + fin)
        tickerPage = requests.get(tickerURL)
        tickerSoup = BeautifulSoup(tickerPage.text, 'html.parser')
        stock_price_span = tickerSoup.findAll(
            "span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})
        stock_price = stock_price_span[0].text

        if ("," in stock_price):
            stock_price = stock_price.replace(",", "")

        ytdURL = (URL + ticker + YTD)
        ytdPage = requests.get(ytdURL)
        ytdSoup = BeautifulSoup(ytdPage.text, 'html.parser')
        # ytd_tr = ytdSoup.findAll("tr", {"class": "BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)"})
        ytd_td = ytdSoup.findAll("td", {"class": "Py(10px) Pstart(10px)"})
        jan_price = ytd_td[len(ytd_td)-2].text

        if ("," in jan_price):
            jan_price = jan_price.replace(",", "")

        YTDfinal = ((float(stock_price) - float(jan_price)) /
                    float(jan_price))*100
        YTDfinalrounded = ((YTDfinal*100)//1)/100.0

        # Running averages of YTDs
        asset_class = line[2]
        if (asset_class_YTDs.get(asset_class) == None):
            asset_class_YTDs[asset_class] = [YTDfinal, 1]
        else:
            asset_class_YTDs[asset_class][0] += YTDfinal
            asset_class_YTDs[asset_class][1] += 1

        line[3] = stock_price_span[0].text
        line[4] = str(YTDfinalrounded) + "%"

    for i in range(len(portfolioTickers)):
        line = portfolioLines[i+1]
        asset_class = line[2]
        asset_class_YTD = asset_class_YTDs[asset_class][0] / \
            asset_class_YTDs[asset_class][1]
        asset_class_YTD_rounded = ((asset_class_YTD*100)//1)/100.0
        line[5] = str(asset_class_YTD_rounded) + "%"
        print(line)

    print()
    writer = csv.writer(open(csvFilename, 'w'))
    writer.writerows(portfolioLines)


if __name__ == "__main__":
    main()

"""
, "FTCS", "SDSCX", "SEEGX", "OTICX"
# store the website URL in a variable
# use the url variable to fetch the entire page, store in a variable
# use entire page variable, find the HTML, store in a variable
acbpxURL = "https://finance.yahoo.com/quote/ACBPX?p=ACBPX&.tsrc=fin-srch"
acbpxPage = requests.get(acbpxURL)
acbpxSoup = BeautifulSoup(acbpxPage.text, 'html.parser')

# find a specific span by its class, store in a variable
# "D(ib) Mend(20px)" contains the share price of a stock
stock_price_span = acbpxSoup.findAll("span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})
"""