# -*- coding: utf-8 -*-
import os
import json
import concurrent.futures
from openai import OpenAI
import time

# 设置API密钥和base_url
api_key = ''
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# 定义文件夹路径
text_folder = '/home/qiayi/project/webspider/new_protocol/data/wiki_texts'

# 定义输出JSON文件路径
output_json_folder = './data/json_outputs/'

# 定义失败日志文件路径
error_log = './data/error_log.txt'

# 定义缓存文件路径
processed_files_cache = './data/processed_files_cache.json'

# 函数：加载已经处理过的文件名
def load_processed_files(processed_files_cache):
    processed_files = set()
    if os.path.exists(processed_files_cache):
        try:
            with open(processed_files_cache, 'r', encoding='utf-8') as cache_file:
                processed_files = set(json.load(cache_file))
        except Exception as e:
            print(f"Error reading cache: {e}")
    return processed_files

# 函数：更新处理过的文件名缓存
def update_processed_files(processed_files_cache, processed_files):
    try:
        with open(processed_files_cache, 'w', encoding='utf-8') as cache_file:
            json.dump(list(processed_files), cache_file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error updating cache: {e}")

# 函数：读取并分组文本文件
def read_text_files(text_folder, processed_files):
    grouped_data = {}
    total_files = 0
    processed_count = 0

    for filename in os.listdir(text_folder):
        if filename.endswith('.txt'):
            total_files += 1
            if filename in processed_files:
                processed_count += 1
                print(f"File {filename} already processed, skipping.")
                continue

            parts = filename.split('_')
            if len(parts) < 3:
                print(f"Skipping file with unexpected format: {filename}")
                continue
            
            year = parts[0]
            team_name = parts[1]
            file_type = parts[2].replace('.txt', '')

            key = f"{year}_{team_name}_{file_type}"

            with open(os.path.join(text_folder, filename), 'r', encoding='utf-8') as file:
                content = file.read()
            
            if key not in grouped_data:
                grouped_data[key] = []
            grouped_data[key].append(content)

    print(f"Total files: {total_files}, Processed files: {processed_count}, Remaining files: {total_files - processed_count}")
    return grouped_data

# 函数：调用OpenAI API进行总结
def summarize_text(text, model_name="qwen-plus"):
    prompt = f"""
请根据以下内容生成一个JSON格式的输出，包含所有实验细节。JSON格式如下所示：

{{
  "team": "iGEM_Team_Name_Year",
  "project": {{
    "title": "Project_Title",
    "description": "Project_Description",
    "goals": ["Goal1", "Goal2", "Goal3"]
  }},
  "experiments": [
    {{
      "title": "Experiment_Title",
      "objective": "Objective of the experiment",
      "concepts": "Concepts underlying the experiment",
      "materials": [
        {{
          "name": "Material_Name",
          "dosage": "Dosage or amount"
        }}
      ],
      "methods": [
        {{
          "step": "Step_Description"
        }}
      ],
      "protocols": [
        {{
          "protocol_name": "Protocol_Name",
          "steps": [
            "Step_1_Description",
            "Step_2_Description"
          ]
        }}
      ],
      "results": [
        "Result_1_Description",
        "Result_2_Description"
      ]
    }}
  ]
}}

请按照上述格式总结以下内容：

{text}
"""
    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )
    completion = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )
    return completion.choices[0].message.content

# 函数：逐次更新保存 JSON 文件
def save_to_json(output_json_path, data):
    try:
        with open(output_json_path, 'w', encoding='utf-8', errors='replace') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving to JSON: {e}")

# 函数：记录错误日志
def log_error(error_log, filename, error_message=None, content=None):
    with open(error_log, 'a', encoding='utf-8', errors='replace') as log_file:
        log_file.write(filename + "\n")
        if error_message:
            log_file.write(error_message + "\n")
        if content:
            log_file.write(content + "\n")

# 函数：处理单个任务批次
def process_batch(batch, processed_files, processed_files_cache, output_json_folder, error_log, model_name):
    for key, texts in batch.items():
        filename = f"{key}.txt"  # 生成对应的文件名
        combined_text = "\n\n".join(texts)
        summary = summarize_text(combined_text, model_name)
        try:
            json_data = json.loads(summary)
            output_json_path = os.path.join(output_json_folder, f"{key}.json")
            save_to_json(output_json_path, json_data)
            processed_files.add(filename)
            update_processed_files(processed_files_cache, processed_files)  # 更新缓存文件
            print(f"Summarized and saved JSON for {key}")
        except json.JSONDecodeError as e:
            error_message = f"Error decoding JSON for {filename}: {str(e)}"
            log_error(error_log, filename, error_message, summary)
            print(error_message)

# 函数：生成任务批次
def generate_batches(grouped_data, batch_size):
    batches = []
    current_batch = {}
    count = 0
    for key, texts in grouped_data.items():
        current_batch[key] = texts
        count += 1
        if count >= batch_size:
            batches.append(current_batch)
            current_batch = {}
            count = 0
    if current_batch:
        batches.append(current_batch)
    return batches

# 主函数
def main():
    model_name = "qwen-long"  # 在此更改模型类别
    batch_size = 50  # 每个批次处理50个任务
    processed_files = load_processed_files(processed_files_cache)
    grouped_data = read_text_files(text_folder, processed_files)
    batches = generate_batches(grouped_data, batch_size)

    total_batches = len(batches)
    print(f"Total batches to process: {total_batches}")

    # 确保输出文件夹存在
    os.makedirs(output_json_folder, exist_ok=True)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_batch, batch, processed_files, processed_files_cache, output_json_folder, error_log, model_name) for batch in batches]
        concurrent.futures.wait(futures)

    print(f"Summary JSONs generated in {output_json_folder}")

if __name__ == "__main__":
    main()
