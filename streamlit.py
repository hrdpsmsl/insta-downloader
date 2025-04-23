# import streamlit as st
# import google.generativeai as genai
# from google.generativeai import upload_file, get_file
# import tempfile
# import os
# import time
# import hashlib
# from dotenv import load_dotenv

# # Load API Key from .env
# load_dotenv()
# API_KEY = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=API_KEY)

# # Initialize Gemini model
# model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# st.set_page_config(page_title="Gemini Video Analyzer", layout="centered")
# st.title("🎥 Gemini Video Analyzer")
# st.caption("Upload a video and ask questions about its content.")

# # Session cache for uploaded videos
# if 'uploaded_files' not in st.session_state:
#     st.session_state.uploaded_files = {}  # key: hash, value: Gemini file object


# def get_file_hash(file_bytes):
#     return hashlib.md5(file_bytes).hexdigest()


# # Upload video file
# video_file = st.file_uploader("Upload a video (MP4/MOV/AVI)", type=["mp4", "mov", "avi"])

# if video_file:
#     file_bytes = video_file.read()
#     file_hash = get_file_hash(file_bytes)

#     # Check if already uploaded
#     if file_hash in st.session_state.uploaded_files:
#         st.success("✅ This video is already uploaded and cached.")
#         gemini_file = st.session_state.uploaded_files[file_hash]
#     else:
#         with st.spinner("Uploading to Gemini..."):
#             with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
#                 tmp.write(file_bytes)
#                 tmp_path = tmp.name

#             uploaded = upload_file(tmp_path)

#             # Wait until it's processed
#             while uploaded.state.name == "PROCESSING":
#                 time.sleep(2)
#                 uploaded = get_file(uploaded.name)

#             gemini_file = uploaded
#             st.session_state.uploaded_files[file_hash] = gemini_file
#             st.success("✅ Video uploaded and cached successfully.")

#     st.video(gemini_file.uri)

#     user_query = st.text_area("💬 What would you like to know about the video?", height=100)

#     if st.button("Analyze Video"):
#         if not user_query.strip():
#             st.warning("Please enter a question or prompt for analysis.")
#         else:
#             with st.spinner("Analyzing with Gemini..."):
#                 response = model.generate_content([user_query, gemini_file])
#                 st.subheader("📊 Gemini Analysis Result")
#                 st.markdown(response.text)
# else:
#     st.info("Please upload a video to begin.")




#V2 

# import streamlit as st
# import google.generativeai as genai
# from google.generativeai import upload_file, get_file
# import tempfile
# import os
# import time
# import hashlib
# import instaloader
# import shutil
# import glob

# from dotenv import load_dotenv
# load_dotenv()

# # Configure Gemini
# API_KEY = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=API_KEY)
# model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# st.set_page_config(page_title="Gemini Reel Analyzer", layout="centered")
# st.title("📲 Instagram Reel Analyzer using Gemini")

# # Session state init
# if 'video_path' not in st.session_state:
#     st.session_state.video_path = None
# if 'file_hash' not in st.session_state:
#     st.session_state.file_hash = None
# if 'gemini_file' not in st.session_state:
#     st.session_state.gemini_file = None
# if 'uploaded_files' not in st.session_state:
#     st.session_state.uploaded_files = {}

# # Helper functions
# def get_file_hash(file_path):
#     with open(file_path, "rb") as f:
#         return hashlib.md5(f.read()).hexdigest()

# def clear_folder(folder_path):
#     if not os.path.exists(folder_path):
#         return
#     for item in os.listdir(folder_path):
#         item_path = os.path.join(folder_path, item)
#         try:
#             if os.path.isfile(item_path) or os.path.islink(item_path):
#                 os.unlink(item_path)
#             elif os.path.isdir(item_path):
#                 shutil.rmtree(item_path)
#         except Exception as e:
#             print(f"Failed to delete {item_path}. Reason: {e}")

# def rename_reel(shortcode, dir):
#     mp4_files = glob.glob(os.path.join(dir, "*.mp4"))
#     if mp4_files:
#         original_file = mp4_files[0]
#         new_file = os.path.join(dir, shortcode + ".mp4")
#         os.rename(original_file, new_file)
#         return new_file
#     return None

