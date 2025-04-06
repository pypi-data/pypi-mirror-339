from context.MetricCalculationContext import MetricCalculationContext
from database.CommunityDetection import Leiden, Louvain
from database.GraphDbManager import GraphDBManager
from database.MetricsCalculate import Betweenness, PageRank
"""
    Класс записывающий метрики сетей в бд
"""


class MetricDataPreparer:
    def __init__(
            self,
            metric_calculation_context: MetricCalculationContext,
            graph_name,
            db_manager: GraphDBManager
    ):
        self.leiden_calculator = None
        self.louvain_calculator = None
        self.betweenessens_calculator = None
        self.page_rank_calculator = None
        if metric_calculation_context.need_leiden_community_id or metric_calculation_context.need_leiden_modulariry:
            self.leiden_calculator = Leiden()
        if metric_calculation_context.need_louvain_community_id or metric_calculation_context.need_louvain_modulariry:
            self.louvain_calculator = Louvain()
        if metric_calculation_context.need_betweenessens:
            self.betweenessens_calculator = Betweenness()
        if metric_calculation_context.need_page_rank:
            self.page_rank_calculator = PageRank()
        self.graph_name = graph_name
        self.db_manager = db_manager

    def prepare_metrics(self):
        result = {}
        if self.leiden_calculator is not None:
            result["leiden_modularity_value"] = self.prepare_leiden()
        if self.louvain_calculator is not None:
            result["louvain_modularity_value"] = self.prepare_louvain()
        if self.betweenessens_calculator is not None:
            self.prepare_betweenessens()
        if self.page_rank_calculator is not None:
            self.prepare_page_rank()
        return result

    def prepare_leiden(self):
        result = self.leiden_calculator.detect_communities(
            self.graph_name,
            self.db_manager.weight,
            self.db_manager.get_main_node_name(),
            self.db_manager.get_main_rels_name()
        )
        print(f"LeidenAlgorithm Community detection for graph {self.graph_name} completed.")
        return result

    def prepare_louvain(self):
        result = self.louvain_calculator.detect_communities(
            self.graph_name,
            self.db_manager.weight,
            self.db_manager.get_main_node_name(),
            self.db_manager.get_main_rels_name()
        )
        print(f"LovainAlgorithm Community detection for graph {self.graph_name} completed.")
        return result

    def prepare_betweenessens(self):
        self.betweenessens_calculator.metric_calculate(
            self.graph_name,
            self.db_manager.weight,
            self.db_manager.get_main_node_name(),
            self.db_manager.get_main_rels_name()
        )
        print(f"betweenessens metric calculated for graph {self.graph_name}.")

    def prepare_page_rank(self):
        self.page_rank_calculator.metric_calculate(
            self.graph_name,
            self.db_manager.weight,
            self.db_manager.get_main_node_name(),
            self.db_manager.get_main_rels_name()
        )
        print(f"pageRank metric calculated for graph {self.graph_name}.")

