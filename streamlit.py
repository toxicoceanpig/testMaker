import streamlit as st
import main as main
import os

st.title("考试模拟生成器")


uploaded_file = st.file_uploader(
    "Upload PDF",
    type="pdf",
    accept_multiple_files=False
)

if uploaded_file:
    main.upload_pdf(uploaded_file)
    db = main.create_vector_store(main.pdfs_directory + uploaded_file.name)
    #用户输入考点
    topic = st.chat_input()

    if topic:
        st.chat_message("user").write(topic)
        related_documents = main.retrieve_docs(db, topic)
        # questions = main.question_pdf(topic, related_documents)
        # st.chat_message("assistant").write(questions)

        pdf_path = main.question_pdf(topic, related_documents)
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 下载生成的考试卷 PDF",
                data=f,
                file_name="exam.pdf",
                mime="application/pdf"
            )


