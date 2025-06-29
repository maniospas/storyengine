import sys
import time
import threading
import random
import sys
import time
import threading
import os


"""
SUPPORTING FUNCTIONS
"""

if sys.platform == 'win32':
    import msvcrt
else:
    import select
    import tty
    import termios
def key_pressed():
    if sys.platform == 'win32': return msvcrt.kbhit()
    if not sys.stdin.isatty(): return False
    try:
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        return bool(dr)
    except Exception: return False
    return False
def get_key():
    if sys.platform == 'win32': return msvcrt.getch().decode('utf-8', errors='ignore')
    return sys.stdin.read(1)
class TerminalInput:
    def __enter__(self):
        self.enabled = sys.stdin.isatty() and sys.platform != 'win32'
        if not self.enabled: return self
        try:
            self.fd = sys.stdin.fileno()
            self.old_settings = termios.tcgetattr(self.fd)
            tty.setcbreak(self.fd)
        except Exception: self.enabled = False
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.enabled: termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
def print_with_skip(text, delay):
    skip = False
    def check_skip():
        nonlocal skip
        while not skip:
            if key_pressed():
                skip = True
    with TerminalInput():
        threading.Thread(target=check_skip, daemon=True).start()
        for i, c in enumerate(text):
            if skip:
                print(text[i:], end="", flush=True)
                break
            print(c, end="", flush=True)
            time.sleep(delay)
    print()
    return skip

KEY_LEFT  = 'LEFT'
KEY_RIGHT = 'RIGHT'
KEY_ENTER = 'ENTER'
KEY_SPACE = ' '
KEY_UNKNOWN = 'UNKNOWN'

def readchar():
    if sys.platform == 'win32':
        ch = msvcrt.getch()
        if ch == b'\r': return KEY_ENTER
        if ch == b' ': return KEY_SPACE
        if ch in (b'\x00', b'\xe0'):
            ch2 = msvcrt.getch()
            if ch2 == b'K': return KEY_LEFT
            if ch2 == b'M': return KEY_RIGHT
            return KEY_UNKNOWN
        return ch.decode('utf-8', errors='ignore')
    if not sys.stdin.isatty(): return KEY_UNKNOWN
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        ch1 = sys.stdin.read(1)
        if ch1 == '\x1b':
            ch2 = sys.stdin.read(1)
            if ch2 == '[':
                ch3 = sys.stdin.read(1)
                sequence = f'\x1b[{ch3}'
                if sequence == '\x1b[D': return KEY_LEFT
                if sequence == '\x1b[C': return KEY_RIGHT
                return KEY_UNKNOWN
            return KEY_UNKNOWN
        if ch1 in ('\r', '\n'): return KEY_ENTER
        if ch1 == ' ': return KEY_SPACE
        return ch1
    finally: termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def enable_ansi_support():
    if os.name != 'nt':
        return
    import ctypes
    kernel32 = ctypes.windll.kernel32
    handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE = -11
    mode = ctypes.c_ulong()
    if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
        return  # Cannot get mode, likely not a real console
    mode.value |= 0x0004  # ENABLE_VIRTUAL_TERMINAL_PROCESSING
    kernel32.SetConsoleMode(handle, mode)
enable_ansi_support()


"""
BUILTINS ([noend] is handled manually)
"""

vars = {
    "[black]": "\033[030m",
    "[red]": "\033[031m",
    "[green]": "\033[032m",
    "[yellow]": "\033[033m",
    "[blue]": "\033[034m",
    "[purple]": "\033[035m",
    "[cyan]": "\033[036m",
    "[white]": "\033[037m",
    "[lightblack]": "\033[090m",
    "[lightred]": "\033[091m",
    "[lightgreen]": "\033[092m",
    "[lightyellow]": "\033[093m",
    "[lightblue]": "\033[094m",
    "[lightpurple]": "\033[095m",
    "[lightcyan]": "\033[096m",
    "[lightwhite]": "\033[097m",
    "[reset]": "\033[0m",
    "[end]": "\n",
    "[__refresh]": 36,
}
clear_screen = "\033[2J\033[H" # also moves the cursor to the top-left
clear_last = "\033[1A\033[K" # clears last line

def process_value(value):
    if value.startswith("["):
        assert value in vars, "Variable not found: "+value[1:-1]
        value = vars[value]
    try: return int(value)
    except:
        assert value[0]=="\"" and value[-1]=="\"" and len(value)>=2, "Value should be either a number or a string enclosed in \" but is neither: "+value
        return value[1:-1]

def process_variable_name(expr):
    prev = expr
    if expr.startswith("["): 
        expr = process_value(expr)
        assert isinstance(expr, string), "Can only obtain names from string values: "+prev
    return f"[{expr}]"

