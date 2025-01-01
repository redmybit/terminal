
def execute(tokens, token, stack):
    error = None
    soft_error = None
    new_token = None
    console_output = None
    skip = 3
    
    if len(tokens) - 1 > token[0] + skip: # goofy if statement
        error = "parameter not given"
    else:
        mode = str(tokens[token[0] + 1])
        path = str(tokens[token[0] + 2])
        data = str(tokens[token[0] + 3])
        
        """
        
        Character	Meaning
        'r'	open for reading (default)
        'w'	open for writing, truncating the file first
        'x'	create a new file and open it for writing
        'a'	open for writing, appending to the end of the file if it exists
        (NOT USED) 'b' binary mode
        (NOT USED) 't' text mode (default)
        (NOT USED) '+' open a disk file for updating (reading and writing)

        """
        
        modes = ["r", "w", "x", "a"]
        if modes.count(mode) == 0: error = f"invalid file mode \"{mode}\""
        
        full_path = stack.getnp() + "\\" + path
        
        # Reading from a file (file must exist)
        if mode == "r" and not (error is not None):
            
            # prep the data
            if data == "*":
                data = None # read the entire file
            elif data <= 0:
                error = "can't read negative bytes"
            elif type(data) == str:
                error = "data must be int or inf."
            
            if not error:  # cancel out on errors
                try:
                    with open(full_path, mode) as file:
                        content = file.read(data)
                        new_token = content
                except FileNotFoundError:
                    error = f"file \"{path}\" not found"
        
        # Writing to a file (overwrites if file exists)
        if mode == "w" and not (error is not None):
            with open(full_path, mode) as file:
                file.write(data)
        
        # Appending to a file (creates the file if it doesn't exist)   
        if mode == "a" and not (error is not None):
            with open(full_path, mode) as file:
                file.write(data)

        # Creating a new file (raises an error if file exists)
        if mode == "x" and not (error is not None):
            try:
                with open(path, mode) as file:
                    file.write(data)
            except FileExistsError:
                error == "file exists"
        
    return new_token, skip, error, soft_error, console_output