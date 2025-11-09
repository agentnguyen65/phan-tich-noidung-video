import streamlit as st
import time

# -----------------------------------------------
# PHẦN LOGIC API (Tương đương Bước 2 - Sẽ gọi tới SPG lõi thực tế)
# -----------------------------------------------
def generate_response_spg(video_url):
    """
    Hàm này mô phỏng việc gọi đến SPG lõi để phân tích video từ URL.
    Trong ứng dụng thực tế, phần này cần được kết nối với thư viện
    xử lý YouTube và mô hình ngôn ngữ/API phân tích.
    """
    if not video_url or not "youtube.com" in video_url:
        return "Lỗi: Vui lòng nhập một đường dẫn YouTube (URL) hợp lệ."

    # Mô phỏng quá trình xử lý mất thời gian
    with st.spinner('Đang phân tích video và xây dựng báo cáo...'):
        time.sleep(4)  # Giả lập thời gian xử lý

    # KẾT QUẢ ĐẦU RA BẮT BUỘC (OUTPUT_SCHEMA)
    result = f"""
# 📝 Báo Cáo Phân Tích Nội Dung Video Học Thuật

**Video URL:** `{video_url}`
---

## 🎬 Tóm Tắt Nội Dung Video
Đây là phần tóm tắt chính xác, tập trung vào các điểm học thuật quan trọng nhất mà video truyền tải.

## 🔬 Phân Tích Chi Tiết Nội Dung Học
Nội dung học được phân tích sâu, tập trung vào phương pháp, lý thuyết và các ví dụ được sử dụng trong video.

## 🎙️ Đánh Giá Giọng Văn
Người hướng dẫn sử dụng giọng văn **Chuyên nghiệp, có tính học thuật** (Ví dụ). Giọng điệu rõ ràng, tốc độ vừa phải, rất phù hợp cho nội dung đào tạo chuyên sâu.

## ⏱️ Danh Sách Các Nội Dung Học Kèm Mốc Thời Gian (Timestamp)
* **[00:00 - 00:45]:** Giới thiệu đề tài và định hướng mục tiêu học tập.
* **[00:46 - 03:10]:** Khái niệm cốt lõi 1: **(Tên khái niệm)** và ứng dụng.
* **[03:11 - 06:50]:** Phân tích chi tiết trường hợp nghiên cứu: **(Tên case study)**.
* **[06:51 - END]:** Tóm tắt các điểm chính và các bước tiếp theo.
"""
    return result

# -----------------------------------------------
# CẤU TRÚC GIAO DIỆN WEB APP (Streamlit UI)
# -----------------------------------------------
st.set_page_config(page_title="SPG-WebApp: Phân Tích Video Học Thuật", layout="centered")

st.title("📺 SPG-WebApp: Công Cụ Phân Tích Video Học Thuật")
st.markdown("Chuyển đổi URL video YouTube thành báo cáo học thuật chi tiết kèm mốc thời gian.")

# --- Ô nhập thông tin (INPUT_SCHEMA) ---
video_url_input = st.text_input(
    label="**1. Nhập Mã URL Video YouTube Cần Phân Tích**",
    placeholder="Dán đường dẫn video YouTube tại đây (ví dụ: https://www.youtube.com/watch?v=XXXXXXX)"
)

# --- Nút “Tạo kết quả” ---
if st.button("🚀 Tạo Báo Cáo Phân Tích", type="primary"):
    if video_url_input:
        # Gọi hàm logic xử lý
        report = generate_response_spg(video_url_input)
        
        # --- Khung hiển thị kết quả (OUTPUT_SCHEMA) ---
        st.subheader("Báo Cáo Phân Tích Đã Hoàn Thành")
        st.markdown(report)
    else:
        st.error("Vui lòng nhập Mã URL Video để tiếp tục.")
