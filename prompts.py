from typing import List

def gpt4_prompt(func: str):
    return [
        {
            'role': 'system',
            'content': f'''
You may only respond with code and comments and the <|start_of_completion|> token.'''
        },
        {
            'role': 'user',
            'content': f'''
You must complete the python function I give you. You will write the completion in the following form:

${{ORIG_FUNCTION}}
    <|start_of_completion|>
${{INSERT_COMPLETION}}

ORIG_FUNCTION=
{func}

Please follow the template by repeating the original function, including the <|start_of_completion|> token, then writing the completion.
'''
    }
]

def gpt_3_5_prompt(func: str) -> List[dict]:
    return [
        {
            'role': 'system',
            'content': f'''
You are an intelligent programmer. You must complete the python function given to you by the user. And you must follow the format they present when giving your answer!

You can only respond with comments and actual code and the <|start_of_completion|> token, no free-flowing text (unless in a comment).'''
        },
        {
            'role': 'user',
            'content': f'''
You must complete the python function I give you. When doing so, you must write the completion int he following form:
${{ORIG_FUNCTION}}
    <|start_of_completion|>
    ${{INSERT_COMPLETION}}

Be sure to use the same indentation I specified. Furthermore, you may only write your response in code/comments.

ORIG_FUNCTION=
{func}

Once more, please follow the template by repeating the original function, including the <|start_of_completion|> token, then writing the completion.
'''
        }
    ]


def claude_prompt(func: str) -> str:
    return f'''
Human: You are an intelligent programmer. You must complete the python function I give you.

Here is the function you must complete:
```python
{func}
```

Now you must complete it.

Assistant: I shall complete the python function you gave me to be completely accurate:
```python
{func.strip()}'''

def azure_prompt(func: str) -> str:
    return f'''
<|im_start|>system<|im_sep|>
You are an intelligent programmer. You must complete the python function the user gives you
<|im_end|>
<|im_start|>user<|im_sep|>
Here is the python function you must complete:
```
{func}
```

Now you must complete it
<|im_end|>
<|im_start|>assistant<|im_sep|>
I shall complete the python function you gave me to be completely accurate:
```python
{func.strip()}'''

def completion_prompt(func: str) -> str:
    return f'''
The following is a conversation between a human and a very intelligent programming assistant.

Human:
You must complete the python function I specify below
Here it is:
```python
{func}
```

Assistant:
I shall complete the python function you gave me to be completely accurate:
```python
{func.strip()}'''