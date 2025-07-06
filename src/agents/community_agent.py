import asyncio

from agents import Agent, OpenAIChatCompletionsModel, enable_verbose_stdout_logging, set_tracing_disabled, Runner
from agents.mcp import MCPServer, MCPServerStdio
from openai import AsyncOpenAI

from src.config import config


instructions = '''  
You are an expert in evaluating GitHub project activity levels. Calculate a **comprehensive activity score (0-100)** based exclusively on the following GitHub metrics:  

### Evaluation Criteria  
1. **Issue Responsiveness**  
   - For the 10 most recent open issues (if available):  
   - Measure hours since last activity (comment/labeling/status change)  
   - **Scoring logic**: Lower time delta = Higher score  
   - *Formula*: `Score = max(0, 50 - (avg_hours / 24))` (Cap at 50 points)  

2. **Growth Metrics**  
   - Stars gained in last 30 days (20% weight)  
   - Active contributors in last 30 days (30% weight)  
  
- *Critical rule*: When data unavailable, deduct 25% per missing metric  

### Output Requirements Example
{
  "final_score": "83/100",
  "reasoning": {
    "issue_responsiveness": "18h avg → 47/50",
    "stars": "+142 (90d)",
    "contributors": "9 active (180d)",
    "sub_score": "36/50"
}
'''

model=OpenAIChatCompletionsModel(
    model=config.community_agent.model,
    openai_client=AsyncOpenAI(api_key=config.community_agent.api_key, base_url=config.community_agent.base_url)
)

def get_community_agent(mcp_server: MCPServer):
    agent = Agent(
        name="community_agent",
        instructions=instructions,
        mcp_servers=[mcp_server],
        model=model
    )

    return agent

async def main():
    async with MCPServerStdio(
        cache_tools_list=True,
        params={
            "command": config.community_agent.mcp[0].command,
            "args": ["stdio", "--read-only", "--toolsets", "issues,users,context"],
            "env": config.community_agent.mcp[0].env
        },
    ) as server:
        result = await Runner.run(get_community_agent(server), "github repo url: https://github.com/FoundationAgents/OpenManus")
        print(result.final_output)

if __name__ == '__main__':
    enable_verbose_stdout_logging()
    set_tracing_disabled(disabled=True)

    asyncio.run(main())