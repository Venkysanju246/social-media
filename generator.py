# generator.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
from utils import search_web

# Load .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Context Agent
def build_brand_context(brand_voice):
    search_query = f"{brand_voice} company profile and marketing strategies"
    search_results = search_web(search_query, num_results=5)
    summary = "\n".join(search_results)

    prompt = f"""
Act as a branding expert.
Summarize the business profile based on this info:
{summary}

Focus on:
- Industry
- Target audience
- Competitors
- Strengths
- Weaknesses

Format in bullet points.
"""
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    return response.text.strip()

# Content Generator Agent
def generate_social_post(brand_context, instructions, platform):
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
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    return response.text.strip()
