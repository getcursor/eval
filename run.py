"""
Runs the human eval dataset through code-davinci for a pass@k evaluation.

I didn't test pass@100 because I started running into the rate limit for
tokens/minute.

"""

import aiohttp
import asyncio
import json
import os
import re
import requests
import tqdm
import time
import openai

from dotenv import load_dotenv
from prompt_utils import parse_prompt, to_prompt

load_dotenv()

HEADERS = {
    "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
    "Content-Type": "application/json",
}

HUMAN_EVAL = os.environ['PWD'] + '/data/HumanEval.jsonl'
OUT_FILE = os.environ['PWD'] + '/results/results-{}-{}.jsonl'

async def get_completion(sem, prompt, num_tries=1, model='code-davinci-002', num_errors=0):
    #print(num_tries)
    if num_tries == 1:
        temperature = 0.0
    elif num_tries == 10:
        temperature = 0.6
    elif num_tries == 100:
        temperature = 0.8
    else:
        raise ValueError("num_tries must be 1, 10, or 100")


    async with sem:
        if model in {'gpt-3.5-turbo', 'gpt-4'}:
            messages = parse_prompt(prompt)
            completion = await openai.ChatCompletion.acreate(messages=messages, model=model, temperature=temperature, max_tokens=1000, n=num_tries)
            choices = completion.choices
            return [choice['message']['content'] for choice in choices]

        else:
            completion = await openai.Completion.acreate(prompt=prompt, model=model, temperature=temperature, max_tokens=1000, n=num_tries)
            choices = completion.choices
            return [choice['text'] for choice in choices]


def iter_hval():
    all_lines = []
    with open(HUMAN_EVAL) as f:
        for line in f:
            all_lines.append(json.loads(line))

    return all_lines

async def get_results(num_tries=10, model='code-davinci-002'):
    out_file = OUT_FILE.format(model, num_tries)

    with open(out_file, 'w') as f:
        pass

    sem = asyncio.Semaphore(10)

    async def output(prompt, task_id):
        full_prompt = f'''
<|im_start|>system<|im_sep|>
You may only respond with code and comments and the <|start_of_completion|> token.
<|im_end|>
<|im_start|>user<|im_sep|>
You must complete the python function I give you. You will write the completion in the following form:

${{ORIG_FUNCTION}}
    <|start_of_completion|>
${{INSERT_COMPLETION}}

ORIG_FUNCTION=
{prompt}

Please follow the template by repeating the original function, including the <|start_of_completion|> token, then writing the completion.
<|im_end|>
'''

        async with sem:
            completions = await get_completion(sem, full_prompt, num_tries=num_tries, model=model)

        outs = []
        for idx, completion in enumerate(completions):
            if '<|start_of_completion|>' in completion:
                completion = completion.split('<|start_of_completion|>')[1]
            else:
                print('no <|start_of_completion|> token')
                print(completion)
                print('______')
                print(prompt)
                print('')
            outs.append({'task_id': task_id, 'completion': completion})

        return outs


    futures = []
    for line in tqdm.tqdm(iter_hval()):
        prompt = line['prompt']
        task_id = line['task_id']
        futures.append(output(prompt, task_id))

    with open(out_file, 'a') as out_f:
        for future in tqdm.tqdm(asyncio.as_completed(futures), total=len(futures)):
            outs = await future
            for out in outs:
                out_f.write(json.dumps(out) + '\n')

    remove_bloat(out_file)


def remove_bloat(in_jsonl):
    new_results = []
    with open(in_jsonl, 'r') as f:
        for line in f:
            out = json.loads(line)
            special_token = re.search('\<\|\S+\|\>', out['completion'])

            if special_token:
                print(special_token)
                out['completion'] = out['completion'][:special_token.start()]

            stop_token = re.search('\n\S', out['completion'])
            if stop_token:
                out['completion'] = out['completion'][:stop_token.start()]


            new_results.append(out)

    with open(in_jsonl, 'w') as f:
        for result in new_results:
            f.write(json.dumps(result) + '\n')

if __name__ == '__main__':
    num_tries=1
    model = 'gpt-4'

    asyncio.run(get_results(num_tries=num_tries, model=model))

    out_f = OUT_FILE.format(model, num_tries)
    remove_bloat(out_f)
    print(out_f)
