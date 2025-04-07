"""
Documentation Agent

An agent that can answer questions about LightWave documentation.
"""
from typing import List, Optional
from pydantic import Field

from lightwave_cli.agents.base import LightWaveAgent, AgentResponse


class DocsAgent(LightWaveAgent):
    """Agent for answering questions about documentation."""
    
    class DocsAgentResponse(AgentResponse):
        """Response model for the docs agent."""
        sources: Optional[List[str]] = Field(
            None, 
            description="Sources from documentation used to answer the question"
        )
    
    def run(self, prompt: str, **kwargs) -> DocsAgentResponse:
        """
        Process the user's question about documentation.
        
        Args:
            prompt: The user's question about documentation
            **kwargs: Additional parameters to override agent configuration
            
        Returns:
            DocsAgentResponse with the answer
        """
        # In a real implementation, we would use a vector store of documentation
        # for now, we'll use a simple AI call
        
        system_prompt = """
        You are a helpful documentation assistant for the LightWave ecosystem.
        Answer questions about the LightWave documentation, tools, and codebase.
        If you don't know the answer, say so clearly rather than making something up.
        
        The LightWave ecosystem consists of these main components:
        1. lightwave-api-gateway - API gateway for all LightWave services
        2. lightwave-cli - Command-line tools for LightWave development
        3. lightwave-ai-services - AI services and agents for the ecosystem
        4. lightwave-design-system - Shared design components and standards
        5. lightwave-eco-system-docs - Documentation for all LightWave projects
        6. lightwave-shared-core - Shared libraries and utilities
        7. lightwave-infrastructure - Infrastructure and deployment tools
        8. lightwave-monitoring - Monitoring and observability tools
        
        When answering, cite the specific documentation source if you know it.
        """
        
        # Override configuration if needed
        config_overrides = {}
        for key, value in kwargs.items():
            config_overrides[key] = value
            
        try:
            response = self.generate(
                system=system_prompt,
                user=prompt,
                **config_overrides
            )
            
            # Simple logic to extract possible sources
            sources = []
            for component in [
                "lightwave-api-gateway", "lightwave-cli", "lightwave-ai-services",
                "lightwave-design-system", "lightwave-eco-system-docs", 
                "lightwave-shared-core", "lightwave-infrastructure", "lightwave-monitoring"
            ]:
                if component.lower() in response.lower():
                    sources.append(component)
            
            return self.DocsAgentResponse(
                success=True,
                message="Successfully retrieved information",
                data={"answer": response},
                sources=sources if sources else None
            )
            
        except Exception as e:
            return self.DocsAgentResponse(
                success=False,
                message="Failed to process documentation question",
                errors=[str(e)]
            )


# Create a singleton instance of the agent
agent = DocsAgent() 