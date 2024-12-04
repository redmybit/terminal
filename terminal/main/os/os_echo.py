def execute(tokens, token, stack):
    error = None
    new_token = None
    skip = 1
    
    printing = str(tokens[token[0] + 1])
    console_output = printing
    
    return new_token, skip, error, console_output