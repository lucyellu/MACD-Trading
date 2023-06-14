from AlgorithmImports import *

class CustomUniverseSelectionModel(UniverseSelectionModel):
    def __init__(self, algorithm: QCAlgorithm, universe_settings: UniverseSettings = None, coarse_size: int = 100, portfolio_size: int = 10) -> None:
        self.algorithm = algorithm
        self.coarse_size = coarse_size
        self.portfolio_size = portfolio_size
        self.month = -1
        self.hours = None

    def SelectCoarse(self, coarse: List[CoarseFundamental]) -> List[Symbol]:
        if not self.hours or self.algorithm.LiveMode:
            self.hours = self.algorithm.MarketHoursDatabase.GetEntry(Market.USA, "SPY", SecurityType.Equity).ExchangeHours
        self.next_open = self.hours.GetNextMarketOpen(self.algorithm.Time, False)
        if self.month == self.next_open.month:
            return Universe.Unchanged
        selected = [c for c in coarse if c.HasFundamentalData]
        sorted_by_dollar_volume = sorted(selected, key=lambda c: c.DollarVolume, reverse=True)
        return [c.Symbol for c in sorted_by_dollar_volume[:self.portfolio_size]]

    def CreateUniverses(self, algorithm: QCAlgorithm) -> List[Universe]:
        def selection_function(coarse):
            return self.SelectCoarse(coarse)

        coarse_universe = algorithm.AddUniverse(CoarseFundamentalUniverse, selection_function)
        return [coarse_universe]