# def move_video(shortcode, source_folder, destination_folder):
#     os.makedirs(destination_folder, exist_ok=True)
#     source_path = os.path.join(source_folder, shortcode)
#     destination_path = os.path.join(destination_folder, shortcode)
#     if os.path.exists(source_path):
#         shutil.move(source_path, destination_path)
#         clear_folder("reels")
#         return destination_path
#     return None

# def download_reel(shortcode, target_dir="reels"):
#     L = instaloader.Instaloader(dirname_pattern=target_dir)
#     try:
#         post = instaloader.Post.from_shortcode(L.context, shortcode)
#         L.download_post(post, target=shortcode)
#         return True
#     except Exception as e:
#         st.error(f"❌ Failed to download reel: {e}")
#         return False

# # Input: Instagram URL
# insta_url = st.text_input("Paste Instagram Reel URL", placeholder="https://www.instagram.com/reel/XXXXXXX/")
# if insta_url:
#     shortcode = insta_url.rstrip("/").split("/")[-1]

#     if st.button("Download & Prepare Reel"):
#         with st.spinner("📥 Downloading Reel..."):
#             clear_folder("reels")
#             if download_reel(shortcode):
#                 renamed_path = rename_reel(shortcode, "reels")
#                 if renamed_path:
#                     final_path = move_video(shortcode + ".mp4", "reels", "videos")
#                     if final_path:
#                         st.session_state.video_path = final_path
#                         st.session_state.file_hash = get_file_hash(final_path)

#                         if st.session_state.file_hash in st.session_state.uploaded_files:
#                             st.session_state.gemini_file = st.session_state.uploaded_files[st.session_state.file_hash]
#                             st.success("✅ Reel already cached and ready.")
#                         else:
#                             with st.spinner("📤 Uploading to Gemini..."):
#                                 uploaded = upload_file(final_path)
#                                 while uploaded.state.name == "PROCESSING":
#                                     time.sleep(2)
#                                     uploaded = get_file(uploaded.name)
#                                 st.session_state.gemini_file = uploaded
#                                 st.session_state.uploaded_files[st.session_state.file_hash] = uploaded
#                             st.success("✅ Upload successful.")
#                     else:
#                         st.error("Failed to move video.")
#                 else:
#                     st.error("Renaming failed.")
#             else:
#                 st.error("Download failed.")

# # Video playback and analysis UI
# if st.session_state.video_path:
#     st.video(st.session_state.video_path)
#     query = st.text_area("💬 What do you want to know about the reel?", height=100)

#     if st.button("Analyze Reel"):
#         if not query.strip():
#             st.warning("Please enter a question or prompt.")
#         elif not st.session_state.gemini_file:
#             st.error("Gemini file not uploaded.")
#         else:
#             with st.spinner("🤖 Analyzing with Gemini..."):
#                 response = model.generate_content([query, st.session_state.gemini_file])
#                 st.subheader("📊 Gemini Analysis")
#                 st.markdown(response.text)

#V3

# import streamlit as st
# import google.generativeai as genai
# from google.generativeai import upload_file, get_file
# import os
# import time
# import hashlib
# import instaloader
# import shutil
# import glob
# from dotenv import load_dotenv

# load_dotenv()

# # Configure Gemini
# API_KEY = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=API_KEY)
# model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# st.set_page_config(page_title="Gemini Reel Analyzer", layout="centered")
# st.title("📲 Instagram Multi-Reel Analyzer using Gemini")

# # Session init
# if 'videos' not in st.session_state:
#     st.session_state.videos = {}  # {shortcode: {"path": ..., "hash": ..., "gemini_file": ...}}

# # Utils
# def clear_folder(folder_path):
#     if os.path.exists(folder_path):
#         for item in os.listdir(folder_path):
#             item_path = os.path.join(folder_path, item)
#             try:
#                 if os.path.isfile(item_path) or os.path.islink(item_path):
#                     os.unlink(item_path)
#                 elif os.path.isdir(item_path):
#                     shutil.rmtree(item_path)
#             except Exception as e:
#                 print(f"Failed to delete {item_path}. Reason: {e}")

