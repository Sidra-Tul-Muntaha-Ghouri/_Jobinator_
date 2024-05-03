import os
import streamlit as st
import shutil
import openai
from streamlit_chat import message
from llama import generate_response
from key import KEY
from vector import create_vector
from streamlit_modal import Modal

def set_page_config():
    st.set_page_config(page_title="hassaan", page_icon="chart_with_upwards_trend")
    st.markdown("<h1 style='text-align: center;'>Job Advisor</h1>", unsafe_allow_html=True)

def create_directories():
    saved_path = "data"
    if not os.path.exists(saved_path):
        os.makedirs(saved_path)
    saved_path = "data_dir"
    return saved_path

def display_hello_message():
    st.write(f"Hello EveryONE")

def select_directory(subdirs):
    selected_dir = st.sidebar.radio('Select a directory:', options=subdirs)
    return selected_dir

def upload_pdf(selected_dir):
    uploaded_file = st.sidebar.file_uploader('Upload a PDF', type=['pdf'])
    st.write("Selected Dir", selected_dir)
    if uploaded_file is not None:
        save_path = os.path.join(f'./{saved_path}', selected_dir)
        with open(os.path.join(save_path, uploaded_file.name), 'wb') as f:
            f.write(uploaded_file.getbuffer())
        st.success('File uploaded successfully.')

def create_vectors(selected_dir):
    if st.sidebar.button('Submit'):
        create_vector(selected_dir)

def select_folders(subdirs):
    checkbox_states = {}
    for folder_name in subdirs:
        checkbox_states[folder_name] = st.sidebar.checkbox(folder_name)
    selected_folders = [folder_name for folder_name, state in checkbox_states.items() if state]
    return selected_folders

def initialize_session_state():
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [{"role": "system", "content": "You are a helpful assistant."}]

def process_user_input(selected_folders):
    response_container = st.container()
    container = st.container()
    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_area("You:", key='input', height=50)
            submit_button = st.form_submit_button(label='Send')
        if submit_button and user_input:
            output = generate_response(user_input, selected_folders)
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user1')
                message(st.session_state["generated"][i], key=str(i))

if __name__ == "__main__":
    set_page_config()
    saved_path = create_directories()
    display_hello_message()
    subdirs = [name for name in os.listdir(f'./{saved_path}') if os.path.isdir(os.path.join(f'./{saved_path}', name))]
    selected_dir = select_directory(subdirs)
    upload_pdf(selected_dir)
    create_vectors(selected_dir)
    selected_folders = select_folders(subdirs)
    initialize_session_state()
    process_user_input(selected_folders)
