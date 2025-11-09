import streamlit as st
import re
# SỬA LỖI CUỐI CÙNG: Import module gốc và gọi hàm đầy đủ
import youtube_transcript_api 
# ******************************************************


# ****************** HÀM PHÂN TÍCH SPG LÕI (placeholder) ******************

def spg_analyze_transcript(transcript):
    """
    Hàm mô phỏng logic SPG lõi: Phân tích phụ đề (transcript) để tạo báo cáo.
    """
    placeholder_report = f"""
    ## ✅ Phụ đề đã được trích xuất thành công!
    
    ### ⚠️ Hướng Dẫn Kỹ Thuật (LLM Logic)
    
    Hàm `spg_analyze_transcript` hiện đang thiếu logic gọi LLM/AI. 
    Bạn cần chèn mã gọi API LLM (ví dụ: Gemini, OpenAI) vào hàm này để xử lý `transcript`.
    
    **Transcript Thực Tế Đã Lấy Được (Ví dụ 500 ký tự đầu):**
    > "{transcript[:500]}..."
    
    Tổng số từ đã trích xuất: **{len(transcript.split())}**
    """
    return placeholder_report

# ****************** HÀM CHÍNH (API LOGIC) ĐÃ SỬA LỖI TRIỆT ĐỂ ******************

# Regex đã sửa để chấp nhận youtu.be/
VIDEO_ID_REGEX = re.compile(
    r'(?:https?://)?(?:www\.)?'
    r'(?:youtu\.be/|youtube\.com/(?:watch\?v=|embed/|v/))'
    r'([\w-]{11})' 
)

def generate_response(input_data):
    video_url = input_data.get('Video_URL')
    
    video_id_match = VIDEO_ID_REGEX.search(video_url)
    
    if not video_id_match:
        return "Lỗi: URL không hợp lệ. Vui lòng kiểm tra lại đường dẫn YouTube (cần có ID video)."
        
    video_id = video_id_match.group(1)

    try:
        st.info(f"Đang tìm kiếm phụ đề cho Video ID: **{video_id}**...")
        
        # SỬA LỖI GỌI HÀM CUỐI CÙNG: Gọi hàm đầy đủ qua module.class.method
        transcript_list = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'vi', 'ja', 'zh'])
        
        full_transcript = " ".join([item['text'] for item in transcript_list])
        
        if not full_transcript:
            return "Lỗi: Không tìm thấy phụ đề hợp lệ cho video này. Video có thể không có phụ đề hoặc không hỗ trợ ngôn ngữ."
        
        # 3. GỌI SPG LÕI
        return spg_analyze_transcript(full_transcript)
        
    except Exception as e:
        # Nếu lỗi là do thiếu phụ đề, thông báo sẽ rõ ràng hơn.
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