# def get_file_hash(file_path):
#     with open(file_path, "rb") as f:
#         return hashlib.md5(f.read()).hexdigest()

# def rename_reel(shortcode, dir):
#     mp4_files = glob.glob(os.path.join(dir, "*.mp4"))
#     if mp4_files:
#         original_file = mp4_files[0]
#         new_file = os.path.join(dir, shortcode + ".mp4")
#         os.rename(original_file, new_file)
#         return new_file
#     return None

# def move_video(filename, source_folder, destination_folder):
#     os.makedirs(destination_folder, exist_ok=True)
#     source_path = os.path.join(source_folder, filename)
#     destination_path = os.path.join(destination_folder, filename)
#     if os.path.exists(source_path):
#         shutil.move(source_path, destination_path)
#         return destination_path
#     return None

# def download_reel(shortcode, target_dir="reels"):
#     L = instaloader.Instaloader(dirname_pattern=target_dir)
#     try:
#         post = instaloader.Post.from_shortcode(L.context, shortcode)
#         L.download_post(post, target=shortcode)
#         return True
#     except Exception as e:
#         st.error(f"❌ Failed to download reel {shortcode}: {e}")
#         return False

# # Input: Multiple URLs
# urls = st.text_area("Paste multiple Instagram Reel URLs (one per line):")
# if st.button("Download & Cache Reels"):
#     if not urls.strip():
#         st.warning("Please provide at least one URL.")
#     else:
#         url_list = [u.strip() for u in urls.splitlines() if u.strip()]
#         clear_folder("reels")  # Fresh folder each run
#         with st.spinner("📥 Downloading & preparing reels..."):
#             for url in url_list:
#                 shortcode = url.rstrip("/").split("/")[-1]
#                 if shortcode in st.session_state.videos:
#                     st.info(f"ℹ️ {shortcode} already processed.")
#                     continue
#                 success = download_reel(shortcode)
#                 if success:
#                     renamed_path = rename_reel(shortcode, "reels")
#                     if renamed_path:
#                         final_path = move_video(shortcode + ".mp4", "reels", "videos")
#                         if final_path:
#                             file_hash = get_file_hash(final_path)
#                             if any(v['hash'] == file_hash for v in st.session_state.videos.values()):
#                                 # Already uploaded
#                                 st.info(f"✅ {shortcode} already cached.")
#                                 continue
#                             uploaded = upload_file(final_path)
#                             while uploaded.state.name == "PROCESSING":
#                                 time.sleep(2)
#                                 uploaded = get_file(uploaded.name)
#                             st.session_state.videos[shortcode] = {
#                                 "path": final_path,
#                                 "hash": file_hash,
#                                 "gemini_file": uploaded
#                             }
#                             st.success(f"✅ {shortcode} ready.")
#                         else:
#                             st.error(f"Could not move {shortcode}")
#                     else:
#                         st.error(f"Could not rename {shortcode}")
#                 else:
#                     st.error(f"Failed to download {shortcode}")

# # Select Reel
# if st.session_state.videos:
#     selected_shortcode = st.selectbox("📁 Select a Reel to analyze", options=list(st.session_state.videos.keys()))
#     st.video(st.session_state.videos[selected_shortcode]["path"])

#     query = st.text_area("💬 What do you want to ask about this reel?", height=100)

#     if st.button("Analyze Reel"):
#         if not query.strip():
#             st.warning("Please enter a question.")
#         else:
#             with st.spinner("🤖 Thinking..."):
#                 file = st.session_state.videos[selected_shortcode]["gemini_file"]
#                 response = model.generate_content([query, file])
#                 st.subheader("📊 Gemini Analysis")
#                 st.markdown(response.text)
# else:
#     st.info("No reels processed yet.")


#v4

# import streamlit as st
# import google.generativeai as genai
# from google.generativeai import upload_file, get_file
# import os
# import time
# import hashlib
# import instaloader
# import shutil
# import glob
# from dotenv import load_dotenv
# import pandas as pd
# from io import BytesIO
# import math

