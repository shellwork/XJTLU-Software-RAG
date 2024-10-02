import re
import json
import openai

# 第一步: 处理文本并移除换行符
def process_text(input_file_path, output_file_path, sentences_per_paragraph=15):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read().replace('\n', '')

    paragraph = []
    sentence_count = 0
    paragraphs = []

    for sentence in content.split('。'):
        if sentence:
            paragraph.append(sentence + '。')
            sentence_count += 1
            if sentence_count >= sentences_per_paragraph:
                paragraphs.append('《问题》\n' + ''.join(paragraph))
                paragraph = []
                sentence_count = 0

    if paragraph:
        paragraphs.append('《问题》\n' + ''.join(paragraph))

    with open(output_file_path, 'w', encoding='utf-8') as file:
        for paragraph in paragraphs:
            file.write(paragraph + '\n\n')

    print('文件处理中.....')

# 第二步: 使用OpenAI模型生成问答对
def chat_with_gpt3_5(user_input, max_retries=3):
    api_key = ""
    openai.api_base = "https://api.xty.app/v1"

    system_message = {
        "role": "system",
        "content": "把其中关键的内容提取出来，制作成我需要的对话数据集的格式，也就是常见的问答数据语料，请不要用第三视角制作数据集。请你用第一或者第二视角例如：问:你觉得为什么我总是倒霉？答:我觉得你太消极了，你可以多关注一些别的好的一方面。不要总关心坏的一方面。仿照我给的例子用问: 答: 这样的格式制作数据集。最后，问答对中，在答的部分，要给出足够长的回答。下面是原文："
    }
    user_message = {"role": "user", "content": user_input}

    for attempt in range(1, max_retries + 1):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[system_message, user_message],
                api_key=api_key
            )
            assistant_reply = response['choices'][0]['message']['content']
            return assistant_reply
        except Exception as e:
            print(f"处理问题时出错，尝试次数：{attempt}/{max_retries}。错误信息：{e}")
            if attempt == max_retries:
                return f"重试{max_retries}次后仍然失败，错误信息：{e}"

def batch_chat_with_gpt3_5_immediate_print_and_save(question_list, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for question in question_list:
            answer = chat_with_gpt3_5(question)
            print(f"Assistant: {answer}\n")
            file.write(f"{answer}\n\n")

def load_questions_from_file(file_path):
    questions = []
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        questions = content.split("《问题》")[1:]
        questions = [q.strip() for q in questions]
    return questions

# 第三步: 格式化生成的问答对文本
def format_text(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    questions = re.split('问[：:]\s*', content)[1:]

    formatted_text = ''
    for q in questions:
        if re.search('答[：:]\s*', q):
            parts = re.split('答[：:]\s*', q, 1)
            question, answer = parts[0], parts[1]
            formatted_question = '问：' + question.strip()
            formatted_answer = '答：' + answer.replace('\n', ' ').strip()
            formatted_answer = re.sub(r'(\d+)\.', r' \1.', formatted_answer)
            formatted_text += f'{formatted_question}\n{formatted_answer}\n\n'
        else:
            formatted_text += '问：' + q.strip() + '\n\n'

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(formatted_text)

# 第四步: 转换为LLM格式
def convert_file_to_llm_format(file_path):
    llm_data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for i in range(len(lines) - 1):
            if lines[i].startswith('问：') and lines[i+1].startswith('答：'):
                instruction = lines[i].split('问：', 1)[1].strip()
                output = lines[i+1].split('答：', 1)[1].strip()
                llm_data.append({
                    "instruction": instruction,
                    "input": "",
                    "output": output
                })
    return llm_data

def save_llm_data_to_file(llm_data, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(llm_data, file, ensure_ascii=False, indent=4)

# 主函数: 整合所有步骤
def main():
    # 路径配置
    raw_text_path = '/root/LLaMA-Factory/数据集全自动处理/受刑文本.txt'
    processed_text_path = '/root/LLaMA-Factory/chuli/重生文本.txt'
    gpt_output_path = '/root/LLaMA-Factory/chuli/内容回复.txt'
    formatted_output_path = '/root/LLaMA-Factory/chuli/内容回复2.txt'
    final_llm_output_path = '/root/LLaMA-Factory/data/train2.json'

    # 处理文本
    process_text(raw_text_path, processed_text_path)

    # 使用模型生成问答对
    questions = load_questions_from_file(processed_text_path)
    batch_chat_with_gpt3_5_immediate_print_and_save(questions, gpt_output_path)

    # 格式化文本
    format_text(gpt_output_path, formatted_output_path)

    # 转换为LLM格式并保存
    llm_formatted_data = convert_file_to_llm_format(formatted_output_path)
    save_llm_data_to_file(llm_formatted_data, final_llm_output_path)

    print(f'最终数据已成功保存到文件：{final_llm_output_path}')

if __name__ == "__main__":
    main()
