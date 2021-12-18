import streamlit as st
import requests
import json
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config


@st.cache
def get_all_subject_options():
    r = requests.get("http://localhost:8000/subjects")
    data = r.json()
    return [f"{item['subject_id']} - {item['subject_name']} - {item['subject_credit']}" for item in data]

def process_raw_progress(raw_progress):
    return list(map(lambda subject_list: [item.split("-")[0].strip() for item in subject_list], raw_progress))

def check_valid_courses(course_list):
    total_credit = sum(map(lambda item: int(item.split('-')[2].strip()), course_list))
    if total_credit < 12:
        raise Exception("Course list does not satisfy the university's requirements")

@st.cache
def get_all_suggestions(progress, level):
    payload = {
        "studied_subjects": process_raw_progress(progress)
    }
    r = requests.post("http://localhost:8000/suggestion", 
                      data=json.dumps(payload), 
                      params=dict(level=level))
    return r.json()

@st.cache
def get_subject_dependency(subject_id):
    r = requests.get("http://localhost:8000/subjects/previous", params=dict(subject_id=subject_id))
    return r.json()

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
                
def build_presuggest_page():
    all_subject_options = get_all_subject_options()
    st.header("What should I learn before this subject?")
    chosen_subject = st.selectbox("Choose a subject", options=all_subject_options)
    isPressed = st.button("Suggest...")
    
    if isPressed:
        subject_id = chosen_subject.split("-")[0].strip()
        dependency_graph = get_subject_dependency(subject_id)
        
        nodes = []
        edges = []
        
        for node_id in dependency_graph["nodes"]:
            nodes.append(Node(
                id=node_id,
                label=dependency_graph["nodes"][node_id]["subject_name"]
            ))
            
        for edge in dependency_graph["edges"]:
            edges.append(Edge(source=edge[0], target=edge[1]))
            
        config = Config(width=1200, 
                height=500, 
                directed=True,
                nodeHighlightBehavior=True, 
                highlightColor="#F7A7A6", # or "blue"
                collapsible=True,
                node={'labelProperty':'label'},
                link={'labelProperty': 'label', 'renderLabel': True}
                # **kwargs e.g. node_size=1000 or node_color="blue"
                )
        
        agraph(nodes=nodes, 
               edges=edges, 
               config=config)