# load_dotenv()

# # Configure Gemini
# API_KEY = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=API_KEY)
# model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# st.set_page_config(page_title="Gemini Reel Analyzer", layout="wide")
# st.title("Instagram Multi-Reel Analyzer using Gemini")
# st.markdown(
#     """
#     <style>
#     .stToolbarActions.st-emotion-cache-1p1m4ay.ekuhni82 {
#         display: none;
#     }
#     ._profileContainer_gzau3_53 {
#         display: none;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Session state setup
# if 'videos' not in st.session_state:
#     st.session_state.videos = {}

# if 'analysis_results' not in st.session_state:
#     st.session_state.analysis_results = []

# # Utils
# def clear_folder(folder_path):
#     if os.path.exists(folder_path):
#         for item in os.listdir(folder_path):
#             item_path = os.path.join(folder_path, item)
#             try:
#                 if os.path.isfile(item_path) or os.path.islink(item_path):
#                     os.unlink(item_path)
#                 elif os.path.isdir(item_path):
#                     shutil.rmtree(item_path)
#             except Exception as e:
#                 print(f"Failed to delete {item_path}. Reason: {e}")

# def get_file_hash(file_path):
#     with open(file_path, "rb") as f:
#         return hashlib.md5(f.read()).hexdigest()

# def rename_reel(shortcode, dir):
#     mp4_files = glob.glob(os.path.join(dir, "*.mp4"))
#     if mp4_files:
#         original_file = mp4_files[0]
#         new_file = os.path.join(dir, shortcode + ".mp4")
#         os.rename(original_file, new_file)
#         return new_file
#     return None

# def move_video(filename, source_folder, destination_folder):
#     os.makedirs(destination_folder, exist_ok=True)
#     source_path = os.path.join(source_folder, filename)
#     destination_path = os.path.join(destination_folder, filename)
#     if os.path.exists(source_path):
#         shutil.move(source_path, destination_path)
#         return destination_path
#     return None

# def download_reel(shortcode, target_dir="reels"):
#     L = instaloader.Instaloader(dirname_pattern=target_dir)
#     try:
#         post = instaloader.Post.from_shortcode(L.context, shortcode)
#         L.download_post(post, target=shortcode)
#         return True
#     except Exception as e:
#         st.error(f"Failed to download reel {shortcode}: {e}")
#         return False

# # Input: Instagram URLs
# urls = st.text_area("Paste multiple Instagram Reel URLs (one per line):")

# col1, col2 = st.columns([1, 1])
# with col1:
#     if st.button("Download & Cache Reels"):
#         if not urls.strip():
#             st.warning("Please provide at least one URL.")
#         else:
#             url_list = [u.strip() for u in urls.splitlines() if u.strip()]
#             clear_folder("reels")
#             with st.spinner("Downloading & preparing reels..."):
#                 for url in url_list:
#                     shortcode = url.rstrip("/").split("/")[-1]
#                     if shortcode in st.session_state.videos:
#                         st.info(f" {shortcode} already processed.")
#                         continue
#                     success = download_reel(shortcode)
#                     if success:
#                         renamed_path = rename_reel(shortcode, "reels")
#                         if renamed_path:
#                             final_path = move_video(shortcode + ".mp4", "reels", "videos")
#                             if final_path:
#                                 file_hash = get_file_hash(final_path)
#                                 if any(v['hash'] == file_hash for v in st.session_state.videos.values()):
#                                     st.info(f"{shortcode} already cached.")
#                                     continue
#                                 uploaded = upload_file(final_path)
#                                 while uploaded.state.name == "PROCESSING":
#                                     time.sleep(2)
#                                     uploaded = get_file(uploaded.name)
#                                 st.session_state.videos[shortcode] = {
#                                     "path": final_path,
#                                     "hash": file_hash,
#                                     "gemini_file": uploaded
#                                 }
#                                 st.success(f"{shortcode} ready.")
#                             else:
#                                 st.error(f"Could not move {shortcode}")
#                         else:
#                             st.error(f"Could not rename {shortcode}")
#                     else:
#                         st.error(f"Failed to download {shortcode}")

