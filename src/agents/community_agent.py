from agents import Agent, OpenAIChatCompletionsModel, enable_verbose_stdout_logging, set_tracing_disabled
from agents.mcp import MCPServer
from openai import AsyncOpenAI

from src.config import config

enable_verbose_stdout_logging()
set_tracing_disabled(disabled=True)


instructions = f'''  
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

### Output Requirements  
- **Final Score Format**:  
  ```
  Final Score: [0-100]/100  
  Reasoning:  
  1. Issue responsiveness: [avg_hours]h avg → [X]/50  
  2. Growth analysis:  
     - Stars: +[N] (90d)  
     - Contributors: [K] active (180d)  
     - Subscore: [Y]/50  
  ```  
- *Critical rule*: When data unavailable, deduct 25% per missing metric  

### Scoring Example  
> Final Score: 83/100  
> Reasoning:  
> 1. Issue responsiveness: 18h avg → 47/50  
> 2. Growth analysis:  
>    - Stars: +142 (90d)  
>    - Contributors: 9 active (180d)  
>    - Subscore: 36/50  

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