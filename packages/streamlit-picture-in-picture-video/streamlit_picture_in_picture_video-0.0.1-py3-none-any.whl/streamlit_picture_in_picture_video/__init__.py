import os
import streamlit.components.v1 as components
import streamlit as st

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = True

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        "streamlit_picture_in_picture_video",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    _component_func = components.declare_component("streamlit_picture_in_picture_video")


def float_init(theme=True, include_unstable_primary=False):
    # add css to streamlit app
    html_style = '''<style>
    div.element-container:has(div.float) {
        position: absolute!important;
    }
    div.element-container:has(div.floating) {
        position: absolute!important;
    }
    div:has( >.element-container div.float) {
        display: flex;
        flex-direction: column;
        position: fixed;
        z-index: 99;
    }
    div.float, div.elim {
        display: none;
        height:0%;
    }
    div.floating {
        display: flex;
        flex-direction: column;
        position: fixed;
        z-index: 99; 
    }

    /* Target element-container that contains a video#main-video at any depth */
    div.element-container:has(video#main-video) {
        position: fixed !important;
        z-index: 99;
        bottom: 20px;
        right: 20px;
        width: 25vw; /* 1/4 of viewport width */
        max-width: 50vw;
        height: auto;
        border-radius: 10px;
        box-shadow: 0 0 12px rgba(0,0,0,0.3);
        overflow: hidden;
        resize: both;
        background-color: black;
        padding: 0;
        margin: 0;
        transform-origin: bottom right;
    }
    
    /* Add a resize handle */
    div.element-container:has(video#main-video)::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 10px;
        height: 10px;
        cursor: nwse-resize;
        background: linear-gradient(135deg, rgba(255,255,255,0.5) 0%, rgba(255,255,255,0) 50%);
    }
    
    /* Make sure the video itself fits correctly in the container */
    video#main-video {
        width: 100%;
        height: auto;
        display: block;
        object-fit: contain;
    }
    
    /* Add a draggable header for moving the video */
    div.element-container:has(video#main-video)::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 65px;
        // for debugging
        // background-color: rgba(0,0,0,0.5);
        cursor: move;
        z-index: 101;
        opacity: 0;
        transition: opacity 0.2s;
    }
    
    div.element-container:has(video#main-video):hover::before {
        opacity: 1;
    }
    
    /* Style for any controls or elements inside the container */
    div.element-container:has(video#main-video) button {
        position: absolute;
        bottom: 10px;
        right: 10px;
        z-index: 100;
    }

    /* Workaround for 1rem gap between containers that injects JS */
    div.element-container:has(div.pin-container) {
        margin-top: -3.5rem;
        display: block;
        background: green;
    }
    </style>
    '''
    
    html_script = """
        <script>
            console.log("Injecting JavaScript for handling dragging and resizing");
            
            // Get references to the parent document
            const root = window.parent.document;
            
            // Find the video container after a short delay to ensure DOM is loaded
            setTimeout(function() {
                    
                    
                const videoContainer = root.querySelector('div.element-container:has(video#main-video)');
                const video = root.querySelector('video#main-video');
                
                if (!videoContainer || !video) {
                    console.log("Video container not found yet");
                    return;
                }
                
                console.log("Found video container, setting up resize and drag");
                
                // Create a resize handle in the top-left corner
                const resizeHandle = document.createElement('div');
                resizeHandle.style.position = 'absolute';
                resizeHandle.style.top = '0';
                resizeHandle.style.left = '0';
                resizeHandle.style.width = '20px';
                resizeHandle.style.height = '20px';
                resizeHandle.style.cursor = 'nwse-resize';
                resizeHandle.style.background = 'linear-gradient(135deg, rgba(255,255,255,0.5) 0%, rgba(255,255,255,0.5) 50%, transparent 50%, transparent 100%)';
                resizeHandle.style.zIndex = '102';
                videoContainer.appendChild(resizeHandle);
                
                // Add necessary styles to maintain proper positioning
                videoContainer.style.transformOrigin = 'top left';
                videoContainer.style.resize = 'none'; // Disable default resize
                
                // Store original dimensions to maintain aspect ratio
                const originalWidth = videoContainer.offsetWidth;
                const originalHeight = videoContainer.offsetHeight;
                const aspectRatio = originalWidth / originalHeight;
                
                // Variables for drag and resize
                let isDragging = false;
                let isResizing = false;
                let startX, startY, startWidth, startHeight;
                
                // Clean up event listeners
                function cleanupEvents() {
                    isResizing = false;
                    isDragging = false;
                    root.removeEventListener('mousemove', handleMouseMove);
                    root.removeEventListener('mouseup', handleMouseUp);
                }
                
                // Handle mousedown events for both drag and resize
                videoContainer.addEventListener('mousedown', function(e) {
                    // Check if it's the resize handle
                    if (e.target === resizeHandle) {
                        isResizing = true;
                        startX = e.clientX;
                        startY = e.clientY;
                        startWidth = videoContainer.offsetWidth;
                        startHeight = videoContainer.offsetHeight;
                    } 
                    // Check if we're over the video controls (bottom area)
                    else {
                        // Determine if we're in the controls area (bottom ~40px of the video)
                        const controlsHeight = 40; // Approximate height of controls
                        const isOverControls = videoContainer.offsetHeight - e.offsetY <= controlsHeight;
                        
                        // If we're not over controls, enable dragging
                        if (!isOverControls) {
                            isDragging = true;
                            startX = e.clientX;
                            startY = e.clientY;
                        }
                    }
                    
                    if (isDragging || isResizing) {
                        e.preventDefault();
                        root.addEventListener('mousemove', handleMouseMove);
                        root.addEventListener('mouseup', handleMouseUp);
                    }
                });
                
                // Handle mouse movement
                function handleMouseMove(e) {
                    if (isResizing) {
                        // Calculate new width based on mouse movement
                        const deltaX = startX - e.clientX;
                        const newWidth = Math.max(240, startWidth + deltaX);
                        
                        // Calculate height based on aspect ratio
                        const newHeight = newWidth / aspectRatio;
                        
                        // Keep the bottom-right corner fixed
                        // Update container dimensions only
                        videoContainer.style.width = newWidth + 'px';
                        videoContainer.style.height = newHeight + 'px';
                    } else if (isDragging) {
                        // Calculate new position
                        const deltaX = e.clientX - startX;
                        const deltaY = e.clientY - startY;
                        
                        // Update position (keeping it anchored to bottom-right)
                        const viewportWidth = window.innerWidth;
                        const viewportHeight = window.innerHeight;
                        
                        const currRight = parseInt(videoContainer.style.right || '20', 10);
                        const currBottom = parseInt(videoContainer.style.bottom || '20', 10);
                        
                        videoContainer.style.right = (currRight - deltaX) + 'px';
                        videoContainer.style.bottom = (currBottom - deltaY) + 'px';
                        
                        // Update starting position for next move
                        startX = e.clientX;
                        startY = e.clientY;
                    }
                }
                
                // Handle mouse up
                function handleMouseUp() {
                    cleanupEvents();
                }
                
            }, 100); // Wait for elements to be fully loaded
        </script>
    """

    st.html(html_style)

    # Inject JavaScript for handling dragging and resizing
    # Use components.html to make sure JS can be executed and is run after page load
    components.html(html_script, height=0)

    # Add a container that allows to compensate for 1rem gap between containers that injects JS
    st.html("""<div class="pin-container" style="padding: 0;"></div>""")


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def streamlit_picture_in_picture_video(video_src: str, controls: bool = True, auto_play: bool=False, key=None):
    """Create a new instance of "streamlit_picture_in_picture_video".

    Parameters
    ----------
    video_src: str
        The URL of the video to display.
    controls: bool
        Whether to show video controls.
    auto_play: bool
        Whether to autoplay the video.
    key: str or None
        An optional key that uniquely identifies this component.

    Returns
    -------
    int
        The number of times the component's "Click Me" button has been clicked.
        (This is the value passed to `Streamlit.setComponentValue` on the
        frontend.)

    """
    # Initialize the floating video functionality
    float_init()

    # Create the video tag with proper HTML
    video_tag = f'<video id="main-video" src="{video_src}" style="width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);"'
    
    if controls:
        video_tag += ' controls'
    if auto_play:
        video_tag += ' autoplay muted'
        
    # Close the video tag properly
    video_tag += '></video>'

    # Create a video element with HTML
    video_html = f"""
    <div style="position: relative;">
        {video_tag}
    </div>
    """
    st.html(video_html)
