import asyncio

from agents.mcp import MCPServer, MCPServerStdio
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel, Agent, Runner, enable_verbose_stdout_logging, set_tracing_disabled
from pydantic import BaseModel, Field

from src.config import config
from src.tools.file import tree, read_file, get_current_time

instructions = '''  
You are an expert in assessing **structural and documentation compliance of GitHub repositories**. Evaluate repositories exclusively based on file presence, content patterns, and commit history (NO code analysis). Follow this workflow when users provide a repository path:

### Evaluation Workflow
1. **Scan root directory** for required files
2. **Analyze README content** for embedded sections
3. **Examine latest 10 commits** from `git log`

### Assessment Criteria
**1. Documentation**
- `README`: Presence of any file matching `readme*` (root directory)
- `QUICKSTART`: Satisfied if EITHER:
  - Dedicated file: `quickstart*` or `gettingstarted*` (case-insensitive) in root 
  - README section: Heading matching `# Quick Start` or `## Getting Started` followed by ≥3 steps/commands
- `CONTRIBUTING`: Satisfied if EITHER:
  - Dedicated file: `contributing*` or `contribution*` in root
  - README section: Heading matching `# Contribut(e|ing|ions)` with ≥100 characters of guidelines
- `ROADMAP`: Satisfied if EITHER:
  - Dedicated file: `roadmap*` or `plan*` in root
  - README section: Heading matching `# Roadmap` or `## Future Plans` with dated/versioned milestones
- `WEBSITE`: Official link exists in either:
  - Repository description (GitHub header)
  - First 200 characters of README

**2. Licensing**
- Identify license type from:
  - `LICENSE`/`COPYING` file in root
  - GitHub-detected license badge
- Return SPDX identifier (e.g., "MIT", "GPL-3.0") or "None"

**3. Code Activity**
- Calculate from last 10 commits:
  - `average_update_interval_days`: Mean days between commit dates (1 decimal)
  - `days_since_last_update`: Days from latest commit to current date

### Output Requirements
{
  "has_readme": boolean,
  "has_quickstart": boolean,
  "has_contributors_guide": boolean,
  "has_roadmap": boolean,
  "has_official_website": boolean,
  "license_type": "string",
  "average_update_interval_days": float,
  "days_since_last_update": integer
}
'''

model=OpenAIChatCompletionsModel(
    model=config.repo_agent.model,
    openai_client=AsyncOpenAI(api_key=config.repo_agent.api_key,base_url=config.repo_agent.base_url),
)

# todo deepseek do not support Structured Output now, just for future
class StandardCheckerOutput(BaseModel):
    has_readme: bool = Field(description="whether the project has a readme file")
    has_quickstart: bool = Field(description="whether the project has a quick start guide")
    has_contributors_guide: bool
    has_roadmap: bool
    has_official_website: bool
    open_source_license: str
    average_update_interval_days: int
    days_since_last_update: int

def get_repo_agent(mcp_server: MCPServer):
    agent = Agent(
        name="repo_agent",
        instructions=instructions,
        tools=[tree, read_file, get_current_time],
        mcp_servers=[mcp_server],
        model=model,
    )

    return agent

async def main():
    async with MCPServerStdio(
        cache_tools_list=True,
        params={"command": "uvx", "args": ["mcp-server-git"]},
    ) as server:
        result = await Runner.run(get_repo_agent(server), "/Users/gujin/workspace/python/RepoCompass/OpenManus")
        print(result.final_output)

if __name__ == '__main__':
    enable_verbose_stdout_logging()
    set_tracing_disabled(disabled=True)

    asyncio.run(main())
