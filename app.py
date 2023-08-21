import os
import streamlit as st
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits.github.toolkit import GitHubToolkit
from langchain.llms import OpenAI
from langchain.utilities.github import GitHubAPIWrapper
from pydantic import ValidationError

# Set your environment variables using os.environ
st.title("GitHub Assistant")
os.environ["GITHUB_APP_ID"]
os.environ["APP_PRIVATE_KEY"]
os.environ["GITHUB_REPOSITORY"] = "shroominic/codeinterpreter-api"
os.environ["GITHUB_BRANCH"] = "main"
os.environ["GITHUB_BASE_BRANCH"] = "main"
os.environ["OPENAI_API_KEY"]



github_repo = st.text_input("GitHub Repository (username/repo-name)")
github_branch = st.text_input("GitHub Branch")
github_base_branch = st.text_input("GitHub Base Branch")

if github_repo and github_branch and github_base_branch:
    os.environ["GITHUB_REPOSITORY"] = github_repo
    os.environ["GITHUB_BRANCH"] = github_branch
    os.environ["GITHUB_BASE_BRANCH"] = github_base_branch
# Streamlit input fields



prompt = st.text_area("Prompt")


class GitHubAPIWrapper:
    def __init__(self):
        try:
            # Your code to initialize the GitHubAPIWrapper
            # This might involve creating an instance of a Pydantic model or performing other operations
            
        except ValidationError as e:
            # Handle the validation error here
            print("Validation Error:", e)
            # You can choose to log the error, provide a custom error message, or take any necessary actions

# Create an instance of GitHubAPIWrapper
try:
    github = GitHubAPIWrapper()
except Exception as e:
    print("Error:", e)
    # Handle the exception raised during GitHubAPIWrapper instantiation
    # This could be a ValidationError or any other exception

# Initialize components
llm = OpenAI(temperature=0)
toolkit = GitHubToolkit.from_github_api_wrapper(github)
agent = initialize_agent(
    toolkit.get_tools(), llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

# Run the agent when the user clicks the "Run" button
if st.button("Run Agent"):
    if github_repo and github_branch and github_base_branch and prompt:
        os.environ["GITHUB_REPOSITORY"] = github_repo
        os.environ["GITHUB_BRANCH"] = github_branch
        os.environ["GITHUB_BASE_BRANCH"] = github_base_branch

        # Run the agent
        response = agent.run(prompt)
        st.write("Agent Response:")
        st.write(response)
    else:
        st.warning("Please fill in all the input fields.")
