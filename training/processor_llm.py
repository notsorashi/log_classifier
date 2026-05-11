import os
from dotenv import load_dotenv
from groq import Groq
from typer import prompt

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY is not set in environment or .env file")

groq = Groq(api_key=api_key)



def classify_with_llm(log_message):

    allowed_categories = [
        "Workflow Error",
        "Deprecation Warning",
        "Unrecognized"
    ]

    prompt = f"""
You are a log classification assistant.

You MUST classify the log into ONLY one of these exact categories:

- Workflow Error
- Deprecation Warning
- Unrecognized

Do not create new labels.

Return ONLY the category name.

Log Message:
{log_message}
"""

    chat_completion = groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    response = chat_completion.choices[0].message.content.strip()

    if response not in allowed_categories:
        return "Unrecognized"

    return response

if __name__ == "__main__":
    logs = [
        "alpha.osapi.com - - [01/Jun/2024:10:00:00 +0000] \"GET /api/v1/resource HTTP/1.1\" 200 1234",
        "GET /api/v1/resource HTTP/1.1\" 200 1234",
        "User User123 logged in",
        "Multiple failed login attempts detected for user User123", 
        "Backup started at 2024-06-01 10:00:00",
        "System updated to version 2.1.0",
    ]
    for log in logs:
        print(f"Log: {log}\nPredicted Class: {classify_with_llm(log)}\n")
        
        