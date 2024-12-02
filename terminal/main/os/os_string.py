def execute(tokens, token, stack):
    new_token = 0
    skip = 0
    error = None
    
    # set the token to be a string
    next = ""
    index = 0
    final = ""
    while next != ";":
        index += 1
        next = tokens[token[0] + index]
        
        final += " " + str(next)
    
    # format the string (remove the unneccessary spaces at the front & at the end)
    final = final[:-2]
    final = final[1:]
    new_token = final # set the new token to be the final string
    
    skip = index # not index - 1 because of the sneaky semi-colon
    
    return new_token, skip, error