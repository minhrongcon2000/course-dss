import streamlit as st

from build_page import build_overview_page, build_presuggest_page, build_suggestion_page
import hydralit_components as hc


# st.set_page_config(layout='wide')

menu_data = [
    {
        "id": "overview",
        "label": "Overview"
    },
    {
        'id':'suggestion', 
        'label':"What should I learn next?"
    },
    {
        'id':'presuggestion', 
        'label':"What should I learn before?"
    }
    
]

over_theme = {'txc_inactive': '#FFFFFF'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
    sticky_nav=True, #at the top or not
    sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
)

if menu_id == "overview":
    build_overview_page()

if menu_id == "suggestion":
    build_suggestion_page()
    
if menu_id == "presuggestion":
    build_presuggest_page()
