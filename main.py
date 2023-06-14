from AlgorithmImports import *
from datetime import timedelta, datetime

'''
class IntradayMACDAlgorithm(QCAlgorithm):

    def Initialize(self):
        start_date = self.GetParameter("start_date") or "2023-01-01"
        end_date = self.GetParameter("end_date") or datetime.today().strftime('%Y-%m-%d')

        start_year, start_month, start_day = map(int, start_date.split('-'))
        end_year, end_month, end_day = map(int, end_date.split('-'))

        self.SetStartDate(start_year, start_month, start_day)
        self.SetEndDate(end_year, end_month, end_day)
        self.SetCash(100000)

        ticker = self.GetParameter("ticker") or "AAPL"

        self.AddEquity(ticker, Resolution.Minute)
        self.symbol = self.Securities[ticker].Symbol

        # Create and register custom consolidators for 5-minute, 15-minute, weekly, and monthly intervals
        self.macds = {
            '1d': self.MACD(self.symbol, 12, 26, 9, MovingAverageType.Wilders, Resolution.Daily, Field.SevenBar),
            '1h': self.MACD(self.symbol, 12, 26, 9, MovingAverageType.Wilders, Resolution.Hour, Field.SevenBar),
            '1m': self.MACD(self.symbol, 12, 26, 9, MovingAverageType.Wilders, Resolution.Minute, Field.SevenBar),
            '5m': self.custom_macd(5),
            '15m': self.custom_macd(15),
            '1w': self.custom_macd(7 * 24 * 60), # 7 days
            '1M': self.custom_macd(30 * 24 * 60), # 30 days, approximate for 1 month
        }

        self.SetWarmUp(26)

        self.previous_histograms = {key: None for key in self.macds.keys()}
        self.buy_histogram_threshold = float(self.GetParameter("buy_histogram_threshold") or 0.1)
        self.sell_histogram_threshold = float(self.GetParameter("sell_histogram_threshold") or 0.1)
        self.min_required_signals = int(self.GetParameter("min_required_signals") or 5)

    def custom_macd(self, minutes):
        macd = self.MACD(self.symbol, 12, 26, 9, MovingAverageType.Wilders, Resolution.Minute, Field.SevenBar)
        consolidator = TradeBarConsolidator(timedelta(minutes=minutes))
        consolidator.DataConsolidated += lambda sender, bar: macd.Update(bar.EndTime, bar.Close)
        self.SubscriptionManager.AddConsolidator(self.symbol, consolidator)
        return macd

    def OnData(self, data):
        if self.IsWarmingUp:
            return

        holdings = self.Portfolio[self.symbol].Quantity
        buy_signals = 0
        sell_signals = 0

        for key, macd in self.macds.items():
            histogram = macd.Current.Value - macd.Signal.Current.Value

            if self.previous_histograms[key] is not None:
                if self.previous_histograms[key] <= self.buy_histogram_threshold and histogram > self.buy_histogram_threshold:
                    buy_signals += 1
                if self.previous_histograms[key] >= -self.sell_histogram_threshold and histogram < -self.sell_histogram_threshold:
                    sell_signals += 1

            self.previous_histograms[key] = histogram

        if holdings <= 0 and buy_signals >= self.min_required_signals:
            self.SetHoldings(self.symbol, 0.9)
        elif holdings > 0 and sell_signals >= self.min_required_signals:
            self.Liquidate(self.symbol)

'''


