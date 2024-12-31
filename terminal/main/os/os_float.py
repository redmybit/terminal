def execute(tokens, token, stack):
    error = None
    soft_error = None
    console_output = None
    skip = 1
    
    if len(tokens) - 1 > token[0] + 1: # goofy if statement
        error = "parameter not given"
    else:
        new_token = float(tokens[token[0] + 1])
    
    return new_token, skip, error, soft_error, console_output