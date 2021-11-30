import mysql.connector as connector
from typing import List, Tuple
from utils import Subject

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
        
    def get_subject_data(self) -> List[Subject]:
        cursor = self.db.cursor()
        
        # This is a bad practice; however, since this project is small
        # this doesn't matter
        sql_statement = "SELECT * FROM Course;"
        
        cursor.execute(sql_statement)
        result = cursor.fetchall()
        return [Subject(subject_id=subject_id,
                        subject_name=subject_name,
                        subject_credit=subject_credit,
                        prerequisite_credit=prerequisite_credit) 
                for 
                    subject_id, 
                    subject_name, 
                    subject_credit, 
                    prerequisite_credit
                in result]
        
    def get_prerequisite_data(self) -> List[Tuple]:
        cursor = self.db.cursor()
        
        # This is a bad practice; however, since this project is small
        # this doesn't matter
        sql_statement = "SELECT * FROM Prerequisite;"
        cursor.execute(sql_statement)
        result = cursor.fetchall()
        
        return [(course_id, prerequisite_id) for course_id, prerequisite_id in result]