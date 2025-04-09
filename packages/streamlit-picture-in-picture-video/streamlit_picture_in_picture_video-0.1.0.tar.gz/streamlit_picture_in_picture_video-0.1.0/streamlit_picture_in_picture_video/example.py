import streamlit as st
from streamlit_picture_in_picture_video import streamlit_picture_in_picture_video

# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/example.py`

st.subheader("Picture-in-Picture Video")

# Initialize session state for video visibility
if 'show_video' not in st.session_state:
    st.session_state.show_video = False

# Create an instance of our component with a constant `name` arg, and
# print its output value.

show_controls = st.checkbox("Show video controls", True)
auto_play = st.checkbox("Auto-play video", True)

# Toggle video visibility when button is clicked
if st.button("Show/Hide video"):
    st.session_state.show_video = not st.session_state.show_video



video_src = "https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"

# Display video based on session state
if st.session_state.show_video:
    streamlit_picture_in_picture_video(
        video_src=video_src,
        controls=show_controls,
        auto_play=auto_play,
    )