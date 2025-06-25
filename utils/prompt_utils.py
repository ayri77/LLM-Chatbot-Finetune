from config import MAX_TOKENS

def build_prompt(system, instruction):
    return (
        f"<|im_start|>system\n{system}<|im_end|>\n"
        f"<|im_start|>user\n{instruction}<|im_end|>\n"
        f"<|im_start|>assistant\n"
    )

# TODO: 
def format_messages_as_prompt(messages):
    pass

def parse_response(response):
    pass
