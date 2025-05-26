import streamlit as st
import os
from huffman import HuffmanCoding  

os.makedirs('Output', exist_ok= True)
os.makedirs('Input', exist_ok= True)

def delete_files_in_directory(directory_path):
    if os.path.exists(directory_path):
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)  
         
st.title("Bài tập lớn môn lý thuyết thông tin")
st.title("Nén và giải nén file bằng thuật toán huffman")

mode = st.radio("Chọn chế độ:", ("Nén", "Giải nén"))

uploaded_file = st.file_uploader("Chọn file")

if mode == "Giải nén":
    type_of_file_output = st.selectbox(
        "Chọn định dạng file sau khi giải nén:",
        ("txt", "doc", "docx", "jpg", "png", "mp4")
    )

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
            st.success("Đã nén xong")
            with open(output_path, "rb") as f:
                st.download_button("Tải file đã nén", f, file_name=output_path)
        else:
            output_path = 'Output/out_' + os.path.splitext(uploaded_file.name)[0] + '.' + type_of_file_output
            tool.decompress(input_path, output_path)
            st.success("Đã giải nén xong!")
            with open(output_path, "rb") as f:
                st.download_button("Tải file đã giải nén", f, file_name=output_path)
        uploaded_file = None

        os.remove(input_path)
        os.remove(output_path)
