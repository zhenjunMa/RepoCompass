from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel, Agent

from src.config import config
from src.tools.file import tree, read_file

instructions = '''  
You are an expert in assessing the standardization of GitHub open-source projects. Your evaluation focuses **exclusively** on repository normative compliance and **does not involve analysis of source code**. Assess the following categories:  

### Evaluation Criteria  
1. **Documentation**  
   a. Presence of `README` file  
   b. Presence of `quickstart` guide  
   c. Presence of `CONTRIBUTING` guidelines  
   d. Presence of `ROADMAP`  
   e. Presence of official website link  

2. **Licensing**  
   a. Type of open-source license used  

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

def get_repo_agent():
    agent = Agent(
        name="repo_agent",
        instructions=instructions,
        tools=[tree, read_file],
        model=model
    )

    return agent