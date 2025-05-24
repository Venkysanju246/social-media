import streamlit as st
from workflows import SocialMediaWorkflow
from customAgents import BrandContextAgent

st.set_page_config(page_title="Social Media Content Generator", layout="centered")
st.title("🎯 Social Media Content Generator (Agno Agents)")

# Session State Setup
if 'brand_context' not in st.session_state:
    st.session_state['brand_context'] = None

st.subheader("Step 1: Brand Voice")
brand_voice = st.text_area("Brand Voice", placeholder="Describe your brand (e.g., social media marketing agency)...")

if st.button("Build Brand Context"):
    with st.spinner("Generating brand context..."):
        context_response = BrandContextAgent().run(brand_voice)
        brand_context_text = context_response.content.strip() if context_response.content else "No content generated."
        st.session_state['brand_context'] = brand_context_text
        st.success("Brand Context Generated!")
        st.markdown(brand_context_text)

# Step 2: Content Generation
if st.session_state['brand_context']:
    st.subheader("Step 2: Refine Context, Add Instructions & Generate Post")

    final_context = st.text_area("Review/Edit Brand Context", st.session_state['brand_context'])
    instructions = st.text_area("Content Instructions", placeholder="What should the post talk about?")
    platform = st.selectbox("Select Platform", ["Twitter", "LinkedIn", "Instagram", "Facebook", "Other"])

    if st.button("Generate Social Media Post"):
        with st.spinner("Generating post..."):
            workflow = SocialMediaWorkflow()
            input_data = {
                "brand_context": final_context,
                "instructions": instructions,
                "platform": platform
            }
            post = workflow.run(input=input_data)  # Only single response now
            st.success("Generated Post:")
            st.markdown(post.content if hasattr(post, 'content') else str(post))

