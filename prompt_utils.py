import re

def parse_prompt(prompt):
    # Grab all blocks between the <|im_start|> and <|im_end|> tokens
    im_blocks = re.findall(r"<\|im_start\|>(.+?)<\|im_end\|>", prompt, re.DOTALL)

    messages = []
    for block in im_blocks:
        # Separate by <|im_sep|> token
        role, content = block.split("<|im_sep|>")
        messages.append({"role": role.strip(), "content": content.strip()})

    return messages

def to_prompt(messages):
    prompt = ""
    for message in messages:
        prompt += f"<|im_start|>{message['role']}<|im_sep|>{message['content']}<|im_end|>"

    return prompt
