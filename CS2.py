import streamlit as st
import pathlib
import textwrap
import google.generativeai as genai
import time
#import config
from fpdf import FPDF

gemini_key = st.secrets["GEMINI_API_KEY"]
#st.secrets["gemini_api_key"]
#config.GEMINI_API_KEY
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel('gemini-pro')

#create PDF file to be downloaded
#CS^2
def generate_pdf(output):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size= 14)
    pdf.multi_cell(200, 10, txt = output,
              align = 'L')
    pdf_file = "Cheat-Sheet.pdf"
    pdf.output(pdf_file)
    return pdf_file

st.set_page_config(layout='wide')
st.title('Cheat Sheet Generator')
st.divider()
st.write('Select any CS topic that comes to your mind and generate its cheat-sheet')
# refactor code later & use tabs
tab1, tab2 = st.tabs(['PRG Langs', 'CS Topics'])

with tab1:
    st.header('PRG Langs')
    st.write("Select the type of programming language")


    functional_prg_langs = ['Haskell', 'Common Lisp', 'Clojure', 'Scala', 'Elixir', 'Racket', 'Erlang', 'F#', 'Scheme' , 'OCaml']
    imperative_prg_langs = ['C','C++', 'Python', 'Java', 'Javascript', 'Swift', 'Go', 'Ruby', 'Kotlin', 'Rust']
    prg_type = st.radio(
        "Programming Language Type",
        ["Functional", "Imperative"]
    )

    # input
    functional_prg_choices = st.selectbox("Functional Programming Languages", functional_prg_langs)
    imperative_prg_choices = st.selectbox("Imperative/OOP Programming Languages", imperative_prg_langs)
    # prg_langs = ['C','C++', 'Python', 'Java', 'Javascript', 'Haskell', 'Common Lisp','Clojure','Golang']
    # prg_choices = st.radio("Programming Languages", prg_langs)
    pnum_pages = st.selectbox('Pages',
                            ['1 page', '2 pages', '3 pages (max)'])
    func_prg_prompt = f"Generate a descriptive cheat sheet on {functional_prg_choices} (should include code snippets for examples or use cases)and the sheet should be {pnum_pages} in markdown format"
    imperative_prg_prompt = f"Generate a descriptive cheat sheet on {imperative_prg_choices} (should include code snippets for examples or use cases)and the sheet should be {pnum_pages} in markdown format"

    generate_btn = st.button('Generate Sheet')
# define a func for the generation code block
if generate_btn:
    if prg_type == "Functional":
        with st.spinner("Generating..."):
            time.sleep(45)
            response = model.generate_content(func_prg_prompt)
            pdf_file = generate_pdf(response.text)
            st.success(response.text)
            with open(pdf_file, "rb") as file:
                st.download_button(
                    label='Download Sheet',
                    data=file,
                    file_name=f'{functional_prg_choices} Cheat-Sheet.pdf',
                    mime='application/pdf'
                )
    elif prg_type == "Imperative":
         with st.spinner("Generating..."):
            time.sleep(45)
            response = model.generate_content(imperative_prg_prompt)
            pdf_file = generate_pdf(response.text)
            st.success(response.text)
            with open(pdf_file, "rb") as file:
                st.download_button(
                    label='Download Sheet',
                    data=file,
                    file_name=f'{imperative_prg_choices} Cheat-Sheet.pdf',
                    mime='application/pdf'
                )

with tab2:
    st.header('CS Topics')
    cs_topics = ['Computer Architecture', 'Data Structures & Algorithms', 'Operating Systems', 'Distributed Systems', 'Computer Networking', 'Databases' ,'Other'] # add or del elemnts to list later
    topics_list = st.selectbox('Topics', cs_topics)
    cnum_pages = st.selectbox('No. of Pages',
                            ['1 page', '2 pages', '3 pages (max)'])
    cs_prompt = f"Generate a descriptive cheat sheet on this topic {topics_list} and the sheet should be {cnum_pages} in markdown format"

    generate_btn2 = st.button('Generate CS Sheet')

if generate_btn2:
    with st.spinner("Generating..."):
        time.sleep(35)
    response = model.generate_content(cs_prompt)
    pdf_file = generate_pdf(response.text)
    st.success(response.text)
    with open(pdf_file, "rb") as file:
        st.download_button(
            label='Download Sheet',
            data=file,
            file_name=f'{topics_list} Cheat-Sheet.pdf',
            mime='application/pdf'
        )

#with st.form('form1'):
    #st.subheader('Sheet Data')
    #st.write('Select your topic || PRG Lang')
# user can type topic name if topic is not present on the list
    #cs_topics = ['Computer Architecture', 'Data Structures & Algorithms', 'Operating Systems', 'Distributed Systems', 'Other'] # add or del elemnts to list later
    #prg_langs = ['C','C++', 'Python', 'Java', 'Javascript', 'Haskell', 'Common Lisp','Clojure','Golang', 'Other']
    # allow user to input lang/topic if 'Other' is selected
    #sheet_type = st.radio(
     #   "PRG Language or CS Topic/Subject ?",
     #   ["PRG language", "CS subject"]
   # )
    #topics_list = st.selectbox('Topics', cs_topics)
   # prg_choices = st.radio("Programming Languages", prg_langs)
#    num_pages = st.selectbox('Pages',
    #                         ['1 page', '2 pages', '3 pages (max)'])

   # cs_prompt = f"Generate a descriptive cheat sheet on this topic {topics_list} and the sheet should be {num_pages} in markdown format"
   # prg_prompt = f"Generate a descriptive cheat sheet on {prg_choices} (should include code snippets for examples or use cases)and the sheet should be {num_pages} in markdown format"
    #generate_btn = st.form_submit_button('Generate Sheet')
