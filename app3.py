import streamlit as st
import csv
import webbrowser
import base64

# Read CSV file and create a dictionary of professors' data
data = {}
with open('iiserfaculty.csv', 'r', encoding='utf-8', errors='ignore') as file:
    reader = csv.DictReader(file)
    for row in reader:
        name = row['Name']
        data[name] = {
            'Name': row['Name'],
            'Research': row['ResearchAreas'],
            'Publications': row['ResearchAndPublications'],
            'Email': row['Email'],
            'ProfilePic': row['ProfileImage'],
            'Webpage': row['ResearchGroupWebsite'],
            'About': row['About']
        }

# Set page configuration
st.set_page_config(page_title='Professor Search')


# Add logo as a banner on top of the page
logo_path = 'logo.png'
banner_html = f"""
    <style>
        .banner {{
            background-image: url("data:image/png;base64,{base64.b64encode(open(logo_path, "rb").read()).decode()}");
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            padding: 2rem;
            margin-bottom: 2rem;
            max-width: 100%;
            width: 100%;
            height: 100px;
        }}
    </style>

    <div class="banner"></div>
"""
st.markdown(banner_html, unsafe_allow_html=True)


# Streamlit web application
st.title("Search your supervisor - IISER Pune")

# Search bar for research interest and publications
query = st.text_input("Enter name, research interest or publication:")
found_professors = []

# Search and display professors based on research interest or publications
if query:
    for professor_name, professor_data in data.items():
        if (
            query.lower() in professor_data['Name'].lower()
            or query.lower() in professor_data['Research'].lower()
            or query.lower() in professor_data['Publications'].lower()
            or query.lower() in professor_data['About'].lower()

        ):
            st.write(f"**Name:** {professor_name}")
            st.write(f"**About:** {professor_data['About']}")
            if professor_data['ProfilePic']:
                st.image(professor_data['ProfilePic'], use_column_width=True)
            else:
                st.write("No profile image found.")
            st.write(f"**Research Interest:** {professor_data['Research']}")
            # st.write(f"**Publications:** {professor_data['Publications']}")
            st.write("**Publications:**")
            publications = professor_data['Publications'].split("////")[:-1]
            for i, publication in enumerate(publications, start=1):
                st.write(f"{i}. {publication.strip()}")
            st.write(f"**Email:** {professor_data['Email']}")

            # Generate a unique key using professor's name
            button_key = f"button_{professor_name}"

            # Use unique key for the button
            if st.button('Go to Webpage', key=button_key):
                if professor_data['Webpage']:
                    webbrowser.open_new_tab(professor_data['Webpage'])
                else:
                    st.write("No research group website found.")

            found_professors.append(professor_name)
            st.markdown("""<hr style="height:5px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

# Create a sidebar column for the dropdown
with st.sidebar:
    # Dropdown to select professor's webpage or option to return all professors
    option = st.selectbox("Select option:", ["All Professors"] + found_professors)
    if option == "All Professors":
        for professor_name, professor_data in data.items():
            if (
                query.lower() in professor_data['Name'].lower()
                or query.lower() in professor_data['Research'].lower()
                or query.lower() in professor_data['Publications'].lower()
                or query.lower() in professor_data['About'].lower()
            ):
                st.write(f"**Name:** {professor_name}")
                st.write(f"**Research Interest:** {professor_data['Research']}")
                # st.write(f"**Publications:** {professor_data['Publications']}")
                st.write(f"**Email:** {professor_data['Email']}")
                if professor_data['ProfilePic']:
                    st.image(professor_data['ProfilePic'], use_column_width=True)
                else:
                    st.write("No profile image found.")

                # Generate a unique key using professor's name
                button_key = f"button_{professor_name}_dropdown"

                # Use unique key for the button
                if st.button('Go to Webpage', key=button_key):
                    if professor_data['Webpage']:
                        webbrowser.open_new_tab(professor_data['Webpage'])
                    else:
                        st.write("No research group website found.")
    elif option in found_professors:
        professor_data = data[option]
        st.write(f"**Name:** {option}")
        st.write(f"**Research Interest:** {professor_data['Research']}")
        # st.write(f"**Publications:** {professor_data['Publications']}")
        st.write(f"**Email:** {professor_data['Email']}")
        if professor_data['ProfilePic']:
            st.image(professor_data['ProfilePic'], use_column_width=True)
        else:
            st.write("No profile image found.")

        # Generate a unique key using professor's name
        button_key = f"button_{option}_dropdown"

        # Use unique key for the button
        if st.button('Go to Webpage', key=button_key):
            if professor_data['Webpage']:
                webbrowser.open_new_tab(professor_data['Webpage'])
            else:
                st.write("No research group website found.")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
