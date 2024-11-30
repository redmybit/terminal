import pygame

pygame.init()

WIDTH, HEIGHT = (750, 750)
FPS = 60

font_name = pygame.font.match_font('couriernew')
TERMINAL_FONT_SIZE = 16
TERMINAL_FONT = pygame.font.Font(font_name, TERMINAL_FONT_SIZE)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption("Terminal")

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

def put_line(text, offset, underline = False):
    updated_text = text
    if underline: updated_text += "|"
    draw_text(screen, updated_text, TERMINAL_FONT, (255, 255, 255), (0, offset))
    return offset + TERMINAL_FONT_SIZE

def putf_line(text):
    lines.append(text)

def clear_terminal():
    global lines
    lines = []

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

# command class
class Command:
    def __init__(self, name, command, skip=0) -> None:
        self.name = name
        self.command = command
        self.skip = skip
    
    def execute(self, context, index):
        global stack
        eval(self.command)

# list of commands
commands = [
    Command("echo", "putf_line(str(context[index + 1]))", 1), # prints the next token
    Command("var", "putf_line(str(stack.add(Variable(context[index + 1],context[index + 2],stack.gets()))))", 2), # creates a new variable
    Command("clear", "clear_terminal()", 0), # clears the console
]

# function to execute commands
def execute_command(command : str):
    global stack
    global commands
    
    error = False
    
    # split the command into tokens
    tokens = command.split(" ")
    formatted_tokens = []
    
    # variable to keep track of how many tokens to skip
    skipping = 0
    
    # format the tokens (for variables)
    for token in enumerate(tokens):
        
        # account for errors
        if error:
            break
        
        # account for skipped tokens
        if skipping > 0:
            skipping -= 1
            continue
        
        new_token = token[1]
        
        # check if the token is get
        if token[1] == "get":
            # replace the token with the value
            variable = stack.getn(tokens[token[0] + 1])
            if variable is not None:
                new_token = variable.value
            else:
                error = True
                break
            
            skipping += 1
        
        # add the new token to the formatted string
        formatted_tokens.append(new_token)
    
    tokens = formatted_tokens.copy()
    formatted_tokens = []
    
    # reset skipping to 0
    skipping = 0
    
    # format the tokens (for integers)
    for token in enumerate(tokens):
        
        # account for errors
        if error:
            break
        
        # account for skipped tokens
        if skipping > 0:
            skipping -= 1
            continue
        
        new_token = token[1]
        
        # check if the token is get
        if token[1] == "integer":
            new_token = int(tokens[token[0] + 1])
            skipping += 1
        
        # add the new token to the formatted string
        formatted_tokens.append(new_token)
    
    tokens = formatted_tokens.copy()
    formatted_tokens = []
    
    # reset skipping to 0
    skipping = 0
    
    # format the tokens (for strings)
    for token in enumerate(tokens):
        
        # account for errors
        if error:
            break
        
        # account for skipped tokens
        if skipping > 0:
            skipping -= 1
            continue
        
        new_token = token[1]
        
        # check if the token is string
        if token[1] == "string":
            new_token = ""
            
            # set the token to be a string
            next = ""
            index = 0
            final = ""
            while next != ";":
                index += 1
                next = tokens[token[0] + index]
                
                # catch errors
                if index + token[0] > len(tokens) - 1:
                    
                    # throw an error
                    putf_line("syntax error")
                    error = True
                    break
                
                final += " " + next
            
            # format the string (remove the unneccessary semi-colon and spaces)
            final = final[:-2]
            final = final[1:]
            
            # set the new token to be the final string
            new_token = final
            
            # skip over the next values
            skipping += len(final)
        
        # add the new token to the formatted string
        formatted_tokens.append(new_token)
    
    print(formatted_tokens)
    tokens = formatted_tokens.copy()
    
    # reset skipping to 0
    skipping = 0
    
    # parse through the tokens
    for token in enumerate(tokens):
        if error:
            break
        
        # account for skipped tokens
        if skipping > 0:
            skipping -= 1
            continue
        
        # check if the token is a valid command and if it is execute the command
        for checking in commands:
            if token[1] == checking.name:
                checking.execute(formatted_tokens, token[0])
                skipping += checking.skip

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
        offset = put_line(">> " + line, offset)
    
    underline = (frames % FPS) > (FPS / 2)
    offset = put_line(message, offset, underline=underline)
    
    # if the text is offscreen clear the first line
    if offset > HEIGHT:
        lines.pop(0)
    
    frames += 1
    
# main loop
running = True
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
