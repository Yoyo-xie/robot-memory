import csv
import json

# Read the CSV file
data = []
with open(r'E:\Users\My PromptTool\my_prompts.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append({
            'title': row['标题'],
            'category': row['分类'],
            'systemPrompt': row['系统指令'],
            'userPrompt': row['用户指令'],
            'date': row['添加时间']
        })

# Write to a temp file as JavaScript
js_content = "const PROMPTS_DATA=" + json.dumps(data, ensure_ascii=False) + ";"

with open(r'D:\Personal\Downloads\robot-memory-git\prompts_data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Converted {len(data)} prompts")
