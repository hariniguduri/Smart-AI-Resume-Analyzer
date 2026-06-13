import streamlit as st
from typing import List, Dict
from .job_portals import JobPortal
from .suggestions import (
    JOB_SUGGESTIONS, 
    LOCATION_SUGGESTIONS, 
    EXPERIENCE_RANGES,
    SALARY_RANGES,
    JOB_TYPES,
    get_cities_by_state,
    get_all_states
)
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_option_menu import option_menu

def filter_suggestions(query: str, suggestions: List[Dict]) -> List[Dict]:
    """Filter suggestions based on user input"""
    if not query:
        return []
    return [
        s for s in suggestions 
        if query.lower() in s["text"].lower()
    ][:5]

def filter_location_suggestions(query: str, suggestions: List[Dict]) -> List[Dict]:
    """Filter location suggestions based on user input with smart categorization"""
    if not query or len(query) < 2:
        return []
        
    # First check if query matches any state
    matching_states = [s for s in suggestions if s.get("type") == "state" and query.lower() in s["text"].lower()]
    
    # Then check cities
    matching_cities = [s for s in suggestions if s.get("type") == "city" and query.lower() in s["text"].lower()]
    
    # Then check work modes
    matching_work_modes = [s for s in suggestions if s.get("type") == "work_mode" and query.lower() in s["text"].lower()]
    
    # Combine results with states first, then major cities, then other matches
    results = matching_states + matching_cities + matching_work_modes
    return results[:7]  # Return top 7 matches

def get_filter_options():
    """Get filter options for job search"""
    return {
        "experience_levels": [
            {"id": "all", "text": "All Levels"},
            {"id": "fresher", "text": "Fresher"},
            {"id": "0-1", "text": "0-1 years"},
            {"id": "1-3", "text": "1-3 years"},
            {"id": "3-5", "text": "3-5 years"},
            {"id": "5-7", "text": "5-7 years"},
            {"id": "7-10", "text": "7-10 years"},
            {"id": "10+", "text": "10+ years"}
        ],
        "salary_ranges": [
            {"id": "all", "text": "All Ranges"},
            {"id": "0-3", "text": "0-3 LPA"},
            {"id": "3-6", "text": "3-6 LPA"},
            {"id": "6-10", "text": "6-10 LPA"},
            {"id": "10-15", "text": "10-15 LPA"},
            {"id": "15+", "text": "15+ LPA"}
        ],
        "job_types": [
            {"id": "all", "text": "All Types"},
            {"id": "full-time", "text": "Full Time"},
            {"id": "part-time", "text": "Part Time"},
            {"id": "contract", "text": "Contract"},
            {"id": "remote", "text": "Remote"}
        ]
    }



