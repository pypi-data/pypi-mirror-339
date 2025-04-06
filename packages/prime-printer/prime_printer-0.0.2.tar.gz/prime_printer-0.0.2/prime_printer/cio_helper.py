#     XXX XXX
# XXX Imports XXX
#     XXX XXX
import sys
import os
import platform
import threading
import time
import random
import re

import climage

# Redirect standard output to suppress pygame's print message
sys.stdout = open(os.devnull, 'w')
import pygame
# Initialize pygame mixer
pygame.mixer.init()
# Restore standard output
sys.stdout = sys.__stdout__

if platform.system() == "Linux":
    import tty
    import termios
else:
    import msvcrt






#    XXX XXX XXX
# XXX Constants XXX
#    XXX XXX XXX
# Colors
PURPLE = '\033[95m'
CYAN = '\033[96m'
DARKCYAN = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
MAGENTA = '\u001b[35m'
RED = '\033[91m'
WHITE = '\u001b[37m'
BLACK = '\u001b[30m'

# Background-Colors
BACKGROUND_BLACK = "\u001b[40m"
BACKGROUND_RED = "\u001b[41m"
BACKGROUND_GREEN = "\u001b[42m"
BACKGROUND_YELLOW = "\u001b[43m"
BACKGROUND_BLUE = "\u001b[44m"
BACKGROUND_MAGENTA = "\u001b[45m"
BACKGROUND_CYAN = "\u001b[46m"
BACKGROUND_WHITE = "\u001b[47m"

# Styles
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
REVERSED = "\u001b[7m"
HEADER = "\033[95m"

# Cursor Navigations -> functions!
# move cursor in A/B/C/D Direction by n characters
UP = lambda n: f"\u001b[{n}A"
DOWN = lambda n: f"\u001b[{n}B"
RIGHT = lambda n: f"\u001b[{n}C"
LEFT = lambda n: f"\u001b[{n}D"

NEXT_LINE = lambda n: f"\u001b[{n}E" #moves cursor to beginning of line n lines down
PREV_LINE = lambda n: f"\u001b[{n}F" #moves cursor to beginning of line n lines down

SET_COLUMN = lambda n: f"\u001b[{n}G" #moves cursor to column n
SET_POSITION = lambda n, m: f"\u001b[{n};{m}H" #moves cursor to row n column m


# Clearing
CLEAR_SCREEN = lambda n: f"\u001b[{n}J" #clears the screen
#    n=0 clears from cursor until end of screen,
#    n=1 clears from cursor to beginning of screen
#    n=2 clears entire screen

CLEAR_LINE = lambda n: f"\u001b[{n}K" #clears the current line
#    n=0 clears from cursor to end of line
#    n=1 clears from cursor to start of line
#    n=2 clears entire line

# Reset
END = '\033[0m'

# Sounds (no text styling)
PATH_TO_SOUND = os.path.join( os.path.dirname(os.path.abspath(__file__)), "sounds" )
SOUNDS = [os.path.join(PATH_TO_SOUND, f"typing_{cur_n}.wav") for cur_n in [1, 3, 4, 5, 7, 8, 9, 15, 16]]

