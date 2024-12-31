def execute(tokens, token, stack):
    error = None
    soft_error = None
    console_output = None
    
    new_token = int(tokens[token[0] + 1])
    skip = 1
    
    return new_token, skip, error, soft_error, console_output