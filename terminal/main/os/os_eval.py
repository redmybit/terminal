def execute(tokens, token, stack):
    error = None
    soft_error = None
    console_output = None
    
    operation = tokens[token[0] + 1]
    inputs = []
    
    index = 2
    input_token = None
    while input_token != ";":
        input_token = tokens[token[0] + index]
        inputs.append(input_token)
        index += 1
    
    new_token = None
    
    class Operation:
        def __init__(self, name : str, line : str) -> None:
            self.name = name
            self.line = line
        
        def out(self, inputs):
            return eval(self.line)
        
    ADD = Operation("add", "sum(inputs)")
    
    operations = [ADD]
    
    for checking in operations:
        if operation == checking.name:
            new_token = checking.out(inputs)   
            break
        
        if new_token is not None:
            break
    
    skip = len(inputs) + 1 # eval has a skip of inputs (+1 to account for the semi-colon)
    
    return new_token, skip, error, soft_error, console_output
