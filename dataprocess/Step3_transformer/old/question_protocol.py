# -*- coding: utf-8 -*-

import os
import json
import concurrent.futures
from openai import OpenAI

# 设置API密钥
api_key = ''
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# 初始化OpenAI客户端
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

# 定义文件夹路径
text_folder = './data/wiki_texts'
output_json_folder = './data/json_outputs_qa/'
error_folder = './data/error_files/'

# 确保错误文件夹存在
os.makedirs(error_folder, exist_ok=True)

# 读取文本文件
def read_text_files(text_folder):
    data = {}
    for filename in os.listdir(text_folder):
        if filename.endswith('.txt'):
            with open(os.path.join(text_folder, filename), 'r', encoding='utf-8') as file:
                content = file.read()
                data[filename] = content
    return data

# 调用OpenAI API进行总结
def summarize_text(text):
    prompt = f"""
请根据以下 iGEM 讲述合成生物学实验文档的内容生成问答对。如有可能，至少应有 10 对问答。每对问答应根据文档信息回答一个具体问题。上下文长度应至少为 3 句话，并与文档内容完全一致，不得有任何修改。答案应尽可能详细，超过 2 句话。问答对应尽可能多地涵盖文档内容，重点关注实验设计方案、使用材料和最终结果。

[
    {{
        "instruction": "用户问题或者叫prompts",
        "input": "上下文信息",
        "output": "模型的回答"
    }}
]

Example output:
[
    {{
        "instruction": "What methods did the Aalto-Helsinki iGEM team use for their ribosome display experiments?",
        "input": "The Aalto-Helsinki iGEM team in 2022 focused their experiments on ribosome display, bioreporter cloning, and GFP-DARPin expression. Ribosome display was chosen for protein-peptide binding assays, with the aim of proving the method with a known protein-protein binding. They used GFP binding DARPins as the test targeting protein and GFP as the target protein. The bioreporter was designed to produce membrane and internal signaling proteins to bind signaling molecules and give an output to show that the cell has received the binding information.",
        "output": "The Aalto-Helsinki iGEM team used in vitro transcription and translation for their ribosome display experiments. They aimed to produce their own GFP protein by expressing superfold-GFP in E. coli expression cells. The ribosome display method ensured that the targeting protein did not have a stop codon, allowing the peptide to be far out from the ribosome but still attached. They tested both their own AIP binding DARPins and known GFP binding DARPins, and sequenced the mRNA to identify the best-binding DARPin."
    }},
    {{
        "instruction": "How did the Aalto-Helsinki iGEM team construct and test their bioreporter?",
        "input": "The bioreporter experiment conducted by the Aalto-Helsinki iGEM team was inspired by the 2021 iGEM team from IISER Kolkata. They aimed to clone two composite parts, one for GFP transcription and one for the membrane protein AgrC and internal signaling protein AgrA. The goal was to measure GFP fluorescence when the bioreporter cells were induced with AIP molecules.",
        "output": "The Aalto-Helsinki iGEM team constructed their bioreporter by ordering and cloning two composite parts from IDT. They tested the bioreporter by measuring GFP fluorescence in cells induced with AIP molecules. They also aimed to test the effect of DARPins on GFP intensity, but due to time constraints, they only tested AIP inducement. They used different concentrations of AIP to observe the effect on GFP signal and confirmed the functionality of the bioreporter by comparing the GFP signal from bioreporter cells to negative controls."
    }},
    {{
        "instruction": "What was the aim and outcome of the GFP-DARPin synthesis experiment by the Aalto-Helsinki iGEM team?",
        "input": "In their GFP-DARPin synthesis experiment, the Aalto-Helsinki iGEM team aimed to express a GFP binding DARPin with a His-tag and Avi-tag for purification and downstream processing. They used a pET42b-HF-BE3 plasmid and transformed it into BL21 E. coli expression cells. The protein was extracted and purified, although most remained in the pellet.",
        "output": "The aim of the GFP-DARPin synthesis experiment was to express a GFP binding DARPin with His-tag and Avi-tag for purification and downstream processing. The team used a pET42b-HF-BE3 plasmid, transformed it into BL21 E. coli expression cells, and induced the cells with IPTG. Despite attempts to improve expression and extraction, most of the expressed protein remained in the pellet. The best results were obtained at 20°C overnight induction. Due to time constraints, they proceeded with in vitro transcription and translation for their collaboration with TU Dresden."
    }}
]

Please summarize the following content:

{text}
"""
    try:
        response = client.chat.completions.create(
            model="qwen-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return ""

# 保存 JSON 文件
def save_to_json(output_json_path, data):
    try:
        with open(output_json_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving to JSON: {e}")

# 保存错误文件
def save_to_error_file(filename, content):
    error_file_path = os.path.join(error_folder, filename)
    try:
        with open(error_file_path, 'w', encoding='utf-8') as errorfile:
            errorfile.write(content)
        print(f"Saved erroneous file to {error_file_path}")
    except Exception as e:
        print(f"Error saving erroneous file: {e}")

# 处理单个任务
def process_file(filename, content, output_json_folder):
    summary = summarize_text(content)
    if summary:
        try:
            json_data = json.loads(summary)
            output_json_path = os.path.join(output_json_folder, os.path.splitext(filename)[0] + ".json")
            save_to_json(output_json_path, json_data)
            print(f"Summarized and saved JSON for {filename}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON for {filename}: {e}")
            save_to_error_file(filename, summary)

# 主函数
def main():
    data = read_text_files(text_folder)
    print(f"Total files to process: {len(data)}")

    # 确保输出文件夹存在
    os.makedirs(output_json_folder, exist_ok=True)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_file, filename, content, output_json_folder) for filename, content in data.items()]
        concurrent.futures.wait(futures)

    print(f"Summary JSONs generated in {output_json_folder}")

if __name__ == "__main__":
    main()
