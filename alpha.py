#region imports
from AlgorithmImports import *
#endregion

from AlgorithmImports import *

class MACDAlphaModel(AlphaModel):

    def __init__(self):
        self.macd_by_symbol = {}

    def Update(self, algorithm, data):
        insights = []

        for symbol, macd in self.macd_by_symbol.items():
            if not data.ContainsKey(symbol) or data[symbol] is None:
                continue

            if not macd.IsReady:
                return insights

            signal_delta = macd.Current.Value - macd.Signal.Current.Value

            if signal_delta > 0:
                insights.append(Insight.Price(symbol, timedelta(days=1), InsightDirection.Up))
            elif signal_delta < 0:
                insights.append(Insight.Price(symbol, timedelta(days=1), InsightDirection.Down))

        return insights

    def OnSecuritiesChanged(self, algorithm, changes):
        for added in changes.AddedSecurities:
            if added.Symbol not in self.macd_by_symbol:
                macd = algorithm.MACD(added.Symbol, 12, 26, 9, MovingAverageType.Wilders, Resolution.Daily, Field.SevenBar)
                self.macd_by_symbol[added.Symbol] = macd

        for removed in changes.RemovedSecurities:
            if removed.Symbol in self.macd_by_symbol:
                self.macd_by_symbol.pop(removed.Symbol, None)

