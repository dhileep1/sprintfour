import streamlit as st
import os
import shutil
import json
import time
from script_gen import generate_script
from audio_gen import generate_audio_sync
from image_gen import generate_image
from video_renderer import check_ffmpeg, get_audio_duration, render_final_video
from subtitle_gen import generate_subtitles

st.set_page_config(page_title="AI Shorts Generator", page_icon="🎬", layout="wide")

st.markdown("""
<style>
    .reportview-container {
        background: #0f172a;
    }
    .main {
        background: #0f172a;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎬 AI Shorts Generator")
st.subheader("Turn your ideas into viral shorts instantly")

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Settings")
    tone = st.selectbox("Tone", ["Energetic", "Funny", "Mysterious", "Inspirational", "Professional"])
    style = st.text_input("Visual Style", "Cinematic Digital Art, High Quality")
    duration = st.slider("Duration (seconds)", 5, 180, 20)
    
    if st.button("🧹 Clear Workspace"):
        if os.path.exists("output"):
            shutil.rmtree("output")
        st.success("Workspace cleared!")

# Main logic
idea = st.text_area("💡 Enter your video idea...", placeholder="e.g. A futuristic restaurant for robots")

if st.button("🚀 Generate Video"):
    if not idea:
        st.error("Please enter an idea first.")
    else:
        if not check_ffmpeg():
            st.error("FFmpeg not found! Please check installation.")
            st.stop()
            
        # Initialization
        output_dir = "output"
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir, exist_ok=True)
        
        with st.status("🎬 Building your short...", expanded=True) as status:
            # 1. Script Generation
            st.write("📝 Generating Script...")
            try:
                script_data = generate_script(idea, tone, style, duration)
                meta = script_data.get("meta", {})
                scenes = script_data.get("scenes", [])
                st.session_state['script'] = script_data
            except Exception as e:
                st.error(f"Script error: {e}")
                st.stop()
            
            # Show script in sub-tab later, but keep going
            st.write("🎙️ Generating Voiceover...")
            master_audio_path = os.path.join(output_dir, "master_audio.mp3")
            generate_audio_sync(meta.get("full_narration", ""), master_audio_path)
            master_duration = get_audio_duration(master_audio_path)
            st.write(f"Voiceover length: {master_duration:.2f}s")
            
            # 2. Subtitles
            st.write("💬 Creating Subtitles...")
            srt_path = os.path.join(output_dir, "subtitles.srt")
            generate_subtitles(master_audio_path, srt_path)
            
            # 3. Images
            st.write("🖼️ Generating Images (This takes time)...")
            image_paths = []
            
            # Word count weights for timing
            weights = [len(s.get("segment_text", "").split()) for s in scenes]
            total_weight = sum(weights) if sum(weights) > 0 else 1
            scene_durations = [(w / total_weight) * master_duration for w in weights]

            # Display area for images
            cols = st.columns(min(len(scenes), 3))
            for idx, scene in enumerate(scenes):
                scene_id = idx + 1
                img_path = os.path.join(output_dir, f"image_{scene_id}.jpg")
                st.write(f"  - Generating Scene {scene_id}...")
                
                generate_image(scene.get("visual_prompt", ""), img_path)
                image_paths.append(img_path)
                
                # Show image in UI
                with cols[idx % 3]:
                    st.image(img_path, caption=f"Scene {scene_id}")
            
            # 4. Rendering
            st.write("🎬 Stitching everything together...")
            final_output = "final_short.mp4"
            bgm_mood = meta.get("bgm_mood", "happy").lower()
            bgm_path = os.path.join("Audio", f"{bgm_mood}.mp3")
            
            if not os.path.exists(bgm_path):
                bgm_path = None
                
            render_final_video(image_paths, master_audio_path, final_output, scene_durations, bgm_path=bgm_path, srt_path=srt_path)
            
            status.update(label="✅ Generation Complete!", state="complete", expanded=False)

        # Final Display
        st.divider()
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.header("📽️ Final Result")
            if os.path.exists(final_output):
                st.video(final_output)
                with open(final_output, "rb") as file:
                    st.download_button(label="📥 Download Video", data=file, file_name="ai_short.mp4", mime="video/mp4")
            else:
                st.error("Video file not found.")

        with col2:
            st.header("📄 Script & Metadata")
            st.json(script_data)
            
            st.subheader("Scene Descriptions")
            for idx, scene in enumerate(scenes):
                with st.expander(f"Scene {idx+1}"):
                    st.write(f"**Narration:** {scene.get('segment_text')}")
                    st.write(f"**Visual Prompt:** {scene.get('visual_prompt')}")

# Display placeholder if no video generated yet
if 'script' not in st.session_state and not idea:
    st.info("👋 Welcome! Set your settings in the sidebar and enter an idea to start.")
