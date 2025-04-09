"""

issue_document = read_github_issue(owner="tqdm",repo="tqdm")

issue_document[2]

print(issue_document[2].dict().get('text'))

"https://api.github.com/repos/tqdm/tqdm/issues/454/comments"
"""

import requests
import json
import re

def extract_comments(url):
    # 发送 GET 请求获取数据
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        return None
    
    # 解析 JSON 数据
    try:
        data = response.json()
    except json.JSONDecodeError:
        print("Failed to parse JSON")
        return None
    
    return data

def convert_to_markdown(comments):
    markdown = ""
    
    for comment in comments:
        user = comment.get("user", {}).get("login", "Unknown User")
        created_at = comment.get("created_at", "")
        body = comment.get("body", "")
        
        # 转义 Markdown 特殊字符
        body = re.sub(r'([\\`*_{}[\]()#+\-.!])', r'\\\1', body)
        
        markdown += f"### Comment by {user} ({created_at})\n"
        markdown += f">{body}\n\n"
    
    return markdown

def save_to_file(markdown, filename="output.md"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"Markdown content saved to {filename}")

def get_comments(url):
    comments = extract_comments(url)
    if comments:
        markdown = convert_to_markdown(comments)
        return markdown
    return None