'''
class IntradayMACDAlgorithm(QCAlgorithm):

    def Initialize(self):
        start_date = self.GetParameter("start_date") or "2023-01-01"
        end_date = self.GetParameter("end_date") or datetime.today().strftime('%Y-%m-%d')

        start_year, start_month, start_day = map(int, start_date.split('-'))
        end_year, end_month, end_day = map(int, end_date.split('-'))

        self.SetStartDate(start_year, start_month, start_day)
        self.SetEndDate(end_year, end_month, end_day)
        self.SetCash(100000)

        ticker = self.GetParameter("ticker") or "AAPL"

        self.AddEquity(ticker, Resolution.Minute)
        self.symbol = self.Securities[ticker].Symbol

        # Create and register custom consolidators for 5-minute, 15-minute, weekly, and monthly intervals
        self.macds = {
            '1d': self.MACD(self.symbol, 12, 26, 9, MovingAverageType.Wilders, Resolution.Daily, Field.SevenBar),
            '1h': self.MACD(self.symbol, 12, 26, 9, MovingAverageType.Wilders, Resolution.Hour, Field.SevenBar),
            '1m': self.MACD(self.symbol, 12, 26, 9, MovingAverageType.Wilders, Resolution.Minute, Field.SevenBar),
            '5m': self.custom_macd(5),
            '15m': self.custom_macd(15),
            '1w': self.custom_macd(7 * 24 * 60), # 7 days
            '1M': self.custom_macd(30 * 24 * 60), # 30 days, approximate for 1 month
        }

        self.SetWarmUp(26)

        self.previous_histograms = {key: None for key in self.macds.keys()}
        self.buy_histogram_threshold = float(self.GetParameter("buy_histogram_threshold") or 0.1)
        self.sell_histogram_threshold = float(self.GetParameter("sell_histogram_threshold") or 0.1)
        self.min_required_signals = 1

    def custom_macd(self, minutes):
        macd = self.MACD(self.symbol, 12, 26, 9, MovingAverageType.Wilders, Resolution.Minute, Field.SevenBar)
        consolidator = TradeBarConsolidator(timedelta(minutes=minutes))
        consolidator.DataConsolidated += lambda sender, bar: macd.Update(bar.EndTime, bar.Close)
        self.SubscriptionManager.AddConsolidator(self.symbol, consolidator)
        return macd

    def OnData(self, data):
        if self.IsWarmingUp:
            return

        holdings = self.Portfolio[self.symbol].Quantity
        buy_signals = 0
        sell_signals = 0

        for key, macd in self.macds.items():
            histogram = macd.Current.Value - macd.Signal.Current.Value

            if self.previous_histograms[key] is not None:
                if self.previous_histograms[key] <= self.buy_histogram_threshold and histogram > self.buy_histogram_threshold:
                    buy_signals += 1
                if self.previous_histograms[key] >= -self.sell_histogram_threshold and histogram < -self.sell_histogram_threshold:
                    sell_signals += 1

            self.previous_histograms[key] = histogram

        if holdings <= 0 and buy_signals >= self.min_required_signals:
            self.SetHoldings(self.symbol, 0.9)
        elif holdings > 0 and sell_signals >= self.min_required_signals:
            self.Liquidate(self.symbol)
'''
'''
class IntradayMACDAlgorithm(QCAlgorithm):

    def Initialize(self):
        start_date = self.GetParameter("start_date") or "2023-01-01"
        end_date = self.GetParameter("end_date") or datetime.today().strftime('%Y-%m-%d')
        min_required_signals = self.GetParameter(

        start_year, start_month, start_day = map(int, start_date.split('-'))
        end_year, end_month, end_day = map(int, end_date.split('-'))


        self.SetStartDate(start_year, start_month, start_day)
        self.SetEndDate(end_year, end_month, end_day)
        self.SetMinRequiredSignals(min_required_signals)
        self.SetCash(100000)

        ticker = self.GetParameter("ticker") or "AAPL"

        self.AddEquity(ticker, Resolution.Minute)
        self.symbol = self.Securities[ticker].Symbol

        # Create and register custom consolidators for 5-minute, 15-minute, weekly, and monthly intervals
        self.macds = {
            '1d': self.MACD(self.symbol, 12, 26, 9, MovingAverageType.Wilders, Resolution.Daily, Field.SevenBar),
            '1h': self.MACD(self.symbol, 12, 26, 9, MovingAverageType.Wilders, Resolution.Hour, Field.SevenBar),
            '1m': self.MACD(self.symbol, 12, 26, 9, MovingAverageType.Wilders, Resolution.Minute, Field.SevenBar),
            '5m': self.custom_macd(5),
            '15m': self.custom_macd(15),
            '1w': self.custom_macd(7 * 24 * 60), # 7 days
            '1M': self.custom_macd(30 * 24 * 60), # 30 days, approximate for 1 month
        }

        self.SetWarmUp(26)

        self.previous_histograms = {key: None for key in self.macds.keys()}
        self.buy_histogram_threshold = float(self.GetParameter("buy_histogram_threshold") or 0.1)
        self.sell_histogram_threshold = float(self.GetParameter("sell_histogram_threshold") or 0.1)
        self.min_required_signals = float(self.GetParameter("min_required_signals") or 4)

    def custom_macd(self, minutes):
        macd = self.MACD(self.symbol, 12, 26, 9, MovingAverageType.Wilders, Resolution.Minute, Field.SevenBar)
        consolidator = TradeBarConsolidator(timedelta(minutes=minutes))
        consolidator.DataConsolidated += lambda sender, bar: macd.Update(bar.EndTime, bar.Close)
        self.SubscriptionManager.AddConsolidator(self.symbol, consolidator)
        return macd

    def OnData(self, data):
        if self.IsWarmingUp:
            return

        holdings = self.Portfolio[self.symbol].Quantity
        buy_signals = 0
        sell_signals = 0

        for key, macd in self.macds.items():
            histogram = macd.Current.Value - macd.Signal.Current.Value

            if self.previous_histograms[key] is not None:
                if self.previous_histograms[key] <= self.buy_histogram_threshold and histogram > self.buy_histogram_threshold:
                    buy_signals += 1
                if self.previous_histograms[key] >= -self.sell_histogram_threshold and histogram < -self.sell_histogram_threshold:
                    sell_signals += 1

            self.previous_histograms[key] = histogram

        if holdings <= 0 and buy_signals >= self.min_required_signals:
            self.SetHoldings(self.symbol, 0.9)
        elif holdings > 0 and sell_signals >= self.min_required_signals:
            self.Liquidate(self.symbol)
'''
'''
class IntradayMACDAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2010, 1, 1)
        self.SetCash(100000)

        ticker = self.GetParameter("ticker") or "AAPL"

        self.AddEquity(ticker, Resolution.Minute)
        self.symbol = self.Securities[ticker].Symbol

        # Create and register custom consolidators for 5-minute, 15-minute, weekly, and monthly intervals
        self.macds = {
            '1d': self.MACD(self.symbol, 12, 26, 9, MovingAverageType.Wilders, Resolution.Daily, Field.SevenBar),
            '1h': self.MACD(self.symbol, 12, 26, 9, MovingAverageType.Wilders, Resolution.Hour, Field.SevenBar),
            '1m': self.MACD(self.symbol, 12, 26, 9, MovingAverageType.Wilders, Resolution.Minute, Field.SevenBar),
            '5m': self.custom_macd(5),
            '15m': self.custom_macd(15),
            '1w': self.custom_macd(7 * 24 * 60), # 7 days
            '1M': self.custom_macd(30 * 24 * 60), # 30 days, approximate for 1 month
        }

        self.SetWarmUp(26)

        self.previous_histograms = {key: None for key in self.macds.keys()}
        self.buy_histogram_threshold = float(self.GetParameter("buy_histogram_threshold") or 0.2)
        self.sell_histogram_threshold = float(self.GetParameter("sell_histogram_threshold") or 0.2)
        self.min_required_signals = 4

    def custom_macd(self, minutes):
        macd = self.MACD(self.symbol, 12, 26, 9, MovingAverageType.Wilders, Resolution.Minute, Field.SevenBar)
        consolidator = TradeBarConsolidator(timedelta(minutes=minutes))
        consolidator.DataConsolidated += lambda sender, bar: macd.Update(bar.EndTime, bar.Close)
        self.SubscriptionManager.AddConsolidator(self.symbol, consolidator)
        return macd

    def OnData(self, data):
        if self.IsWarmingUp:
            return

        holdings = self.Portfolio[self.symbol].Quantity
        buy_signals = 0
        sell_signals = 0

        for key, macd in self.macds.items():
            histogram = macd.Current.Value - macd.Signal.Current.Value

            if self.previous_histograms[key] is not None:
                if self.previous_histograms[key] <= self.buy_histogram_threshold and histogram > self.buy_histogram_threshold:
                    buy_signals += 1
                if self.previous_histograms[key] >= -self.sell_histogram_threshold and histogram < -self.sell_histogram_threshold:
                    sell_signals += 1

            self.previous_histograms[key] = histogram

        if holdings <= 0 and buy_signals >= self.min_required_signals:
            self.SetHoldings(self.symbol, 0.9)
        elif holdings > 0 and sell_signals >= self.min_required_signals:
            self.Liquidate(self.symbol)
'''
'''
class IntradayMACDAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2023, 1 , 1)
        self.SetCash(100000)

        ticker = self.GetParameter("ticker") or "AAPL"

        self.symbol = self.AddEquity(ticker, Resolution.Minute).Symbol

        # Create and register custom consolidators for 5-minute and 15-minute intervals
        self.macds = {
            '1d': self.MACD(self.symbol, 12, 26, 9, MovingAverageType.Wilders, Resolution.Daily, Field.SevenBar),
            '1h': self.MACD(self.symbol, 12, 26, 9, MovingAverageType.Wilders, Resolution.Hour, Field.SevenBar),
            '1m': self.MACD(self.symbol, 12, 26, 9, MovingAverageType.Wilders, Resolution.Minute, Field.SevenBar),
            '5m': self.custom_macd(5),
            '15m': self.custom_macd(15),
        }

        self.SetWarmUp(26)

        self.previous_histograms = {key: None for key in self.macds.keys()}
        self.histogram_threshold = 0.1

    def custom_macd(self, minutes):
        macd = self.MACD(self.symbol, 12, 26, 9, MovingAverageType.Wilders, Resolution.Minute, Field.SevenBar)
        consolidator = TradeBarConsolidator(timedelta(minutes=minutes))
        consolidator.DataConsolidated += lambda sender, bar: macd.Update(bar.EndTime, bar.Close)
        self.SubscriptionManager.AddConsolidator(self.symbol, consolidator)
        return macd

    def OnData(self, data):
        if self.IsWarmingUp:
            return

        holdings = self.Portfolio[self.symbol].Quantity
        buy_signals = 0
        sell_signals = 0

        for key, macd in self.macds.items():
            histogram = macd.Current.Value - macd.Signal.Current.Value

            if self.previous_histograms[key] is not None:
                if self.previous_histograms[key] <= self.histogram_threshold and histogram > self.histogram_threshold:
                    buy_signals += 1
                if self.previous_histograms[key] >= -self.histogram_threshold and histogram < -self.histogram_threshold:
                    sell_signals += 1

            self.previous_histograms[key] = histogram

        threshold = len(self.macds) // 2

        if holdings <= 0 and buy_signals > threshold:
            self.SetHoldings(self.symbol, 0.9)
        elif holdings > 0 and sell_signals > threshold:
            self.Liquidate(self.symbol)
'''
'''
class MyAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2023, 1, 1)
        self.SetCash(100000)

        # Get the ticker symbol from the user input or use "SPY" as the default value
        ticker = self.GetParameter("ticker") or "SPY"

        self.symbol = self.AddEquity(ticker, Resolution.Daily).Symbol

        # Create a MACD indicator with default parameters (12, 26, 9)
        self.macd = self.MACD(self.symbol, 12, 26, 9, MovingAverageType.Wilders, Resolution.Daily, Field.SevenBar)

        # Wait for the indicator to be fully initialized
        self.SetWarmUp(30)

    def OnData(self, data):
        if self.IsWarmingUp:
            return

        # Check if we have enough data to make trading decisions
        if not self.macd.IsReady:
            self.Debug("MACD is not ready")
            return

        holdings = self.Portfolio[self.symbol].Quantity

        # Buy signal: MACD crosses above its signal line
        if holdings <= 0 and self.macd.Current.Value > self.macd.Signal.Current.Value:
            self.SetHoldings(self.symbol, 1.0)

        # Sell signal: MACD crosses below its signal line
        elif holdings > 0 and self.macd.Current.Value < self.macd.Signal.Current.Value:
            self.Liquidate(self.symbol)
'''   


#'''
#benchmark just buy and hold ticker
class BuyAndHoldAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2023, 1, 1)
        self.SetCash(100000)

        # Get the ticker symbol from the user input or use "SPY" as the default value
        ticker = self.GetParameter("ticker") or "SPY"

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
