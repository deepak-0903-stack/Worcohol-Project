# Video Script Writer

*Video Script Writer* is a Streamlit-based AI application that creates scene-based video scripts using Google Gemini (Generative AI). Users can generate engaging video scripts for YouTube, Shorts, LinkedIn, or Podcasts, using content from YouTube transcripts or Wikipedia.

---

## Features

- *AI-Powered Script Generation* using Google Gemini
- *Supports Various Formats*: YouTube, Instagram Reels, LinkedIn, Podcast
- *Scene-Based Output*: Includes intro, labeled scenes, and outro
- *Vibe Options*: Casual, Professional, Funny, Creative, Informative
- *Content Source Options*: YouTube transcript or Wikipedia
- *Previous Script History* in-app
- *Script Download Option* as .txt

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
