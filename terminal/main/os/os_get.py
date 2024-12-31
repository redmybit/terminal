def execute(tokens, token, stack):
    stack = stack
    console_output = None
    
    new_token = 0
    skip = 1 # always 1 for variables
    error = None
    soft_error = None
    
    # check if the parameter is given
    if len(tokens) - 1 > token[0] + 1: # goofy if statement
        error = "parameter not given"
    else:
        
        # replace the token with the value
        variable = stack.getn(tokens[token[0] + 1])
    
        if variable is not None:
            new_token = variable.value
        else:
            error = "variable undefined"
    
    return new_token, skip, error, soft_error, console_output