def execute(tokens, token, stack):
    error = None
    soft_error = None
    new_token = None
    console_output = None
    skip = 1
    
    if len(tokens) - 1 > token[0] + skip: # goofy if statement
        error = "parameter not given"
    else:
        printing = str(tokens[token[0] + 1])
        console_output = printing
    
    return new_token, skip, error, soft_error, console_output