# with col2:
#     if st.button("Reset All Reels"):
#         st.session_state.videos.clear()
#         st.session_state.analysis_results.clear()
#         st.success("Cleared all reels and results.")

# # Select reels for analysis
# if st.session_state.videos:
#     st.subheader("Select Reels to Analyze")

#     all_reel_keys = list(st.session_state.videos.keys())
#     select_all = st.checkbox("Select All", value=True)

#     if select_all:
#         selected_reels = st.multiselect(
#             "Selected Reels",
#             options=all_reel_keys,
#             default=all_reel_keys
#         )
#     else:
#         selected_reels = st.multiselect(
#             "Select one or more Reels",
#             options=all_reel_keys
#         )
#     cols_per_row = 10
#     num_reels = len(selected_reels)
#     rows = math.ceil(num_reels / cols_per_row)
#     for row_idx in range(rows):
#         cols = st.columns(cols_per_row)
#         for col_idx in range(cols_per_row):
#             reel_idx = row_idx * cols_per_row + col_idx
#             if reel_idx < num_reels:
#                 reel = selected_reels[reel_idx]
#                 with cols[col_idx]:
#                     st.video(st.session_state.videos[reel]["path"])
#     # for reel in selected_reels:
#     #     col1,col2=st.columns([1,6])
#     #     with col1:
#     #         st.video(st.session_state.videos[reel]["path"])

#     query = st.text_area("What do you want to ask about the selected reel(s)?", height=100)

#     # if st.button("Analyze with Gemini"):
#     #     if not query.strip():
#     #         st.warning("Please enter a question.")
#     #     else:
#     #         with st.spinner("Thinking..."):
#     #             files = [st.session_state.videos[k]["gemini_file"] for k in selected_reels]
#     #             response = model.generate_content([query] + files)
#     #             st.subheader("Gemini Response")
#     #             st.markdown(response.text)

#     #             # Save response
#     #             st.session_state.analysis_results.append({
#     #                 "Reels": ", ".join(selected_reels),
#     #                 "Prompt": query,
#     #                 "Response": response.text
#     #             })
#     #second_iteration
#     # if st.button("Analyze with Gemini"):
#     #     if not query.strip():
#     #         st.warning("Please enter a question.")
#     #     else:
#     #         with st.spinner("Thinking..."):
#     #             files = [st.session_state.videos[k]["gemini_file"] for k in selected_reels]
#     #             batch_size = 9
#     #             all_responses = []

#     #             for i in range(0, len(files), batch_size):
#     #                 batch_files = files[i:i + batch_size]
#     #                 try:
#     #                     response = model.generate_content([query] + batch_files)
#     #                     all_responses.append(response.text)
#     #                 except Exception as e:
#     #                     all_responses.append(f"Error in batch {i//batch_size + 1}: {str(e)}")

#     #             full_response = "\n\n---\n\n".join(all_responses)
#     #             st.subheader("Gemini Response")
#     #             st.markdown(full_response)

#     #             # Save response
#     #             st.session_state.analysis_results.append({
#     #                 "Reels": ", ".join(selected_reels),
#     #                 "Prompt": query,
#     #                 "Response": full_response
#     #             })

#     #third iteration
#     if st.button("Analyze with Gemini"):
#         if "last_response" in st.session_state and st.session_state.last_response:
#             st.subheader("Gemini Response")
#             st.markdown(st.session_state.last_response)
#         if not query.strip():
#             st.warning("Please enter a question.")
#         else:
#             with st.spinner("Thinking..."):
#                 files = [st.session_state.videos[k]["gemini_file"] for k in selected_reels]
#                 batch_size = 10
#                 all_responses = []

#                 for i in range(0, len(files), batch_size):
#                     batch_files = files[i:i + batch_size]
#                     try:
#                         response = model.generate_content([query] + batch_files)
#                         all_responses.append(response.text)
#                     except Exception as e:
#                         all_responses.append(f"Error in batch {i//batch_size + 1}: {str(e)}")

