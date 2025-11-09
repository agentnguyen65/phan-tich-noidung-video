import streamlit as st
import re
from youtube_transcript_api import YouTubeTranscriptApi
# Lưu ý: Bạn cần thêm thư viện/API LLM của mình tại đây (ví dụ: openai, google-genai, etc.)

# ****************** HÀM PHÂN TÍCH SPG LÕI ******************

def spg_analyze_transcript(transcript):
    """
    Hàm mô phỏng logic SPG lõi: Phân tích phụ đề (transcript) để tạo báo cáo.
    
    >>> CHỈNH SỬA TẠI ĐÂY: <<<
    Bạn cần chèn logic gọi mô hình AI/LLM của mình (ví dụ: GPT-4, Gemini)
    để phân tích 'transcript' và tạo ra Báo Cáo Phân Tích theo yêu cầu:
    1. Tóm tắt nội dung video
    2. Phân tích chi tiết nội dung học
    3. Đánh giá Giọng văn
    4. Danh sách các nội dung học kèm Mốc thời gian (Timestamp)
    
    Đầu vào: 'transcript' (chuỗi nội dung phụ đề thực tế).
    Đầu ra mong muốn: Chuỗi định dạng Markdown chứa Báo Cáo Phân Tích.
    """
    
    # 🛑 PHẦN CODE MÔ PHỎNG GIẢ ĐỊNH ĐÃ BỊ LOẠI BỎ THEO YÊU CẦU
    
    # Trả về một thông báo lỗi/hướng dẫn nếu logic LLM chưa được chèn vào
    placeholder_report = f"""
    ## ⚠️ Lỗi: Logic Phân Tích (SPG Lõi) Chưa Được Tích Hợp
    
    ### Hướng Dẫn Kỹ Thuật
    
    Hàm `spg_analyze_transcript` hiện đang thiếu logic gọi LLM/AI. 
    Để hoàn tất, bạn cần chèn mã gọi API LLM (ví dụ: OpenAI, Google Gemini, Anthropic) vào hàm này để xử lý `transcript` ({len(transcript.split())} từ đã được trích xuất).
    
    **Transcript Thực Tế Đã Lấy Được (Ví dụ 100 từ đầu):**
    > "{transcript[:500]}..."
    """
    return placeholder_report

# ****************** HÀM CHÍNH (API LOGIC) ĐÃ SỬA LỖI URL ******************

VIDEO_ID_REGEX = re.compile(
    r'(?:https?://)?(?:www\.)?'
    r'(?:youtu\.be/|youtube\.com/(?:watch\?v=|embed/|v/))'
    r'([\w-]{11})' # Nhóm 1: Bắt chính xác 11 ký tự ID
)

def generate_response(input_data):
    video_url = input_data.get('Video_URL')
    
    video_id_match = VIDEO_ID_REGEX.search(video_url)
    
    if not video_id_match:
        return "Lỗi: URL không hợp lệ. Vui lòng kiểm tra lại đường dẫn YouTube (cần có ID video)."
        
    video_id = video_id_match.group(1)

    try:
        st.info(f"Đang tìm kiếm phụ đề cho Video ID: **{video_id}**...")
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'vi', 'ja', 'zh'])
        
        full_transcript = " ".join([item['text'] for item in transcript_list])
        
        if not full_transcript:
            return "Lỗi: Không tìm thấy phụ đề hợp lệ cho video này. Video có thể không có phụ đề hoặc không hỗ trợ ngôn ngữ."
        
        # 3. GỌI SPG LÕI (Hàm này sẽ trả về hướng dẫn vì chưa có LLM)
        return spg_analyze_transcript(full_transcript)
        
    except Exception as e:
        return f"Lỗi: Không thể lấy phụ đề hoặc phân tích nội dung. Nguyên nhân: {e}."


# ****************** PHẦN XÂY DỰNG GIAO DIỆN STREAMLIT ******************

st.set_page_config(page_title="SPG - Phân Tích Video Học Thuật", layout="wide")
st.title("📹 Ứng Dụng Phân Tích Nội Dung Video Học Thuật (SPG)")

with st.container():
    st.header("1. Nhập liệu")
    video_url = st.text_input(
        "Nhập mã URL của video YouTube cần phân tích:",
        placeholder="Ví dụ: https://www.youtube.com/watch?v=xxxxxxxxxxx"
    )
    
    if st.button("Tạo Báo Cáo Phân Tích", type="primary"):
        if video_url:
            with st.status("Đang thực hiện quy trình phân tích...", expanded=True) as status:
                result = generate_response({"Video_URL": video_url})
                status.update(label="Phân tích hoàn tất!", state="complete", expanded=False)
            
            st.session_state['report_result'] = result
        else:
            st.warning("⚠️ Vui lòng nhập URL của video trước khi tạo báo cáo.")


st.header("2. Kết quả")
if 'report_result' in st.session_state:
    st.markdown(st.session_state['report_result'])
else:
    st.info("Kết quả phân tích sẽ hiển thị ở đây sau khi bạn nhấn nút.")



