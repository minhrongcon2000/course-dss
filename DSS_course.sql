DROP DATABASE IF exists all_course;
CREATE DATABASE all_course;
USE all_course;
CREATE TABLE Course(
	Course_Id VARCHAR(20) primary key, 
    Course_Name VARCHAR(50), 
    Credit int, 
    Required_credit int null
);
CREATE TABLE Prerequisite(
	Course_id VARCHAR(20) references Course(Course_Id),
    Prerequisite_id VARCHAR(20) references Course(Course_Id)
);

INSERT INTO Course VALUES ('EN073IU','Listening & Speaking IE1', 11, NULL);
INSERT INTO Course VALUES ('EN072IU','Reading & Writing IE1', 11, NULL);
INSERT INTO Course VALUES ('PH013IU','Physics 1', 2, NULL);
INSERT INTO Course VALUES ('EN075IU','Listening & Speaking IE2', 8, NULL);
INSERT INTO Course VALUES ('EN074IU','Reading & Writing IE2', 8, NULL);
INSERT INTO Course VALUES ('IT135IU','Introduction to Data Science', 3, NULL);
INSERT INTO Course VALUES ('IT149IU','Fundamentals of Programming', 4, NULL);
INSERT INTO Course VALUES ('MA001IU','Calculus 1', 4, NULL);
INSERT INTO Course VALUES ('MA003IU','Calculus 2', 4,  NULL);
INSERT INTO Course VALUES ('CH011IU','Chemistry for Engineers', 3, NULL);
INSERT INTO Course VALUES ('IT013IU','Algorithms & Data Structures', 4, NULL);
INSERT INTO Course VALUES ('PH014IU','Physics 2', 2, NULL);
INSERT INTO Course VALUES ('CH012IU','Chemistry Laboratory', 1, NULL);
INSERT INTO Course VALUES ('IT137IU','Data Analysis', 4, NULL);
INSERT INTO Course VALUES ('IT069IU','Object-Oriented Programming', 4, NULL);
INSERT INTO Course VALUES ('IT079IU','Principles of Database Management', 4, NULL);
INSERT INTO Course VALUES ('IT136IU','Regression Analysis', 4, NULL);
INSERT INTO Course VALUES ('IT090IU','Object-Oriented Analysis and Design', 4, NULL);
INSERT INTO Course VALUES ('MA023IU','Calculus 3', 4, NULL);
INSERT INTO Course VALUES ("IT138IU","Data Science and Data Visualization",4, NULL);
INSERT INTO Course VALUES ("IT151IU","Statistical Methods",3, NULL);
INSERT INTO Course VALUES ("IT139IU","Scalable and Distributed Computing",4, NULL);
INSERT INTO Course VALUES ("IT097IU","Introduction to Artificial Intelligence",4, NULL);
INSERT INTO Course VALUES ("EN007IU","Writing AE1",2, NULL);
INSERT INTO Course VALUES ("EN008IU","Listening AE1",2, NULL);
INSERT INTO Course VALUES ("PE011IU","Principles of Marxism",5, NULL);
INSERT INTO Course VALUES ("MA026IU","Probability, Statistic & Random Process",3, NULL);
INSERT INTO Course VALUES ("IT140IU","Fundamental Concepts of Data Security",4, NULL);
INSERT INTO Course VALUES ("EN011IU","Writing AE2",2, NULL);
INSERT INTO Course VALUES ("IT132IU","Introduction to Data Mining",4, NULL);
INSERT INTO Course VALUES ("IT142IU","Analytics for Observational Data",4, NULL);
INSERT INTO Course VALUES ("PE008IU","Critical Thinking",3, NULL);
INSERT INTO Course VALUES ("EN012IU","Speaking AE2",2,NULL);
INSERT INTO Course VALUES ("PE012IU","Ho Chi Minh's Thoughts",2, NULL);
INSERT INTO Course VALUES ("IT082IU","Internship",3, NULL);
INSERT INTO Course VALUES ("IT145IU","Decision Support System",4, NULL);
INSERT INTO Course VALUES ("IT083IU","Special Study of the Field",3,90);
INSERT INTO Course VALUES ("IT143IU","Fundamentals of Big Data Technology",4, NULL);
INSERT INTO Course VALUES ("PE013IU","Revolutionary Lines of Vietnamese Communist Party",3, NULL);
INSERT INTO Course VALUES ("PE014IU","Environmental Science",3, NULL);
INSERT INTO Course VALUES ("IT147IU","Mobile Cloud Computing",4, NULL);
INSERT INTO Course VALUES ("ISME105IU","Optimization",3, NULL);
INSERT INTO Course VALUES ("IT148IU","Experimental Design",4, NULL);
INSERT INTO Course VALUES ("IT058IU","Thesis",10, NULL);
INSERT INTO Course VALUES ("IT152IU","Data Mining for IoT",4, NULL);
INSERT INTO Course VALUES ("IT056IU","IT Project Management",4, NULL);
INSERT INTO Course VALUES ("IT120IU","Entrepreneurship",3, NULL);
INSERT INTO Course VALUES ("IT094IU","Information System Management",4, NULL);
INSERT INTO Course VALUES ("IT150IU","Blockchain",4, NULL);