# Emojis Constants
EMOJI_SMILE = "\U0001F604"  # 😄
EMOJI_HEART = "\U00002764"  # ❤️
EMOJI_THUMBS_UP = "\U0001F44D"  # 👍
EMOJI_LAUGHING = "\U0001F606"  # 😆
EMOJI_WINK = "\U0001F609"  # 😉
EMOJI_SAD = "\U0001F61E"  # 😞
EMOJI_ANGRY = "\U0001F620"  # 😠
EMOJI_SUN = "\U00002600"  # ☀️
EMOJI_STAR = "\U00002B50"  # ⭐
EMOJI_FLEXED_ARM = "\U0001F4AA"  # 💪
EMOJI_FIRE = "\U0001F525"  # 🔥
EMOJI_PARTY_POPPER = "\U0001F389"  # 🎉
EMOJI_THINKING = "\U0001F914"  # 🤔
EMOJI_GHOST = "\U0001F47B"  # 👻
EMOJI_CAT_FACE = "\U0001F638"  # 😸
EMOJI_PIZZA = "\U0001F355"  # 🍕
EMOJI_COFFEE = "\U00002615"  # ☕
EMOJI_BOOK = "\U0001F4D6"  # 📖
EMOJI_MUSIC_NOTE = "\U0001F3B5"  # 🎵
EMOJI_TROPHY = "\U0001F3C6"  # 🏆
EMOJI_FRIENDS = "\U0001F46B"  # 👯
EMOJI_BIRTHDAY_CAKE = "\U0001F382"  # 🎂
EMOJI_MONEY_BAG = "\U0001F4B0"  # 💰
EMOJI_CROWN = "\U0001F451"  # 👑
EMOJI_PANDA_FACE = "\U0001F43C"  # 🐼
EMOJI_UNICORN = "\U0001F984"  # 🦄
EMOJI_SPORTS = "\U0001F3C0"  # 🏀
EMOJI_PAPER_PLANE = "\U0001F68F"  # ✈️
EMOJI_OWL = "\U0001F989"  # 🦉
EMOJI_ICE_CREAM = "\U0001F368"  # 🍨
EMOJI_SNOWMAN = "\U00002603"  # ☃️
EMOJIS = [EMOJI_SMILE, EMOJI_HEART, EMOJI_THUMBS_UP, 
          EMOJI_LAUGHING, EMOJI_WINK, EMOJI_SAD, 
          EMOJI_ANGRY, EMOJI_SUN, EMOJI_STAR, 
          EMOJI_FLEXED_ARM, EMOJI_FIRE, EMOJI_PARTY_POPPER, 
          EMOJI_THINKING, EMOJI_GHOST, EMOJI_CAT_FACE, 
          EMOJI_PIZZA, EMOJI_COFFEE, EMOJI_BOOK, 
          EMOJI_MUSIC_NOTE, EMOJI_TROPHY, EMOJI_FRIENDS, 
          EMOJI_BIRTHDAY_CAKE, EMOJI_MONEY_BAG, EMOJI_CROWN,
          EMOJI_PANDA_FACE, EMOJI_UNICORN, EMOJI_SPORTS,
          EMOJI_PAPER_PLANE, EMOJI_OWL, EMOJI_ICE_CREAM,
          EMOJI_SNOWMAN]

# Helpful Lists
NUMBERS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
ALPHABET = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
CHINESE_SIGNS = ["你", "好", "我", "们", "的", "是", "在", "不", "有", "吗"]
GREEK_ALPHABET = [
    "α", "β", "γ", "δ", "ε", "ζ", "η", "θ", "ι", "κ", "λ", "μ", "ν", "ξ", "ο", "π", 
    "ρ", "σ", "τ", "υ", "φ", "χ", "ψ", "ω", "Α", "Β", "Γ", "Δ", "Ε", "Ζ", "Η", "Θ", 
    "Ι", "Κ", "Λ", "Μ", "Ν", "Ξ", "Ο", "Π", "Ρ", "Σ", "Τ", "Υ", "Φ", "Χ", "Ψ", "Ω"
]
COMMON_SIGNS = [
    ".", ",", "!", "?", ":", ";", "-", "_", "(", ")", "[", "]", "{", "}", "<", ">", 
    "/", "\\", "|", "@", "#", "$", "%", "^", "&", "*", "+", "=", "~", "`", "'", "\"", 
    "“", "”", "‘", "’", "°", "©", "®", "™", "•", "¶", "§", "♪", "★", "♡", "☀", "☁", 
    "★", "☆", "☘", "☹", "☺", "✈", "⚽", "⚡", "♥", "♦", "♠", "♣", "♻", "✖", "✔"
]

COMMON_USER_INPUT_LIST = EMOJIS + NUMBERS + ALPHABET + CHINESE_SIGNS + GREEK_ALPHABET + COMMON_SIGNS



#    XXX XXX XXX
# XXX Functions XXX
#    XXX XXX XXX
def play_sound(path_to_sound_file):
    """
    Plays a sound on windows or linux asychnronisly.
    """
    # Initialize pygame mixer
    pygame.mixer.init()
    
    # Load the sound file
    sound = pygame.mixer.Sound(path_to_sound_file)
    
    # Play the sound asynchronously
    sound.play()

def clear():
    """
    Clears the console.
    """
    txt = f"{CLEAR_SCREEN(2)}{SET_POSITION(0,0)}"
    print(txt)

