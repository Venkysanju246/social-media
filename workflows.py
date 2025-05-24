# workflows.py
from agno.workflow import Workflow
from agno.agent import RunResponse
from customAgents import ContentGeneratorAgent

class SocialMediaWorkflow(Workflow):
    def run(self, input: dict):
        post_response = ContentGeneratorAgent().run({
            "brand_context": input["brand_context"],
            "instructions": input["instructions"],
            "platform": input["platform"]
        })
        return RunResponse(post_response.content)
