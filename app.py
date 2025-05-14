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
st.title("Video Script Writer :clapper:")

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
            "tone": "Informative and engaging",
            "style": "Use engaging narrative with a mix of on-screen actions, host dialogue, and creative transitions. Include clear formatting like [INTRO:], [CUT TO:], [Host:], etc."
        },
        "Instagram Reel/Youtube Shorts": {
            "length": "30–60 seconds",
            "tone": "Fast-paced, fun, Gen-Z-friendly",
            "style": "Use short, punchy lines with visual cues like [HOOK:], [CUT TO:], [TEXT ON SCREEN:], [Host:], etc. Keep language upbeat and visuals dynamic"
        },
        "Linkedin Video": {
            "length": "1–2 minutes",
            "tone": "Professional and insightful",
            "style": "Use [INTRO:], [Host:], [CUT TO DATA:], [OUTRO:] formatting. Keep it tight, focused, and data-driven with clear takeaways."
        },
        "Podcast": {
            "length": "5–15 minutes",
            "tone": "Conversational and informative",
            "style": "Use paragraph format with speaker turns marked as [Host:], [Guest:], etc. No visual directions. Focus on smooth natural flow."
        }
    }

    guide = format_guidelines.get(format, format_guidelines["YouTube"])
    return f"""
You're a professional and creative video script writer.

Write a video script for the topic: "{topic}", using the following reference content:\n\n{info}\n\n

### Script Constraints:
- Platform: {format}
- Length: {guide['length']}
- Tone: {guide['tone']}
- Style Guidelines: {guide['style']}
- Vibe: {vibe}

### Output Format Instructions:
- Write the video script which is best suitable for {format} , u can change the format of the output based on the {format}
- Format the script using stage directions and camera cues like: [INTRO:], [TRANSITION:], [CUT TO:], [Host:], etc.
- Begin with an attention-grabbing intro with music or visual elements
- Write natural host dialogue with personality and energy
- Use paragraph-style storytelling with embedded visual/audio suggestions
- Use creative transitions and descriptions of visuals or sound effects
- Conclude with a clear, engaging outro and CTA suited for {format}
- Do not use scene numbers or timestamps
- Keep the script flowing like a real video shoot, not a scene-based breakdown

Return only the formatted video script in the described style. Do not add commentary or explanations.
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

                st.subheader(f"Generated Video Script for: {topic}")
                st.text_area("Video Script", script, height=1000, key="script_output")
                st.download_button("Download Script", script, file_name=f"{topic}_scene_script.txt")
                st.code(script, language="markdown")

            except Exception as e:
                st.error(f"An error occurred: {e}")