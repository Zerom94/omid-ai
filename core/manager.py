from agents.base import BaseAgent, Task, Result
import traceback
import asyncio
import httpx
import json
import re
import os
from core.web_search import WebResearcher

class ManagerAgent(BaseAgent):
    name = "Manager"
    display_name = "Manager"

    def __init__(self, config=None, memory=None):
        super().__init__(config, memory)
        self.router_url = "http://127.0.0.1:5001/v1/chat/completions"
        self.knowledge_base_path = "/sdcard/omid-ai/agents_knowledge.json"
        
        if not os.path.exists(self.knowledge_base_path):
            with open(self.knowledge_base_path, "w", encoding="utf-8") as f:
                json.dump({"developer": "", "security": "", "recon": ""}, f)

    async def execute(self, task: Task) -> Result:
        return Result(task_id=task.id, success=True)

    async def train_agents(self):
        print("[Manager] 🧠 Starting Self-Improvement & Agent Training Protocol...", flush=True)
        self.log_event("working", {"agent": self.name, "status": "Training Agents..."})
        
        # موضوعات جدید (هوش مصنوعی، امنیت، دور زدن، کپچا)
        topics = {
            "manager": "advanced AI multi-agent orchestration and LLM routing techniques",
            "research": "web scraping bypass cloudflare captcha solving techniques and OSINT",
            "developer": "python AI integration security tools exploit development scripts",
            "analyst": "AI data analysis threat intelligence and anomaly detection",
            "security": "advanced web exploitation WAF bypass sql injection xss captcha bypass",
            "recon": "advanced bug bounty reconnaissance active directory enumeration osint techniques",
            "testing": "automated security testing and AI fuzzing techniques",
            "automation": "AI workflow automation bypass rate limits and robotic process automation",
            "memory": "vector database RAG techniques for cybersecurity data",
            "quality_control": "static code analysis for finding zero-day vulnerabilities",
            "other": "latest trends in artificial intelligence and cybersecurity 2024"
        }
        
        new_knowledge = {}
        
        for agent, topic in topics.items():
            print(f"\n[Manager] 🌐 Researching for {agent} agent...", flush=True)
            self.log_event("working", {"agent": "Research", "status": f"Searching for {agent}..."})
            
            raw_web = await asyncio.to_thread(WebResearcher.search, topic)
            
            prompt = f"""
            You are an Elite AI Trainer. Your job is to generate the top 3 highly technical rules for an AI agent of type '{agent}'.
            Web Context: {raw_web[:1500]}
            
            INSTRUCTIONS: If the context is empty or unhelpful, use your internal expert knowledge. Output ONLY 3 plain text rules.
            """
            
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.post(self.router_url, json={"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}]}, timeout=60.0)
                    rules = resp.json()['choices'][0]['message']['content'].strip()
                    
                    if "No actionable rules" in rules or len(rules) < 20:
                        rules = f"- Follow standard best practices for {agent}.\n- Ensure high quality and security."
                        
                    new_knowledge[agent] = rules
                    print(f"[Manager] ✅ Extracted rules for {agent}.", flush=True)
                    self.log_event("complete", {"agent": "Research", "status": f"Learned {agent}"})
            except Exception as e:
                print(f"[Manager] ❌ Failed to train {agent}: {e}", flush=True)
        
        with open(self.knowledge_base_path, "w", encoding="utf-8") as f:
            json.dump(new_knowledge, f, ensure_ascii=False, indent=4)
            
        print("\n[Manager] 🎓 Training Complete. Knowledge Base Updated!", flush=True)

    async def plan_and_dispatch(self, goal: str) -> list:
        if goal.strip().startswith("!train") or "train all agents" in goal.lower():
            await self.train_agents()
            self.log_event("complete", {"agent": self.name, "status": "Done"})
            return [Result(task_id="train", success=True, output="Agents upgraded.")]

        self.log_event("working", {"agent": self.name, "status": "Thinking & Planning..."})
        
        with open(self.knowledge_base_path, "r", encoding="utf-8") as f:
            memory = f.read()

        web_context = await asyncio.to_thread(WebResearcher.search, f"best approach to: {goal[:50]}")
        
        prompt = f"""
        You are the Master Manager. You are highly logical.
        Goal: "{goal}"
        Available agents: Research, Developer, Analyst, Security, Recon, Testing, Automation, Memory, QC, Other.
        
        CRITICAL RULES:
        1. If the user says "First X, then Y", you MUST output tasks in that exact order.
        2. Provide a VERY DETAILED description for each task.
        3. If the goal does not contain a valid URL (http:// or https://), DO NOT assign any tasks to the "Security" or "Recon" agents.
        
        Web context: {web_context[:500]}

        TASK: Break down the goal into a sequence of tasks. Output ONLY valid JSON.
        Format: {{"tasks": [{{"agent": "Developer", "description": "..."}}]}}
        """
        
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(self.router_url, json={"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": prompt}], "response_format": {"type": "json_object"}}, timeout=60.0)
                raw_plan = resp.json()['choices'][0]['message']['content']
                match = re.search(r'\{.*\}', raw_plan, re.DOTALL)
                planned_tasks = json.loads(match.group(0)).get("tasks", [])
        except Exception as e:
            print(f"[Manager] AI Planning failed: {e}")
            planned_tasks = [{"agent": "Developer", "description": goal}]

        results = []
        agent_map_names = {"manager": "Manager", "research": "Research", "developer": "Developer", "analyst": "Analyst", "security": "Security", "recon": "Recon", "testing": "Testing", "automation": "Automation", "memory": "Memory", "quality_control": "QC", "other": "Other"}
        agent_id_map = {"manager": "manager", "research": "research", "developer": "developer", "analyst": "analyst", "security": "security", "recon": "recon", "testing": "testing", "automation": "automation", "memory": "memory_agent", "qc": "quality_control", "other": "other"}

        for i, pt in enumerate(planned_tasks):
            agent_name = pt.get("agent", "Developer").lower()
            desc = pt.get("description", "")
            agent_id = agent_id_map.get(agent_name, "developer")
            agent_display_name = agent_map_names.get(agent_id, agent_name.capitalize())
            
            max_retries = 1
            for attempt in range(max_retries + 1):
                self.log_event("working", {"agent": agent_display_name, "status": "Working"})
                await asyncio.sleep(0.1)
                
                try:
                    agent = self._get_agent(agent_id)
                    task_obj = Task(id=f"task_{i}_{attempt}", description=desc, agent_id=agent_id, priority=3)
                    res = await agent.execute(task_obj)
                    
                    if res and res.success:
                        self.log_event("complete", {"agent": agent_display_name, "status": "Done"})
                        results.append(res)
                        break
                    else:
                        error_msg = res.output if res else "Unknown Error"
                        self.log_event("fail", {"agent": agent_display_name, "status": f"Failed"})
                        
                        if attempt < max_retries:
                            print(f"\n[Manager] 🔄 Task failed. Retrying {agent_display_name}...", flush=True)
                            desc = f"{desc}\n\n[PREVIOUS ATTEMPT FAILED WITH ERROR]:\n{error_msg}\nPlease FIX this error."
                except Exception as e:
                    traceback.print_exc()
                    self.log_event("fail", {"agent": agent_display_name, "status": "Failed"})
                    break
            
            await asyncio.sleep(0.5)

        self.log_event("working", {"agent": "QC", "status": "Working"})
        agent = self._get_agent("quality_control")
        await agent.execute(Task(id="qc_final", description="Final Quality Control", agent_id="quality_control", priority=2))
        self.log_event("complete", {"agent": "QC", "status": "Done"})

        return results

    def _get_agent(self, agent_id: str):
        if agent_id == "developer":
            from agents.developer_agent import DeveloperAgent
            return DeveloperAgent(config=self.config)
        elif agent_id == "research":
            from agents.research_agent import ResearchAgent
            return ResearchAgent(config=self.config)
        elif agent_id == "quality_control":
            from agents.quality_control_agent import QualityControlAgent
            return QualityControlAgent(config=self.config, memory=self.memory)
        elif agent_id == "security":
            from agents.security_agent import SecurityAgent
            return SecurityAgent(config=self.config)
        elif agent_id == "recon":
            from agents.recon_agent import ReconAgent
            return ReconAgent(config=self.config)
        return self
