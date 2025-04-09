import os
import streamlit.components.v1 as components
import streamlit as st
import base64

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
    _component_func = components.declare_component("streamlit_picture_in_picture_video", url="")


def inject_styles_and_scripts(max_video_width_percentage: int=50):
    # add css to streamlit app
    html_style = '''<style>
    /* Target element-container that contains a video.picture-in-picture-video at any depth */
    div.element-container:has(video.picture-in-picture-video) {
        position: fixed !important;
        z-index: 99;
        bottom: 20px;
        right: 20px;
        width: 25vw; /* 1/4 of viewport width */
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
    div.element-container:has(video.picture-in-picture-video)::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 10px;
        height: 10px;
        cursor: nwse-resize;
        background: linear-gradient(135deg, rgba(255,255,255,0.5) 0%, rgba(255,255,255,0) 50%);
    }
    
    div.stHtml:has(video.picture-in-picture-video) {
        width: 100% !important;
        height: 100% !important;
    }

    /* Make sure the video itself fits correctly in the container */
    video.picture-in-picture-video {
        width: 100%;
        height: auto;
        display: block;
        object-fit: contain;
    }
    
    /* Add a draggable header for moving the video */
    div.element-container:has(video.picture-in-picture-video)::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 65px;
        cursor: move;
        z-index: 101;
        opacity: 0;
        transition: opacity 0.2s;
    }
    
    div.element-container:has(video.picture-in-picture-video):hover::before {
        opacity: 1;
    }

    /* Workaround for 1rem gap between containers that injects JS */
    div.element-container:has(div.margin-eater) {
        margin-top: -3.5rem;
        display: block;
        background: green;
        height: 0px !important;
    }
    </style>
    '''
    
    # Create a JavaScript string with the maxWidthPercentage properly injected
    html_script = """
        <script>
            // Get references to the parent document
            const root = window.parent.document;
            
            // Find the video container after a short delay to ensure DOM is loaded
            setTimeout(function() {
                    
                    
                const videoContainer = root.querySelector('div.element-container:has(video.picture-in-picture-video)');
                const video = root.querySelector('video.picture-in-picture-video');                
                if (!videoContainer || !video) {
                    console.log("!! Video container for picture-in-picture video not found yet");
                    return;
                }
                
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
                
                // Function to calculate maximum width based on viewport width
                function calculateMaxWidth() {
                    // Calculate max width (percentage of viewport width)
                    const maxWidthPercentage = MAX_WIDTH_PERCENTAGE_PLACEHOLDER;
                    return root.defaultView.innerWidth * (maxWidthPercentage / 100);
                }
                
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
                        
                        // Get max width from the calculation function
                        const maxWidth = calculateMaxWidth();
                        const minWidth = 240;
                        
                        // Apply min/max constraints
                        const newWidth = Math.min(maxWidth, Math.max(minWidth, startWidth + deltaX));
                        
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
                        const viewportWidth = root.defaultView.innerWidth;
                        const viewportHeight = root.defaultView.innerHeight;
                        
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
                
                // Handle window resize to maintain constraints
                root.defaultView.addEventListener('resize', function() {
                    // Get current width
                    const currentWidth = videoContainer.offsetWidth;
                    
                    // Get max width from the calculation function
                    const maxWidth = calculateMaxWidth();
                    
                    // If current width exceeds max width, resize
                    if (currentWidth > maxWidth) {
                        const newWidth = maxWidth;
                        const newHeight = newWidth / aspectRatio;
                        
                        videoContainer.style.width = newWidth + 'px';
                        videoContainer.style.height = newHeight + 'px';
                    }
                });
            }, 100); // Wait for elements to be fully loaded
        </script>
    """
    
    # Replace placeholder with actual value
    html_script = html_script.replace('MAX_WIDTH_PERCENTAGE_PLACEHOLDER', str(max_video_width_percentage))

    st.html(html_style)

    # Inject JavaScript for handling dragging and resizing
    # Use components.html to make sure JS can be executed and is run after page load
    components.html(html_script, height=0)

    # Add a container that allows to compensate for 1rem gap between containers that injects JS
    st.html("""<div class="margin-eater" style="padding: 0;"></div>""")


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def streamlit_picture_in_picture_video(video_src: str, controls: bool = True, auto_play: bool=False, max_width: int=50, key=None):
    """Create a new instance of "streamlit_picture_in_picture_video".

    Parameters
    ----------
    video_src: str
        The URL of the video to display or the path to the video file.
    controls: bool
        Whether to show video controls.
    auto_play: bool
        Whether to autoplay the video.
    max_width: int
        The maximum width of the video in % of the window width.
    key: str or None
        An optional key that uniquely identifies this component.

    """
    # Initialize the floating video functionality
    inject_styles_and_scripts(max_video_width_percentage=max_width)

    # Check if the video is a local file, if yes, encode it to base64. Otherwise, use the url.
    if os.path.exists(video_src):
        with open(video_src, "rb") as f:
            video_bytes = f.read()
        b64_encoded = base64.b64encode(video_bytes).decode()
        video_src = f"data:video/mp4;base64,{b64_encoded}"

    # Create the video tag with proper HTML
    video_tag = f'<video class="picture-in-picture-video" src="{video_src}" style="width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);"'
    if controls:
        video_tag += ' controls'
    if auto_play:
        video_tag += ' autoplay muted'
        
    # Close the video tag properly
    video_tag += '></video>'
    video_html = f"""
    <div style="position: relative;">
        {video_tag}
    </div>
    """
    st.html(video_html)