def awesome_print(txt:str, *features:tuple, should_cut_str_in_chars=True, 
                  should_play_sound:bool=False, should_add_backspace_at_end:bool=True,
                  print_delay:float=None, print_delay_min:float=None, print_delay_max:float=None) -> None:
    """
    Print something with delay, type-sound and/or style-effects on console.

    ---
    Parameters:
    - txt : str
        Text to print
    - features : tuple(str), optional
        Style-Effects to add (like BOLD, RED, ...)
    - should_cut_str_in_chars : bool, optional (default=True)
        Decides to cut the input text in parts to process, or not.
    - should_play_sound : bool, optional (default=False)
        Whether to play a typing sound or not.
    - should_add_backspace_at_end : bool, optional (default=True)
        Whether to add a backspace at the end of the printing process.
    - print_delay : float, optional (default=None)
        Delay with which each character of the text should be printed in seconds (set None to deactivate)
    - print_delay_min : float, optional (default=None)
        Only gets used if print_delay is None and print_delay_max has a value. 
        Defines the minimum delay of each character printing in seconds.
    - print_delay_max : float, optional (default=None)
        Only gets used if print_delay is None and print_delay_min has a value. 
        Defines the maximum delay of each character printing in seconds.
    """
    # apply special styling effects on the text
    if len(features) > 0:
        txt = add_special_effect(txt, features)
    
    # reset shell colors
    os.system("color")

    # split text in parts
    if should_cut_str_in_chars:
        escape_sequence_pattern = r'(\x1b\[[0-9;]*m|\\u[0-9a-fA-F]+|\\U[0-9a-fA-F]+|\\033\[48;2;([0-9]{1,3});([0-9]{1,3});([0-9]{1,3})m)'

        # extract escape-sequences and common text
        parts = re.split(escape_sequence_pattern, txt)
        chars = []
        for part in parts:
            if part == '' or not part:
                continue

            if re.match(escape_sequence_pattern, part):
                chars += [part]
            else:
                chars += [subpart for subpart in part]
    else:
        chars = [txt]

    for c in chars:
        # printing
        sys.stdout.write(c)
        sys.stdout.flush()    # forces buffer to flush the txt (normally it collect all and take it out togheter)
    
        # make type sound if printing is not too fast
        if ((print_delay and print_delay > 0.0) or (print_delay_max and print_delay_max > 0.0)) \
                and should_play_sound \
                and c in COMMON_USER_INPUT_LIST:
            if c == "\n":
                play_sound(SOUNDS[0])
            else:
                play_sound(SOUNDS[random.randint(1, 8)])
        
        # wait for print delay
        if print_delay:
            time.sleep(print_delay)
        elif print_delay_min and print_delay_max:
            time.sleep(random.uniform(print_delay_min, print_delay_max))
    
    # if fast printing, then make type sound at the end
    if ((print_delay and print_delay <= 0.0) or (print_delay_max and print_delay_max <= 0.0)) and should_play_sound:
        play_sound(SOUNDS[random.randint(0, 8)])
    
    # add backslash and end stylings
    if should_add_backspace_at_end:
        sys.stdout.write("\n")
    sys.stdout.write(END)
    sys.stdout.flush()

def add_special_effect(txt:str, *features) -> str:
    """
    Adds special style ffects to a given text.
    """
    if type(features[0]) == tuple and len(features) == 1:
        features = features[0]
    new_txt = txt
    for cur_feature in features:
        new_txt = cur_feature + new_txt + END
    return new_txt

def img_to_str(img_path:str, width=60, is_256color=False, is_truecolor=True, is_unicode=True):
    """
    Loads and returns an image as a text-based representation for awesome image prints in the console.

    ---
    Parameters:
    - img_path : str
        Path to the image file.
    - width : int, optional (default=60)
        Width of the output image in characters.
    - is_256color : bool, optional (default=False)
        Whether to use 256-color ANSI mode.
    - is_truecolor : bool, optional (default=True)
        Whether to use truecolor (24-bit color) if supported.
    - is_unicode : bool, optional (default=True)
        Whether to use Unicode characters for higher fidelity.

    ---
    Returns:
    - str: The converted image as a string that can be printed to the terminal.
    """
    return climage.convert(
                img_path,
                width=width,
                is_256color=is_256color,
                is_truecolor=is_truecolor,
                is_unicode=is_unicode
            )

