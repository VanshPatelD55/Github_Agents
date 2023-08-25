import os
import streamlit as st
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits.github.toolkit import GitHubToolkit
from langchain.llms import OpenAI
from langchain.utilities.github import GitHubAPIWrapper
from pydantic import ValidationError
from codeboxapi import CodeBox
import json
from PIL import Image
import io

# Set your environment variables using os.environ
st.set_page_config(
    page_title="GitHub Assistant",
    page_icon=":octocat:",
    layout="wide"
)

os.environ["GITHUB_APP_ID"] = st.secrets["GITHUB_APP_ID"]
os.environ["GITHUB_APP_PRIVATE_KEY"] = "vns-genai.2023-08-17.private-key.pem"
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Styling
st.markdown(
    """
    <style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
        background-color: #D3D3D3;
        padding: 20px;
        font-family: congenial, sans-serif;
    }
    .input-box {
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 5px;
        background-color: white;
        font-family: congenial, sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit input fields
st.title("GitHub Assistant")

with st.container():
    github_repo = st.text_input("GitHub Repository (username/repo-name)", key="github_repo")
    github_branch = st.text_input("GitHub Branch", key="github_branch")
    github_base_branch = st.text_input("GitHub Base Branch", key="github_base_branch")

    action_options = [
        "Get Issues", "Get Issue", "Comment on Issue", 
        "Create Pull Request", "Create File", 
        "Read File", "Update File", "Delete File"
    ]
    selected_action = st.selectbox("Select Action:", action_options, key="selected_action")

    # File and folder inputs
    file_name = st.text_input("Enter File Name (Display folder in addition to file name if exists)", key="file_name")

prompt = selected_action + file_name

# Check if the agent has already been run
agent_has_run = False

if github_repo and github_branch and github_base_branch:
    os.environ["GITHUB_REPOSITORY"] = github_repo
    os.environ["GITHUB_BRANCH"] = github_branch
    os.environ["GITHUB_BASE_BRANCH"] = github_base_branch

# Run Agent button
cols = st.columns([1, 2])
if cols[0].button("Run Agent", key="run"):
    with cols[1]:
        if github_repo and github_branch and github_base_branch and prompt:
            # Initialize components
            llm = OpenAI(temperature=0)
            github = GitHubAPIWrapper()
            toolkit = GitHubToolkit.from_github_api_wrapper(github)
            agent = initialize_agent(
                toolkit.get_tools(), llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
            )
            
            if not agent_has_run:
                agent_has_run = True
                final_prompt = f""" 
                   You are a skilled software developer with an in-depth understanding of various programming languages and proficient in performing GitHub operations. 
                   When generating code, please only include code snippets from the given file. 
                   Refrain from adding any additional content to the response. 
                   Ensure that the code provided is correctly formatted and, if necessary, you can complete code snippets that might have errors to ensure they compile successfully.


                   follow the above given instructions while performing prompt given below by the user
                   prompt:{prompt}
                   Strictly do not give any other text, only and only give code as an output
                """
                
                # Run the agent
                response = agent.run(final_prompt)
                st.write(response)
                # Display code result
                with CodeBox() as codebox:
                    result = codebox.run(response)
                    encoded_data = result
                    codebox.stop()
                    image = Image.open(io.BytesIO(encoded_data))
                    st.image(image, caption='My Captured Image', use_column_width=True)
                
                # Stop the Streamlit script after the initial run
                
            else:
                st.warning("Agent has already been run. Please reset the input fields to run again.")
            
            # Reset the agent_has_run flag to allow running again
            agent_has_run = False
