#region imports
from AlgorithmImports import *
#endregion


class CustomPortfolioConstructionModel(PortfolioConstructionModel):

    def CreateTargets(self, algorithm, insights):
        targets = []

        # Calculate the total weight for all insights with direction (Up or Down)
        up_down_insights = [i for i in insights if i.Direction != InsightDirection.Flat]
        total_weight = len(up_down_insights)

        # If there are no insights with direction, return an empty target list
        if total_weight == 0:
            return targets

        # Calculate the individual weight for each security
        weight = 1 / total_weight

        for insight in insights:
            # Set target weights based on the insight direction
            if insight.Direction == InsightDirection.Up:
                targets.append(PortfolioTarget.Percent(algorithm, insight.Symbol, weight))
            elif insight.Direction == InsightDirection.Down:
                targets.append(PortfolioTarget.Percent(algorithm, insight.Symbol, -weight))
            else:
                targets.append(PortfolioTarget.Percent(algorithm, insight.Symbol, 0))

        return targets


'''

class EqualWeightingRebalanceOnInsightsPortfolioConstructionModel(EqualWeightingPortfolioConstructionModel):
    def __init__(self, algorithm):
        super().__init__()
        self.algorithm = algorithm
        self.new_insights = False

    def IsRebalanceDue(self, insights: List[Insight], algorithmUtc: datetime) -> bool:
        if not self.new_insights:
            self.new_insights = len(insights) > 0
        is_rebalance_due = self.new_insights and not self.algorithm.IsWarmingUp and self.algorithm.CurrentSlice.QuoteBars.Count > 0
        if is_rebalance_due:
            self.new_insights = False
        return is_rebalance_due

'''
