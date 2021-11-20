CREATE DATABASE all_course;
CREATE DATABASE IF NOT exists all_course;
USE all_course;
CREATE TABLE Course(
	Course_Id char primary key, 
    Course_Name char, 
    Credit int, 
    Required_credit int null, 
    Prerequisite_id char null references Course(Course_Id)
    );
    
INSERT INTO Course VALUES ('EN073IU','Listening & Speaking IE1', 11, NULL, NULL);
INSERT INTO Course VALUES ('EN072IU','Reading & Writing IE1', 11, NULL, NULL);
INSERT INTO Course VALUES ('PT001IU','Physical Training 1', 3, NULL, NULL);
INSERT INTO Course VALUES ('PH013IU','Physics 1', 2, NULL, NULL);
INSERT INTO Course VALUES ('EN075IU','Listening & Speaking IE2', 8, NULL, 'EN073IU');
INSERT INTO Course VALUES ('EN074IU','Reading & Writing IE2', 8, NULL, 'EN072IU');
INSERT INTO Course VALUES ('PT002IU','Physical Training 2', 3, NULL, 'PT001IU');
INSERT INTO Course VALUES ('IT135IU','Introduction to Data Science', 3, NULL, NULL);
INSERT INTO Course VALUES ('IT149IU','Fundamentals of Programming', 4, NULL, NULL);
INSERT INTO Course VALUES ('MA001IU','Calculus 1', 4, NULL, NULL);
INSERT INTO Course VALUES ('MA003IU','Calculus 2', 4,  NULL, 'MA001IU');
INSERT INTO Course VALUES ('CH011IU','Chemistry for Engineers', 3, NULL, NULL);
INSERT INTO Course VALUES ('IT013IU','Algorithms & Data Structures', 4, NULL, NULL);
INSERT INTO Course VALUES ('PH014IU','Physics 2', 2, 'PH013IU', NULL, NULL);
INSERT INTO Course VALUES ('CH012IU','Chemistry Laboratory', 1, NULL, NULL);
INSERT INTO Course VALUES ('IT137IU','Data Analysis', 4, NULL, NULL);
INSERT INTO Course VALUES ('IT069IU','Object-Oriented Programming', 4, NULL, NULL);
INSERT INTO Course VALUES ('IT079IU','Principles of Database Management', 4, NULL, NULL);
INSERT INTO Course VALUES ('IT136IU','Regression Analysis', 4, NULL, NULL);
INSERT INTO Course VALUES ('IT090IU','Object-Oriented Analysis and Design', 4, NULL, 'IT069IU');
INSERT INTO Course VALUES ('MA023IU','Calculus 3', 4, NULL, 'MA003IU');
INSERT INTO Course VALUES ("IT138IU","Data Science and Data Visualization",4, NULL, NULL);
INSERT INTO Course VALUES ("IT151IU","Statistical Methods",3, NULL, NULL);
INSERT INTO Course VALUES ("IT139IU","Scalable and Distributed Computing",4, NULL, NULL);
INSERT INTO Course VALUES ("IT097IU","Introduction to Artificial Intelligence",4, NULL, NULL);
INSERT INTO Course VALUES ("EN007IU","Writing AE1",2, NULL, NULL);
INSERT INTO Course VALUES ("EN008IU","Listening AE1",2, NULL, NULL);
INSERT INTO Course VALUES ("PE011IU","Principles of Marxism",5, NULL, NULL);
INSERT INTO Course VALUES ("MA026IU","Probability, Statistic & Random Process",3, NULL, NULL);
INSERT INTO Course VALUES ("IT140IU","Fundamental Concepts of Data Security",4, NULL, NULL);
INSERT INTO Course VALUES ("EN011IU","Writing AE2",2, NULL,  "EN007IU");
INSERT INTO Course VALUES ("IT132IU","Introduction to Data Mining",4, NULL, NULL);
INSERT INTO Course VALUES ("IT142IU","Analytics for Observational Data",4, NULL, NULL);
INSERT INTO Course VALUES ("PE008IU","Critical Thinking",3, NULL, NULL);
INSERT INTO Course VALUES ("EN012IU","Speaking AE2",2,NULL,"EN008IU");
INSERT INTO Course VALUES ("PE012IU","Ho Chi Minh's Thoughts",2, NULL, NULL);
INSERT INTO Course VALUES ("IT082IU","Internship",3, NULL, NULL);
INSERT INTO Course VALUES ("IT145IU","Decision Support System",4, NULL, NULL);
INSERT INTO Course VALUES ("IT083IU","Special Study of the Field",3,90, NULL);
INSERT INTO Course VALUES ("IT143IU","Fundamentals of Big Data Technology",4, NULL, NULL);
INSERT INTO Course VALUES ("PE013IU","Revolutionary Lines of Vietnamese Communist Party",3, NULL, NULL);
INSERT INTO Course VALUES ("PE014IU","Environmental Science",3, NULL, NULL);
INSERT INTO Course VALUES ("IT146IU","Theory of Networks",4, NULL, NULL);
INSERT INTO Course VALUES ("IT144IU","Business Process Analysis",4, NULL, NULL);
INSERT INTO Course VALUES ("IS021IU","Deterministic models in Operations Research",3, NULL, NULL);
INSERT INTO Course VALUES ("IT147IU","Mobile Cloud Computing",4, NULL, NULL);
INSERT INTO Course VALUES ("ISME105IU","Optimization",3, NULL, NULL);
INSERT INTO Course VALUES ("IT141IU","Big Data Applications: Machine Learning at Scale",4, NULL, NULL);
INSERT INTO Course VALUES ("IT148IU","Experimental Design",4, NULL, NULL);
INSERT INTO Course VALUES ("IT058IU","Thesis",10, NULL, 'IT083IU');
INSERT INTO Course VALUES ("IT152IU","Data Mining for IoT",4, NULL, NULL);
INSERT INTO Course VALUES ("IT056IU","IT Project Management",4, NULL, NULL);
INSERT INTO Course VALUES ("IT120IU","Entrepreneurship",3, NULL, NULL);
INSERT INTO Course VALUES ("IT094IU","Information System Management",4, NULL, NULL);
INSERT INTO Course VALUES ("IT150IU","Blockchain",4, NULL, NULL);