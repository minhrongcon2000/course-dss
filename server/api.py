from functools import reduce
from fastapi import FastAPI
from api_typing import Progress
from graph import SubjectGraph
from utils import ServerConfig
from data_loader import MySQLSubjectData


app = FastAPI()

@app.get("/")
def read_root():
    return "Hello"

@app.post("/suggestion")
def get_suggestion(progress: Progress, level: int=1):
    subject_graph = SubjectGraph()
    config = ServerConfig()
    subject_graph.load_from_mysql_database(config.host, 
                                       config.user, 
                                       config.password, 
                                       config.database)
    max_level, max_score, suggestion = subject_graph.suggest(progress.studied_subjects, level=level)
    total_credit = reduce(lambda a, b: a+b, map(subject_graph.get_total_credit, progress.studied_subjects))
    return {"max_level": max_level, 
            "score": max_score, 
            "requested_level": level,
            "total_credit": total_credit, 
            "suggestion": suggestion}
    
@app.get("/subjects")
def get_all_subjects():
    config = ServerConfig()
    loader = MySQLSubjectData(
        host=config.host,
        user=config.user,
        password=config.password,
        database=config.database
    )
    return loader.get_subject_data()
