import streamlit as st
import base64

def load_visual_identity(header_image_path, background_image_path = 'background.svg'):
    # Load the image and encode it in Base64 format
    with open(header_image_path, "rb") as image_file:
        header_image = base64.b64encode(image_file.read()).decode("utf-8")
    # Load the image and encode it in Base64 format
    with open(background_image_path, "rb") as image_file:
        background_image = base64.b64encode(image_file.read()).decode("utf-8")
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
                margin: 0;
                padding: 0;
                overflow-x: hidden;
                display: block;
            }}
            /* Needed to make container relatively positioned */
            .block-container {{
                position: relative;
                z-index: 0;
                overflow-x: hidden;
                overflow-y: visible;
            }}

            .block-container::before {{
                content: "";
                position: absolute;
                top: 40vh;  /* halfway-ish down */
                left: 40vw; /* start from the right-ish */
                width: 40vw; /* not too large */
                height: 40vw;
                background-image: url("data:image/svg+xml;base64,{background_image}");
                background-repeat: no-repeat;
                background-size: contain;
                background-position: center;
                z-index: 0;
                opacity: 0.6;
                pointer-events: none;
            }}

            /* Make header fixed at the top with full viewport width */
            .header-image {{
                position: absolute;
                top: o;
                left: -20vw;
                overflow-x: hidden;
                width: 120vw;
                height: 20vw;  /* Adjust height as needed */
                background-image: url("data:image/jpg;base64,{header_image}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                z-index: 0;
                margin: 0 ;
            }}

            /* Extend the gradient to blend into content smoothly */
            .header-gradient {{
                position: absolute;
                bottom: 0;
                width: 100%;
                height: 90%;  /* Match header-image height */
                background: linear-gradient(to bottom, rgba(255, 255, 255, 0) 30%, rgba(255, 255, 255, 1) 100%);
                z-index: 1;
            }}
            

        </style>
        <div class="header-image">
            <div class="header-gradient"></div>
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
                        padding-top: 0rem;
                        padding-bottom: 5rem;
                        padding-left: 5rem;
                        padding-right: 5rem;
                    }
            </style>
            """, unsafe_allow_html=True)
