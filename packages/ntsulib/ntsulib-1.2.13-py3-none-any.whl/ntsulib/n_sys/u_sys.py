import chardet
def get_file_bom(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read(4)
    if raw_data.startswith(b'\xff\xfe\x00\x00') or raw_data.startswith(b'\x00\x00\xfe\xff'):
        return 'UTF-32'
    elif raw_data.startswith(b'\xff\xfe') or raw_data.startswith(b'\xfe\xff'):
        return 'UTF-16'
    elif raw_data.startswith(b'\xef\xbb\xbf'):
        return 'UTF-8'
    else:
        return None
def get_file_encoding(file_path, candidate_encodings=['utf-8', 'gbk', 'iso-8859-9']):
    # 先尝试检测 BOM
    bom_encoding = get_file_bom(file_path)
    if bom_encoding:
        return bom_encoding
    # 如果 BOM 不存在，尝试手动检测
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    # 优先尝试候选编码
    for encoding in candidate_encodings:
        try:
            raw_data.decode(encoding)
            return encoding
        except UnicodeDecodeError:
            continue
    # 如果候选编码都失败，再使用 chardet
    result = chardet.detect(raw_data)
    if result['confidence'] > 0.9:  # 只有当可信度较高时才返回
        return result['encoding']
    else:
        return None

# 自动解析编码并获取文件的内容
def get_file_content(file_path, candidate_encodings=['utf-8', 'gbk', 'iso-8859-9']):
    # 检测文件编码
    encoding = get_file_encoding(file_path, candidate_encodings)
    if encoding is None:
        # print("无法确定文件的编码格式。")
        return None
    # 打开文件并读取内容
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            content = file.read()
        # print(f"文件内容（编码: {encoding}）:")
        #print(content)
        return content
    except UnicodeDecodeError:
        # print(f"无法使用编码 {encoding} 解码文件。")
        return None