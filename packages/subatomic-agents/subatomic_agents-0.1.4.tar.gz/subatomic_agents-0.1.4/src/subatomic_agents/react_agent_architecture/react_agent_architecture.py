from abc import ABC, abstractmethod
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# 1. Abstract Builder
class AgentBuilder(ABC):
    @abstractmethod
    def build_prompt(self) -> str:
        pass

    @abstractmethod
    def build_tools(self) -> List[Any]:
        pass

    def build_llm(self):
        return ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    def build_agent(self) -> Any:
        prompt = self.build_prompt()
        tools = self.build_tools()
        llm = self.build_llm()
        return create_react_agent(model=llm, tools=tools, prompt=prompt)


# 2. Strategy Interface for Toolsets
class ToolsetStrategy(ABC):
    @abstractmethod
    def get_tools(self):
        """Return a list of tools."""
        pass


# 3. Concrete Strategy: Sales Proposal Toolset
class SalesProposalToolset(ToolsetStrategy):
    def __init__(self, tools):
        self._tools = tools

    def get_tools(self):
        return self._tools

# 4. Concrete Agent Builder
class SalesProposalAgentBuilder(AgentBuilder):
    def __init__(self, toolset_strategy: ToolsetStrategy):
        self.toolset_strategy = toolset_strategy

    def build_prompt(self) -> str:
        return """
        You are an Expert Agent on creating Sales Proposals.
        You can use sales_proposal_tool for creating a sales proposal effectively.
        """

    def build_tools(self):
        return self.toolset_strategy.get_tools()


# 5. Orchestrator
class AgentOrchestrator:
    def __init__(self, builder: AgentBuilder):
        self.agent = builder.build_agent()

    def run(self, query: str) -> str:
        user_input = {
            "messages": [{"role": "user", "content": query}]
        }
        response = self.agent.invoke(user_input)
        return response["messages"][-1].content
