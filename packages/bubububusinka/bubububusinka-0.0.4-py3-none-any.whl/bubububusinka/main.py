DS_API = "sk-33a6bc022a774cda9ae54a7d809707e6"

import argparse
from openai import OpenAI

def main():
    parser = argparse.ArgumentParser(description="meow meow meow")
    parser.add_argument("model", 
                        type=str, 
                        help="default (deepseek-chat)  | r1 (deepseek-reasoner)")
    parser.add_argument("input", 
                        type=str, 
                        help="insert you question to deepseek")
    parser.add_argument("--api_key",
                        type=str,
                        default=DS_API,
                        help="insert path to your file.txt with deepseek question")
    parser.add_argument("--temperature",
                        type=int,
                        default=0,
                        help="Coding|Math = 0 \n  Data Cleaning|Data Analysis = 1.0 \n General_Conversation = 1.3 \n  Translation|Creativity = 1.3")

    args = parser.parse_args()
    print(args)

    hmodel2model = {"default":"deepseek-chat",
                    "r1":"deepseek-reasoner"}

    model_type = hmodel2model[args.model]
    model_in = args.input
    model_key = args.api_key
    model_temperature = args.temperature
    client = OpenAI(api_key=model_key, base_url="https://api.deepseek.com")

    file_content = None
    with open(model_in) as f:
        file_content = f.read()

    response = client.chat.completions.create(
        model=model_type,
        messages=[
            {"role": "system", "content": file_content},
            {"role": "user", "content": model_in},
        ],
        stream=False,
        temperature=model_temperature
    )
    with open("out.txt", "w") as f:
        f.write(response.choices[0].message.content)
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main() 
