import requests
import json

def send_msg_to_feishu(webhook_url, msg):
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url=webhook_url, headers=headers, data=json.dumps(msg))
    if response.status_code == 200:
        print("消息发送成功")
        print(response.text)
    else:
        print("消息发送失败，错误代码：", response.status_code)

# def gen_csv(input_file):
#     with open(input_file, 'r', encoding='utf-8') as f:
#         data = json.load(f)
    
def gen_msg_and_send(input_file,url, num, html_url):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    content = "发现高危漏洞{}个，发现中危漏洞{}个，详细信息可以查看http://162.14.151.236:1333/{}".format(num[0],num[1],html_url)
    num_f = num[0] + num[1]
    msg = {
        "msg_type": "interactive",
        "card": {
            "elements": 
            [   
                {
                "tag": "div",
                "text": {
                        "content": content,
                        "tag": "lark_md"
                        }
                },
                {
                    "tag": "table", 
                    "page_size": 5,
                    "row_height": "low", 
                    "header_style": {
                        "lines": 1 
                    },
                    "columns": [ 
                        { 
                            "name": "vuln_name", 
                            "display_name": "漏洞类型", 
                            "data_type": "lark_md"
                        },
                        { 
                            "name": "vuln_link",
                            "display_name": "漏洞链接",
                            "data_type": "lark_md"
                        },
                        { 
                            "name": "vuln_scale",
                            "display_name": "漏洞评级",
                            "data_type": "options"
                        },
                        { 
                            "name": "vuln_date",
                            "display_name": "发现时间",
                            "data_type": "date",
                            "date_format": "YYYY/MM/DD"
                        },
                    ],
                    "rows": [ 
                    ]
                }
            ],
            "header": {
                    "title": {
                            "content": "漏洞推送-XRAY",
                            "tag": "plain_text"
                    }
            }
        }
    }

    for element in data:
        new_row = {
            "vuln_name": element['plugin'],
            "vuln_date": element['create_time'],
            "vuln_scale": [
                {
                    "text": "中危",
                    "color": "blue"
                }
            ],
            "vuln_link": "[漏洞链接]({})".format(element['target']['url'])
        }   
        if('poc-yaml' in element.get('plugin') or 'cmd-injection' in element.get('plugin')):
            new_row['vuln_scale'][0]['text'] = "高危"
            new_row['vuln_scale'][0]['color'] = "red"
        msg['card']['elements'][1]['rows'].append(new_row)
    # print(json.dumps(msg))
    send_msg_to_feishu(url, msg)



