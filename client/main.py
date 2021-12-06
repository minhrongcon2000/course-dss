import json
import streamlit as st
import requests
import pandas as pd


sem_container = st.container()
progress_container = st.container()
suggestion_container = st.container()

@st.cache
def get_all_subject_options():
    r = requests.get("http://localhost:8000/subjects")
    data = r.json()
    return [f"{item['subject_id']} - {item['subject_name']} - {item['subject_credit']}" for item in data]

def process_raw_progress(raw_progress):
    return list(map(lambda subject_list: [item.split("-")[0].strip() for item in subject_list], raw_progress))

@st.cache
def get_all_suggestions(progress, level):
    payload = {
        "studied_subjects": process_raw_progress(progress)
    }
    r = requests.post("http://localhost:8000/suggestion", 
                      data=json.dumps(payload), 
                      params=dict(level=level))
    return r.json()

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
        if "level" not in st.session_state:
            data = get_all_suggestions(progress, level=1)
        else:
            data = get_all_suggestions(progress, level=st.session_state.level)
            
        level = st.number_input("Level of suggestion (The lower the better)",
                                min_value=1, max_value=data["max_level"], key="level")
        
        page = st.number_input("Pages", min_value=1, max_value=len(data["suggestion"]), key="page", value=1)
        
        index = int(st.session_state.page - 1)
            
        df = pd.DataFrame(data["suggestion"][index])
        st.table(df)
        
        
        
        
                
            
