from functools import reduce
from fastapi import FastAPI
from api_typing import Progress
from graph import SubjectGraph


app = FastAPI()

subject_graph = SubjectGraph()
subject_graph.load_from_mysql_database("localhost", 
                                       "root", 
                                       "johnuwu2000", 
                                       "all_course")

@app.get("/")
def read_root():
    return "Hello"

@app.post("/suggestion")
def get_suggestion(progress: Progress, level: int=1):
    max_level, max_score, suggestion = subject_graph.suggest(progress.studied_subjects, level=level)
    total_credit = reduce(lambda a, b: a+b, map(subject_graph.get_total_credit, progress.studied_subjects))
    return {"max_level": max_level, 
            "score": max_score, 
            "total_credit": total_credit, 
            "suggestion": suggestion}
