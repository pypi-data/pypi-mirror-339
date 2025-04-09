from .reader import read_github_issue,read_github_repo
from .utils import save_to_file,create_file_structure, parse_markdown_to_custom_structure
from .utils2 import get_comments
from datetime import datetime
import time
import os


template = """---
topic: {topic}
describe: {describe}
creation date: {date}
type: 案例
tags: []
status:
链接: {link}
---
"""

def process_github_repo(base_path:str="./test_md",github_path:str = "tqdm/tqdm",overwrite_files:bool=True)->None:
    """
    从GitHub存储库读取文档，解析其Markdown内容并创建文件结构.   

    base_path : 基础路径   

    github_path : 目标仓库 tqdm/tqdm   
    """
    owner,repo = github_path.split('/')
    docs_documents = read_github_repo(owner=owner, repo=repo)

    file_dict = {}
    for docs_document in docs_documents:
        file_name = docs_document.metadata.get("file_name")[:-3]
        text = docs_document.text
        structure = parse_markdown_to_custom_structure(markdown_content=text,
                                                       folder_name=file_name)
        file_dict.update(structure)

    # overwrite_files = True
    create_file_structure(file_dict, base_path=base_path, overwrite=overwrite_files)

def process_github_issues(base_path:str = "./test2_md",github_path:str = "tqdm/tqdm")->None:
    """
    从GitHub读取问题，生成相应的Markdown文件。   

    base_path : 基础路径   
    github_path : 目标仓库 tqdm/tqdm   
    """

    owner,repo = github_path.split('/')
    issue_documents = read_github_issue(owner=owner, repo=repo)

    issues = {}
    for issue_document in issue_documents:
        question = issue_document.text
        http_url = os.path.join(issue_document.metadata.get('url'), 'comments')
        # answer_markdown = get_comments(http_url)
        # answer_markdown = answer_markdown or ''
        answer_markdown = ''
        topic = question[:20].replace('/','_').replace('\n','_')
        values = template.format(topic = topic,
                        describe =question,
                        date = datetime.today().strftime("%Y-%m-%d"),
                        link = http_url)
        issues.update({topic:values + '\n\n' + answer_markdown})

    for topic,content in issues.items():
        save_to_file(content,base_path,f"{topic}.md")

