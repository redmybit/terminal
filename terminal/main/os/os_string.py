def execute(tokens, token, stack):
    new_token = 0
    skip = 0
    error = None
    soft_error = None
    console_output = None
    
    # set the token to be a string
    next = ""
    index = 0
    final = ""
    while next != ";" and error is None:
        index += 1
        
        # error handling
        if len(tokens) - 1 > token[0] + index: # goofy if statement
            error = "parameter not given"
        else:
            next = tokens[token[0] + index]
            
            final += " " + str(next)
        
        # prevents the while loop from infinitely incurring
        if index >= 101:
            error = "max string depth reached"
            
    # format the string (remove the unneccessary spaces at the front & at the end)
    final = final[:-2]
    final = final[1:]
    new_token = final # set the new token to be the final string
    
    skip = index # not index - 1 because of the sneaky semi-colon
    
    return new_token, skip, error, soft_error, console_output