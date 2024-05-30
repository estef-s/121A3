import streamlit as sl
import searcher as s

s.setUP()
sl.write('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">', unsafe_allow_html=True)

def icon(icon_name):
    return f'<i class="fas fa-{icon_name}"></i>'

background = """
<style>
    .stApp {
        background-color: #B9B7A7;
    }
    .stApp h1{
        color: #4E5166;
    }
    .stApp h3{
        color: #4E5166;
    }
    .stApp p{
        color: #4E5166;
    }

    a.custom-link {
    color: #B9B7A7; /* Tomato color */
    text-decoration: none;
    }

    a.custom-link:hover {
        color: #ff4500; /* OrangeRed color */
        text-decoration: underline;
    }
</style>
"""

sl.markdown(background, unsafe_allow_html=True)


sl.title("Searching for...")

# icon_pic = sl.markdown(icon("search") + " Search", unsafe_allow_html=True)
# query = sl.text_input("Enter your search", value="")


icon_pic = sl.markdown(icon("search") + " Search", unsafe_allow_html=True)
query = sl.text_input(label = "Enter Search", value = "")


sl.subheader("Previous Search") #h3

if query:
    results = s.startEngine(query)
    sl.write(query)
    for r in results:
        sl.write(r)