#                 full_response = "\n\n---\n\n".join(all_responses)
#                 st.subheader("Gemini Response")
#                 st.markdown(full_response)

#                 # Save response
#                 st.session_state.analysis_results.append({
#                     "Reels": ", ".join(selected_reels),
#                     "Prompt": query,
#                     "Response": full_response
#                 })

#                 # Add the full response to session state for follow-up
#                 st.session_state.last_response = full_response

#     # Secondary prompt using Gemini-generated response
#     if "last_response" in st.session_state and st.session_state.last_response:
#         st.markdown("---")
#         st.subheader("Use Previous Response as Knowledge Base")
        
#         default_followup_prompt = """Based on the generated information, create a data-driven story with more than 1000 words with the following structure:

#     1. **Title** – Catchy and informative.  
#     2. **Summary** – Brief overview of key findings.  
#     3. **Introduction** – Context and relevance of the topic.  
#     4. **Data & Methodology** – Data sources and how AI was used.  
#     5. **Key Insights** – Highlight trends, patterns, and findings.  
#     6. **AI Analysis** – Show AI-generated insights or predictions.  
#     7. **Interpretation** – What the data means in real-world terms.  
#     8. **Limitations** – Biases or gaps in data or AI.  
#     9. **Conclusion** – Final thoughts and implications.  
#     10. **Call to Action** – Suggestions or next steps.  
#     """

#         followup_prompt = st.text_area(
#             "Ask a follow-up prompt using the above as knowledge base:",
#             value=default_followup_prompt,
#             height=300
#         )

#         if st.button("Generate Response"):
#             with st.spinner("Generating story..."):
#                 try:
#                     followup_response = model.generate_content([st.session_state.last_response, followup_prompt])
#                     st.subheader("Data-Driven Story")
#                     st.markdown(followup_response.text)
#                 except Exception as e:
#                     st.error(f"Error while generating story: {str(e)}")


# # Export to Excel
# if st.session_state.analysis_results:
#     print(st.session_state.analysis_results)
#     df = pd.DataFrame(st.session_state.analysis_results)
    
#     # Create a BytesIO buffer
#     buffer = BytesIO()
#     with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
#         df.to_excel(writer, index=False)

#     # Move to the beginning of the BytesIO buffer
#     buffer.seek(0)

#     st.download_button(
#         label="Export Responses to Excel",
#         data=buffer,
#         file_name="gemini_reel_analysis.xlsx",
#         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#     )


#v5
import streamlit as st
import google.generativeai as genai
from google.generativeai import upload_file, get_file
import os
import time
import hashlib
import instaloader
import shutil
import glob
from dotenv import load_dotenv
import pandas as pd
from io import BytesIO
import math
import yt_dlp

load_dotenv()

# Configure Gemini
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

