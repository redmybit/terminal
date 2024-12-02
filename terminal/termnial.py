import pygame
import importlib.util as util

# initilize pygame
pygame.init()

WIDTH, HEIGHT = (500, 500)
FPS = 60
PATH = "main"

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

running = True

pygame.display.set_caption("Terminal")

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
            putf_line("variable not defined")
            return None
    
    def geti(self, index):
        if index > len(self.memory):
            putf_line("index out of range")
            return None

        return self.memory[index]
    
    def getn(self, name):
        names = []
        for variable in self.memory:
            names.append(variable.name)
        
        if name in names:
            return self.geti(names.index(name))
        else: 
            putf_line("variable not defined")
            return None
    
    def gets(self):
        return len(self.memory)


# main stack
stack = Stack()

# function that can be executed
class Function:
    def __init__(self, name, skip=0) -> None:
        self.name = name
        self.lines = []
        self.skip = skip
    
    def new_line(self, line):
        self.lines.append(line)
        return len(self.lines) - 1
    
    def del_line(self, index):
        del self.lines[index]
    
    def execute(self, context, index):
        global stack
        
        for line in self.lines:
            eval(line)

# program
class Program:
    def __init__(self, name, program_object) -> None:
        self.name = name
        self.program_object = program_object
    
    def execute(self, tokens, token, stack):
        return self.program_object.execute(tokens, token, stack)

# functions
ECHO = Function("echo", 1) # prints a value to the terminal
ECHO.new_line("putf_line(str(token_of(context, index, 1)))")

VAR = Function("var", 2) # creates a new variable with a given name and value
VAR.new_line("putf_line(str(token_of(context, index, 1) + ' at ' + str(stack.add(Variable(token_of(context, index, 1), token_of(context, index, 2), stack.gets())))))")

CLEAR = Function("clear") # clears the terminal
CLEAR.new_line("clear_terminal()")

EXIT = Function("exit") # exits the terminal
EXIT.new_line("exit_terminal()")

RUN = Function("run", 1) # runs a program
RUN.new_line("execute_command(str(token_of(context, index, 1)))")

UPD = Function("upd", 2) # updates a given variable with a new value
UPD.new_line("putf_line(str(stack.update(token_of(context, index, 1), token_of(context, index, 2))))")

COPY = Function("copy") # sets the message to the previous command
COPY.new_line("set_message(get_last_line())")

# list used for easy access
functions = [
    ECHO,
    VAR,
    CLEAR,
    EXIT,
    RUN,
    UPD,
]

# programs
update_path("main\\os") # update the path to be in the os directory

STRING = Program("string", load_module("os_string"))
GET = Program("get", load_module("os_get"))
INTEGER = Program("integer", load_module("os_integer"))
FLOAT = Program("float", load_module("os_float"))

update_path("main") # reset the path to be back in the main directory

# list of all the programs NOTE: ORDER IS IMPORTANT
programs = [
    GET, # gets variables
    INTEGER, # integer data type
    FLOAT, # float data type
    STRING, # handles the string data type
]

# function to execute commands
def execute_command(command : str):
    error = False
    
    # split the command into tokens
    tokens = command.split(" ")
    formatted_tokens = []
    
    for program in programs:
        
        # variable to keep track of how many tokens to skip
        skipping = 0
        
        # format the tokens (for variables)
        for token in enumerate(tokens):
            
            # account for errors and skipped tokens
            if error: break
            if skipping > 0:
                skipping -= 1
                continue
            
            new_token = token[1]
            
            if token[1] == program.name:
                new_token, skip, error_message = program.execute(tokens, token, stack)
                
                if error_message is not None:
                    putf_line(error_message)
                    error = True
                
                # account for skipping
                skipping += skip
            
            # add the new token to the formatted string
            formatted_tokens.append(new_token)
        
        tokens = formatted_tokens.copy()
        formatted_tokens = []
        
        # reset skipping to 0
        skipping = 0
    
    print(tokens) # debug
    
    # reset skipping to 0
    skipping = 0
    
    # parse through the tokens
    for token in enumerate(tokens):
        # account for errors and skipped tokens
        if error: break
        if skipping > 0:
            skipping -= 1
            continue
        
        # tracks if the token is valid
        valid = False
        
        # check if the token is a valid command and if it is execute the command
        for function in functions:
            if token[1] == function.name:
                valid = True
                function.execute(tokens, token[0])
                skipping += function.skip
        
        # handle invalid tokens
        if not valid:
            # throw an error because the value / function is not defined
            putf_line("~und.")
            error = True
            break

def color_message(message : str):
    # split the message into tokens
    tokens = message.split(" ")
    
    # list that stores the color key
    color_key = []
    
    # loop through the message and color the token if it is a program or a function
    for token in tokens:
        color = (255, 255, 255) # default to white
        
        for program in programs:
            if token == program.name:
                color = (230, 79, 48) # redish magenta
        
        for function in functions:
            if token == function.name:
                color = (39, 152, 152) # dark aqua
        
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