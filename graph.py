from utils import SubjectGraph


graph = SubjectGraph()
graph.load_from_mysql_database(host="localhost", user="root", password="johnuwu2000", database="all_course")
graph.visualize()
