from langchain.agents import initialize_agent, AgentExecutor, AgentType
from langchain.tools import Tool
import pdfkit
import main as main
from langchain_ollama.llms import OllamaLLM
from weasyprint import HTML

model = OllamaLLM(model="deepseek-r1:1.5b")

def save_exam_to_pdf(questions, filename="/Users/kaiwenliu/PycharmProjects/LangChain/testMaker/exam.pdf"):
    questions_formatted = questions.replace("\n", "<br>")
    html_template = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ text-align: center; }}
            .question {{ margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <h1>模拟考试题</h1>
        <hr>
        <div class="questions">
            {questions_formatted}
        </div>
    </body>
    </html>
    """

    HTML(string=html_template).write_pdf(filename)
    print(f"Exam saved as {filename}")
    return filename

# 定义 PDF 处理的 `Agent Tool`
pdf_tool = Tool(
    name="PDF Generator",
    func=save_exam_to_pdf,
    description="Converts generated questions into a formatted PDF file."
)

# 初始化 `Agent Chain`
agent_executor = initialize_agent(
    tools=[pdf_tool],
    llm=model,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)
