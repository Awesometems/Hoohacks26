from config import client, MODEL_NAME


def vulnerable_llm(prompt):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        timeout=10,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content