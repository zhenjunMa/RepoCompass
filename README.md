<div align="center">
  <h1>RepoCompass</h1>
</div>

**RepoCompass** is an AI-powered GitHub repository evaluation assistant that assesses both technical standards compliance and community activity metrics for open-source projects.

## ✨ Features

- **Automated Repository Standards Assessment**
  - Checks for essential documentation (README, CONTRIBUTING, ROADMAP etc.)
  - Verifies license presence
  - Provides actionable improvement suggestions

- **Community Activity Analysis**
  - Measures issue response time and resolution rate
  - Analyzes commit frequency and contributor activity

- **AI-Powered Insights**
  - Natural language evaluation reports
  - Actionable recommendations for improvement
  - Comparative scoring against industry standards

## 🧠 Architecture Overview

RepoCompass uses a multi-agent system powered by OpenAI's Agent SDK:

```mermaid
graph LR
    A[Manager Agent] --> B[Repo Agent]
    A --> C[Community Agent]
    B --> D[Function Calls]
    C --> E[MCP Server]
```

### Core Agents

1. **Manager Agent**  
   - Routes requests to appropriate evaluation agents
   - Consolidates results into final report
   - Handles user communication

2. **Repo Agent**  
   - Performs local repository analysis
   - Uses function calling for file system operations
   - Evaluates documentation quality and project structure

3. **Community Agent**  
   - Interfaces with GitHub API via MCP server
   - Analyzes community engagement metrics
   - Assesses project activity and maintenance patterns

## ⚙️ Installation

Download github-mcp-server from [here](https://github.com/github/github-mcp-server/releases)

```bash
# Clone the repository
git clone https://github.com/zhenjunMa/RepoCompass.git
cd RepoCompass

# Set up environment variables
cp config/config.example.toml config/config.toml

# Install dependencies
uv venv .venv --python=3.12
source .venv/bin/activate
uv sync

uv run main.py

# please input your github repo url: ${github repo url}
```

## 🚀 Usage

### Sample Output

```
### Evaluation Summary for XXX Repository

#### **Standardization Compliance**
- **Documentation**:
  - ✅ **README file**: Comprehensive and includes a quickstart guide.
  - ✅ **Official website link**: Provided (Demo link).
  - ❌ **CONTRIBUTING guidelines**: Missing.
  - ❌ **ROADMAP**: Missing.
- **Licensing**:
  - ✅ **License type**: MIT (clearly stated).

#### **Community Activity Score**
- **Final Score**: **75/100**
  - **Issue Responsiveness**: **49/50** (average response time of ~24 hours).
  - **Growth Analysis**: **25/50** (due to missing data on stars and active contributors).

### Recommendations
1. **Improve Documentation**:
   - Add a `CONTRIBUTING.md` file to guide contributors.
   - Include a `ROADMAP.md` to outline future plans.
2. **Enhance Community Engagement**:
   - Encourage more stars and contributions to improve growth metrics.
   - Maintain the current responsiveness to issues.
```

## 🌐 Roadmap

- [ ] Auto download repo from Github
- [ ] Crawler for more data
- [ ] Historical trend analysis
- [ ] Custom evaluation rule sets

## 🤝 Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
