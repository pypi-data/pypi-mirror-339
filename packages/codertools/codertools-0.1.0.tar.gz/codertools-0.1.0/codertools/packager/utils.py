import os


def save_to_file(markdown, base_path,filename="output.md"):
    os.makedirs(base_path, exist_ok=True)
    file_path = os.path.join(base_path,filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"Markdown content saved to {filename}")


def create_file_structure(data, base_path=".", overwrite=False):
    """
    递归创建文件夹和文件结构，增加防止覆盖和异常处理
    """
    # 检查 data 是否为字典
    if not isinstance(data, dict):
        print(f"数据类型不正确，跳过处理: {data}")
        return

    for key, value in data.items():
        if value.get("type") == "folder":
            try:
                # 创建文件夹
                folder_path = os.path.join(base_path, key)
                os.makedirs(folder_path, exist_ok=True)
                
                # 创建与文件夹同名的 Markdown 文件
                folder_md_file = os.path.join(folder_path, f"{key}.md")
                
                # 检查文件是否已存在
                if os.path.exists(folder_md_file) and not overwrite:
                    print(f"文件已存在，跳过创建: {folder_md_file}")
                    continue
                
                with open(folder_md_file, "w", encoding="utf-8") as f:
                    f.write(value.get("text", ""))
                
                # 递归处理文件夹内容
                if "context" in value:
                    # 确保 context 是一个字典
                    if isinstance(value["context"], dict):
                        create_file_structure(value["context"], folder_path, overwrite)
                    else:
                        print(f"context 不是字典，跳过处理: {value['context']}")
            except Exception as e:
                print(f"创建文件夹或文件时出错: {e}")
        elif value.get("type") == "md":
            try:
                # 创建 Markdown 文件
                file_name = key.replace(" ", "_").lower() + ".md"
                file_path = os.path.join(base_path, file_name)
                
                # 检查文件是否已存在
                if os.path.exists(file_path) and not overwrite:
                    print(f"文件已存在，跳过创建: {file_path}")
                    continue
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(value.get("text", ""))
            except Exception as e:
                print(f"创建文件时出错: {e}")


def parse_markdown_to_custom_structure(markdown_content: str, folder_name: str = "Alias") -> dict:
    # 将Markdown内容按二级标题分割
    parts = markdown_content.split("\n## ")
    
    result = {}
    
    # 处理第一个部分（可能没有二级标题）
    if parts[0].strip():
        # 将第一部分作为文件夹同名文件的数据
        result[folder_name] = {
            "type": "folder",
            "context": {}  # 初始化为空字典
        }
    
    md_titles = []  # 用于存储所有md单元的标题
    
    # 处理剩下的部分
    for part in parts[1:]:
        # 将每个部分按第一个换行符分割为标题和内容
        if "\n" in part:
            title, content = part.split("\n", 1)
            md_entry = {
                "type": "md",
                "text": content.strip()
            }
            # 将MD条目直接添加到context字典中
            result[folder_name]["context"][title] = md_entry
            md_titles.append(title)  # 添加标题到md_titles列表
    
    # 动态生成folder的text字段
    if folder_name in result:
        text_content = "\n".join(f"[[{title}]]" for title in md_titles)
        result[folder_name]["text"] = text_content
    
    return result
