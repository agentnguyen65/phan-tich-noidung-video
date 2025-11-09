import streamlit as st
import re
from youtube_transcript_api import YouTubeTranscriptApi
# Lưu ý: Vì không có LLM tích hợp, hàm phân tích chi tiết vẫn là mô phỏng,
# nhưng nó sử dụng 'full_transcript' thực tế làm đầu vào.

# ****************** HÀM PHÂN TÍCH SPG LÕI (Cập nhật) ******************

def spg_analyze_transcript(transcript):
    """
    Hàm mô phỏng logic SPG lõi: Phân tích phụ đề (transcript) để tạo báo cáo.
    Trong ứng dụng thực tế, hàm này sẽ gọi LLM/AI để thực hiện các yêu cầu phân tích 
    (Tóm tắt, Phân tích chi tiết, Đánh giá Giọng văn, Chia Timestamp).
    """
    # Vì không thể chạy LLM/AI phân tích, ta vẫn phải mô phỏng kết quả cuối.
    # Tuy nhiên, đầu vào đã là 'transcript' thực tế, sẵn sàng cho việc tích hợp LLM sau này.
    
    # Giả định LLM/AI đã phân tích nội dung học thuật từ 'transcript'
    # và tạo ra báo cáo có cấu trúc bắt buộc.
    
    # Đoạn mô phỏng này chỉ là placeholder cho kết quả phân tích
    # Dựa trên input: full_transcript
    
    bao_cao = f"""
    ## 📄 Báo Cáo Phân Tích Nội Dung Video Học Thuật (Đã Xử Lý)
    
    ### 1. Tóm tắt nội dung video
    (Đã được tóm tắt từ nội dung phụ đề thực tế...)
    Video này có nội dung học thuật chuyên sâu, tập trung vào [1-2 chủ đề chính được trích xuất từ phụ đề]. Tổng thời lượng phân tích: {len(transcript.split())} từ.
    
    ### 2. Phân tích chi tiết nội dung học
    (Phân tích chi tiết dựa trên từng đoạn phụ đề...)
    Cấu trúc bài giảng rõ ràng, đi từ khái niệm cơ bản đến nâng cao. Điểm mạnh là sử dụng ngôn ngữ [chuyên nghiệp/đơn giản] để giải thích các thuật toán phức tạp.
    
    ### 3. Đánh giá Giọng văn
    (Đánh giá dựa trên phân tích âm điệu và từ vựng trong phụ đề...)
    Giọng văn của người hướng dẫn là **chuyên nghiệp và có độ tin cậy cao**, phù hợp để truyền đạt kiến thức học thuật nghiêm túc.
    
    ### 4. Danh sách các nội dung học kèm Mốc thời gian (Timestamp)
    (Các mốc thời gian đã được chia theo cấu trúc phụ đề...)
    | Nội dung học | Mốc thời gian |
    | :--- | :--- |
    | Mở đầu và Đặt vấn đề | **00:00 - 01:15** |
    | Khái niệm cốt lõi (Trích xuất từ transcript) | **01:16 - 04:30** |
    | Thử nghiệm/Ứng dụng thực hành | **04:31 - 09:00** |
    | Tóm tắt và kết luận | **09:01 - Kết thúc** |
    
    """
    return bao_cao

def generate_response(input_data):
    """API Logic: Trích xuất ID, lấy phụ đề và gọi hàm phân tích."""
    video_url = input_data.get('Video_URL')
    
    # 1. Trích xuất ID video
    video_id_match = re.search(r'(?<=v=)[\w-]+', video_url)
    if not video_id_match:
        return "Lỗi: URL không hợp lệ. Vui lòng kiểm tra lại đường dẫn YouTube."
    video_id = video_id_match.group(0)

    try:
        # 2. Lấy phụ đề (transcript) của video
        st.info(f"Đang tìm kiếm phụ đề cho Video ID: **{video_id}**...")
        # Ưu tiên tiếng Anh, nếu không có sẽ cố gắng tìm ngôn ngữ khác
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'vi', 'ja', 'zh'])
        
        # Nối nội dung
        full_transcript = " ".join([item['text'] for item in transcript_list])
        
        if not full_transcript:
            return "Lỗi: Không tìm thấy phụ đề hợp lệ cho video này."
        
        # 3. GỌI SPG LÕI (Hàm phân tích đã mô phỏng)
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
                st.write("Kiểm tra URL và trích xuất Video ID...")
                st.write("Đang lấy phụ đề video...")
                
                # Gọi hàm xử lý và nhận kết quả
                result = generate_response({"Video_URL": video_url})
                
                status.update(label="Phân tích hoàn tất!", state="complete", expanded=False)
            
            st.success("🎉 Báo cáo đã sẵn sàng!")
            st.session_state['report_result'] = result
        else:
            st.warning("⚠️ Vui lòng nhập URL của video trước khi tạo báo cáo.")


st.header("2. Kết quả")
if 'report_result' in st.session_state:
    st.markdown(st.session_state['report_result'])
else:
    st.info("Kết quả phân tích sẽ hiển thị ở đây sau khi bạn nhấn nút.")


