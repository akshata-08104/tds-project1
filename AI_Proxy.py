import requests
AIPROXY_TOKEN = 'eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIyZjMwMDE2ODhAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.jYmNTBqa8dPE-tPot4mREzIxIGhbHmwvccgWoh-qWX4'
def add_two_numbers(a, b):
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