import pandas as pd
import streamlit as st
import io
import zipfile
import os
from docx import Document
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings

# --- 1. INITIALIZATION ---
try:
    API_KEY = st.secrets["ELEVEN_API_KEY"]
    client = ElevenLabs(api_key=API_KEY)
    available_voices = client.voices.get_all().voices
    voice_map = {v.name: v.voice_id for v in available_voices}
except Exception as e:
    st.error(f"❌ Connection Error: {e}")
    st.stop()

st.set_page_config(page_title="Credit-Safe Processor", layout="wide")
st.title("🎙️ Batch Audio: Safety & Validation Mode")

# --- 2. MULTI-FILE UPLOADER ---
uploaded_files = st.file_uploader("Upload Document Chunks (Word/Excel):", type=["docx", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    all_data_to_process = [] 
    validation_errors = []

    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        file_base = os.path.splitext(file_name)[0]
        
        # --- DOCX SCANNING ---
        if file_name.endswith('.docx'):
            doc = Document(uploaded_file)
            current_chapter = "Introduction"
            chapters = {current_chapter: []}

            for para in doc.paragraphs:
                text = para.text.strip()
                if not text: continue
                
                # Clean tags
                clean_text = text.split("]")[-1].strip() if "]" in text else text

                # Heading Detection (Strict: Short & Numbered)
                is_num = any(clean_text.startswith(str(d)) for d in range(10)) or \
                         any(clean_text.startswith(d) for d in ['೧','೨','೩','೪','೫','೬','೭','೮','೯','೦'])
                
                if is_num and len(clean_text) < 65 and "." in clean_text[:5]:
                    current_chapter = clean_text.replace(".", "_").replace(" ", "_")
                    if current_chapter not in chapters: chapters[current_chapter] = []
                else:
                    chapters[current_chapter].append(clean_text)

            for title, content_list in chapters.items():
                full_text = " ".join(content_list).strip()
                if not full_text:
                    validation_errors.append(f"⚠️ Warning: '{title}' in {file_name} has no body text.")
                else:
                    all_data_to_process.append({"Source": file_base, "File": title, "Content": full_text, "Chars": len(full_text)})

    # --- 3. THE VALIDATION DASHBOARD (Credit Protection) ---
    st.subheader("🛡️ Validation & Credit Check")
    
    if validation_errors:
        for err in validation_errors: st.warning(err)
    
    if all_data_to_process:
        view_df = pd.DataFrame(all_data_to_process)
        total_chars = view_df["Chars"].sum()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Files Queued", len(uploaded_files))
        c2.metric("Total Audio Segments", len(all_data_to_process))
        c3.metric("Estimated Credit Cost", f"{total_chars} chars")

        st.write("🔍 **Final Review of Text (Check this before clicking Generate):**")
        st.dataframe(view_df[["Source", "File", "Content"]])
        
        st.markdown("---")
        
        # --- 4. VOICE & EXECUTION ---
        selected_voice_name = st.selectbox("Select Account Voice:", ["-- Choose --"] + list(voice_map.keys()))
        final_voice_id = voice_map.get(selected_voice_name, "")

        if st.button("🚀 Confirm & Generate (SPENDS CREDITS)"):
            if not final_voice_id:
                st.error("❌ Select a voice first.")
                st.stop()

            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                progress_bar = st.progress(0)
                for i, item in enumerate(all_data_to_process):
                    try:
                        audio_gen = client.text_to_speech.convert(
                            text=item["Content"],
                            voice_id=final_voice_id,
                            model_id="eleven_v3"
                        )
                        zip_file.writestr(f"{item['Source']}/{item['File']}.mp3", b"".join(list(audio_gen)))
                    except Exception as e:
                        st.error(f"Error at {item['File']}: {e}")
                    progress_bar.progress((i + 1) / len(all_data_to_process))

            st.success("🏁 All documents converted!")
            st.download_button("💾 Download ZIP", zip_buffer.getvalue(), "Production_Batch.zip")