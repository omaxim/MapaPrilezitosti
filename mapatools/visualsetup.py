import streamlit as st
import base64

def load_visual_identity(header_image_path, background_image_path = 'resources/background.svg'):
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
                right: 0vw; /* start from the right-ish */
                width: 40vw; /* not too large */
                height: 40vw;
                background-image: url("data:image/svg+xml;base64,{background_image}");
                background-repeat: no-repeat;
                background-size: contain;
                background-position: center;
                z-index: 0;
                opacity: 0.4;
                pointer-events: none;
            }}

            /* Make header fixed at the top with full viewport width */
            .header-image {{
                position: absolute;
                top: o;
                left: -20vw;
                overflow-x: hidden;
                width: 120vw;
                height: 35vh;  /* Adjust height as needed */
                background-image: url("data:image/jpg;base64,{header_image}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                z-index: 0;
                opacity: 0.8;
                margin: 0 ;
            }}

            /* Extend the gradient to blend into content smoothly */
            .header-gradient {{
                position: absolute;
                bottom: 0;
                width: 100%;
                height: 100%;  /* Match header-image height */
                background: linear-gradient(to bottom, rgba(255, 255, 255, 0) 60%, rgba(255, 255, 255, 1) 100%);
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
    
    st.logo('resources/logo_notext.svg', size='large', icon_image='resources/logo_notext.svg')
    logocol1, logocol2 = st.columns([2, 4])
    logocol1.image('resources/logo_text.svg', use_container_width=True)
    logocol2.text("")
    logocol2.text("")
    #p1, p2, p3, p4, p5, p6, p7 = logocol2.columns(7)
    #p1.image('resources/partners/01.png',width=200)
    #p2.image('resources/partners/07.png',width=200)
    #p3.image('resources/partners/03.png',width=200)
    #p4.image('resources/partners/04.png',width=200)
    #p5.image('resources/partners/05.png',width=200)
    #p6.image('resources/partners/06.png',width=200)
    #p7.image('resources/partners/02.png',width=200)

    def img_to_base64(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()

    # Convert all logos to base64
    logos = [
        "resources/partners/01.png",
        "resources/partners/07.png",
        "resources/partners/03.png",
        "resources/partners/04.png",
        "resources/partners/05.png",
        "resources/partners/06.png",
        "resources/partners/02.png",
    ]
    logo_tags = [
        f'<img src="data:image/png;base64,{img_to_base64(path)}">' for path in logos
    ]

    # Display logos in a responsive container
    logocol2.markdown(
        f"""
        <style>
        .logo-container {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
        }}
        .logo-container img {{
            max-height: 60px;
            max-width: 100px;
            height: auto;
            width: auto;
        }}
        @media (max-width: 768px) {{
            .logo-container {{
                justify-content: center;
            }}
        }}
        </style>

        <div class="logo-container">
            {"".join(logo_tags)}
        </div>
        """,
        unsafe_allow_html=True
    )
