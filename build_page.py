import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import pandas as pd
from PIL import Image

from graph import SubjectGraph


author_g = SubjectGraph()
author_g.load("data/IU/K21_Author")
author_g.visualize("html_page/author_graph.html")

school_g = SubjectGraph()
school_g.load("data/IU/K21_School")
school_g.visualize("html_page/school_graph.html")


@st.cache
def get_all_subject_options():
    data = author_g.graph.nodes
    return [f"{item} - {data[item]['subject_name']} - {data[item]['subject_credit']}" for item in data if data[item]["is_available"]]

def process_raw_progress(raw_progress):
    return list(map(lambda subject_list: set(item.split("-")[0].strip() for item in subject_list), raw_progress))

def check_valid_courses(course_list):
    total_credit = sum(map(lambda item: int(item.split('-')[2].strip()), course_list))
    if total_credit < 12:
        raise Exception("Course list does not satisfy the university's requirements")

@st.cache
def get_all_suggestions(progress, level):
    processed_progress = process_raw_progress(progress)
    max_level, level_score, suggestions = author_g.suggest(processed_progress, level)
    return {
        "max_level": max_level,
        "score": level_score,
        "suggestion": suggestions
    }
    
@st.cache
def get_all_extra_subjects(subjects):
    return author_g.get_extra_subject(subjects)

def build_suggestion_page():
    sem_container = st.container()
    progress_container = st.container()
    suggestion_container = st.container()
    
    all_subject_options = get_all_subject_options()

    with sem_container:
        sem_input = st.sidebar.number_input("How many semester have you learnt?", min_value=1)
        isGeneratePressed = st.sidebar.button("Generate...")
        isClearPressed = st.sidebar.button("Clear...")
        
        if isGeneratePressed:
            st.session_state.canGenerate = True
            
        if isClearPressed:
            st.session_state.canGenerate = False
            st.session_state.display_suggest = False
            
    with progress_container:
        if "canGenerate" in st.session_state and st.session_state.canGenerate:
            progress = []
            for i in range(int(sem_input)):
                progress.append(st.sidebar.multiselect(f"Sem {i + 1}", options=all_subject_options))
                
            isSuggestPressed = st.sidebar.button("Suggest...")
            
            if isSuggestPressed:
                st.session_state.display_suggest = True
                
    with suggestion_container:
        st.header("Recommended courses")
        if "display_suggest" in st.session_state and st.session_state.display_suggest:
            try:
                for course_list in progress:
                    check_valid_courses(course_list)
            except Exception as e:
                st.write("Courses do not satisfy university requirements")
            else:
                if "level" not in st.session_state:
                    data = get_all_suggestions(progress, level=1)
                else:
                    data = get_all_suggestions(progress, level=st.session_state.level)
                    
                st.number_input("Level of suggestion (The lower the better)",
                                        min_value=1, max_value=data["max_level"], key="level")
                
                st.number_input("Pages", min_value=1, max_value=len(data["suggestion"]), key="page", value=1)
                
                index = int(st.session_state.page - 1)
                    
                df = pd.DataFrame(data["suggestion"][index])
                st.table(df)
                
                extra_subject = get_all_extra_subjects(df["subject_id"].tolist())
                
                if len(extra_subject) > 0:
                    st.write("Extra subjects:")
                    st.table(pd.DataFrame(extra_subject))
                
def build_presuggest_page():
    all_subject_options = get_all_subject_options()
    st.header("What should I learn before this subject?")
    chosen_subject = st.selectbox("Choose a subject", options=all_subject_options)
    isPressed = st.button("Suggest...")
    
    if isPressed:
        subject_id = chosen_subject.split("-")[0].strip()
        dependency_graph = author_g.get_dependency_graph(subject_id)
        
        net = Network(width="550px", height="550px", directed=True)
        
        for node_id in dependency_graph.nodes:
            subject_id = node_id
            subject_name = dependency_graph.nodes[node_id]["subject_name"]
            subject_credit = dependency_graph.nodes[node_id]["subject_credit"]
            subject_required_credit = dependency_graph.nodes[node_id]["prerequisite_credit"]
            subject_color = "#ffcccc" if not dependency_graph.nodes[node_id]["is_available"] else "#00ffff"
            title = "{}:{}\n{}: {}\n{}: {}".format(
                "Subject name",
                subject_name,
                "Credit",
                subject_credit,
                "Required credit",
                subject_required_credit
            )
            net.add_node(node_id, 
                         label=subject_name,
                         title=title,
                         color=subject_color)
            
        for source, target in dependency_graph.edges:
            net.add_edge(source, target, physics=False)
            
        net.show("presuggest.html")
        html_file = open("presuggest.html")
        source_code = html_file.read()
        components.html(source_code, height=600, width=1000)
        
