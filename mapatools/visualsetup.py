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
                height: 150%;  /* Match header-image height */
                background: linear-gradient(to bottom, rgba(255, 255, 255, 0) 65%, rgba(255, 255, 255, 1) 100%);
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
    #logocol1, logocol2 = st.columns([2, 6])
    #logocol1.image('resources/logo_text.svg', use_container_width=True)
    #logocol2.text("")
    #logocol2.text("")

    # Function to convert any image file to base64
    def img_to_base64(path, file_type):
        """Converts an image file to a base64 string."""
        try:
            with open(path, "rb") as f:
                encoded_string = base64.b64encode(f.read()).decode()
            # Determine the correct MIME type based on the file type
            mime_type = f"image/{file_type.lower()}"
            if file_type.lower() == 'svg':
                 mime_type = "image/svg+xml" # Specific MIME type for SVG
            return f"data:{mime_type};base64,{encoded_string}"
        except FileNotFoundError:
            st.error(f"Error: Image file not found at {path}")
            return ""
        except Exception as e:
            st.error(f"Error encoding image {path}: {e}")
            return ""


    # --- Logo Configuration ---
    text_logo_path = 'resources/logo_text.svg'
    partner_logos_paths = [
        "resources/partners/01.png",
        "resources/partners/07.png",
        "resources/partners/03.png",
        "resources/partners/04.png",
        "resources/partners/05.png",
        "resources/partners/06.png",
        "resources/partners/02.png",
    ]

    # --- Base64 Encoding ---
    text_logo_base64 = img_to_base64(text_logo_path, 'svg')

    partner_logo_tags = []
    for path in partner_logos_paths:
        # Determine file type (assuming .png)
        file_type = path.split('.')[-1]
        base64_data = img_to_base64(path, file_type)
        if base64_data: # Only add if encoding was successful
            partner_logo_tags.append(f'<img src="{base64_data}">')

    # Join partner logo tags into a single string
    partner_logos_html = "".join(partner_logo_tags)

    # --- HTML and CSS for layout ---
    # We'll use flexbox for the main layout (text logo vs partners)
    # and flexbox again for the partner logos row.
    # We'll set a max-height for the partner logos and
    # a calculated height (2.5x) for the text logo.

    # Define the target height for partner logos
    partner_logo_max_height = 50 # pixels
    text_logo_height = partner_logo_max_height * 2 # pixels

    html_content = f"""
    <style>
        /* Main container using flexbox */
        .logo-header-container {{
            display: flex;
            align-items: center; /* Vertically center items */
            gap: 200px; /* Space between text logo and partner logos */
            margin-bottom: -20px; /* Add some space below the logo section */
            flex-wrap: wrap; /* Allow wrapping if needed */
        }}

        /* Style for the text logo */
        .text-logo-container {{
            /* Flex properties to control text logo size and shrinking */
            /* Don't set a fixed width here, let height control it */
        }}

        .text-logo-container img {{
            height: {text_logo_height}px; /* Set height based on calculation */
            width: auto; /* Maintain aspect ratio */
            /* Optional: Limit max width on larger screens if it gets too wide */
            /* max-width: 80%; */
        }}

        /* Container for partner logos (reusing/modifying your original styles) */
        .partner-logos-container {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: flex-start; /* Align logos to the start */
            gap: 10px; /* Space between partner logos */
            flex-grow: 1; /* Allow this container to take up available space */
            /* min-width: 0; /* Allow shrinking below content size */
        }}

        .partner-logos-container img {{
            max-height: {partner_logo_max_height}px; /* Set max height for partner logos */
            width: auto; /* Maintain aspect ratio */
            /* max-width: {partner_logo_max_height}px; /* Optional: Set max width as well */
        }}

        /* Responsive adjustments */
        @media (max-width: 768px) {{
            .logo-header-container {{
                flex-direction: column; /* Stack items vertically on small screens */
                align-items: center; /* Center items when stacked */
            }}

            .text-logo-container {{
                 width: 100%; /* Allow text logo container to take full width */
                 text-align: center; /* Center the image horizontally */
                 margin-bottom: 10px; /* Add space below text logo when stacked */
            }}

            .text-logo-container img {{
                height: auto; /* Allow height to adjust */
                max-width: 90%; /* Prevent overflowing on small screens */
            }}

            .partner-logos-container {{
                justify-content: center; /* Center partner logos when stacked */
                width: 100%; /* Allow partner logos container to take full width */
            }}

            .partner-logos-container img {{
                 max-height: {partner_logo_max_height * 0.8}px; /* Slightly smaller on mobile */
            }}
        }}

    </style>

    <div class="logo-header-container">
        <div class="text-logo-container">
            {'<img src="' + text_logo_base64 + '">' if text_logo_base64 else ''}
        </div>
        <div class="partner-logos-container">
            {partner_logos_html}
        </div>
    </div>
    """

    # --- Display using Streamlit Markdown ---
    st.markdown(html_content, unsafe_allow_html=True)