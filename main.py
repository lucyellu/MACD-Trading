from AlgorithmImports import *
from datetime import timedelta, datetime
#'''
class IntradayMACDAlgorithm(QCAlgorithm):
    def Initialize(self):
        start_date = self.GetParameter("start_date") or "2023-01-01"
        end_date = self.GetParameter("end_date") or datetime.today().strftime('%Y-%m-%d')
        start_year, start_month, start_day = map(int, start_date.split('-'))
        end_year, end_month, end_day = map(int, end_date.split('-'))
        self.SetStartDate(start_year, start_month, start_day)
        self.SetEndDate(end_year, end_month, end_day)
        self.SetCash(100000)
        ticker = self.GetParameter("ticker") or "ARKK"
        self.AddEquity(ticker, Resolution.Minute)
        self.SetWarmUp(365)
        self.symbol = self.Securities[ticker].Symbol
       
        self.macds = {
            '1m': self.MACD(self.symbol, 12, 26, 9, MovingAverageType.Wilders, Resolution.Minute, Field.SevenBar),
            '5m': self.custom_macd(5),
            '10m': self.custom_macd(10),
            '15m': self.custom_macd(15),
            '30m': self.custom_macd(30),
            '60m': self.custom_macd(60),
            '1440m': self.custom_macd(1440),
            '10080m': self.custom_macd(10080),

        }
        self.buy_threshold = {
            '1m': float(self.GetParameter("buy_threshold_1m") or 0.01),
            '5m': float(self.GetParameter("buy_threshold_5m") or 0.01),
            '10m': float(self.GetParameter("buy_threshold_10m") or 0.1),
            '15m': float(self.GetParameter("buy_threshold_15m") or 0.15),
            '30m': float(self.GetParameter("buy_threshold_30m") or 0.1),
            '60m': float(self.GetParameter("buy_threshold_60m") or 0.1),
            '1440m': float(self.GetParameter("buy_threshold_1440m") or 0.1),
            '10080m': float(self.GetParameter("buy_threshold_10080m") or 0.1),  
        }
        self.sell_threshold = {
            '1m': float(self.GetParameter("sell_threshold_1m") or 0.05),
            '5m': float(self.GetParameter("sell_threshold_5m") or 0.1),
            '10m': float(self.GetParameter("sell_threshold_10m") or 0.1),
            '15m': float(self.GetParameter("sell_threshold_15m") or 0.2),
            '30m': float(self.GetParameter("sell_threshold_30m") or 0.1),
            '60m': float(self.GetParameter("sell_threshold_60m") or 0.1),
            '1440m': float(self.GetParameter("sell_threshold_1440m") or 0.2),
            '10080m': float(self.GetParameter("sell_threshold_10080m") or 0.1),
        }
        self.min_buy_signals = int(self.GetParameter("min_buy_signals") or 1)
        self.min_sell_signals = int(self.GetParameter("min_sell_signals") or 1)
        self.previous_histograms = {key: None for key in self.macds.keys()}
        
    def custom_macd(self, minutes):
        macd = MovingAverageConvergenceDivergence(12, 26, 9, MovingAverageType.Exponential)
        consolidator = QuoteBarConsolidator(timedelta(minutes=minutes))
        consolidator.DataConsolidated += lambda sender, bar: macd.Update(bar.EndTime, bar.Close)
        self.SubscriptionManager.AddConsolidator(self.symbol, consolidator)
        return macd
        
    def OnData(self, data):
        if not data.ContainsKey(self.symbol):
            return
        if self.IsWarmingUp:
            return

        self.symbol = self.AddEquity(ticker, Resolution.Minute).Symbol



    
    def OnData(self, data):
        if self.IsWarmingUp:
            return
        holdings = self.Portfolio[self.symbol].Quantity
        buy_signals = 0
        sell_signals = 0
        for key, macd in self.macds.items():
            histogram = macd.Current.Value - macd.Signal.Current.Value
            if self.previous_histograms[key] is not None:
                if self.previous_histograms[key] <= self.sell_threshold[key] and histogram > self.sell_threshold[key]:
                    sell_signals += 1                 
                if self.previous_histograms[key] >= -self.buy_threshold[key] and histogram < -self.buy_threshold[key]:
                    buy_signals += 1
            self.previous_histograms[key] = histogram
        shares_to_buy = int(self.GetParameter("shares_to_buy") or 100)
        shares_to_sell = int(self.GetParameter("shares_to_sell") or 100)     
        

        if holdings <= 2100 and buy_signals >= self.min_buy_signals:
            self.Buy(self.symbol, shares_to_buy)
        elif holdings > 0 and sell_signals >= self.min_sell_signals:
            self.Sell(self.symbol, shares_to_sell)
#'''

#
'''

'''
        if holdings <= 200 and buy_signals >= self.min_buy_signals:
            self.SetHoldings(self.symbol, 0.9)
        elif holdings > 0 and sell_signals >= self.min_sell_signals:
            self.SetHoldings(self.symbol, 0)
#'''

=======
        if holdings <= 200 and buy_signals >= self.min_buy_signals:
            self.SetHoldings(self.symbol, 0.9)
        elif holdings > 0 and sell_signals >= self.min_sell_signals:
            self.SetHoldings(self.symbol, 0)

#'''





'''

#benchmark just buy and hold ticker
class BuyAndHoldAlgorithm(QCAlgorithm):

    def Initialize(self):
        start_date = self.GetParameter("start_date") or "2023-06-15"
        end_date = self.GetParameter("end_date") or "2023-06-16"

        start_year, start_month, start_day = map(int, start_date.split('-'))
        end_year, end_month, end_day = map(int, end_date.split('-'))

        self.SetStartDate(start_year, start_month, start_day)
        self.SetEndDate(end_year, end_month, end_day)
        self.SetCash(100000)

        ticker = self.GetParameter("ticker") or "ARKK"


        self.symbol = self.AddEquity(ticker, Resolution.Minute).Symbol

        # Set a flag to indicate whether we have already purchased the security
        self.purchased = False

    def OnData(self, data):
        if not data.ContainsKey(self.symbol):
            return

        # If we have not purchased the security yet, buy it and set the purchased flag to True
        if not self.purchased:
            self.SetHoldings(self.symbol, 0.9)
            self.purchased = True

 #           '''


'''

#benchmark just buy and hold ticker
class BuyAndHoldAlgorithm(QCAlgorithm):

    def Initialize(self):
        start_date = self.GetParameter("start_date") or "2023-06-15"
        end_date = self.GetParameter("end_date") or "2023-06-16"

        start_year, start_month, start_day = map(int, start_date.split('-'))
        end_year, end_month, end_day = map(int, end_date.split('-'))

        self.SetStartDate(start_year, start_month, start_day)
        self.SetEndDate(end_year, end_month, end_day)
        self.SetCash(100000)

        ticker = self.GetParameter("ticker") or "AAPL"


        self.symbol = self.AddEquity(ticker, Resolution.Daily).Symbol

        # Set a flag to indicate whether we have already purchased the security
        self.purchased = False

    def OnData(self, data):
        if not data.ContainsKey(self.symbol):
            return

        # If we have not purchased the security yet, buy it and set the purchased flag to True
        if not self.purchased:
            self.SetHoldings(self.symbol, 1.0)
            self.purchased = True

 #           '''
