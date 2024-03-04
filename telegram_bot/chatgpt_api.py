import openai
import json
def request(prompt):
    with open('setings.json', 'r') as f:
        config = json.load(f)
    openai.api_key = config["gpt_api_key"]
    engine = "text-davinci-003"
    completion = openai.Completion.create(engine=engine,
                                          prompt=prompt,
                                          temperature=0.5,
                                          max_tokens=1000)
    return completion.choices[0]['text']
