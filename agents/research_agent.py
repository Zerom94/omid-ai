"""Research Agent Implementation

Searches web APIs, GitHub, and documentation. Uses free search APIs and
grepping via curl. No paid dependencies required.

Uses urllib + curl for web calls. Results stored in structured format with
credibility ratings.
"""
from __future__ import annotations
import asyncio
import json
import time
from typing import Any
from urllib.parse import quote

import urllib.request
import urllib.error

from agents.base import BaseAgent, Task, Result


class ResearchAgent(BaseAgent):
    name = "Research"
    display_name = "Research Agent"

    async def execute(self, task: Task) -> Result:
        start = time.time()
        query = task.description.lower() if not task.metadata.get("goal_line", "") else task.metadata["goal_line"]

        # Determine what kind of research is needed from the goal line
        kind = self._infer_kind(query)
        findings = []

        if kind == "web":
            findings = await self._search_web(query)
        elif kind == "github":
            findings = await self._search_github(query)
        elif kind == "docs":
            findings = await self._fetch_docs(query)
        else:
            findings = await self._search_web(query)

        result = Result(
            task_id=task.id,
            success=True,
            output={"findings": findings, "count": len(findings)},
            execution_time_ms=round((time.time() - start) * 1000, 2),
        )
        self.store_result(result)
        return result

    def _infer_kind(self, query: str) -> str:
        q = query.strip().lower()
        if "license" in q or "dependency" in q or "package" in q:
            return "docs"
        if "github" in q or "repo" in q or "source code" in q:
            return "github"
        return "web"

    async def _search_web(self, query: str) -> list[dict]:
        results = []
        # Use DuckDuckGo HTML (no API key needed) for lightweight search
        search_url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
        try:
            data = await asyncio.to_thread(self._http_get, search_url)
            for i, item in enumerate(data.split("</div>")):
                if "abstractsnippet" in item or "snippet" in item:
                    continue  # skip parse noise
                if "<a" in item and "href" in item:
                    text = item.replace("<a ", "").replace("</a>", "").replace("<b>", "").replace("</b>", "")
                    title = item.replace("<a ", "").replace("</a>", "")[:150].strip()
                    href = ""
                    idx = item.find('class="result--url"')
                    if idx >= 0:
                        href_end = item.rfind('"', idx)
                        if href_end > idx:
                            href = item[item.find('"', item.find('href=', item.find('\"', idx))) + 6: href_end]
                    if len(title) > 20:
                        results.append({
                            "kind": "web",
                            "source": "duckduckgo",
                            "url": href if href else search_url,
                            "title": title[:100],
                            "snippet": "",
                            "credibility": "medium",
                        })
        except Exception as e:
            return [{"error": str(e), "credibility": "low"}]
        return results

    async def _search_github(self, query: str) -> list[dict]:
        url = f"https://api.github.com/search/repositories?q={quote(query)}&per_page=5"
        try:
            resp = await asyncio.to_thread(self._http_get, url, headers={"Accept": "application/vnd.github+json"})
            items = json.loads(resp).get("items", [])
            for r in items:
                results = [
                    {
                        "kind": "github",
                        "source": "github",
                        "url": r["html_url"],
                        "title": r["full_name"],
                        "snippet": f"{r['description']} ({r['language']}, {r['stars']} stars)",
                        "credibility": "high",
                        "license": r.get("license", {}).get("spdx_id", "unknown") if r.get("license") else "none",
                    }
                ]
                results.extend(await self._fetch_info(r["id"]))
                results.append(None)  # placeholder, then filter
                results = [x for x in results if x]
                results = [x for x in results if x is not None]
            return [x for x in results if x] if isinstance(results, list) else []
        except Exception as e:
            return [{"error": str(e), "credibility": "low"}]

    async def _fetch_docs(self, query: str) -> list[dict]:
        # Search Wikipedia / generic docs pages — lightweight
        return await self._search_web(f"documentation {query}")

    async def _fetch_info(self, repo_id: int) -> dict:
        url = f"https://api.github.com/repos/{repo_id}"
        try:
            resp = await asyncio.to_thread(self._http_get, url, headers={"Accept": "application/vnd.github+json"})
            d = json.loads(resp)
            return {
                "kind": "github_detail",
                "source": "github",
                "url": d["html_url"],
                "title": d["full_name"],
                "snippet": f"{d['description']} | {d['language']} | Stars: {d['stargazers_count']}",
                "credibility": "high",
                "license": d.get("license", {}).get("spdx_id", "unknown"),
                "issues": d.get("open_issues_count", 0),
            }
        except Exception:
            return {}

    @staticmethod
    def _http_get(url: str, headers: dict | None = None) -> str:
        req = urllib.request.Request(url, headers=headers or {})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", errors="replace")
