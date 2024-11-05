import streamlit as st
import base64

def load_visual_identity(header_image_path):
    # Load the image and encode it in Base64 format
    with open(header_image_path, "rb") as image_file:
        header_image = base64.b64encode(image_file.read()).decode("utf-8")
    # Load Montserrat font from Google Fonts
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

        /* Apply Montserrat font globally */
        body {
            font-family: 'Montserrat', sans-serif;
        }

        /* Optional: Customize other elements as needed */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Montserrat', sans-serif;
        }
        </style>
        """,
        unsafe_allow_html=True
    )



    
    st.markdown(
    f"""
    <style>
        /* Remove default padding and margin from body and html to prevent gaps */
        html, body {{
            margin: 0;            /* No margin */
            padding: 0;           /* No padding */
            width: 100%;          /* Ensure full width */
            height: 100%;         /* Ensure full height */
            overflow-x: hidden;   /* Prevent horizontal scroll */
        }}

        /* Make header image oversized to fill viewport */
        .header-image {{
            position: absolute;    /* Use absolute positioning */
            top: 0;                /* Start from the top */
            left: 0;               /* Start from the left */
            width: 100vw;          /* Full viewport width */
            height: 100vh;         /* Full viewport height */
            background-image: url("data:image/jpg;base64,{header_image}");
            background-size: cover;  /* Ensure image covers the area */
            background-position: center; /* Center the image */
            background-repeat: no-repeat;
            z-index: 0;
        }}

        /* Extend the gradient to blend into content smoothly */
        .header-gradient {{
            position: absolute;
            bottom: 0;
            width: 100%;
            height: 80%;          /* Match header-image height */
            background: linear-gradient(to bottom, rgba(255, 255, 255, 0) 40%, rgba(255, 255, 255, 1) 100%);
            z-index: 1;
        }}

        /* Create overlap effect with main content */
        .main-content {{
            margin-top: 200px;   /* Adjust margin-top to push content below the header */
            margin: 0;           /* Ensure no margin around main content */
            padding: 20px;       /* Add some padding to content, adjust as needed */
            position: relative;
        }}
    </style>
    <div class="header-image">
        <div class="header-gradient"></div>
    </div>
    <div class="main-content">
        <!-- Your main content goes here -->
    </div>
    """,
    unsafe_allow_html=True
)

    st.markdown("""
    <style>
        /* Set sidebar background color */
        [data-testid="stSidebar"] {
            background-color: #000000;
        }

        /* Set sidebar text color */
        [data-testid="stSidebar"] * {
            color: #FFFFFF;
        }
        [data-testid="stHeader"] {
            background-color: rgba(0,0,0,0);
        }
        
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
            <style>
                   .block-container {
                        padding-top: 1rem;
                        padding-bottom: 5rem;
                        padding-left: 5rem;
                        padding-right: 5rem;
                    }
            </style>
            """, unsafe_allow_html=True)
