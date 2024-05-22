import streamlit as sl

sl.write('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">', unsafe_allow_html=True)

def icon(icon_name):
    return f'<i class="fas fa-{icon_name}"></i>'

background = """
<style>
    .stApp {
        background-color: #4E5166;
    }
    .stApp h1{
        color: #B9B7A7;
    }
    .stApp h3{
        color: #B9B7A7;
    }
    .stApp p{
        color: #B9B7A7;
    }
</style>
"""

sl.markdown(background, unsafe_allow_html=True)


sl.title("Searching for...")

# icon_pic = sl.markdown(icon("search") + " Search", unsafe_allow_html=True)
# query = sl.text_input("Enter your search", value="")


icon_pic = sl.markdown(icon("search") + " Search", unsafe_allow_html=True)
query = sl.text_input(label = "", value = "")



# # Display a text input box in the second column
# with col2:
#     user_input = st.text_input("Search", value="", help="Search for something")

# # Add a search icon to the first column
# with col1:
#     st.markdown(icon("search"), unsafe_allow_html=True)

sl.subheader("Previous Search") #h3

if query:
    sl.write(query)