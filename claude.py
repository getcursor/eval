import aiohttp
import os

ANTHROPIC_HEADERS = {
    "X-API-Key": os.environ['ANTHROPIC_API_KEY'],
    "Content-Type": "application/json",
 }

async def claude_complete(prompt: str, model: str, temperature=0.0):
  async with aiohttp.ClientSession() as session:
    print('Running claude')
    response = await session.post('https://api.anthropic.com/v1/complete', 
                                  headers=ANTHROPIC_HEADERS, 
                                  json={
        "prompt": prompt,
        "model": model,
        "max_tokens_to_sample": 500,
        "temperature": temperature,
        # "n": num_tries,
        "stream": False,
        "stop": "```"
        # "logprobs": None,
    })
    data = await response.json()
    # print(repr(data))
    completion = data['completion']
    if completion.endswith('```'):
      completion = completion[:-3]
    print(prompt)
    print('_____')
    print(completion)
    print('\n\n\n')

    return [completion]