def print_image(img_path, width=60, is_256color=False, is_truecolor=True, is_unicode=True):
    """
    Prints an image as a text-based representation for awesome image prints in the console.

    ---
    Parameters:
    - img_path : str
        Path to the image file.
    - width : int, optional (default=60)
        Width of the output image in characters.
    - is_256color : bool, optional (default=False)
        Whether to use 256-color ANSI mode.
    - is_truecolor : bool, optional (default=True)
        Whether to use truecolor (24-bit color) if supported.
    - is_unicode : bool, optional (default=True)
        Whether to use Unicode characters for higher fidelity.
    """
    print(img_to_str(img_path, width=width, is_256color=is_256color, is_truecolor=is_truecolor, is_unicode=is_unicode))

def print_progress_bar(total, progress, should_clear=False, 
                       left_bar_char="|", right_bar_char="|", progress_char="#", empty_char=" ",
                       front_message="", back_message="",
                       size=100, should_print=True) -> str:
    """
    Prints one step of a progress as a progress bar.

    ---
    Parameters:
    - total : union(int, float)
        Number of the total amount of the progress (the goal number).
    - progress : union(int, float)
        Number of the current state of the progress (how far the progress).
    - should_clear : bool, optional (default=False)
        Should the console output be cleared?
    - left_bar_char : str, optional (default='|')
        Left sign of the progress bar.
    - right_bar_char : str, optional (default='|')
        Right sign of the progress bar.
    - progress_char : str, optional (default='#')
        Sign of the progress in the progress bar.
    - empty_char : str, optional (default=' ')
        Sign of the missing progress in the progress bar.
    - front_message : str, optional (default="")
        Message for the progress bar.
    - back_message : str, optional (default="")
        Message behind the progress bar.
    - size : int, optional (default=100)
        Amount of signs of the progress bar.
    - should_print : bool, optional (default=True)
        Whether to print the progress bar.

    ---
    Returns:
    - str
        Created progress bar.
    """
    # clearing
    if should_clear:
        clear()
    
    # calc progress bar
    percentage = progress/float(total)
    percentage_adjusted = int( size * percentage )
    bar = progress_char*percentage_adjusted + empty_char*(size-percentage_adjusted)
    progress_str = f"{front_message} {left_bar_char}{bar}{right_bar_char} {percentage*100:0.2f}% {back_message}".strip()
    
    # writing
    if should_print:
        sys.stdout.write(progress_str+"\n")
        sys.stdout.flush()

    # add optional delay?
    # awesome_print(progress_str, should_play_sound=False, print_delay=None, print_delay_min=None)

    return progress_str

def get_char():
    """
    Receives the current input char of a console.
    """
    if platform.system() == "Linux":
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            char = os.read(fd, 1).decode()  # Read a single character
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return char
    else:
        return msvcrt.getch().decode()

def get_input(message='User: ', 
              should_lower=True,
              end_chars=['\n', '\r'], 
              back_chars=['\u0008', '\b'],
              should_play_sound=False,
              condition=lambda x: True,
              *features) -> str:
    """
    Method for receiving text input as str.

    ---
    Parameters:
    - message : str, optional (default='User: ')
        Message to the user.
    - should_lower : bool, optional (default=True)
        Lower user input during the return.
    - end_chars : List[str], optional (default=['\n', '\r'])
        Which characters should end the input?
    - back_chars : List[str], optional (default=['\u0008', '\b'])
        Chars which should delete the last input.
    - should_play_sound : bool, optional (default=False)
        If True, sound will be played if receiving an input.
    - condition : Call(x), optional (default=lambda x: True)
        Condition, which the input have to pass, else it will ask again.
    - *features : Tuple[str], optional
        Special effects for the input (e.g. you can turn the input in a different color).

    ---
    Returns
    - str
        Received User Input.
    """
    user_input = ""
    first_loop = True
    while condition(user_input) == False or first_loop:
        user_input = ""
        first_loop = False
        awesome_print(message, should_add_backspace_at_end=False)
        while True:
            
            try:
                char = get_char()
                user_input += char
            except UnicodeDecodeError:
                continue
            
            if char in end_chars:
                for cur_end_char in end_chars:
                    user_input = user_input.replace(cur_end_char, "")
                awesome_print("\n")
                break
            elif char in back_chars:
                awesome_print('\b \b', should_add_backspace_at_end=False)
                # awesome_print(f"{LEFT(1)} ", should_add_backspace_at_end=False)
                user_input = user_input[:-2]
            awesome_print(char, should_add_backspace_at_end=False, should_play_sound=should_play_sound, *features)
    result = user_input.replace("\r", "").replace("\n", "").replace("\b", "")
    if should_lower:
        result = result.lower()
    return result

