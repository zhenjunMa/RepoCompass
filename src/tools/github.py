from agents import function_tool
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
import json

@function_tool()
async def get_statistics_from_github(repo_url: str) -> dict[str, str] | None:
    """
    fetches the relevant data, and returns a dictionary containing the statistics for the repository.

    Args:
        repo_url: the URL of the GitHub repository to analyze and fetch statistics from

    Returns:
        - `dict`: A dictionary where each key is a unique identifier for a repository (e.g., "repo_1", "repo_2", etc.), and the value is another dictionary containing the following statistics:
            - `star` (int): The number of stars the repository has.
            - `fork` (int): The number of forks the repository has.
            - `issues` (int): The number of open issues in the repository.
            - `pr` (int): The number of open pull requests in the repository.
            - `contributor` (int): The number of contributors to the repository.
    """
    browser_config = BrowserConfig(browser_type="chromium", headless=True)

    crawler_config = CrawlerRunConfig(
        extraction_strategy=JsonCssExtractionStrategy(
            schema={
                "name": "github statistics",
                "baseSelector": "body",
                "fields": [
                    {
                        "name": "star",
                        "selector": "#repo-stars-counter-star",
                        "type": "text",
                    },
                    {
                        "name": "fork",
                        "selector": "#repo-network-counter",
                        "type": "text"
                    },
                    {
                        "name": "issues",
                        "selector": "#issues-repo-tab-count",
                        "type": "text"
                    },
                    {
                        "name": "pr",
                        "selector": "#pull-requests-repo-tab-count",
                        "type": "text",
                    },
                    {
                        "name": "contributor",
                        "selector": "#repo-content-pjax-container div div div div.Layout-sidebar div div:nth-child(5) div h2 a span",
                        "type": "text",
                    },
                ],
            }
        )
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=repo_url, config=crawler_config)

        if result and result.extracted_content:
            products = json.loads(result.extracted_content)

            for product in products:
                return {
                    "star": product.get("star"),
                    "fork": product.get("fork"),
                    "issues": product.get("issues"),
                    "pr": product.get("pr"),
                    "contributor": product.get("contributor")
                }