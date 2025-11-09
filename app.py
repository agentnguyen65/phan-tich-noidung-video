import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai
from google.genai.errors import APIError
import re # Cần thiết để trích xuất ID video

# -----------------------------------------------
# PHẦN LOGIC API (ĐÃ CẬP NHẬT HOÀN TOÀN)
# -----------------------------------------------

def extract_video_id(url):
    """Lấy ID video từ URL (hỗ trợ cả đường dẫn rút gọn và đầy đủ)."""
    # Pattern regex để tìm ID video trong các định dạng URL khác nhau
    match = re.search(r"(?<=v=)[\w-]+|(?<=youtu\.be/)[\w-]+", url)
    return match.group(0) if match else None

def get_transcript(video_id):
    """Gọi API để lấy bản phiên âm của video."""
    try:
        # Lấy danh sách các bản phiên âm (có thể có nhiều ngôn ngữ)
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Thử lấy bản phiên âm tiếng Việt (vi) hoặc tiếng Anh (en)
        # Nếu không có, sẽ lấy bản phiên âm tự động được tạo (generated)
        
        transcript = transcript_list.find_transcript(['vi', 'en']).fetch()
        
        # Kết hợp các đoạn text lại thành một chuỗi duy nhất
        full_transcript = " ".join([item['text'] for item in transcript])
        
        return full_transcript, transcript
    except Exception as e:
        return f"Lỗi lấy phiên âm: Video có thể không có phụ đề, hoặc không công khai. Chi tiết: {e}", None

def generate_response_spg(video_url):
    """
    Kết nối các bước: Lấy ID -> Lấy Phiên âm -> Gửi đến LLM Lõi (Gemini) -> Trả về Báo cáo.
    """
    video_id = extract_video_id(video_url)
    
    if not video_id:
        return "Lỗi: Không thể trích xuất ID video từ URL. Vui lòng kiểm tra lại đường dẫn."

    # 1. LẤY PHIÊN ÂM
    st.info(f"Đang lấy phiên âm cho Video ID: {video_id}...")
    full_transcript, timed_transcript = get_transcript(video_id)
    
    if "Lỗi lấy phiên âm" in full_transcript:
        return full_transcript

    # 2. CHUẨN BỊ LỆNH GỌI SPG LÕI
    # (Đã thay thế logic SPG mô phỏng bằng lệnh gọi LLM thực tế)
    
    # Lấy API Key từ Streamlit Secrets (hoặc biến môi trường)
    try:
        # Thay 'GEMINI_API_KEY' bằng tên biến bạn đặt
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"]) 
    except KeyError:
        return "Lỗi cấu hình: Vui lòng thiết lập GEMINI_API_KEY trong Streamlit Secrets."
    except Exception as e:
        return f"Lỗi khởi tạo Gemini Client: {e}"

    # Hướng dẫn SPG Lõi (Prompt)
    # Lồng ghép hướng dẫn SPG chi tiết của bạn vào đây
    spg_prompt = f"""
    Bạn là một chuyên gia phân tích nội dung video học thuật.
    Phân tích bản phiên âm dưới đây và tạo báo cáo dựa trên **Cấu trúc Bắt Buộc** sau:
    1. Tóm tắt nội dung video.
    2. Phân tích chi tiết nội dung học (tập trung vào phương pháp, lý thuyết).
    3. Đánh giá Giọng văn của người hướng dẫn (chuyên nghiệp, học thuật, thân thiện...).
    4. Danh sách các nội dung học kèm Mốc thời gian (Timestamp) TƯƠNG ỨNG trong video.
    
    BẢN PHIÊN ÂM VIDEO:
    ---
    {full_transcript}
    ---
    """
    
    # 3. GỌI API GEMINI
    try:
        with st.spinner('Đang gửi phiên âm và phân tích bởi LLM Lõi...'):
            response = client.models.generate_content(
                model='gemini-2.5-flash', # Hoặc model phù hợp khác
                contents=spg_prompt
            )
        
        # 4. TRẢ VỀ KẾT QUẢ BÁO CÁO THỰC TẾ
        return f"""
# 📝 Báo Cáo Phân Tích Nội Dung Video Học Thuật (Thực Tế)

**Video URL:** `{video_url}`
---
{response.text}
"""
    except APIError as e:
        return f"Lỗi API Gemini: Đã xảy ra lỗi khi gọi LLM Lõi. Chi tiết: {e}"
    except Exception as e:
        return f"Lỗi chung: {e}"

# -----------------------------------------------
# PHẦN UI CỦA STREAMLIT VẪN GIỮ NGUYÊN
# -----------------------------------------------
st.set_page_config(page_title="SPG-WebApp: Phân Tích Video Học Thuật", layout="centered")
# (Phần còn lại của code UI không thay đổi)
# ...
    
      
