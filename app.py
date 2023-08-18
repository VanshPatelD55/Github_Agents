import os
import streamlit as st
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits.github.toolkit import GitHubToolkit
from langchain.llms import OpenAI
from langchain.utilities.github import GitHubAPIWrapper

# Set your environment variables using os.environ
os.environ["GITHUB_APP_ID"] = "123456"
os.environ["GITHUB_APP_PRIVATE_KEY"] = "path/to/your/private-key.pem"

# Streamlit input fields
st.title("GitHub Assistant")

github_repo = st.text_input("GitHub Repository (username/repo-name)")
github_branch = st.text_input("GitHub Branch")
github_base_branch = st.text_input("GitHub Base Branch")
prompt = st.text_area("Prompt")

# Initialize components
llm = OpenAI(temperature=0)
github = GitHubAPIWrapper()
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
