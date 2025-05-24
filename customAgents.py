import os
from agno.agent import Agent, RunResponse
import google.generativeai as genai
from utils import search_web

# Setup Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash-latest')

class BrandContextAgent(Agent):
    name = "Brand Context Builder"
    description = "Fetches brand-related information and generates a summary"

    def run(self, input: str) -> RunResponse:
        search_query = f"{input} company profile and marketing strategies"
        results = search_web(search_query, num_results=5)
        search_text = "\n".join(results)

        prompt = f"""
Act as a brand analyst. Given the following search results:
{search_text}

Summarize the business context in bullet points covering:
- Industry
- Target audience
- Competitors
- Strengths
- Weaknesses
"""
        try:
            response = model.generate_content(prompt)
            if response and response.text:
                content = response.text.strip()
            else:
                content = "⚠️ No content generated. Please try again."
        except Exception as e:
            content = f"⚠️ Error generating content: {e}"

        return RunResponse(content)

class ContentGeneratorAgent(Agent):
    name = "Social Media Content Generator"
    description = "Generates a social media post based on brand context and instructions"

    def run(self, input: dict) -> RunResponse:
        brand_context = input.get("brand_context")
        instructions = input.get("instructions")
        platform = input.get("platform")

        prompt = f"""
Write a **single** social media post for **{platform}** based on this business context:
{brand_context}

Instructions: {instructions}

Ensure the post:
- Is engaging and relevant
- Follows best practices for {platform}
- Includes appropriate hashtags
- No explanations, just the post content
"""
        try:
            response = model.generate_content(prompt)
            if response and response.text:
                post = response.text.strip()
            else:
                post = "⚠️ No content generated. Please try again."
        except Exception as e:
            post = f"⚠️ Error generating post: {e}"

        return RunResponse(post)
