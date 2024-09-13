# 高速道路上のIC間経路を計算するためのプログラム
from typing import Dict, List

import networkx as nx
import pandas as pd


class ExpresswayRouter:
    SMALL_IC_SET = {
        "1040014",
        "1040019",
        "1040021",
        "1040041",
        "1040071",
        "1040081",
        "1040111",
        "1800004",
        "1800031",
        "1800046",
        "1800093",
        "1800101",
    }

    def __init__(self, icnet_file: str) -> None:
        df_icnet = pd.read_csv(
            icnet_file, dtype={"start_code": str, "end_code": str, "road_code": str}
        )
        self.__ic_graph = nx.from_pandas_edgelist(
            df_icnet,
            source="start_code",
            target="end_code",
            edge_attr=["distance", "road_code", "direction"],
            create_using=nx.DiGraph(),
        )
        self.__ic_nodes_set: set = set(self.__ic_graph.nodes)

        print("Loading IC Network...")
        self.__route_dict: Dict[str, Dict[str, List[str]]] = dict(
            nx.all_pairs_dijkstra_path(self.__ic_graph, weight="distance")
        )
        print("Finished.")

    def __get_route(self, src: str, dest: str) -> List[str]:
        if not (src in self.__ic_nodes_set and dest in self.__ic_nodes_set):
            return []
        try:
            path = self.__route_dict[src][dest]
            return path
        except:  # 経路が存在しない, もしくはノードがグラフ上に存在しない場合
            return []

    def get_route(self, src: str, dest: str) -> List[str]:
        """
        ic_graph上で出発地から目的地までの経路を得る関数

        Parameters
        ----------
        src: 出発ICコード
        dest: 目的ICコード
        """
        path = [
            ic
            for ic in self.__get_route(src, dest)
            if ic not in ExpresswayRouter.SMALL_IC_SET
        ]
        return path
