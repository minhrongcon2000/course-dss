from typing import Callable, Iterable, List, Set
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.shortest_paths.unweighted import predecessor
from data_loader import MySQLSubjectData
import numpy as np
from functools import reduce
from itertools import combinations
import copy


class SubjectGraph:
    MIN_SUBJECT = 3
    MAX_SUBJECT = 8
    MIN_CREDIT = 12
    MAX_CREDIT = 24
    def __init__(self) -> None:
        self.graph = nx.DiGraph()

    def add_node(self,
                 subject_id: str,
                 subject_name: str,
                 subject_credit: int,
                 prerequisite_credit: int = None) -> None:
        self.graph.add_node(subject_id,
                            subject_name=subject_name,
                            subject_credit=subject_credit,
                            prerequisite_credit=prerequisite_credit)

    def make_constraint(self, prerequisite_id: str, main_subject_id: str):
        self.graph.add_edge(prerequisite_id, main_subject_id)

    def visualize(self):
        plt.figure(figsize=(20, 5))
        nx.draw(self.graph, with_labels=True)
        plt.show()
        
    def load_from_mysql_database(self, host: str, user: str, password: str, database: str):
        dataloader = MySQLSubjectData(host=host, user=user, password=password, database=database)
        subject_data = dataloader.get_subject_data()
        constraint_data = dataloader.get_prerequisite_data()
        
        for subject in subject_data:
            self.add_node(subject_id=subject.subject_id,
                          subject_name=subject.subject_name,
                          subject_credit=subject.subject_credit,
                          prerequisite_credit=subject.prerequisite_credit)
            
        for course_id, prerequisite_id in constraint_data:
            self.make_constraint(prerequisite_id, course_id)
            
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
            if subject_id in enrich_studied_subjects:
                next_subject = set(self.graph.successors(subject_id))
                isNextSubject = len(next_subject) > 0 and len(next_subject.intersection(enrich_studied_subjects)) == 0
                if isNextSubject:
                    next_subjects = next_subjects.union(next_subject)
            else:
                subject_next = set(self.graph.successors(subject_id))
                subject_prev = set(self.graph.predecessors(subject_id))
                subject_info = self.graph.nodes[subject_id]
                
                isNextSubject = len(subject_prev) == 0 and len(subject_next.intersection(enrich_studied_subjects)) == 0 and (subject_info["prerequisite_credit"] is None or total_credit > subject_info["prerequisite_credit"])
                
                if isNextSubject:
                    next_subjects.add(subject_id)
                    
        return next_subjects
    
    def get_total_credit(self, studied_subjects: Iterable[str]) -> int:
        return reduce(lambda a, b: a + b, 
                      map(lambda subject: self.graph.nodes[subject]["subject_credit"], 
                          studied_subjects))
    
    def get_median_speed(self, progress: Iterable[Iterable[str]]) -> float:
        sem_credits = list(map(self.get_total_credit, progress))
        return np.median(sem_credits)
    
    def flatten(self, progress: List[Set[str]]):
        return reduce(lambda a, b: a.union(b), progress)
    
    def suggest(self, 
                progress: List[Set[str]], 
                speed_aggregate_func: Callable[[Iterable[Iterable[str]]], float]):
        studied_subject_set = self.flatten(progress)
        aggregate_speed = speed_aggregate_func(progress)
        
        next_subjects = self.get_next_subject(studied_subject_set)
        
        possible_combos = []
        
        for i in range(self.MIN_SUBJECT, self.MAX_SUBJECT + 1):
            combos = combinations(next_subjects, i)
            for combo in combos:
                combo_credit = self.get_total_credit(combo)
                
                if self.MIN_CREDIT <= combo_credit <= self.MAX_CREDIT:
                    possible_combos.append((combo, abs(combo_credit - aggregate_speed)))
                    
        return possible_combos
