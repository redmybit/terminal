def execute(tokens, token, stack):
    stack = stack
    
    new_token = 0
    skip = 1 # always 1 for variables
    error = None
    
    # replace the token with the value
    variable = stack.getn(tokens[token[0] + 1])
    if variable is not None:
        new_token = variable.value
    else:
        error = "variable undefined"
    
    return new_token, skip, error