import streamlit as st
from openai import OpenAI
import time

# Page configuration
st.set_page_config(
    page_title="Inner Vision - Personal Art Generator",
    page_icon="🎭",
    layout="centered"
)

# Custom CSS for a more calming, therapeutic feel
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1a1c2c 0%, #2a2d4f 100%);
        color: #e0e0e0;
    }
    .element-container {
        background: rgba(255, 255, 255, 0.05);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    .stButton > button {
        background: linear-gradient(45deg, #4a90e2, #67b26f);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 10px;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'stage' not in st.session_state:
    st.session_state.stage = 'questions'

def get_emotional_profile():
    """Gather emotional and psychological information"""
    st.markdown("### 🎭 Let's understand your inner world")
    
    # Core emotional questions
    st.markdown("#### Choose what resonates most with you right now:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.responses['emotional_state'] = st.selectbox(
            "When you think about your life right now, you feel most:",
            ["Seeking Peace", "Yearning for Growth", "Need for Connection", "Desire for Expression", 
             "Looking for Clarity", "Wanting Adventure"]
        )
        
        st.session_state.responses['color_resonance'] = st.selectbox(
            "Which color speaks to your soul today?",
            ["Deep Ocean Blue - Depth & Calm", "Forest Green - Growth & Healing",
             "Soft Gold - Hope & Warmth", "Purple - Wisdom & Mystery",
             "Gentle Pink - Love & Compassion"]
        )

    with col2:
        st.session_state.responses['symbol'] = st.selectbox(
            "Which symbol feels most meaningful to you?",
            ["Tree - Growth & Roots", "Mountain - Strength & Goals",
             "Ocean - Emotion & Depth", "Stars - Dreams & Guidance",
             "Bridge - Connection & Journey"]
        )
        
        st.session_state.responses['environment'] = st.selectbox(
            "Where does your mind find the most peace?",
            ["Ancient Forest", "Mountain Summit", "Peaceful Beach",
             "Starlit Night Sky", "Flowing River"]
        )

    # Deeper insight
    st.markdown("#### Share a little more:")
    st.session_state.responses['challenge'] = st.text_area(
        "What's one challenge you're working through? (optional)",
        help="This helps create more meaningful imagery"
    )

    if st.button("✨ Create My Personal Vision", use_container_width=True):
        st.session_state.stage = 'generate'
        st.rerun()

def create_prompt(responses):
    """Create a therapeutic, personalized prompt based on user responses"""
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    system_message = """You are an expert at crafting therapeutic, emotionally resonant image prompts. 
    Create prompts that address the user's emotional state while promoting healing and growth. 
    Focus on beautiful, uplifting imagery that speaks to their inner journey."""
    
    user_message = f"""
    Create a deeply personal, therapeutic image prompt based on these insights:
    - Emotional State: {responses['emotional_state']}
    - Color Resonance: {responses['color_resonance']}
    - Meaningful Symbol: {responses['symbol']}
    - Peaceful Environment: {responses['environment']}
    - Personal Challenge: {responses['challenge'] if responses['challenge'] else 'Not specified'}

    Guidelines:
    - Create a scene that metaphorically addresses their emotional state
    - Use their chosen color as a key element
    - Incorporate their meaningful symbol in a subtle way
    - Set it in their peaceful environment
    - If they shared a challenge, include subtle elements of hope and growth
    - Make it cinematic and dreamy, yet deeply personal
    - Focus on healing and positive transformation
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7
    )
    
    return response.choices[0].message.content

def generate_image(prompt):
    """Generate image using DALL-E"""
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="hd",
        style="vivid",
        n=1
    )
    
    return response.data[0].url

def show_generation():
    """Show the image generation process and result"""
    st.markdown("### 🎨 Creating Your Personal Vision")
    
    with st.spinner("Crafting your unique image..."):
        # Create the prompt
        prompt = create_prompt(st.session_state.responses)
        
        # Show the interpretation
        with st.expander("💭 Our Understanding"):
            st.write(prompt)
        
        # Generate and display the image
        image_url = generate_image(prompt)
        
        st.image(image_url, caption="Your Personal Vision", use_column_width=True)
        
        # Reflection prompt
        st.markdown("### 🤍 Moment of Reflection")
        st.markdown("""
        Take a moment to sit with this image. What emotions does it bring up for you?
        What aspects of it resonate most deeply with your current journey?
        """)
        
        if st.button("🔄 Create Another Vision", use_container_width=True):
            st.session_state.stage = 'questions'
            st.rerun()

def main():
    st.title("🎭 Inner Vision")
    st.markdown("### Transform your feelings into meaningful art")
    
    if st.session_state.stage == 'questions':
        get_emotional_profile()
    else:
        show_generation()

if __name__ == "__main__":
    main()
