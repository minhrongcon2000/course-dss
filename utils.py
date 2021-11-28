from typing import List, Union
import networkx as nx
import matplotlib.pyplot as plt
import mysql.connector as connector
from dataclasses import dataclass


@dataclass
class Subject:
    subject_id: str
    subject_name: str
    subject_credit: int
    prerequisite_credit: Union[int, None] # mostly None, only thesis and prethesis will have this as not None
    constraint_subject_id: str
    

class MySQLSubjectData:
    def __init__(self, host: str, user: str, password: str, database: str) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        
        self.db = connector.connect(
            user=self.user,
            host=host,
            password=password,
            database=database
        )
        
    def get_data(self) -> List[Subject]:
        cursor = self.db.cursor()
        
        # This is a bad practice; however, since this project is small
        # this doesn't matter
        sql_statement = "SELECT * FROM Course;"
        
        cursor.execute(sql_statement)
        result = cursor.fetchall()
        return [Subject(subject_id=subject_id,
                        subject_name=subject_name,
                        subject_credit=subject_credit,
                        prerequisite_credit=prerequisite_credit,
                        constraint_subject_id=constraint_subject_id) 
                for 
                    subject_id, 
                    subject_name, 
                    subject_credit, 
                    prerequisite_credit, 
                    constraint_subject_id 
                in result]


class SubjectGraph:
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
        nx.draw(self.graph, with_labels=True)
        plt.show()
        
    def load_from_mysql_database(self, host: str, user: str, password: str, database: str):
        dataloader = MySQLSubjectData(host=host, user=user, password=password, database=database)
        subject_data = dataloader.get_data()
        
        for subject in subject_data:
            self.add_node(subject_id=subject.subject_id,
                          subject_name=subject.subject_name,
                          subject_credit=subject.subject_credit,
                          prerequisite_credit=subject.prerequisite_credit)
            
            if subject.constraint_subject_id is not None:
                self.make_constraint(prerequisite_id=subject.constraint_subject_id, main_subject_id=subject.subject_id)
        