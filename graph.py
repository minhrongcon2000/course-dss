from typing import Iterable, List, Set
import networkx as nx
import numpy as np
from functools import reduce
from itertools import combinations
import pandas as pd
import os
import math

from pandas.core.frame import DataFrame

from pyvis.network import Network

class SubjectGraph:
    MIN_SUBJECT = 3
    MAX_SUBJECT = 8
    MIN_CREDIT = 12
    MAX_CREDIT = 24
    def __init__(self) -> None:
        self.graph = nx.DiGraph()
        self.vis_graph = Network(height="700px", width="700px", directed=True)
        # self.vis_graph.barnes_hut()
        # self.vis_graph.force_atlas_2based()
        self.vis_graph.hrepulsion()

    def add_node(self,
                 subject_id: str,
                 subject_name: str,
                 subject_credit: int,
                 is_available: bool,
                 prerequisite_credit: int,
                 is_shown: bool=True) -> None:
        title = "{}:{}\n{}:{}\n{}:{}".format(
            "Subject name", 
            subject_name, 
            "Subject credit", 
            subject_credit,
            "Required credit",
            prerequisite_credit
        )
        self.graph.add_node(subject_id,
                            subject_name=subject_name,
                            subject_credit=subject_credit,
                            prerequisite_credit=prerequisite_credit,
                            is_available=is_available)
        if is_shown:
            self.vis_graph.add_node(subject_id, 
                                label=subject_name,
                                title=title,
                                color="#ffcccc" if not is_available else "#71f5f3",
                                hidden=not is_shown)

    def make_constraint(self, prerequisite_id: str, main_subject_id: str):
        self.graph.add_edge(prerequisite_id, main_subject_id)
        self.vis_graph.add_edge(prerequisite_id, main_subject_id, physics=False, color="#000000")
            
    def get_all_previous_subject(self, subject_id: str) -> Set[str]:
        prev_subject = set()
        cur_subject = set(self.graph.predecessors(subject_id))
        while len(cur_subject) > 0:
            prev_subject = prev_subject.union(cur_subject)
            next_subjects = set()
            
            for cur_subject_id in cur_subject:
                next_subjects = next_subjects.union(set(self.graph.predecessors(cur_subject_id)))
                
            cur_subject = next_subjects
        
        return prev_subject

            
    def enrich(self, studied_subjects: Set[str]):
        return studied_subjects.union(
            reduce(lambda a, b: a.union(b), 
                   map(lambda subject: self.get_all_previous_subject(subject), studied_subjects))
        )
            
    def get_next_subject(self, studied_subjects: Set[str]) -> Set[str]:
        next_subjects = set()
        enrich_studied_subjects = self.enrich(studied_subjects)
        
        total_credit = self.get_total_credit(studied_subjects)
        
        for subject_id in self.graph.nodes:
            if self.graph.nodes[subject_id]["is_available"]:
                if subject_id in enrich_studied_subjects:
                    next_subject = set(self.graph.successors(subject_id))
                    isNextSubject = len(next_subject) > 0 and len(next_subject.intersection(enrich_studied_subjects)) == 0
                    if isNextSubject:
                        next_subjects = next_subjects.union(next_subject)
                else:
                    subject_next = set(self.graph.successors(subject_id))
                    subject_prev = set(self.graph.predecessors(subject_id))
                    subject_info = self.graph.nodes[subject_id]
                    
                    isNextSubject = len(subject_prev) == 0 \
                        and len(subject_next.intersection(enrich_studied_subjects)) == 0 \
                            and (subject_info["prerequisite_credit"] is None or total_credit >= subject_info["prerequisite_credit"])
                    
                    if isNextSubject:
                        next_subjects.add(subject_id)
                    
        return next_subjects
    
    def get_total_credit(self, studied_subjects: Iterable[str]) -> int:
        return reduce(lambda a, b: a + b, 
                      map(lambda subject: self.graph.nodes[subject]["subject_credit"], 
                          studied_subjects))
    
    def flatten(self, progress: List[Set[str]]):
        return reduce(lambda a, b: a.union(b), progress)
    
    def suggest(self, 
                progress: List[Set[str]],
                level: int=1):
        studied_subject_set = self.flatten(progress)
        credit = list(map(self.get_total_credit, progress))
        num_subjects = list(map(lambda item: len(item), progress))
        
        area_of_suggestion = list(zip(credit, num_subjects))
        
        next_subjects = self.get_next_subject(studied_subject_set)
        
        possible_combos = []
        
        for i in range(self.MIN_SUBJECT, self.MAX_SUBJECT + 1):
            combos = combinations(next_subjects, i)
            for combo in combos:
                combo_credit = self.get_total_credit(combo)
                combo_score = 0
                
                for subject_credit, subject_number in area_of_suggestion:
                    combo_score += (combo_credit - subject_credit) ** 2
                    combo_score += (i - subject_number) ** 2
                    combo_score = math.sqrt(combo_score)
                
                if self.MIN_CREDIT <= combo_credit <= self.MAX_CREDIT:
                    combo_full_info = []
                    for subject in combo:
                        subject_info = {k:v for k, v in self.graph.nodes[subject].items() if k not in ["prerequisite_credit", "is_available"]}
                        subject_info["subject_id"] = subject
                        combo_full_info.append(subject_info)
                    possible_combos.append((combo_full_info, combo_score))
                    
        scores = np.unique([item[1] for item in possible_combos])
        scores = np.sort(scores)
        
        level_score = scores[level - 1]
        max_level = len(scores)
                    
        return max_level, level_score, [item[0] for item in possible_combos if item[1] == level_score]
    
    def get_extra_subject(self, subject_list):
        not_avail_subject = []
        for subject_id in subject_list:
            prev_subject_ids = self.graph.predecessors(subject_id)
            for prev_subject_id in prev_subject_ids:
                subject_name = self.graph.nodes[prev_subject_id]["subject_name"]
                subject_credit = self.graph.nodes[prev_subject_id]["subject_credit"]
                subject_avail = self.graph.nodes[prev_subject_id]["is_available"]
                
                if not subject_avail:
                    not_avail_subject.append({"subject_id": prev_subject_id, 
                                              "subject_name": subject_name,
                                              "subject_credit": subject_credit})
        return not_avail_subject
    
    def get_dependency_graph(self, subject_id) -> nx.DiGraph:
        chosen_nodes = self.get_all_previous_subject(subject_id).union({subject_id})
        subgraph = self.graph.subgraph(list(chosen_nodes)).copy()
        
        return subgraph
    
    def _build_subject_data(self):
        node_info = self.graph.nodes
        subject_data = []
        
        for subject_id in node_info:
            subject_info = {k: v for k, v in node_info[subject_id].items()}
            subject_info["subject_id"] = subject_id
            subject_data.append(subject_info)
            
        return pd.DataFrame(subject_data)
    
    def _build_dependency_data(self):
        edge_info = self.graph.edges
        dependency_data = [dict(source=source, target=target) for source, target in edge_info]
        return pd.DataFrame(dependency_data)
    
    def save(self, save_dir):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        subject_data = self._build_subject_data()
        dependency_data = self._build_dependency_data()
        subject_data.to_csv(os.path.join(save_dir, "subjects.csv"), index=False)
        dependency_data.to_csv(os.path.join(save_dir, "dependency.csv"), index=False)
        
    def _load_node_data(self, subject_data: DataFrame, overview: bool):
        for i in range(len(subject_data)):
            subject_id = subject_data.loc[i, "id"]
            subject_name = subject_data.loc[i, "name"]
            subject_credit = subject_data.loc[i, "credit"]
            subject_required_credit = subject_data.loc[i, "required_credit"]
            subject_available = subject_data.loc[i, "is_available"]
            subject_visible = subject_data.loc[i, "is_shown"]
            
            self.add_node(
                subject_id=subject_id,
                subject_name=subject_name,
                subject_credit=subject_credit,
                is_available=subject_available,
                prerequisite_credit=subject_required_credit,
                is_shown=subject_visible if overview else True
            )
            
    def _load_dependency_data(self, dependency_data: DataFrame, shown_data: DataFrame, overview: bool):
        for i in range(len(dependency_data)):
            source = dependency_data.loc[i, "source"]
            target = dependency_data.loc[i, "target"]
            if not overview or (overview and shown_data.loc[source, "is_shown"] and shown_data.loc[target, "is_shown"]):
                self.make_constraint(source, target)
        
    def load(self, save_dir, overview=False):
        subject_data = pd.read_csv(os.path.join(save_dir, "subjects.csv"))
        dependency_data = pd.read_csv(os.path.join(save_dir, "dependency.csv"))
        
        self._load_node_data(subject_data, overview=overview)
        self._load_dependency_data(dependency_data, 
                                   subject_data.loc[:, ["id", "is_shown"]].set_index("id"),
                                   overview=overview)
        
    def visualize(self, save_dir="html/subject_graph.html"):
        self.vis_graph.show(save_dir)