def process_variable_value(expr):
    expr = process_variable_name(expr)
    assert expr in vars, "This was previously not set: "+expr
    return vars[expr]


def process_condition(line):
    if line.startswith("!"):
        args = line[1:].strip().split(" ")
        assert len(args)>2, "Condition `! value var` must be followed by the rest of a line"
        arg0 = process_value(args[0])
        arg1 = process_variable_value(args[1])
        assert isinstance(arg0,int) == isinstance(arg1,int), "`! value var` can only compare both numbers or both strings\nCurrent inputs: "+str(arg0)+","+str(arg1)
        if arg0 == arg1: return
        return process_condition(" ".join(args[2:]))
    if line.startswith("@"):
        args = line[1:].strip().split(" ")
        assert len(args)>2, "Condition `@ value var` must be followed by the rest of a line"
        arg0 = process_value(args[0])
        arg1 = process_variable_value(args[1])
        assert isinstance(arg0,int) == isinstance(arg1,int), "`@ value var` can only compare both numbers or both strings\nCurrent inputs: "+str(arg0)+","+str(arg1)
        if arg0 != arg1: return
        return process_condition(" ".join(args[2:]))
    if line.startswith(">") and not line.startswith(">>>"):
        args = line[1:].strip().split(" ")
        assert len(args)>2, "Condition `> value var` must be followed by the rest of a line: "+args
        arg0 = process_value(args[0])
        arg1 = process_variable_value(args[1])
        assert isinstance(arg0,int) and isinstance(arg1,int), "`> value var` can only compare numbers\nCurrent inputs: "+str(arg0)+","+str(arg1)
        if arg0 >= arg1: return
        return process_condition(" ".join(args[2:]))
    if line.startswith("<") and not line.startswith("<<<"):
        args = line[1:].strip().split(" ")
        assert len(args)>2, "Condition `< value var` must be followed by the rest of a line: "+args
        arg0 = process_value(args[0])
        arg1 = process_variable_value(args[1])
        assert isinstance(arg0,int) and isinstance(arg1,int), "`< value var` can only compare numbers\nCurrent inputs: "+str(arg0)+","+str(arg1)
        if arg0 <= arg1: return
        return process_condition(" ".join(args[2:]))
    return line

def process_line(line):
    line = process_condition(line)
    if not line: return line
    if line.startswith("="):
        line = line[1:].split()
        assert len(line)==2, "Wrong syntax: expected `=value varname`"
        vars[process_variable_name(line[1])] = process_value(line[0])
        return
    if line.startswith("?"):
        line = line[1:].split()
        assert len(line)==2, "Wrong syntax: expected `?value varname`"
        value = process_value(line[0])
        assert isinstance(value, int), "?value can only be applied on number values"
        vars[process_variable_name(line[1])] = random.randint(0, value) if value>=0 else -random.randint(0, -value)
        return
    if line.startswith("+"):
        line = line[1:].split()
        assert len(line)==2, "Wrong syntax: expected `+value varname`"
        value = process_value(line[0])
        var = process_variable_name(line[1])
        assert isinstance(value, int), "+value can only be applied on number values"
        assert var in vars, "This was previously not set: "+var
        assert isinstance(vars[var], int), "-value can only be applied on number variables"
        vars[var] += value
        return
    if line.startswith("-"):
        line = line[1:].split()
        assert len(line)==2, "Wrong syntax: expected `-value varname`"
        value = process_value(line[0])
        var = process_variable_name(line[1])
        assert isinstance(value, int), "-value can only be applied on number values"
        assert var in vars, "This was previously not set: "+var
        assert isinstance(vars[var], int), "-value can only be applied on number variables"
        vars[var] -= value
        return
    if line.startswith("*"):
        line = line[1:].split()
        assert len(line)==2, "Wrong syntax: expected `*value varname`"
        value = process_value(line[0])
        var = process_variable_name(line[1])
        assert isinstance(value, int), "*value can only be applied on number values"
        assert var in vars, "This was previously not set: "+var
        assert isinstance(vars[var], int), "-value can only be applied on number variables"
        vars[var] *= value
        return
    if line.startswith("/"):
        line = line[1:].split()
        assert len(line)==2, "Wrong syntax: expected `/value varname`"
        value = process_value(line[0])
        var = process_variable_name(line[1])
        assert isinstance(value, int), "/value can only be applied on number values"
        assert var in vars, "This was previously not set: "+var
        assert isinstance(vars[var], int), "-value can only be applied on number variables"
        vars[var] /= value
        return
    if line.startswith("^"):
        args = line[1:].strip().split(" ", 2)
        args = [vars.get("["+arg.strip()+"]", arg.strip()) for arg in args]
        assert isinstance(args[1], str)
        line = args[1]*int(args[0])
    for var, value in vars.items():
        line = line.replace(var, str(value))
    return line