def build_overview_page():
    st.markdown("""
        # Data Science Course DSS
        ## Motivation
        The motivation of this project is that the curriculum stated in the university website 
        (see [here](https://it.hcmiu.edu.vn/bachelor-of-science-in-data-science-k21/)) 
        is not logically arranged and organized, especially some key subjects 
        such as probability and statistics and regression analysis. 
        As a result, this site is made to provide a good constraint 
        under the opinion of the author. Readers can also make a comparison 
        and make a judgement for themselves. Besides, a decision support system is made within this project 
        to help freshmen and sophomore choose their subjects wisely 
        in the context of incomplete course design like this.
        
        To save time, the author leaves the visualization of two subject sub-graphs that illustrate 
        the difference between the author's proposed graph and the department's one.
    """)
    author_g = SubjectGraph()
    author_g.load("data/IU/K21_Author", overview=True)
    author_g.visualize("html_page/author_graph.html")

    school_g = SubjectGraph()
    school_g.load("data/IU/K21_School", overview=True)
    school_g.visualize("html_page/school_graph.html")
    
    st.markdown("### Department subject graph")    
    html_file = open("html_page/school_graph.html")
    source_code = html_file.read()
    components.html(source_code, height=800, width=800)
    
    st.markdown("### Author subject graph")
    html_file = open("html_page/author_graph.html")
    source_code = html_file.read()
    components.html(source_code, height=800, width=800)
    
    st.markdown("Side note: In the author's graph, red nodes represent subjects that does not exist in the entire curriculum of Data Science.")
    
    st.markdown("""
        ## Author's remark
        
        As can be seen, the main difference lies in the constraint of statistics-related courses.
        The biggest flaw sadly lied in the subject constraint for freshmen. For some reason, the department
        decides to constraint Regression Analysis on only Linear Algebra (which is only a small part of the picture).
        I'm pretty sure that an apprentice would notice such an illogical arrangement right here. 
        This is why this subject is reconstrainted on two subjects of IT (since it is more controlled by the department
        and more approachable for IT/DS students).
        
        In addition, Probability, Statistics & Random Process (PSR) is 
        a required subject for Statistical Methods (SM) where these two subjects are completely the same 
        with the only difference being that PSR has stochastic process 
        (which makes PSR more specialized than SM, and thus, SM should be a required subject for PSR?).
        As a result, I have arranged these two subjects into the same level.
        
        Another notable flaw is that heavy-math subject like Optimization is not constrainted on any math subjects 
        (again, this caused an insane consequence within the first generation of DS students in IU).
        As a result, this subject is actually constrainted on Calculus 2, Linear Algebra, and Algorithm and Data Structure
        for the purpose of firm math and programming knowledge.
        
        Last but not least, there are two modules that rely on non-existence subjects
        in the DS course list, which are Fundamental of Data Security (FCDS) and Scalable and Distributed Computing (SDC).
        Both subjects depend heavily on computer network and operating system with FCDS
        having an additional subject of discrete math. And Decision Support System is just merely
        a course of web programming with theory being casual talk on AI.
        
        The remaining differences are minor, including additional constraints on Data Analysis,
        Analytics of Observational Data, Blockchain, and Big Data.
        
        Overall, the department dependency graph is inefficient for course registration
        and caused a lot of loss in knowledge gain alongside academic journey.
        
        This is why this project is made to help freshmen and sophomore register their courses more efficient
        and refrain from mistakes that the author has made.
        
        ## "What should I learn next" recommendation
        _Disclaimer_: This part will be full of technical stuff. It's for those who want 
        to know what algorithm I use and why.
        
        Actually, the suggestion algorithm is quite simple but it heavily depends on the
        constraint of the graph (if it does not have well-established constraints, performance will be poor).
        
        > _Problem formulation_: Suppose that subject's credit represents the difficulty of a subject. 
        Given a student's most-updated transcript, provide a collection of new subjects that is close 
        to the student's performance.
        
        In this problem, two variables have been given: one is the credit of each subject and the other
        is the student's most-updated transcript. Providing that we do not have access to student's score
        (which I, personally, consider as private information), the only thing that we can mine from 
        the transcript is the number of subjects and the total credit per semester (again, you can you Collaborative Filtering
        to suggest subjects but it is too complex and sometimes inefficient since we also have order
        relationships). So, the dataset per user will have only two attributes, is it too simple?
        
        Here comes the math part. 2D data is simple, so it can be easily visualized. Let the x-axis
        be the number of credit per semester and the y-axis be the number of subject per semester. 
        If you represent a semester as a point in that 2D plane, the problem becomes finding a point 
        that is "close" to a set of given point. One simple way to define how "close" a point to
        a set of point is to take the total distance (this is similar to how MSE is intuitively understood).
        Hence, the problem becomes:
        
        > Given a set of point, rank each points by the total distance from this point to each
        given point
        
        If you learn a little bit of math, the optimal point should be the center of a polygon created
        by the set of given point. Hence, collection of subject that is "close" to a student's performance
        would lie within the polygon. 
    """)
    st.image(Image.open("img/polygon.png"), caption="For example, in this figure, point D, E, F will have lower total distance than point I, H, G")
    st.markdown("That's the intuition behind my algorithm. The transcript will form an area of suggestion such that most relevant subject to suggest to a student will lie within it.")
    st.markdown("""
        ## "What should I learn before" recommendation
        This is just a matter of traverse through the graph (here I use BFS, but since graph is not too large, BFS and DFS rarely make a difference).
    """)
    st.markdown("## About me")
    st.markdown("""
        My name is Minh and I'm a student from the International University or IU, for short. I'm no one than just 
        a mere Data Science student who loves mining and playing with data. If you find this project useful,
        consider sharing it with your friends and give a star in this [repo](https://github.com/minhrongcon2000/course-dss)\n\n
        
        If you have any concern or conflict regarding to this implementation and my argument, you can raise issues within this repo.
        Thank you for using this product!
    """)
    
