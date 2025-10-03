import streamlit as st
import requests
import os
import json
from datetime import datetime, timezone

# ---------------------- CONFIG ----------------------
# Ollama API endpoint (local)
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma:2b"  # change this to the model you downloaded with Ollama

# ---------------------- PROMPT TEMPLATES ----------------------
SYSTEM_PROMPT = (
    "You are an expert fiction writer specialized in anime/manhwa-style storytelling. "
    "Write immersive, emotive, and twist-filled stories that feel like a human author. "
    "Follow user preferences for genre, tone, length, and twist settings. "
    "Avoid graphic sexual content and illegal instructions."
)

PROMPT_TEMPLATE = (
    "Write a {length_desc} {genres} story in the style of anime/manhwa with a {tone} tone. "
    "Main characters: {characters}. Setting: {setting}. "
    "Plot guidelines: {plot_guidelines} \n\n"
    "Make the story highly engaging so readers are glued to it — use vivid sensory details, strong beats, "
    "cliffhanger micro-scene endings between sections, and at least {twist_count} unexpected but coherent plot twist(es). "
    "Pacing: {pacing}. Write in {perspective} perspective. Use natural dialogue and keep language accessible. "
    "End with an emotionally charged, surprising, and satisfying conclusion that ties the twists together."
)

LENGTH_MAP = {
    "Short (1-2k words)": (800, "short"),
    "Medium (2-5k words)": (2500, "medium"),
    "Long (5k+ words)": (4500, "long"),
}

# ---------------------- HELPER ----------------------
def generate_with_ollama(prompt, model=MODEL):
    """Send prompt to Ollama model and return generated story."""
    response = requests.post(
        OLLAMA_URL,
        json={"model": model, "prompt": prompt},
        stream=True
    )
    story = ""
    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line.decode("utf-8"))
                if "response" in data:
                    story += data["response"]
            except:
                pass
    return story.strip()

# ---------------------- STREAMLIT UI ----------------------
st.set_page_config(page_title="AI Anime/Manhwa Horror Story Maker", page_icon="📜", layout="wide")
st.title("📖 AI Anime/Manhwa Horror Story Maker")
st.markdown("_Generate long, engrossing anime/manhwa-style stories with plot twists — choose genre, tone, and structure._")

with st.sidebar:
    st.header("Story Settings")
    length_choice = st.selectbox("Length", list(LENGTH_MAP.keys()), index=1)
    genres = st.multiselect("Genre(s)", ["Horror", "Action", "Mystery", "Romance", "Slice of Life", "Supernatural", "Thriller", "Psychological"], default=["Horror"]) 
    tone = st.selectbox("Tone", ["Dark & moody", "Creepy & atmospheric", "Fast-paced & violent", "Melancholic & introspective", "Whimsical & eerie"], index=1)
    perspective = st.selectbox("Narrative perspective", ["First-person", "Third-person limited", "Third-person omniscient"], index=1)
    pacing = st.selectbox("Pacing", ["Slow burn", "Balanced", "Fast-paced"], index=1)
    twist_enable = st.checkbox("Include twists", value=True)
    twist_strength = st.slider("Twist intensity", 1, 5, 3)
    twist_count = st.slider("Approx number of twists", 1, 4, 2)
    characters = st.text_input("Main character names (comma-separated)", "Akira, Yumi")
    setting = st.text_input("Setting (short)", "A foggy port town, modern but with old alleys")
    seed_prompt = st.text_area("Optional seed / starting paragraph (leave blank to let AI start)")
    safe_mode = st.checkbox("Disable explicit/graphic content (recommended)", value=True)

col1, col2 = st.columns([3,1])
with col1:
    title = st.text_input("Story title (optional)", "The Lantern in the Alley")
    custom_plot_guidelines = st.text_area("Plot guidelines / special requests (tone, themes, what to avoid)", "Make the story eerie, focused on atmosphere, reveal trauma slowly; avoid gore.")
with col2:
    st.write("\n")
    if st.button("🎲 Generate Story"):
        with st.spinner("Composing your story... this can take a little while for long outputs"):
            # Build dynamic prompt
            max_tokens_est, length_desc = LENGTH_MAP[length_choice]
            genres_joined = ", ".join(genres) if genres else "General"
            prompt = PROMPT_TEMPLATE.format(
                length_desc=length_desc,
                genres=genres_joined,
                tone=tone,
                characters=characters,
                setting=setting,
                plot_guidelines=custom_plot_guidelines if custom_plot_guidelines.strip() else "Follow an engaging mystery arc.",
                twist_count=twist_count if twist_enable else 0,
                pacing=pacing,
                perspective=perspective
            )

            if seed_prompt.strip():
                prompt += "\nStart with this seed paragraph:\n" + seed_prompt.strip()

            # safety: if safe_mode, instruct model to avoid explicit gore/sex
            if safe_mode:
                prompt += "\n\nSafety: Avoid graphic gore, explicit sexual content, illegal instructions, and hateful language. Keep it suitable for a general adult audience."

            # Generate story using Ollama
            try:
                story_text = generate_with_ollama(prompt, model=MODEL)

                # display
                st.header(title if title.strip() else "Untitled Story")
                st.markdown(f"**Genres:** {genres_joined}  \n**Tone:** {tone}  \n**Perspective:** {perspective}  \n**Setting:** {setting}")
                st.write("---")
                st.write(story_text)

                # downloads
                now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
                filename = f"{title.replace(' ', '_')}_{now}.txt"
                st.download_button("📥 Download story as .txt", story_text, file_name=filename, mime="text/plain")

                # Save option (append to local file)
                if st.button("💾 Save to local stories folder"):
                    os.makedirs("stories", exist_ok=True)
                    path = os.path.join("stories", filename)
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(story_text)
                    st.success(f"Saved to {path}")

            except Exception as e:
                st.error(f"Ollama error: {str(e)}")

# small footer
st.markdown("---")
st.caption("Built with ♥ using Streamlit and Ollama. Tweak prompt templates in the source to experiment.")



