import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Google API key not found.")
client = genai.Client(api_key=GOOGLE_API_KEY)

# Initialize session history
if "previous_scripts" not in st.session_state:
    st.session_state.previous_scripts = []

# Sidebar
with st.sidebar:
    st.header("Settings & History")

    with st.expander("User Guide"):
        st.markdown("""
        1. Enter a topic (e.g., "Artificial Intelligence")
        2. Select video format: YouTube, Shorts, LinkedIn, or Podcast
        3. Select vibe: Casual, Professional, etc.
        4. Select Viewers Type: General, student, Experts, Kids, etc
        5. Select Output Style: Full Script, Bullet Point, Summary, etc 
        6. Select Duration ,Select in Seconds
        7. Select language: English, Spanish, Hindi, etc                                    
        8. Click "Generate Script"
        9. Your scripts are saved below in the Previous Scripts section
        """)

    st.subheader("Previous Scripts")
    if st.session_state.previous_scripts:
        options = [
            f"{i+1}. {entry['topic']} ({entry['format']}, {entry['vibe']})"
            for i, entry in enumerate(st.session_state.previous_scripts)
        ]
        selected_index = st.selectbox("Select version to view:", options)
        selected_script = st.session_state.previous_scripts[int(selected_index.split('.')[0]) - 1]
        st.text_area("Previous Script", selected_script['script'], height=400, key="prev_script_view")
    else:
        st.write("No history found.")

# Title
st.title("Video Script Writer :clapper:")

# User Inputs
topic = st.text_input("Enter the Topic :")
format = st.selectbox("Select video format:", ["YouTube", "Instagram Reel/Youtube Shorts", "Linkedin Video", "Podcast"])
vibe = st.selectbox("Select vibe of the Video:", ["Casual", "Professional", "Funny", "Creative", "Informative"])
viewer_type = st.selectbox("Who is the viewer of this Scipt/Video ", ["General", "Students", "Beginners", "Experts", "Kids"])
output_style = st.selectbox("Select Output Style", ["Full Script", "Summary", "Storyboard", "podcast Outline"])
duration = st.slider("Select video duration (in seconds)", min_value=15, max_value=780, step=15, value=60)
language = st.selectbox("Select Language", ["English", "Hindi", "Telugu", "Spanish", "French", "German"])
generate_button = st.button("Generate Script")

# Prompt Builder
def get_output_style_guidelines(output_style, format):
    if output_style == "Full Script":
        if format == "Podcast":
            return """
Write a complete podcast script using speaker labels.

- Use [HOST:] and [GUEST:] to alternate dialogues.
- Donot include any specific names of persons, channels, and organization
- Include an engaging intro, multiple discussion segments, and a closing.
- Maintain a conversational flow suited for audio-only format.
- Avoid any visual references or screen directions.
- Keep it engaging and informative, strictly in the selected tone.
"""
        else:
            return """
Write a complete word-for-word script suitable for the selected format.

- Use markers like [HOST:], [TEXT ON SCREEN:],[TRANSITION:], [CUT TO:], etc.
- No timestamps or scene numbers.
- Follow a logical structure
- Make the script clean, structured, and ready to use.
"""
    elif output_style == "Storyboard":
        return """
Structure the content as a storyboard, broken down into scenes.

Each scene should include:
- Scene #: Number each sequentially.
- [VISUAL]: Describe the visual elements.
- [VOICEOVER]: Narration or speech.
- [TEXT ON SCREEN]: Any written text appearing.
- Ensure clarity and visual planning throughout.
"""
    elif output_style == "Podcast Outline":
        return """
Create a high-level outline for a podcast episode.

Include:
- Episode Title
- Estimated Duration
- Segment structure like: [HOST INTRO], [HOOK], [SEGMENT 1], [GUEST INPUT], [SEGMENT 2], [RECAP], [CTA], [OUTRO]
- Use bullet points to briefly describe content for each section.
- Alternate speaker tags where possible.
"""
    elif output_style == "Summary":
        return """
Write a lenghty, informative, 6-8 paragraph summary.

- Explain the topic clearly and concisely.
- Include the main message and importance.
- Maintain alignment with tone, viewer type, and language.
- No bullet points or formatting tags. Just clean, structured text.
"""
    else:
        return "Follow professional, concise formatting for the selected style."


def build_prompt(topic, format, vibe, viewer_type, output_style, language, duration):
    minutes = duration // 60
    seconds = duration % 60
    formatted_duration = f"{minutes} minutes" if seconds == 0 else f"{minutes} minutes {seconds} seconds"

    style_guidelines = get_output_style_guidelines(output_style, format)

    # Language-specific instructions
    if language.lower() == "hindi":
        language_instruction = "Hindi — strictly use Hindi script"
        language_note = """
### Language Note:
Ensure the script is written entirely in Hindi script . Do NOT use transliterated Roman Hindi like 'Namaste dosto'.
"""
    elif language.lower() == "telugu":
        language_instruction = "Telugu — strictly use Telugu script "
        language_note = """
### Language Note:
Ensure the script is written entirely in Telugu script. Do NOT use transliterated Roman Telugu like 'Meeru Ela Unnaru'.
"""
    else:
        language_instruction = language
        language_note = ""

    return f"""
You are an expert video content writer and script generator.

Generate a *{output_style}* for a *{format}* video on the topic: *"{topic}"*

Strict Guidelines to Follow:
- *Tone/Vibe*: {vibe}
- *Viewer Type*: {viewer_type}
- *Language*: {language_instruction}
- *Target Duration*: {formatted_duration}
- *Do NOT include any specific names of people, companies, or brands* in the entire script.

### Output Formatting Instructions:
{style_guidelines}
{language_note}

Only return the content as per the structure — do not include commentary, explanation, or markdown formatting.
"""


# Generate Script
if generate_button:
    if not topic:
        st.warning("Please enter a valid topic.")
    else:
        with st.spinner("Generating your script..."):
            try:
                prompt = build_prompt(topic, format, vibe, viewer_type, output_style, language, duration)

                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[{"role": "user", "parts": [{"text": prompt}]}]
                )

                script = response.candidates[0].content.parts[0].text

                st.session_state.previous_scripts.append({
                    "topic": topic,
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