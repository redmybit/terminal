import pygame
import importlib.util as util
import copy

# abbreviations guide:

# PARSER
# PFE: Parser found error
# PFSE: Parser found soft error
# PTP: Parser terminated program
# PS: Parser summary
# PPPS: Parser post program summary

# STACK
# SFE: Stack found error
# SFSE: Stack found soft error

# parser class
class Parser:
    def __init__(self) -> None:
        self.keywords = [
            "PFE",
            "PFSE",
            "PTP",
            "PS",
            "PPPS"
        ]
        
        self.colorkey = [
            (255, 0, 0),
            (255, 0, 0),
            (76, 197, 170),
            (76, 197, 170),
            (76, 197, 170)
        ]

# general parser
parser = Parser()

# initilize pygame
pygame.init()

# global variables
WIDTH, HEIGHT = (500, 500)
FPS = 60
PATH = "terminal\\main"
DEBUG = True # debug mode for the console

# functions for loading modules from a path and updating them
def update_path(new_path):
    global PATH
    PATH = new_path

def load_module(name : str):
    # Load the module
    spec = util.spec_from_file_location(name, PATH + "\\" + name + ".py")
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    return module

# font setup
font_name = pygame.font.match_font('couriernew')
TERMINAL_FONT_SIZE = 16
TERMINAL_FONT = pygame.font.Font(font_name, TERMINAL_FONT_SIZE)

# important variables
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption("Terminal")

running = True

# functions for drawing text onto the screen
def draw_colored_text(screen, font, word_color_pairs, position, underline=False):
    x, y = position
    index = 0
    for word, color in word_color_pairs:
        # Render each word
        word_surface = font.render(word, True, color)
        word_rect = word_surface.get_rect()

        # Draw the word on the screen
        screen.blit(word_surface, (x, y))

        # Move x to the right for the next word, adding some spacing
        space_width = TERMINAL_FONT.size(" ")[0]  # Returns a tuple (width, height), we only need width
        if underline and index == len(word_color_pairs) - 2: space_width = 0 # -2 so it effects the word before the |
            
        x += word_rect.width + space_width  # add a space to the end of each word
        
        index += 1

def draw_text(screen, text, font, color, position, center=False):
    # render the text
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    # center the text if specified
    if center:
        text_rect.center = position
    else:
        text_rect.topleft = position

    # draw the text on the screen
    screen.blit(text_surface, text_rect)

def put_line(text : str, offset, underline = False, colored = None):    
    updated_text = text.split(" ") # split the text into an array
    
    # if there is an underline add the typing character
    if underline:
        updated_text.append("|")
        colored.append((255, 255, 255)) # account for the typing character
    
    pairs = []
    if colored is not None:
        for item in enumerate(updated_text):
            
            # set the pair
            pair = (updated_text[item[0]], colored[item[0]])
            
            # add the pair to the list
            pairs.append(pair)
                
    else:
        # if a color key is not given default the text to white
        pairs = [(updated_text[index[0]], (255, 255, 255)) for index in enumerate(updated_text)]
            
    draw_colored_text(screen, TERMINAL_FONT, pairs, (0, offset), underline=underline)
    
    return offset + TERMINAL_FONT_SIZE

def putf_line(text, console=False):
    lines.append(text)

def clear_terminal():
    global lines
    lines = []

def exit_terminal():
    global running
    running = False

def get_last_line():
    return lines[len(lines) - 2] # -2 so that the current line is not counted

def set_message(string):
    global message
    message = string

def token_of(context, index, offset):
    return context[index + offset]

# useful variables
lines = []
message = ""
command = None
frames = 0

# variable class
class Variable:
    def __init__(self, name, value, index) -> None:
        self.name = name
        self.value = value
        self.index = index

