import os, hashlib, time, requests
from flask import Flask, request
import xml.etree.ElementTree as ET

app = Flask(__name__)
TOKEN = os.environ["WECHAT_TOKEN"]
KEY = os.environ["GEMAI_API_KEY"]

@app.route("/wechat", methods=["GET", "POST"])
def wechat():定义 微信():
    if request.method == "GET":
        a = sorted([TOKEN, request.args["timestamp"], request.args["nonce"]])
        if hashlib.sha1("".join(a).encode()).hexdigest() == request.args["signature"]:如果hashlib.sha1("".join(a).编码()).十六进制()等于 request.参数["签名"]:
            return request.args["echostr"]返回request.参数["echostr"]返回请求。参数["echostr"]
        return "no"返回 "no"

    root = ET.fromstring(request.data)
    text = root.find("Content").text
    user = root.find("FromUserName").text
    me = root.find("ToUserName").text

    try:尝试:
        r = requests.post("https://api.gemai.cc/v1/chat/completions",
            headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
            json={"model": "[CodeB]gemini-3.1-pro-preview",
                  "messages": [{"role": "user", "content": text}]},
            timeout=4)超时=4)超时=4)超时=4)
        answer = r.json()["choices"“选择”][0]["message"“消息”]["content"]答案 = r。json()["choices"][0]["message"]["content"]答案 = r.json()["choices"答案 = r。json()["choices"“选择”][0]["message"“消息”]["content"]答案 = r.json()["choices"][0]["message"]["content"]答案 = r。json()["choices"][0]["message"]["content"]答案 = r.json()["choices"][0]["message"]["content"]
    except:除了:
        answer = "稍后再试"答案 ="稍后再试"

    return f"""<xml><ToUserName><![CDATA[{user}]]></ToUserName>返回 f"""<xml><ToUserName><![CDATA[{用户}]]></ToUserName>返回 f"""<xml><ToUserName><![CDATA[{user}]]></ToUserName>返回 f"""用户}]]></ToUserName>返回 f"""<xml><ToUserName><![CDATA[{用户}]]></ToUserName>
<FromUserName><![CDATA[{me}]]></FromUserName>
<CreateTime>{int(time.time())}</CreateTime>
<MsgType><![CDATA[text]]></MsgType><MsgType><![CDATA[文本]]></MsgType>
<Content><![CDATA[{answer}]]></Content></xml>"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