-- English constraint
INSERT INTO Prerequisite VALUES ("EN075IU","EN073IU");
INSERT INTO Prerequisite VALUES ("EN075IU","EN072IU");
INSERT INTO Prerequisite VALUES ("EN074IU","EN073IU");
INSERT INTO Prerequisite VALUES ("EN074IU","EN072IU");
INSERT INTO Prerequisite VALUES ("EN007IU","EN074IU");
INSERT INTO Prerequisite VALUES ("EN007IU","EN075IU");
INSERT INTO Prerequisite VALUES ("EN008IU","EN074IU");
INSERT INTO Prerequisite VALUES ("EN008IU","EN075IU");
INSERT INTO Prerequisite VALUES ("EN011IU","EN007IU");
INSERT INTO Prerequisite VALUES ("EN011IU","EN008IU");

-- math constraint
INSERT INTO Prerequisite VALUES ("MA003IU","MA001IU");
INSERT INTO Prerequisite VALUES ("MA023IU","MA003IU");

-- physics constraint
INSERT INTO Prerequisite VALUES ("PH014IU","PH013IU");

-- constrainted on C/C++
INSERT INTO Prerequisite VALUES ("IT069IU","IT149IU");
INSERT INTO Prerequisite VALUES ("IT142IU","IT149IU");
INSERT INTO Prerequisite VALUES ("IT138IU","IT149IU");
INSERT INTO Prerequisite VALUES ("IT079IU","IT149IU");

-- constrainted on OOP
INSERT INTO Prerequisite VALUES ("IT090IU","IT069IU");
INSERT INTO Prerequisite VALUES ("IT147IU","IT069IU");
INSERT INTO Prerequisite VALUES ("IT145IU","IT069IU");
INSERT INTO Prerequisite VALUES ("IT132IU","IT069IU");
INSERT INTO Prerequisite VALUES ("IT013IU","IT069IU");
INSERT INTO Prerequisite VALUES ("IT097IU","IT069IU");
INSERT INTO Prerequisite VALUES ("IT143IU","IT069IU");
INSERT INTO Prerequisite VALUES ("IT056IU","IT069IU");

-- constrainted on database
INSERT INTO Prerequisite VALUES ("IT143IU","IT079IU");
INSERT INTO Prerequisite VALUES ("IT094IU","IT079IU");

-- constrainted on DSA
INSERT INTO Prerequisite VALUES ("IT139IU","IT013IU");

-- constrainted on DM
INSERT INTO Prerequisite VALUES ("IT152IU","IT132IU");
INSERT INTO Prerequisite VALUES ("IT143IU","IT132IU");

INSERT INTO Prerequisite VALUES ("IT148IU","IT137IU");
INSERT INTO Prerequisite VALUES ("IT148IU","IT136IU");
INSERT INTO Prerequisite VALUES ("IT136IU","IT151IU");

-- thesis
INSERT INTO Prerequisite VALUES ("IT058IU","IT083IU");
