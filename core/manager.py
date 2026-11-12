from agents.base import BaseAgent, Task, Result
import traceback
import re
import asyncio

class ManagerAgent(BaseAgent):
    name = "Manager"
    display_name = "Manager"

    async def execute(self, task: Task) -> Result:
        return Result(task_id=task.id, success=True)

    async def plan_and_dispatch(self, goal: str) -> list:
        tasks = self.goal_to_tasks(goal)
        results = []

        agent_map = {
            "manager": "Manager", 
            "research": "Research", 
            "developer": "Developer",
            "analyst": "Analyst", 
            "security": "Security",
            "recon": "Recon", # 👈 ایجنت جدید
            "testing": "Testing",
            "automation": "Automation", 
            "memory_agent": "Memory", 
            "quality_control": "QC", 
            "other": "Other"
        }

        for t in tasks:
            agent_name = agent_map.get(t.agent_id, t.agent_id.capitalize())
            
            self.log_event("working", {"agent": agent_name, "status": "Working"})
            await asyncio.sleep(0.1)
            
            try:
                agent = self._get_agent(t.agent_id)
                res = await agent.execute(t)
                if res and res.success:
                    self.log_event("complete", {"agent": agent_name, "status": "Done"})
                    results.append(res)
                else:
                    self.log_event("fail", {"agent": agent_name, "status": "Failed"})
            except Exception as e:
                traceback.print_exc()
                self.log_event("fail", {"agent": agent_name, "status": "Failed"})
            
            await asyncio.sleep(0.5)
            
        return results

    def goal_to_tasks(self, goal: str) -> list[Task]:
        tasks = []
        lines = re.split(r'[.\n]|\bthen\b', goal)
        lines = [l.strip() for l in lines if l.strip()]
        counter = 0

        for line in lines:
            line_lower = line.lower()
            
            # اولویت‌بندی جدید با اضافه شدن Recon
            if "security" in line_lower or "hack" in line_lower or "scan" in line_lower: 
                agent_id = "security"
            elif "recon" in line_lower or "subdomain" in line_lower or "fuzz" in line_lower or "directory" in line_lower:
                agent_id = "recon"
            elif "research" in line_lower: 
                agent_id = "research"
            elif "test" in line_lower: 
                agent_id = "testing"
            elif "analyst" in line_lower or "analyze" in line_lower: 
                agent_id = "analyst"
            elif "automation" in line_lower or "automate" in line_lower: 
                agent_id = "automation"
            elif "memory" in line_lower: 
                agent_id = "memory_agent"
            elif "quality" in line_lower: 
                agent_id = "quality_control"
            elif "other" in line_lower: 
                agent_id = "other"
            else: 
                agent_id = "developer"

            tasks.append(Task(id=f"task_{counter}", description=line, agent_id=agent_id, priority=3))
            counter += 1

        tasks.insert(0, Task(id="setup", description="Verify environment", agent_id="manager", priority=1))
        tasks.append(Task(id="qc", description="Final Quality Control", agent_id="quality_control", priority=2))
        return tasks

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
        elif agent_id == "recon": # 👈 اتصال به ایجنت جدید
            from agents.recon_agent import ReconAgent
            return ReconAgent(config=self.config)
        return self
