import os
import streamlit as st
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits.github.toolkit import GitHubToolkit
from langchain.llms import OpenAI
from langchain.utilities.github import GitHubAPIWrapper
from pydantic import ValidationError
from codeboxapi import CodeBox

# Set your environment variables using os.environ
st.title("GitHub Assistant")
os.environ["GITHUB_APP_ID"] = st.secrets['GITHUB_APP_ID']
os.environ["GITHUB_APP_PRIVATE_KEY"] = "vns-genai.2023-08-17.private-key.pem"
os.environ["GITHUB_REPOSITORY"] = "shroominic/codeinterpreter-api"
os.environ["GITHUB_BRANCH"] = "main"
os.environ["GITHUB_BASE_BRANCH"] = "main"
os.environ["OPENAI_API_KEY"] = st.secrets['OPENAI_API_KEY']



github_repo = st.text_input("GitHub Repository (username/repo-name)")
github_branch = st.text_input("GitHub Branch")
github_base_branch = st.text_input("GitHub Base Branch")

if github_repo and github_branch and github_base_branch:
    os.environ["GITHUB_REPOSITORY"] = github_repo
    os.environ["GITHUB_BRANCH"] = github_branch
    os.environ["GITHUB_BASE_BRANCH"] = github_base_branch
# Streamlit input fields



prompt = st.text_area("Prompt")
agent_has_run = False

if github_repo and github_branch and github_base_branch:
    os.environ["GITHUB_REPOSITORY"] = github_repo
    os.environ["GITHUB_BRANCH"] = github_branch
    os.environ["GITHUB_BASE_BRANCH"] = github_base_branch

if st.button("Run Agent"):
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
               
               Strictly do not give any other text only and only give code as an output
               follow the above given instructions while performing prompt given below by the user
               prompt:{prompt}
            """
            
            # Run the agent
            response = agent.run(final_prompt)
            st.write("Agent Response:")
            st.write(response)
            
            # Display code result
            with CodeBox() as codebox:
                result = codebox.run(response)
                st.write(result)
                
        else:
            st.warning("Agent has already been run. Please reset the input fields to run again.")
