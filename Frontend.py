import streamlit as st
import os
from huffman import HuffmanCoding  # import từ file huffman.py


def delete_files_in_directory(directory_path):
    # Kiểm tra xem thư mục có tồn tại không
    if os.path.exists(directory_path):
        # Lấy danh sách các file trong thư mục
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            # Kiểm tra xem đó có phải là file không
            if os.path.isfile(file_path):
                os.remove(file_path)  # Xóa file
        print(f"Tất cả các file trong thư mục {directory_path} đã được xóa.")
    else:
        print(f"Thư mục {directory_path} không tồn tại.")
        
st.title("Bài tập lớn môn lý thuyết thông tin")
st.title("Nén và giải nén file bằng thuật toán huffman")


# 1. Chọn chế độ
mode = st.radio("Chọn chế độ:", ("Nén", "Giải nén"))

# 2. Chọn file
uploaded_file = st.file_uploader("Chọn file")

# 3. Nếu ở chế độ Giải nén thì chọn định dạng đầu ra
if mode == "Giải nén":
    type_of_file_output = st.selectbox(
        "Chọn định dạng file sau khi giải nén:",
        ("txt", "jpg", "png", "doc", "docx", "mp4")
    )

# 4. Thực hiện nếu đã chọn file
if uploaded_file is not None:
    tool = HuffmanCoding()
    # Lưu file tạm
    input_path = f"Input/{uploaded_file.name}"
    if not os.path.exists(input_path):
        delete_files_in_directory("Input")
        with open(input_path, "wb") as f:
            f.write(uploaded_file.read())

    if st.button("Thực hiện"):
        if mode == "Nén":
            output_path = 'Output/out_' + os.path.splitext(uploaded_file.name)[0] + '.bin'
            tool.compress(input_path, output_path)
            st.success("Đã nén xong!")
            with open(output_path, "rb") as f:
                st.download_button("Tải file đã nén", f, file_name=output_path)
                # os.remove(input_path)
        else:
            # Tạo output path có đúng định dạng mở rộng
            output_path = 'Output/out_' + os.path.splitext(uploaded_file.name)[0] + '.' + type_of_file_output
            tool.decompress(input_path, output_path)
            st.success("Đã giải nén xong!")
            with open(output_path, "rb") as f:
                st.download_button("Tải file đã giải nén", f, file_name=output_path)
        uploaded_file = None
        # Xóa file tạm
        os.remove(input_path)
        os.remove(output_path)