st.set_page_config(page_title="Gemini Video Analyzer", layout="wide")
st.title("Instagram / YouTube Multi-Video Analyzer using Gemini")
st.markdown(
    """
    <style>
    ._profileContainer_gzau3_53{ display: none !important;}
    .stToolbarActions.st-emotion-cache-1p1m4ay.ekuhni82 {
        display: none;
    }
    ._profileContainer_gzau3_53 {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Session state setup
if 'videos' not in st.session_state:
    st.session_state.videos = {}

if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = []

# Utils
def clear_folder(folder_path):
    if os.path.exists(folder_path):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            except Exception as e:
                print(f"Failed to delete {item_path}. Reason: {e}")

def get_file_hash(file_path):
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def rename_reel(shortcode, dir):
    mp4_files = glob.glob(os.path.join(dir, "*.mp4"))
    if mp4_files:
        original_file = mp4_files[0]
        new_file = os.path.join(dir, shortcode + ".mp4")
        os.rename(original_file, new_file)
        return new_file
    return None

def move_video(filename, source_folder, destination_folder):
    os.makedirs(destination_folder, exist_ok=True)
    source_path = os.path.join(source_folder, filename)
    destination_path = os.path.join(destination_folder, filename)
    if os.path.exists(source_path):
        shutil.move(source_path, destination_path)
        return destination_path
    return None

def download_reel(shortcode, target_dir="reels"):
    L = instaloader.Instaloader(dirname_pattern=target_dir)
    try:
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        L.download_post(post, target=shortcode)
        return True
    except Exception as e:
        st.error(f"Failed to download reel {shortcode}: {e}")
        return False

def download_youtube_video(url, output_dir="videos"):
    ydl_opts = {
        'format': 'best[height<=360]',  # Updated to avoid separate video/audio
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
        'quiet': True  # Removed 'merge_output_format'
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_id = info_dict.get("id", "")
            file_ext = info_dict.get("ext", "mp4")  # Use actual extension
            file_path = os.path.join(output_dir, f"{video_id}.{file_ext}")
            return file_path, video_id
    except Exception as e:
        st.error(f"Failed to download YouTube video: {e}")
        return None, None

# UI: Video Source Selector and URLs Input
source = st.selectbox("Select Video Source", ["Instagram", "YouTube"])
urls = st.text_area("Paste multiple video URLs (one per line):")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Download & Cache Videos"):
        if not urls.strip():
            st.warning("Please provide at least one URL.")
        else:
            url_list = [u.strip() for u in urls.splitlines() if u.strip()]
            clear_folder("reels")

            with st.spinner("Downloading & preparing videos..."):
                for url in url_list:
                    if source == "Instagram":
                        shortcode = url.rstrip("/").split("/")[-1]
                        if shortcode in st.session_state.videos:
                            st.info(f"{shortcode} already processed.")
                            continue
                        success = download_reel(shortcode)
                        if success: 
                            renamed_path = rename_reel(shortcode, "reels")
                            if renamed_path:
                                final_path = move_video(shortcode + ".mp4", "reels", "videos")
                                if final_path:
                                    file_hash = get_file_hash(final_path)
                                    if any(v['hash'] == file_hash for v in st.session_state.videos.values()):
                                        st.info(f"{shortcode} already cached.")
                                        continue
                                    uploaded = upload_file(final_path)
                                    while uploaded.state.name == "PROCESSING":
                                        time.sleep(2)
                                        uploaded = get_file(uploaded.name)
                                    st.session_state.videos[shortcode] = {
                                        "path": final_path,
                                        "hash": file_hash,
                                        "gemini_file": uploaded
                                    }
                                    st.success(f"{shortcode} ready.")
                                else:
                                    st.error(f"Could not move {shortcode}")
                            else:
                                st.error(f"Could not rename {shortcode}")
                        else:
                            st.error(f"Failed to download {shortcode}")
                    else:  # YouTube
                        file_path, video_id = download_youtube_video(url)
                        if file_path and video_id:
                            file_hash = get_file_hash(file_path)
                            if any(v['hash'] == file_hash for v in st.session_state.videos.values()):
                                st.info(f"{video_id} already cached.")
                                continue
                            uploaded = upload_file(file_path)
                            while uploaded.state.name == "PROCESSING":
                                time.sleep(2)
                                uploaded = get_file(uploaded.name)
                            st.session_state.videos[video_id] = {
                                "path": file_path,
                                "hash": file_hash,
                                "gemini_file": uploaded
                            }
                            st.success(f"{video_id} downloaded and ready.")

with col2:
    if st.button("Reset All Videos  "):
        st.session_state.videos.clear()
        st.session_state.analysis_results.clear()
        files = genai.list_files()
        for file in files:
            print(file.name)
            genai.delete_file(file.name)
            clear_folder("videos")
        st.success("Cleared all reels and results.")

# Select reels for analysis
if st.session_state.videos:
    st.subheader("Select Videos to Analyze")

    all_reel_keys = list(st.session_state.videos.keys())
    select_all = st.checkbox("Select All", value=True)

    if select_all:
        selected_reels = st.multiselect(
            "Selected Videos",
            options=all_reel_keys,
            default=all_reel_keys
        )
    else:
        selected_reels = st.multiselect(
            "Select one or more Videos",
            options=all_reel_keys
        )
    cols_per_row = 10
    num_reels = len(selected_reels)
    rows = math.ceil(num_reels / cols_per_row)
    for row_idx in range(rows):
        cols = st.columns(cols_per_row)
        for col_idx in range(cols_per_row):
            reel_idx = row_idx * cols_per_row + col_idx
            if reel_idx < num_reels:
                reel = selected_reels[reel_idx]
                with cols[col_idx]:
                    st.video(st.session_state.videos[reel]["path"])
    query = st.text_area("What do you want to ask about the selected videos(s)?", height=100)

    if st.button("Analyze with Gemini"):
        if "last_response" in st.session_state and st.session_state.last_response:
            st.subheader("Gemini Response")
            st.markdown(st.session_state.last_response)

        if not query.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking..."):
                all_responses = []
                reels = selected_reels
                chunk_size = 10

                for i in range(0, len(reels), chunk_size):
                    chunk = reels[i:i+chunk_size]
                    chunk_files = [st.session_state.videos[k]["gemini_file"] for k in chunk]

                    try:
                        token_count = model.count_tokens([query] + chunk_files).total_tokens
                    except Exception as e:
                        st.error(f"Failed to count tokens for batch {i//chunk_size+1}: {e}")
                        continue

                    if token_count > 1_000_000:
                        # Split individually if chunk exceeds limit
                        for idx, file in enumerate(chunk_files):
                            try:
                                single_token_count = model.count_tokens([query, file]).total_tokens
                                if single_token_count > 1_000_000:
                                    all_responses.append(f"❌ Skipping reel {chunk[idx]}: token count exceeds limit.")
                                    continue
                                response = model.generate_content([query, file])
                                all_responses.append(f"**{chunk[idx]}**:\n\n{response.text}")
                            except Exception as e:
                                all_responses.append(f"❌ Error analyzing {chunk[idx]}: {str(e)}")
                    else:
                        try:
                            response = model.generate_content([query] + chunk_files)
                            joined_ids = ", ".join(chunk)
                            all_responses.append(f"**[{joined_ids}]**:\n\n{response.text}")
                        except Exception as e:
                            all_responses.append(f"❌ Error in batch {i//chunk_size+1}: {str(e)}")

                full_response = "\n\n---\n\n".join(all_responses)
                st.subheader("Gemini Response")
                st.markdown(full_response)

                st.session_state.analysis_results.append({
                    "Reels": ", ".join(selected_reels),
                    "Prompt": query,
                    "Response": full_response
                })
                st.session_state.last_response = full_response




    # Secondary prompt using Gemini-generated response
    if "last_response" in st.session_state and st.session_state.last_response:
        st.markdown("---")
        st.subheader("Use Previous Response as Knowledge Base")
        
        default_followup_prompt = """Based on the generated information, create a data-driven story with more than 1000 words with the following structure:

1. **Title** – Catchy and informative.  
2. **Summary** – Brief overview of key findings.  
3. **Introduction** – Context and relevance of the topic.  
4. **Data & Methodology** – Data sources and how AI was used.  
5. **Key Insights** – Highlight trends, patterns, and findings.  
6. **AI Analysis** – Show AI-generated insights or predictions.  
7. **Interpretation** – What the data means in real-world terms.  
8. **Limitations** – Biases or gaps in data or AI.  
9. **Conclusion** – Final thoughts and implications.  
10. **Call to Action** – Suggestions or next steps.  
"""

        followup_prompt = st.text_area(
            "Ask a follow-up prompt using the above as knowledge base:",
            value=default_followup_prompt,
            height=300
        )

        if st.button("Generate Response"):
            with st.spinner("Generating story..."):
                try:
                    followup_response = model.generate_content([st.session_state.last_response, followup_prompt])
                    st.subheader("Data-Driven Story")
                    st.markdown(followup_response.text)
                except Exception as e:
                    st.error(f"Error while generating story: {str(e)}")


# Export to Excel
if st.session_state.analysis_results:
    df = pd.DataFrame(st.session_state.analysis_results)
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    buffer.seek(0)

    st.download_button(
        label="Export Responses to Excel",
        data=buffer,
        file_name="gemini_reel_analysis.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

