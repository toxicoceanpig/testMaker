from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
import agentTool as tool
import cleanCot as clean

### Kw

#pdf的地址
pdfs_directory = '/Users/kaiwenliu/Downloads/'

#模型选择

embeddings = OllamaEmbeddings(model="deepseek-r1:1.5b")
model = OllamaLLM(model="deepseek-r1:1.5b")

# embeddings = OllamaEmbeddings(model="llama3.2:1b")
# model = OllamaLLM(model="llama3.2:1b")



#模版定义
template = """
You are an **AI that generates exam-style questions** from a provided context.  
Your task is to **ONLY generate a question**, and DO NOT answer it.

📌 **Instructions**:
- Generate a **short answer** or **multiple-choice** question.
- **DO NOT explain**.
- **DO NOT answer**.
- **DO NOT produce answer**.
- If there is not enough context, respond: **"I don't have enough information to generate a question."**

📌 **Examples**:
1️⃣ **Context**: Newton’s laws of motion describe how objects move.
   **Topic**: Physics - Newton’s Laws
   **Generated Question**: What are the three laws of motion proposed by Newton?

2️⃣ **Context**: The capital of France is Paris.
   **Topic**: Geography - Capitals
   **Generated Question**: What is the capital of France?

Now, generate a question based on the following:

📖 **Context**:
{context}

💡 **Topic**: {input}

❓ **Generated Question**:
"""

#上传pdf
def upload_pdf(file):
    with open(pdfs_directory + file.name, "wb") as f:
        f.write(file.getbuffer())

#根据pdf内容生成向量数据存储
def create_vector_store(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=300,
        add_start_index=True
    )

    chunked_docs = text_splitter.split_documents(documents)
    db = FAISS.from_documents(chunked_docs, embeddings)
    return db

#根据问询在向量数据库中检索
def retrieve_docs(db, query, k=4):
    print(db.similarity_search(query))
    return db.similarity_search(query, k)

#生成相关问题并且调用agent生成pdf问卷
def question_pdf(input, documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    questions =  chain.invoke({"input": input, "context": context})
    print(questions)

    # 确保 `questions` 是字符串
    if isinstance(questions, dict) and "text" in questions:
        questions = questions["text"]

    questions = clean.clean_llm_output(questions)
    questions_formatted = questions.replace("\n", "<br>")

    # return questions
    return tool.save_exam_to_pdf(questions_formatted)


