def execute(tokens, token, stack):
    error = None
    
    new_token = int(tokens[token[0] + 1])
    skip = 1
    
    return new_token, skip, error