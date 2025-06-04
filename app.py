import streamlit as st
import plotly.graph_objects as go
from src import solver, charts
import time

# Configure page
st.set_page_config(
    page_title="DD-AA Model Interactive Viewer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'scenario_index' not in st.session_state:
    st.session_state.scenario_index = 0
if 'frame_index' not in st.session_state:
    st.session_state.frame_index = 0

# Define scenarios
SCENARIOS = [
    "Initial Equilibrium | GDP at Full Employment",
    "Temporary Monetary Expansion",
    "Permanent Monetary Expansion", 
    "Temporary Fiscal Expansion",
    "Permanent Fiscal Expansion",
    "Exchange Rate Crisis"
]

# Main layout
col1, col2 = st.columns([4, 1])

with col1:
    # Title
    st.markdown("""
    <h1 style='text-align: center; color: #003366;'>
    DD-AA Model: Policy Analysis Framework
    </h1>
    """, unsafe_allow_html=True)
    
    # Get current scenario and frame
    scenario = SCENARIOS[st.session_state.scenario_index]
    frames = solver.get_scenario_frames(st.session_state.scenario_index)
    current_frame = frames[st.session_state.frame_index]
    
    # Build and display chart
    fig = charts.build_canvas(current_frame)
    
    # Create placeholder for the chart
    chart_placeholder = st.empty()
    chart_placeholder.plotly_chart(fig, use_container_width=True, key=f"chart_{st.session_state.frame_index}")

with col2:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Scenario selector
    st.markdown("### Select Scenario")
    new_scenario_index = st.selectbox(
        label="Scenario",
        options=range(len(SCENARIOS)),
        format_func=lambda x: SCENARIOS[x],
        index=st.session_state.scenario_index,
        key="scenario_selector",
        label_visibility="collapsed"
    )
    
    # Update scenario if changed
    if new_scenario_index != st.session_state.scenario_index:
        st.session_state.scenario_index = new_scenario_index
        st.session_state.frame_index = 0
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation buttons
    col_back, col_forward = st.columns(2)
    
    with col_back:
        back_disabled = st.session_state.frame_index == 0
        if st.button("⬅️ Back", 
                    disabled=back_disabled, 
                    use_container_width=True,
                    type="secondary" if not back_disabled else "primary"):
            
            # Animate transition
            if st.session_state.frame_index > 0:
                # Get previous frame
                prev_frame = frames[st.session_state.frame_index - 1]
                
                # Create transition frames
                transition_frames = charts.create_transition(
                    current_frame, 
                    prev_frame, 
                    steps=10
                )
                
                # Animate
                for t_frame in transition_frames:
                    fig_t = charts.build_canvas(t_frame)
                    chart_placeholder.plotly_chart(fig_t, use_container_width=True)
                    time.sleep(0.05)
                
                # Update state
                st.session_state.frame_index -= 1
                st.rerun()
    
    with col_forward:
        forward_disabled = st.session_state.frame_index >= len(frames) - 1
        if st.button("Forward ➡️", 
                    disabled=forward_disabled,
                    use_container_width=True,
                    type="primary" if not forward_disabled else "secondary"):
            
            # Animate transition
            if st.session_state.frame_index < len(frames) - 1:
                # Get next frame
                next_frame = frames[st.session_state.frame_index + 1]
                
                # Create transition frames
                transition_frames = charts.create_transition(
                    current_frame,
                    next_frame,
                    steps=10
                )
                
                # Animate
                for t_frame in transition_frames:
                    fig_t = charts.build_canvas(t_frame)
                    chart_placeholder.plotly_chart(fig_t, use_container_width=True)
                    time.sleep(0.05)
                
                # Update state
                st.session_state.frame_index += 1
                st.rerun()
    
    # Frame indicator
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='text-align: center; color: #666;'>
    Frame {st.session_state.frame_index + 1} of {len(frames)}
    </div>
    """, unsafe_allow_html=True)
    
    # Current frame description
    if 'description' in current_frame:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info(current_frame['description'])

# Hide Streamlit branding
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display:none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)