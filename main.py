import asyncio

from agents import Agent, Runner, OpenAIChatCompletionsModel, enable_verbose_stdout_logging, set_tracing_disabled
from agents.mcp import MCPServerStdio
from git import Repo
from openai import AsyncOpenAI

from src.agents.community_agent import get_community_agent
from src.agents.repo_agent import get_repo_agent
from src.config import config, PROJECT_ROOT

enable_verbose_stdout_logging()
set_tracing_disabled(disabled=True)

model=OpenAIChatCompletionsModel(
    model=config.manager_agent.model,
    openai_client=AsyncOpenAI(api_key=config.manager_agent.api_key, base_url=config.manager_agent.base_url)
)

instructions = """
You are RepoInsight AI, a GitHub repository analysis expert. Your task is to analyze repositories using two specialized tools and present findings in a clear, engaging format.

**Workflow**:
1. Receive user input: `<repoURL>` and optional `<repoPath>`
2. Use tools **sequentially**:
   - First call `repo_analyze` with repository details
   - Then call `community_analyze` with same inputs
3. Synthesize both reports into a single analysis

**Output Requirements**:
- Use GitHub-themed emojis for visual organization
- Present data in 3 clear sections
- Convert JSON fields to human-readable insights
- Never show raw JSON outputs
- Highlight critical findings with ⚠️/✅
"""

async def main(user_repo_url: str, user_repo_local_path: str):
    git_mcp_server = MCPServerStdio(
        cache_tools_list=True,
        params={"command": "uvx", "args": ["mcp-server-git"]},
    )

    github_mcp_server = MCPServerStdio(
        cache_tools_list=True,
        params={
            "command": config.community_agent.mcp[0].command,
            "args": ["stdio", "--read-only", "--toolsets", "issues,users,context"],
            "env": config.community_agent.mcp[0].env
        },
    )

    async with git_mcp_server, github_mcp_server:
        repo_agent = get_repo_agent(git_mcp_server)
        community_agent = get_community_agent(github_mcp_server)

        triage_agent = Agent(
            name="manager_agent",
            instructions=instructions,
            tools=[
                repo_agent.as_tool(
                    tool_name="repo_analyze",
                    tool_description="Evaluates structure/metadata for a github repo",
                ),
                community_agent.as_tool(
                    tool_name="community_analyze",
                    tool_description="Calculates activity score from GitHub metrics for a github repo",
                ),
            ],
            model=model
        )

        result = await Runner.run(triage_agent,
                                  input=f"my repo url is {user_repo_url}, i have download the repo in path: {user_repo_local_path}, please help to evaluate this code repo for standardization and calculate the activity score",
                                  max_turns=10)
        print(result.final_output)


if __name__ == "__main__":
    repo_url = input("please input your github repo url:")
    project_local_path = PROJECT_ROOT / repo_url.split("/")[-1]

    asyncio.run(main(repo_url, project_local_path))