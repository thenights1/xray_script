import json


def clean_json(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    allowed_plugins = ['poc-yaml','sqldet','cmd-injection','brute-force','upload','xxe']  # 允许保留的plugin元素列表

    cleaned_data = [entry for entry in data if any(plugin in entry.get('plugin') for plugin in allowed_plugins)]

    final_data = []
    # 过滤sso
    for ele in cleaned_data:
        if("sso" in ele['detail']['addr']): 
            continue
        else: 
            final_data.append(ele)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=4)

def handle_json(input_file, base_html, html_path):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open(base_html, 'r', encoding='utf-8') as h:
        html_data = h.read()
    num = len(data)
    # print(num)
    if(num == 0): return []
    num_high = 0
    num_medium = 0
    # 统计数量并且生成html文件
    for element in data:
        if('poc-yaml' in element.get('plugin')):
            num_high += 1
        if('cmd-injection' in element.get('plugin')):
            num_high += 1
        # 生成html内容
        # print(len(element['detail']['snapshot'][0][1]))
        if(len(element['detail']['snapshot'][0][1]) > 10000):
            element['detail']['snapshot'][0][1] = "返回包过长，仅展示前10000个字符" + element['detail']['snapshot'][0][1][:10000]
        json_str = json.dumps(element)
        html_data = html_data + "<script class=\'web-vulns\'>webVulns.push(" + json_str + ")</script>"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_data)
    num_medium = num - num_high
    return [num_high,num_medium]