if __name__=="__main__":
    import sys
    book_path = "book.st"
    test_mode = 0
    i = 0
    while i < len(sys.argv)-1:
        i += 1
        arg = sys.argv[i]
        if arg == "--test":
            if i>=len(sys.argv)-1:
                test_mode = 1000
            else:
                test_mode = int(sys.argv[i+1])
            i += 1
        else:
            book_path = arg


    lines = list()
    printed = dict()
    ui = list()
    macros = dict()
    macro_args = dict()
    
    def draw(max_lines=20,fewer_lines=0, skipping = False):
        max_lines -= fewer_lines
        if not test_mode: print(clear_screen)
        ui_lines = 0
        accum = ""
        for line in ui:
            if line is None:   # invalidated lines by overwriting components
                continue
            line = process_line(line)
            if line is None:
                continue
            if line.endswith("[noend]"):
                accum += line
                continue
            if not test_mode: print((accum+line).replace("[noend]", "")+vars["[reset]"])
            ui_lines += 1
            accum = ""
        assert not accum
        total_lines = 0
        for line in lines:
            if line is None:
                continue
            if line.endswith("[noend]"):
                continue
            total_lines += 1
        for _ in range(max_lines-total_lines-ui_lines):
            if not test_mode: print()
        count_lines = 0
        accum = ""
        for line in lines:
            if line is None:
                continue
            if line.endswith("[noend]"):
                accum += line
                continue
            if count_lines >= total_lines-max_lines+ui_lines:
                text = (accum+line).replace("[noend]", "")+vars["[reset]"]
                printer = not text.startswith("|") or text=="|"
                if not printer:
                    text = text[1:]
                elif skipping:
                    printer = False
                accum = ""
                if not printed.get(count_lines, False):
                    printed[count_lines] = True
                    count_lines += 1
                    if printer:
                        delay = float(vars["[__refresh]"]) / 1000.0
                        if not test_mode: skipping = print_with_skip(text, delay)
                    elif not test_mode: print(text)
                else:
                    count_lines += 1
                    if not test_mode: print(text)
            else:
                count_lines += 1
        #assert not accum
        return skipping

    declaring_ui = False
    waiting_for = ""
    restarts = True
    ui_components = dict()
    test_mode_progress = 0

    def print_test_resulst():
        print("\033[2J\033[H")
        print(f"Testing {test_mode_progress}/{test_mode}")


    while restarts:
        declaring_ui = False
        declaring_macro = ""
        restarts = False
        skipping = False
        file_lines = list()
        with open(book_path) as file:
            for i, line in enumerate(file):
                file_lines.append((i,line))
        try:
            current_line = 0
            while current_line < len(file_lines):
                line = file_lines[current_line][1]
                current_line = current_line + 1
                if line[-1]=="\n":
                    line = line[:-1]
                line = line.strip()
                if not line:
                    continue
                if declaring_macro:
                    if line.startswith("&"):
                        declaring_macro = ""
                    else:
                        macros[declaring_macro].append((current_line-1, line))
                elif line.startswith("#"):
                    line = line[1:].strip()
                    if line==waiting_for:
                        waiting_for = ""
                        skipping = False
                elif waiting_for:
                    pass
                elif line.startswith("&"):
                    declaring_macro = process_line(line[1:].strip())
                    assert declaring_macro is not None
                    declaring_macro = declaring_macro.split()
                    assert declaring_macro
                    assert declaring_macro[0]
                    macros[declaring_macro[0]] = list()
                    macro_args[declaring_macro[0]] = declaring_macro[1:]
                    declaring_macro = declaring_macro[0]
                elif line.startswith("%"):
                    if declaring_ui:
                        ui_component = ui_components[ui_component_name].append(len(ui)) # get current name
                        ui_components 
                    ui_component_name = process_line(line[1:].strip())
                    assert ui_component_name is not None
                    if declaring_ui:
                        assert not ui_component_name
                    else:
                        if ui_component_name in ui_components:
                            for i in range(*ui_components[ui_component_name]):
                                ui[i] = None
                        ui_components[ui_component_name] = [len(ui)]
                    declaring_ui = not declaring_ui
                elif declaring_ui:
                    ui.append(line)
                else:
                    line = process_condition(line)
                    if line is None: 
                        pass
                    elif line.startswith("`"):
                        line = line[1:].strip()
                        line = process_line(line)
                        assert line is not None
                        if test_mode: continue
                        draw(fewer_lines=1)
                        print(vars["[yellow]"]+"["+line+"]"+vars["[reset]"], end="", flush=True)
                        while True:
                            c = readchar()
                            if c==KEY_SPACE or c==KEY_ENTER:
                                break
                    elif line.startswith("\\\\"):
                        macro_to_apply = process_line(line[2:].strip())
                        assert macro_to_apply
                        pos = macro_to_apply.find(' ') 
                        if pos == -1:
                            macro_to_apply = [macro_to_apply]
                        else:
                            macro_to_apply = [macro_to_apply[:pos]]+macro_to_apply[pos:].split(",")
                        to_inject = macros[macro_to_apply[0]]
                        assert len(macro_args[macro_to_apply[0]]) == len(macro_to_apply)-1
                        for arg,value in zip(macro_args[macro_to_apply[0]], macro_to_apply[1:]):
                            to_inject = [(i,text.replace("["+arg+"]", value)) for i,text in to_inject]
                        file_lines = to_inject + file_lines[current_line:]
                        current_line = 0
                        # we do this trick here to also clean up memory while applying macros,
                        # memory would grow based on macro usage anyway, but also we don't do
                        # the clean up continuously to stress the program
                    elif line.startswith("<<<"):
                        waiting_for = line[3:].strip()
                        waiting_for = process_line(waiting_for)
                        waiting_for_origin = file_lines[current_line]
                        if not waiting_for:
                            lines.clear()
                            printed.clear()
                            continue
                        assert waiting_for
                        options = waiting_for.split(",")
                        selection = random.randint(0,len(options)-1)
                        while len(options)!=1 and not test_mode:
                            opt = ""
                            for i, option in enumerate(options):
                                if i==selection:
                                    opt += vars["[yellow]"]
                                opt += "["+option+"] "
                                if i==selection:
                                    opt += vars["[reset]"]
                            draw(fewer_lines=1)
                            print(opt, end="", flush=True)
                            c = readchar()
                            if c==KEY_LEFT:
                                selection -= 1
                                if selection<0:
                                    selection = 0
                            if c==KEY_RIGHT:
                                selection += 1
                                if selection>=len(options):
                                    selection = len(options)-1
                            if c==KEY_SPACE or c==KEY_ENTER:
                                break
                        waiting_for = options[selection]
                        waiting_for_origin = file_lines[current_line]
                        assert not declaring_ui
                        if waiting_for:
                            restarts = True
                            lines.clear()
                            printed.clear()
                            break
                    elif line.startswith(">>>"):
                        waiting_for = line[3:].strip()
                        waiting_for = process_line(waiting_for)
                        if not waiting_for: continue
                        options = waiting_for.split(",")
                        selection = random.randint(0,len(options)-1)
                        while len(options)!=1 and not test_mode:
                            opt = ""
                            for i, option in enumerate(options):
                                if i==selection:
                                    opt += vars["[yellow]"]
                                opt += "["+option+"] "
                                if i==selection:
                                    opt += vars["[reset]"]
                            draw(fewer_lines=1)
                            print(opt, end="", flush=True)
                            c = readchar()
                            if c==KEY_LEFT:
                                selection -= 1
                                if selection<0:
                                    selection = 0
                            if c==KEY_RIGHT:
                                selection += 1
                                if selection>=len(options):
                                    selection = len(options)-1
                            if c==KEY_SPACE or c==KEY_ENTER:
                                break
                        waiting_for = options[selection]
                        waiting_for_origin = file_lines[current_line]
                        assert not declaring_ui
                    else:
                        line = process_line(line)
                        if line is not None:
                            for line in line.split("\n"):
                                lines.append(line)
                                skipping = draw(skipping=skipping)
            if waiting_for is not None and waiting_for!="" and not restarts:
                if test_mode: print_test_resulst()
                print(f"\n\033[031mError\033[0m did not find a next `{waiting_for}` at book.st line {waiting_for_origin[0]}\n"+waiting_for_origin[1])
                exit(0)
        except AssertionError as e:
            if test_mode: print_test_resulst()
            print(f"\n\033[031mError\033[0m {e} at book.st line {file_lines[current_line][0]}\n"+file_lines[current_line][1])
            exit(0)
        except Exception as e:
            if test_mode: print_test_resulst()
            print(f"\n\033[031mError\033[0m {e} at book.st line {file_lines[current_line][0]}\n"+file_lines[current_line][1])
            raise e
        if test_mode:
            test_mode_progress += 1
            print_test_resulst()
            if test_mode_progress<test_mode:
                restarts = True
    draw()
