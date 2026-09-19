import re
import httpx
from typing import Any, Dict
from hermes.tools.base import BaseTool, ToolParameter

class BrowserTool(BaseTool):
    name = "browser"
    description = "Navigates to web pages, extracts clean readable text, and returns structured page metadata."
    parameters = [
        ToolParameter(name="url", type="string", description="The target URL to scrape or navigate to.", required=True)
    ]

    async def execute(self, url: str) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
                headers = {"User-Agent": "HermesAgent/0.1.0 (Autonomous Cognitive Browser)"}
                resp = await client.get(url, headers=headers)
                if resp.status_code != 200:
                    return {"url": url, "status": resp.status_code, "error": f"HTTP {resp.status_code}", "success": False}
                
                html = resp.text
                # Clean HTML tags
                text = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
                text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)
                text = re.sub(r'<[^>]+>', ' ', text)
                clean_text = ' '.join(text.split())[:3000]
                
                title_match = re.search(r'<title>(.*?)</title>', html, flags=re.IGNORECASE)
                title = title_match.group(1).strip() if title_match else url

                return {
                    "url": url,
                    "title": title,
                    "content_snippet": clean_text,
                    "status": 200,
                    "success": True
                }
        except Exception as e:
            return {"url": url, "error": str(e), "success": False}