def render_job_search():
    """Render job search page with enhanced features"""
    st.title("🔍 Smart Job Search")
    st.markdown("Find Your Dream Job Across Multiple Platforms")
    # Job Search Section
    with st.container():
        st.markdown("""
            <style>
            .search-container {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
            }
            .search-title {
                color: #00bfa5;
                font-weight: bold;
                margin-bottom: 5px;
            }
            .search-description {
                color: #888;
                font-size: 0.9rem;
                margin-bottom: 20px;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        
        # Create tabs with icons
        tabs = option_menu(
            menu_title=None,
            options=["Job Portal", "LinkedIn"],
            icons=["search", "linkedin"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"padding": "0px", "margin-bottom": "20px"},
                "icon": {"font-size": "18px"},
                "nav-link": {"font-size": "16px", "text-align": "center", "padding": "10px", "border-radius": "5px"},
                "nav-link-selected": {"background-color": "#00bfa5", "font-weight": "bold"},
            }
        )
        
        # Display content based on selected tab
        if tabs == "Job Portal":
            st.markdown('<h3 class="search-title"><i class="fas fa-search-dollar" style="color: #00bfa5;"></i> Search Jobs Across Multiple Platforms</h3>', unsafe_allow_html=True)
            st.markdown('<p class="search-description">Find job opportunities from top job portals like LinkedIn, Indeed, Naukri, and Foundit</p>', unsafe_allow_html=True)
            
            # Search inputs
            col1, col2 = st.columns([2, 1])
            
            with col1:
                job_query = st.text_input("Job Title / Skills", 
                                        value="", 
                                        placeholder="e.g. Software Engineer, Data Scientist")
                
                if job_query and len(job_query) >= 2:
                    filtered_jobs = [s["text"] for s in JOB_SUGGESTIONS if job_query.lower() in s["text"].lower()]
                    if filtered_jobs:
                        job_query = st.selectbox("Select Job Title", filtered_jobs)
            
            with col2:
                location = st.text_input("Location", 
                                       value="",
                                       placeholder="e.g. Bangalore, Karnataka")
                
                if location and len(location) >= 2:
                    # Use enhanced location filtering
                    filtered_locations = filter_location_suggestions(location, LOCATION_SUGGESTIONS)
                    
                    if filtered_locations:
                        # Format the display text to show location type
                        location_options = []
                        location_display = {}
                        
                        for loc in filtered_locations:
                            display_text = loc["text"]
                            if loc.get("type") == "state":
                                display_text = f"{loc['text']} (State)"
                            elif loc.get("type") == "city":
                                display_text = f"{loc['text']}, {loc.get('state', '')}"
                            elif loc.get("type") == "work_mode":
                                display_text = f"{loc['text']} (Work Mode)"
                                
                            location_options.append(loc["text"])
                            location_display[loc["text"]] = display_text
                        
                        # Create a selectbox with formatted display
                        selected_location = st.selectbox(
                            "Select Location",
                            options=location_options,
                            format_func=lambda x: location_display.get(x, x)
                        )
                        
                        location = selected_location
                        
                        # If a state is selected, show cities in that state
                        selected_loc_type = next((loc.get("type") for loc in filtered_locations if loc["text"] == selected_location), None)
                        
                        if selected_loc_type == "state":
                            st.markdown(f"**Cities in {selected_location}:**")
                            cities = get_cities_by_state(selected_location)
                            
                            # Display cities as clickable buttons
                            city_cols = st.columns(3)
                            for i, city in enumerate(cities):
                                with city_cols[i % 3]:
                                    if st.button(f"{city['icon']} {city['text']}", key=f"city_{i}"):
                                        location = city['text']

            # Advanced Filters
            with st.expander("🎯 Advanced Filters"):
                st.markdown('<div class="filter-section">', unsafe_allow_html=True)
                filter_cols = st.columns(3)
                
                with filter_cols[0]:
                    experience = st.selectbox("Experience Level",
                                            options=get_filter_options()["experience_levels"],
                                            format_func=lambda x: x["text"])
                
                with filter_cols[1]:
                    salary_range = st.selectbox("Salary Range",
                                              options=get_filter_options()["salary_ranges"],
                                              format_func=lambda x: x["text"])
                
                with filter_cols[2]:
                    job_type = st.selectbox("Job Type",
                                          options=get_filter_options()["job_types"],
                                          format_func=lambda x: x["text"])
                
                st.markdown('</div>', unsafe_allow_html=True)

            # Search button
            if st.button("SEARCH JOBS", type="primary", width="stretch"):
                if job_query:
                    job_portal = JobPortal()
                    results = job_portal.search_jobs(job_query, location, experience)
                    
                    if results:
                        st.markdown("""
                            <style>
                            .result-card {
                                background: rgba(255, 255, 255, 0.05);
                                border-radius: 10px;
                                padding: 15px;
                                margin-bottom: 10px;
                                border-left: 4px solid #00bfa5;
                                transition: transform 0.2s;
                            }
                            .result-card:hover {
                                transform: translateX(5px);
                                background: rgba(255, 255, 255, 0.08);
                            }
                            .portal-name {
                                color: #00bfa5;
                                font-weight: bold;
                                font-size: 1.2rem;
                            }
                            .portal-link {
                                display: inline-block;
                                background: #00bfa5;
                                color: white !important;
                                padding: 5px 15px;
                                border-radius: 5px;
                                text-decoration: none;
                                margin-top: 10px;
                                font-weight: bold;
                            }
                            .portal-link:hover {
                                background: #00a589;
                            }
                            </style>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("### 🎯 Job Search Results")
                        for result in results:
                            with st.container():
                                st.markdown(f"""
                                <div class="result-card">
                                    <div class="portal-name">
                                        <i class="{result["icon"]}" style="color: {result["color"]}"></i>
                                        {result["portal"]}
                                    </div>
                                    <p>{result["title"]}</p>
                                    <a href="{result["url"]}" target="_blank" class="portal-link">
                                        View Jobs on {result["portal"]} →
                                    </a>
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.warning("No results found. Try different search terms or filters.")
                else:
                    st.warning("Please enter a job title or skills to search.")
        st.markdown('</div>', unsafe_allow_html=True)
# Removed render_job_search() call to prevent automatic rendering
