import os
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import google.generativeai as genai
import wikipedia

# Load API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Google API key not found in .env file.")
genai.configure(api_key=GOOGLE_API_KEY)

# Theme Styling
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to right, #1f1c2c, #928dab);
        background-attachment: fixed;
        background-size: cover;
        color: white;
    }

    /* Input fields */
    .stTextArea, .stSelectbox, .stTextInput {
        background-color: #2c2f48 !important;
        color: white !important;
        border-radius: 6px;
    }

    /* Fix label visibility */
    label, .css-1cpxqw2, .css-qrbaxs, .css-81oif8 {
        color: white !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #6a11cb;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session history
if "previous_scripts" not in st.session_state:
    st.session_state.previous_scripts = []

# Sidebar with history and guide
with st.sidebar:
    st.header("Settings & History")

    with st.expander("User Guide"):
        st.markdown("""
        1. Enter a topic (e.g., "Artificial Intelligence")
        2. Choose YouTube or Wikipedia as the source
        3. Select video format: YouTube, Shorts, LinkedIn, or Podcast
        4. Select vibe: Casual, Professional, etc.
        5. Click "Generate Script" and boom your full structurd video script is ready
        6. If you want to access/see your previous generated scripts ,Then you can access it from previous scripts section ,which is present below user guide, as you go on generating the scripts it will get saved in "previous scripts"              
        """)

    st.subheader("Previous Scripts")
    if st.session_state.previous_scripts:
        options = [
            f"{i+1}. {entry['topic']} ({entry['source']}, {entry['format']}, {entry['vibe']})"
            for i, entry in enumerate(st.session_state.previous_scripts)
        ]
        selected_index = st.selectbox("Select version to view:", options)
        selected_script = st.session_state.previous_scripts[int(selected_index.split('.')[0]) - 1]
        st.text_area("Previous Script", selected_script['script'], height=400, key="prev_script_view")
    else:
        st.write("No history found.")

# App main title
st.title("GenAI Video Script Generator")

# User Inputs
topic = st.text_input("Enter the Topic :")
source = st.selectbox("Select content source:", ["YouTube", "Wikipedia"])
format = st.selectbox("Select video format:", ["YouTube", "Instagram Reel/Youtube Shorts", "Linkedin Video", "Podcast Video"])
vibe = st.selectbox("Select vibe of the Video:", ["Casual", "Professional", "Funny", "Creative", "Informative"])
generate_button = st.button("Generate Script")

# Prompt Builder
def build_prompt(topic, info, format, vibe):
    format_guidelines = {
        "YouTube": {
            "length": "4–10 minutes",
            "max_scenes": 9,
            "tone": "Informative and engaging",
            "style": "Start with a compelling intro, include 5–9 clearly labeled SCENES with timestamps, visual storytelling, and end with a strong outro"
        },
        "Instagram Reel/Youtube Shorts": {
            "length": "30–60 seconds",
            "max_scenes": 3,
            "tone": "Fast-paced, fun, Gen-Z-friendly",
            "style": "Start with a hook in the first 3 seconds, keep it visual and punchy, use 2–3 quick SCENES (each scene should be maximum 10–15 seconds only), minimal narration, emojis and Gen-Z language encouraged"
        },
        "Linkedin Video": {
            "length": "1–2 minutes",
            "max_scenes": 3,
            "tone": "Professional and insightful",
            "style": "Short intro (0–10 seconds), focus on 2–3 value-driven SCENES (each scene should be maximum 15–20 seconds only), data and industry language encouraged, end with a reflective outro"
        },
        "Podcast": {
            "length": "5–15 minutes",
            "max_scenes": 5,
            "tone": "Conversational and informative",
            "style": "Natural dialogue style, start with a warm welcome, 3–5 topic-based sections, use real-world examples, end with a reflective outro or teaser"
        }
    }

    guide = format_guidelines.get(format, format_guidelines["YouTube"])
    return f"""
You're a creative, informative and professional video script writer.

Write a scene-based video script based on this topic: "{topic}".  
Use this factual content as reference: \n\n{info}\n\n

### Script Constraints:
- Platform: {format}
- Estimated Duration: {guide['length']} (must stay within this range)
- Max Scenes: {guide['max_scenes']} scenes total (including intro & outro)
- Tone: {guide['tone']}
- Style: {guide['style']}
- Vibe: {vibe}

### Instructions:
- Follow strict video length, tone, for their respective video format 
- Start with an attractive intro and greeting before any scene begins (no creator name). Briefly tease what the video is about
- Include clearly labeled SCENES or SECTIONS
- Use rich visual descriptions, real-world analogies, and relatable narration
- Keep the tone {vibe.lower()}, simple, and suited for {format}
- End with a natural outro that encourages viewers to engage

Only return the formatted scene-based script. Don't explain your choices.
"""

# Content Fetchers
def get_youtube_transcript(url):
    try:
        video_id = parse_qs(urlparse(url).query)["v"][0]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry["text"] for entry in transcript])[:3000]
    except Exception as e:
        return f"(Couldn't fetch YouTube transcript: {e})"

def get_wikipedia_summary(topic):
    try:
        wikipedia.set_lang("en")
        return wikipedia.summary(topic, sentences=10)
    except Exception as e:
        return f"(Couldn't fetch Wikipedia summary: {e})"

# Generate Script
if generate_button:
    if not topic:
        st.warning("Please enter a valid input.")
    else:
        with st.spinner("Generating your script..."):
            try:
                info = get_youtube_transcript(topic) if source == "YouTube" else get_wikipedia_summary(topic)
                prompt = build_prompt(topic, info, format, vibe)

                model = genai.GenerativeModel(
                    model_name="models/gemini-1.5-flash-latest",
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.8,
                        max_output_tokens=1024,
                        top_p=0.95,
                        top_k=40
                    )
                )

                response = model.generate_content(prompt)
                script = response.text

                st.session_state.previous_scripts.append({
                    "topic": topic,
                    "source": source,
                    "format": format,
                    "vibe": vibe,
                    "script": script
                })

                st.subheader("Generated Video Script")
                st.text_area("Scene-Based Script", script, height=1000, key="script_output")
                st.download_button("Download Script", script, file_name=f"{topic}_scene_script.txt")
                st.code(script, language="markdown")

            except Exception as e:
                st.error(f"An error occurred: {e}")