# stack class
class Stack:
    def __init__(self) -> None:
        self.memory = []
    
    def add(self, variable):
        self.memory.append(variable)
        return len(self.memory) - 1
    
    def update(self, name, new_value):
        names = []
        for variable in self.memory:
            names.append(variable.name)
        
        if name in names:
            index = names.index(name)
            self.memory[index] = Variable(name, new_value, index)
            return index
        else: 
            putf_line("SFE: variable not defined")
            return None
    
    def geti(self, index):
        if index > len(self.memory):
            putf_line("SFE: index out of range")
            return None

        return self.memory[index]
    
    def getn(self, name):
        names = []
        for variable in self.memory:
            names.append(variable.name)
        
        if name in names:
            return self.geti(names.index(name))
        else: 
            putf_line("SFE: variable not defined")
            return None
    
    def gets(self):
        return len(self.memory)


# main stack
stack = Stack()

# program
class Program:
    def __init__(self, name, program_object) -> None:
        self.name = name
        self.program_object = program_object
    
    def execute(self, tokens, token, stack):
        return self.program_object.execute(tokens, token, stack)

# programs
update_path("terminal\\main\\os") # make sure the path is in the main\\os directoy when loading modules

ECHO = Program("echo", load_module("os_echo")) # prints a value to the terminal
#ECHO.new_line("putf_line(str(token_of(context, index, 1)))")

#VAR = Program("var", 2) # creates a new variable with a given name and value
#VAR.new_line("putf_line(str(token_of(context, index, 1) + ' at ' + str(stack.add(Variable(token_of(context, index, 1), token_of(context, index, 2), stack.gets())))))")

#CLEAR = Program("clear") # clears the terminal
#CLEAR.new_line("clear_terminal()")

#EXIT = Program("exit") # exits the terminal
#EXIT.new_line("exit_terminal()")

#RUN = Program("run", 1) # runs a program
#RUN.new_line("execute_command(str(token_of(context, index, 1)))")

#UPD = Program("upd", 2) # updates a given variable with a new value
#UPD.new_line("putf_line(str(stack.update(token_of(context, index, 1), token_of(context, index, 2))))")

#COPY = Program("copy") # sets the message to the previous command
#COPY.new_line("set_message(get_last_line())")

STRING = Program("string", load_module("os_string"))
GET = Program("get", load_module("os_get"))
INTEGER = Program("integer", load_module("os_integer"))
FLOAT = Program("float", load_module("os_float"))
EVAL = Program("eval", load_module("os_eval"))

update_path("terminal\\main") # correct the path back to main

# list of all the programs NOTE: ORDER IS IMPORTANT
programs = [
    GET, # gets variables
    INTEGER, # integer data type
    FLOAT, # float data type
    EVAL, # evalutates expressions
    STRING, # handles the string data type
    ECHO,
]

