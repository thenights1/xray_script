import os
import re
import argparse
from clean import clean_json
from clean import handle_json


# 扫描
def get_url(output):
    f = open("url.txt")
    lines = f.readlines()
    # 匹配http | https请求头
    pattern = re.compile(r'^(https|http)://')
    for line in lines:
        try:
            if not pattern.match(line.strip()):
                targeturl = "http://"+line.strip()
                outputfilename = line.strip().split('.')[0]
            else:
                targeturl = line.strip()
                name = targeturl[len("http://"):]
                outputfilename = line.strip().split('.')[0]
            # print(targeturl.strip())
            print(outputfilename)
            do_scan(targeturl.strip(), outputfilename, output)
        except Exception as e:
            print(e)
            pass
    f.close()
    print("Xray Scan End~")
    return

    
# 报告
def do_scan(targeturl,outputfilename,path):
    scan_command="xray webscan --basic-crawler {} --json-output ./{}/vuln-{}-__datetime__.json".format(targeturl, path, outputfilename)
    x = os.system(scan_command)
    #print(x)
    return

if __name__ == '__main__':
    
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(description='Example script to parse -o output.')
    # 添加命令行参数,输出数个json的文件夹名
    parser.add_argument('-o', '--output', help='output path after -o', required=True)
    # -h 后面接输出的html的名字
    parser.add_argument('-h', '--HTML', help='output html path after -h', required=True)
    # 解析命令行参数
    args = parser.parse_args()
    # 创建文件夹
    com = "mkdir {}".format(args.output)
    os.system(com)

    get_url(args.output)

    # 文件夹路径，包含多个要合并的 JSON 文件
    folder_path = "./{}/".format(args.output)
    # 目标合并后的 JSON 文件路径
    output_file = "./{}/merge.json".format(args.output)
    # 最终清洗后的文件路径
    final_file = "./{}/final.json".format(args.output)

    # 初始化一个空的列表来存储所有 JSON 数据
    merged_data = []

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                # 读取单个 JSON 文件的内容
                json_data = json.load(f)
                for single in json_data:
                    # 将读取的 JSON 数据添加到列表中
                    merged_data.append(single)

    # 合并后的 JSON 数据写入到新的 JSON 文件中
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)
    # 清洗数据
    clean_json(output_file, final_file)

    print(f'Cleaned JSON data written to {final_file}')
    # num为高危和低危数量
    num = []
    html_path = "../html/" + args.HTML + ".html"

    html_url = args.HTML + ".html"

    num = handle_json(final_file,"./vuln.html",html_path)

    webhook_url = "your feishu webhook url or other webhook url"

    gen_msg_and_send(final_file,webhook_url, num, html_url)





    

