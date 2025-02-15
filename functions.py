import requests
from datetime import datetime

def get_task_output(AIPROXY_TOKEN, task):       
        proxy_url = 'https://aiproxy.sanand.workers.dev/openai/v1/chat/completions'
        headers = {
            'Content-Type': 'application/json',
            'Authorization' : 'Bearer {}'.format(AIPROXY_TOKEN) 
        }
        payload = {
            model: "gpt-4o-mini",
            messages: [
                {
                    role: "system",
                    content: "You are a python calculator, add two numbers when asked"
                },
                {
                    role: "user",
                    content: "Add {} and {}".format(a, b)
                }
            ],
            'temperature': 0,
            'max_tokens': 50
        }

        response = requests.post(url=proxy_url, headers=headers, json=payload)
        if response.ok:
            ai_response = response.json()
            result = ai_response['choices'][0]['message']['content'].strip()
            return result
        else:
            return "Error in AI Proxy"

def count_days(day:str):
    days = {"monday":0, "tuesday":1, "wednesday":2, "thursday":3, "friday":4, "saturday":5, "sunday":6}
    dayvalue = -1
    day = None
    for d in days:
        if d in day:
            dayvalue = days[d]
            day = d
            break
    try:
        with open("/data/dates.txt") as file:
            data = file.readlines()
            count = sum(l for line in data if datetime.strptime(line.strip(), "%Y-%m-%d").weekday() == dayvalue)
            file = open("/data/{}-count".format(day), "w")
            file.write(str(count))
            file.close()
    except:
        print("Error in counting days")

def extract_dayname(task:str):
    match = re.search(r'count\s+(\w+)', task)
    if match:
        return match.group(1)
    return ""
def extract_package(task:str):
    match = re.search(r'install\s+(\w+)', task)
    if match:
        return match.group(1)
    return ""
def get_correct_package(package:str):
    with open("packages.txt", "r", encoding="utf-8") as file:
        data = file.read().strip()
        packages = [line.strip() for line in data.split(" ")] 
        packages = ["numpy", "pandas", "matplotlib", "seaborn", "scikit-learn"]
        correct = []
        for p in packages:
            if fuzz.ratio(p, package) >= 90:
                correct.append(p)
        if correct:
            if len(correct) == 1:
                return correct[0]
            elif len(correct) >= 2:
                return correct[-1]
    return correct_package