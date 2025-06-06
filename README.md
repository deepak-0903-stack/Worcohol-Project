# Video Script Writer

Video Script Writer is a Streamlit-based AI application that creates an automated video scripts using Google Gemini (Generative AI). Users can generate engaging video scripts for YouTube, Shorts, LinkedIn, or Podcasts, by just entering the topic name.

---

## Features

### 1. Multi-Platform Script Generation
Generate video scripts tailored to specific platforms:
- *YouTube*
- *Instagram Reels / YouTube Shorts*
- *LinkedIn Videos*
- *Podcasts*

### 2. Multiple Output Styles
Choose how you want your script delivered:
- *Full Script*: Complete narrative with directions and flow
- *Storyboard*: Visual layout with scene-by-scene breakdown
- *Podcast Outline*: Speaker turns and segments formatted for audio
- *Summary*: Concise 3–6 sentence wrap-up of the topic

### 3. Customizable Tone and Viewer Type
- Select the *tone/vibe*: Casual, Professional, Funny, Creative, Informative
- Choose the *viewer type*: Students, Professionals, Kids, Beginners, Experts

### 4. Language Support
Generate content in multiple languages:
- English
- Hindi
- Telugu
- Spanish
- French
- German

### 5. Duration Control
Specify your video’s duration in seconds — the script adapts accordingly.

### 6. Neutral, Reusable Output
- *No specific names* of people, companies, or brands are used.
- Clean, reusable scripts for any purpose.

### 7. Script History & Export
- View previously generated scripts within the app
- Download scripts as .txt files

### 8. Streamlit-Powered UI
- Simple, interactive frontend
- Live script generation using Google Gemini API
-

---

### Project Group Details

#### 1.Murali krishna Kancham (Team Leader)
#### 2.Deepak Gumte (Team Member)
#### 3.Rushi Akkunuri (Team Member)

---
## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/deepak-0903-stack/Worcohol-Project.git
cd Worcohol-Project
```
### 2. Create and Activate Virtual Environment

#### For Windows:

```bash
py -m venv .venv

.\.venv\Scripts\activate
```
#### For macOS/Linux:

```bash
python3 -m venv venv

source venv/bin/activate
```
### 3.Install Dependencies

```bash
pip install -r requirements.txt
```
### 4.Set Up Environment variables

Create a .env file in a root directory :

```bash
GOOGLE_API_KEY="your_google_api_key"
```
### 5.Run the App

```bash
streamlit run app.py
```