# function to execute commands
def execute_command(command : str):
    
    # self explanatory
    total_errors = 0
    error = False
    
    # split the command into tokens
    tokens = command.split(" ")
    
    # flip the tokens list to be backwards
    reversed_tokens = tokens.copy()
    reversed_tokens.reverse()
    
    # formated tokens list
    formatted_tokens = []
    
    # keeps track of if the loop should reset or terminate
    processing = True
    
    # keeps track of how many iterations the loop had to go through
    iterations = 0
    
    # main processing loop
    while processing and (error == False):
        
        # flip the tokens list to be backwards
        reversed_tokens = tokens.copy()
        reversed_tokens.reverse()
        
        # formatted lists
        formatted_tokens = []
        
        # reset the processing variable
        processing = False
        
        # summary of changes
        summary = "Parser summary: none"
        
        # debug
        print("tokens: " + str(tokens))
        
        # loop through the flipped tokens
        for reversed_token in enumerate(reversed_tokens):
            
            # skip if a program has been found
            if processing:
                
                # add the token to the formatted tokens (at the front to preserve the order)
                formatted_tokens.insert(0, reversed_token[1])
                
                # skip the program check
                continue
            
            # debug
            # print(str(reversed_token[0]) + ": " + str(reversed_token[1]))
            
            using_token = reversed_token[1]

            # check if the token is a keyword
            for program in programs:
                
                # check if the token is recognized
                if reversed_token[1] == program.name:
                    
                    # program was found so update the loop the reset again
                    processing = True
                    
                    # get the original token index
                    token_index = len(tokens) - reversed_token[0] - 1
                    
                    # define a token to be passed as a parameter
                    token = [token_index, reversed_token[1]]
                    print(">>>>>>>> tokens " + str(tokens))
                    print(">>>>>>>> token " + str(token))
                    
                    # execute the program
                    new_token, skip, error_message, soft_error_message, console_output = program.execute(tokens, token, stack)
                    
                    # account for errors
                    if error_message is not None:
                        putf_line("PFE: " + error_message)
                        error = True
                        
                        # update error count
                        total_errors += 1
                    
                    if soft_error_message is not None:
                        putf_line("PFSE: " + soft_error_message)
                        
                        # update error count
                        total_errors += 1
                    
                    # account for any console messages
                    if console_output is not None:
                        putf_line(console_output)
            
                    # update the parser summary and add the update the formatted tokens list
                    if new_token is not None:
                        summary = "PS: " + str(token[1]) + " => " + str(new_token)
                        using_token = new_token
                    
                    # break on errors
                    if error: break
                if error: break
            if error: break
            
            # add the token to the end of the code
            if (processing == False) and (using_token is not None): formatted_tokens.append(using_token)
        
        # print the parser's summary
        print(summary)
        
        # set the tokens to be the formatted tokens
        tokens = copy.deepcopy(formatted_tokens)
        
        # increment the iterations counter
        iterations += 1
    
    # counter of how many clean runs to do ("reruns" of the code to check for undefined and misc. errors)
    clean_runs = 1
    
    for _ in range(clean_runs):
        
        # loop through the tokens
        for token in tokens:
            
            # check if the token is a string
            if (type(token) == str) and (not token == "$"):
                
                # assume the token is an undefined variable
                putf_line(f"PFSE: undefined token >> \"{token}\" <<")
                
                # update error count
                total_errors += 1
            else:
                # skip if it is a numerical value
                continue
                
    
    # error message
    if error: putf_line("PTP: error occured")

    # program summary message
    if DEBUG:
        putf_line(f"PPPS: executed in {iterations} iteration(s)")
        putf_line(f"PPPS: executed with {total_errors} error(s)")

# determines the color of a given message
def color_message(message : str):
    # split the message into tokens
    tokens = message.split(" ")
    
    # list that stores the color key
    color_key = []
    
    # loop through the message and color the token if it is a program or a function
    for token in tokens:
        color = (255, 255, 255) # default to white
        
        for parser_item in enumerate(parser.keywords):
            if token == parser_item[1] or token == parser_item[1] + ":":
                color = parser.colorkey[parser_item[0]]
        
        for program in programs:
            if token == program.name:
                #color = (230, 79, 48) # reddish magenta
                color = (197, 134, 192) # more pinkish
        
        if token == ";":
            color = (127, 127, 127) # medium gray
        
        color_key.append(color)
    
    return color_key

# main function
def main():
    global frames # frame counter
    global command
    
    offset = 0 # reset the offset every frame
    
    if command is not None:
        lines.append(command)
        execute_command(command)
        command = None
    
    for line in lines:
        updated_line = ">> " + line
        offset = put_line(updated_line, offset, colored=color_message(updated_line))
    
    underline = (frames % FPS) > (FPS / 2)
    color_key = color_message(message)

    offset = put_line(message, offset, underline=underline, colored=color_key)
    
    # if the text is offscreen clear the first line
    if offset > HEIGHT:
        lines.pop(0)
    
    # increment the frame counter
    frames += 1
    
# main loop
while running:
    
    # poll for events
    for event in pygame.event.get():
            
        # check if the terminal is killed
        if event.type == pygame.QUIT:
            running = False
    
        # handle key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:  # Remove the last character
                message = message[:-1]
            elif event.key == pygame.K_RETURN:  # Handle Enter (optional)
                command = message
                message = ""  # Reset the input (optional)
            elif event.key == pygame.K_SPACE:  # Add a space
                message += " "
            else:  # Add other characters to the string
                message += event.unicode
    
    # fill the screen and run the main loop
    screen.fill((0, 0, 0))
    main()
    
    # refresh the screen and tick the clock
    pygame.display.flip()
    clock.tick(FPS)

# quit out of pygame
pygame.display.quit()
pygame.quit()
