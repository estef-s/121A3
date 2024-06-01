import streamlit as sl
import searcher as s
import time 


s.setUP()
sl.write('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">', unsafe_allow_html=True)

def icon(icon_name):
    return f'<i class="fas fa-{icon_name}"></i>'

background = """
<style>
    .stApp {
        background-color: #F3C2CC;
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


sl.title("What do you want to search for?")

# icon_pic = sl.markdown(icon("search") + " Search", unsafe_allow_html=True)
# query = sl.text_input("Enter your search", value="")


icon_pic = sl.markdown(icon("search") + " Search", unsafe_allow_html=True)
query = sl.text_input(label = "Enter Search", value = "")


sl.subheader("Previous Search") #h3

if query:
    # results = s.startEngine(query)
    # sl.write(query)
    start_time = time.time()  # Start time measurement
    results = s.startEngine(query)
    end_time = time.time()  # End time measurement
    search_duration = end_time - start_time  # Calculate search duration

    sl.write(f"Search completed in {search_duration:.2f} seconds")  # Display search time
    sl.write(f"Results for \"{query}\"")
    i = 1
    for r in results:
        sl.write(f"{i}) {r}")
        i += 1
