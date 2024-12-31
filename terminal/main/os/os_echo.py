def execute(tokens, token, stack):
    error = None
    soft_error = None
    new_token = None
    skip = 1
    
    printing = str(tokens[token[0] + 1])
    console_output = printing
    
    return new_token, skip, error, soft_error, console_output