def rgb_to_python(r:int, g:int, b:int, background_color=False) -> str:
    """
    Converts an RGB color value to an ANSI escape sequence for 24-bit colors (truecolor).

    ---
    Parameters:
    - r : int
        The red component of the color (0 to 255).
    - g : int
        The green component of the color (0 to 255).
    - b : int
        The blue component of the color (0 to 255).
    - background_color : bool, optional (default=False)
        Whether to convert to background color or front color.

    ---
    Returns:
    - int
        The corresponding ANSI escape sequence.
    """
    if background_color:
        return f"\033[48;2;{r};{g};{b}m"
    else:
        return f"\033[38;2;{r};{g};{b}m"




#     XXX XXX
# XXX Examples XXX
#     XXX XXX 
def print_example():
    awesome_print("Loading complete!", BOLD, GREEN, should_play_sound=True, print_delay_min=0.08, print_delay_max=0.5)

def color_print_example():
    awesome_print("My awesome text", rgb_to_python(20, 200, 150), BOLD)
    awesome_print("My second awesome text", rgb_to_python(210, 200, 240, background_color=True))
    awesome_print("My thrid awesome text", RED)
    awesome_print(GREEN+"My fourth awesome text"+END)

def loading_example():
    for i in range(101):
        print_progress_bar(total=100, progress=i, should_clear=False, left_bar_char="|", right_bar_char="|", 
                            progress_char="#", empty_char=" ",
                            front_message=f"YOLO Epoch: 1", back_message=f"Loss: {random.uniform(1.0, 0.1)}",
                            size=12, should_print=True)
        time.sleep(random.uniform(0.2, 0.07))

def menu_example():
    awesome_print(f"Menu:\n    -> New Game\n    -> Load Game\n    -> Exit\n", print_delay_min=0.08, print_delay_max=0.7, should_play_sound=True, should_add_backspace_at_end=False)
    while True:
        user_input = get_input("User: ")
        if user_input == "exit":
            awesome_print(f"{UP(5)}    -> New Game\n    -> Load Game\n    {REVERSED}-> Exit{END}\n", should_add_backspace_at_end=False)
            awesome_print(LEFT(100) + " "*6+" "*len(user_input) + LEFT(100), should_add_backspace_at_end=False)
            time.sleep(1)
            awesome_print("bye...", should_add_backspace_at_end=False)
            awesome_print(DOWN(1)+LEFT(10), should_add_backspace_at_end=False)
            time.sleep(0.5)
            break
        elif user_input == "new game":
            awesome_print(f"{UP(5)}    {REVERSED}-> New Game{END}\n    -> Load Game{END}{DOWN(2)}{LEFT(100)}", should_add_backspace_at_end=False)
            awesome_print(" "*6+" "*len(user_input)+LEFT(100), should_add_backspace_at_end=False)
        elif user_input == "load game":
            awesome_print(f"{UP(5)}    -> New Game\n    {REVERSED}-> Load Game{END}{DOWN(2)}{LEFT(100)}", should_add_backspace_at_end=False)
            awesome_print(" "*6+" "*len(user_input)+LEFT(100), should_add_backspace_at_end=False)
        else:
            awesome_print(UP(2)+LEFT(100)+CLEAR_LINE(0)+LEFT(len(user_input)+30), should_cut_str_in_chars=False, should_add_backspace_at_end=False)

def input_confirm_example():
    get_input("Do you accept (y/n): ", condition=lambda x: True if x.lower() in ['y', 'n'] else False)

def print_image_example():
     #or: os.path.split(os.path.abspath(__file__))[0]
    print_image(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logo.png"), 
                width=20, is_256color=False, 
                is_truecolor=True, is_unicode=True)

    print_image(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logo.png"), width=50)

def play_sound_example():
    play_sound(SOUNDS[2])
    time.sleep(1)






if __name__ == "__main__":
    print_example()
    # loading_example()
    # menu_example()
    # color_print_example()
    # input_confirm_example()
    # print_image_example()
    # play_sound_example()


