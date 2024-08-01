import os
import streamlit as st
import google.generativeai as genai
from datetime import datetime, timedelta

# Assuming you've set your API key as an environment variable
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

def generate_campaign_plan(business_info, campaign_goal, target_audience, duration, budget):
    prompt = f"""
    Create a marketing campaign plan for the following business:
    
    Business Information: {business_info}
    Campaign Goal: {campaign_goal}
    Target Audience: {target_audience}
    Campaign Duration: {duration} days
    Budget: ${budget}
    
    Please provide a detailed campaign plan including:
    1. Campaign Strategy
    2. Key Messages
    3. Channel Selection
    4. Timeline of Activities
    5. Budget Allocation
    6. Success Metrics
    
    Format the output in markdown for easy reading.
    """
    
    response = model.generate_content(prompt)
    return response.text

def generate_campaign_messages(business_info, campaign_goal, target_audience, tone, channels):
    prompt = f"""
    Generate marketing messages for the following campaign:
    
    Business Information: {business_info}
    Campaign Goal: {campaign_goal}
    Target Audience: {target_audience}
    Tone of Voice: {tone}
    Marketing Channels: {', '.join(channels)}
    
    Please provide:
    1. A catchy slogan for the campaign
    2. Three short social media posts (max 280 characters each)
    3. One longer form email content (200-300 words)
    4. Two SMS messages (max 160 characters each)
    
    Format the output in markdown for easy reading.
    """
    
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.title("Hyperspace Campaign Generator")

st.header("Business Information")
business_name = st.text_input("Business Name")
business_type = st.text_input("Business Type")
business_location = st.text_input("Business Location")

st.header("Campaign Details")
campaign_goal = st.text_input("Campaign Goal")
target_audience = st.text_area("Target Audience Description")
campaign_duration = st.number_input("Campaign Duration (in days)", min_value=1, value=30)
campaign_budget = st.number_input("Campaign Budget ($)", min_value=0, value=1000)

if st.button("Generate Campaign Plan"):
    business_info = f"{business_name}, a {business_type} based in {business_location}"
    campaign_plan = generate_campaign_plan(business_info, campaign_goal, target_audience, campaign_duration, campaign_budget)
    st.markdown(campaign_plan)

# Optional: Save generated content
if st.button("Save Campaign"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"campaign_plan_{timestamp}.md"
    with open(filename, "w") as f:
        f.write(f"# Campaign Plan for {business_name}\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## Business Information\n")
        f.write(f"Business Name: {business_name}\n")
        f.write(f"Business Type: {business_type}\n")
        f.write(f"Location: {business_location}\n\n")
        f.write("## Campaign Details\n")
        f.write(f"Goal: {campaign_goal}\n")
        f.write(f"Target Audience: {target_audience}\n")
        f.write(f"Duration: {campaign_duration} days\n")
        f.write(f"Budget: ${campaign_budget}\n\n")
        f.write("## Generated Campaign Plan\n")
        f.write(campaign_plan)
        f.write("\n\n## Generated Campaign Messages\n")
        f.write(campaign_messages)
    st.success(f"Campaign saved to {filename}")
