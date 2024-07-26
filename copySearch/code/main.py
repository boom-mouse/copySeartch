import re
import pyperclip
import json

# 打开配置文件
file_path = "config.js"
def read_js_file(file_path):
    try:
        with open(file_path, 'r', encoding="utf8") as file:
            js_content = json.loads(file.read())
            return js_content

    except FileNotFoundError:
            print(f"找不到文件'{file_path}' 检查文件名和路径啊喂！￣へ￣")
            exit()
    except IOError:
            print(f"咋回事，打不开'{file_path}' ＞︿＜")
            exit()

# 导入配置
texts = []
keywords = []
sleep_time = -1
def import_config():
    try:
        json_content = read_js_file("config.json")
        global texts
        texts = json_content["texts"]
        global keywords
        keywords = json_content["keywords"] if (json_content["keywords_enable"]) else []
        global sleep_time
        sleep_time = json_content["sleep_time"]
    except Exception as e:
        print(e)
        print("配置文件导入出错，请检查配置文件是否填写完整")
        print("以下为配置内容：")
        must = {
            "sleep_time":"必填-正整数-休眠时间，单位秒",
            "keywords_enable":"必填-布尔值-是否使用关键词高亮，设置为false则搜索词高亮",
            "keywords":"选填-字符串数组-如果启用了关键词高亮，请填入字符串数组的形式",
            "texts":"必填-字符串数组-文本库"
        }
        for i in must:
            print(i,":",must[i])
        exit()
import_config()

# 已经搜索过的文本列表
searched_texts = []

def highlight_keywords(text, keywords):
    highlighted_text = text
    for keyword in keywords:
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        highlighted_text = pattern.sub(r'\033[91m\g<0>\033[0m', highlighted_text)
    return highlighted_text

def search_and_highlight(text_to_search, keywords):
    global searched_texts
    # 如果复制的是上次输出的内容（完整文本），则不进行重复搜索
    if text_to_search in searched_texts:
        return
    

    searched_texts = []     # 复制的内容不是上一次输出,清空搜索列表
    found_any = False
    for text in texts:
        if text_to_search.lower() in text.lower():
            highlighted_text = highlight_keywords(text, keywords)
            print(highlighted_text)
            found_any = True
            # 将文本添加到已搜索列表
            searched_texts.append(text)
    if found_any:
        print("--------------------")
    if not found_any:
        print(f"未找到含有 '{text_to_search}' 的文本T_T")


def monitor_clipboard():
    last_copied_text = ""
    while True:
        copied_text = pyperclip.paste().strip()
        if copied_text != last_copied_text:     # 防止重复搜索
            last_copied_text = copied_text

            search_and_highlight(copied_text, keywords=[copied_text] if not keywords else keywords)       # 关键词高亮，配置文件中修改，如果未启用则是搜索词高亮
        
        # 自己设置合适的休眠时间
        time.sleep(sleep_time)

if __name__ == "__main__":
    import threading
    import time


    # 启动剪贴板监视线程
    clipboard_thread = threading.Thread(target=monitor_clipboard)
    clipboard_thread.daemon = True
    clipboard_thread.start()

    print("要退出请同时按下 Ctrl+C 或者直接右上角关闭（￣︶￣）↗")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...")
