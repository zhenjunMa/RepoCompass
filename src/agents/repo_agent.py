import asyncio

from agents.mcp import MCPServer, MCPServerStdio
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel, Agent, Runner, enable_verbose_stdout_logging, set_tracing_disabled

from src.config import config
from src.tools.file import tree, read_file, get_current_time

instructions = '''  
You are an expert in assessing **normative compliance of GitHub open-source repositories**. Evaluate projects exclusively based on structural/documentation standards (NO code analysis required). When users provide a repository path:  
1. **Scan directory structure**  
2. **Check critical files**  
3. **Query the latest 10 git log entries**

Systematically assess using these criteria:    

### Evaluation Criteria  
1. **Documentation**  
   a. Presence of `README` file  
   b. Presence of `quickstart` guide  
   c. Presence of `CONTRIBUTING` guidelines  
   d. Presence of `ROADMAP`  
   e. Presence of official website link  

2. **Licensing**  
   a. Type of open-source license used

2. **Code Activity**  
   a. The average update interval in days
   b. The number of days elapsed since the last change until now

### Output Format Requirements  
- Present results in a **structured markdown table**.  
- Columns:  
  - **Category** (e.g., "Documentation")  
  - **Sub-criteria** (e.g., "Presence of README file")  
  - **Compliance Status**:  
    - ✅ if satisfied  
    - ❎ if not satisfied  
    - *For licenses:* State the license name (e.g., "MIT")  

### Example Output  
| Category    | Sub-criteria                 | Compliance Status |  
|-------------|------------------------------|-------------------|  
| Documentation | Presence of README file      | ✅              |  
| Documentation | Presence of quickstart guide | ❎              |  
| Licensing   | Type of open-source license  | MIT               |  

'''

model=OpenAIChatCompletionsModel(
    model=config.repo_agent.model,
    openai_client=AsyncOpenAI(api_key=config.repo_agent.api_key,base_url=config.repo_agent.base_url)
)

def get_repo_agent(mcp_server: MCPServer):
    agent = Agent(
        name="repo_agent",
        instructions=instructions,
        tools=[tree, read_file, get_current_time],
        mcp_servers=[mcp_server],
        model=model
    )

    return agent

async def main():
    async with MCPServerStdio(
        cache_tools_list=True,
        params={"command": "uvx", "args": ["mcp-server-git"]},
    ) as server:
        result = await Runner.run(get_repo_agent(server), "code path:/Users/gujin/workspace/python/RepoCompass/OpenManus")
        print(result.final_output)

if __name__ == '__main__':
    enable_verbose_stdout_logging()
    set_tracing_disabled(disabled=True)

    asyncio.run(main())
