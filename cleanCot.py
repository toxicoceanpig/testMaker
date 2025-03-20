import re

def clean_llm_output(questions):
    """
    移除 LLM 生成的 `<think>...</think>` 段落
    """
    # ✅ 用正则表达式删除 `<think>...</think>` 及其内部所有内容
    cleaned_questions = re.sub(r'<think>[\s\S]*?</think>', '', questions, flags=re.MULTILINE)

    # ✅ 去除首尾空格
    return cleaned_questions.strip()