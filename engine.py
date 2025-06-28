import readchar
import sys
import time
import threading
import random

import sys
import time
import threading

# --- Platform Detection and Setup ---
if sys.platform == 'win32':
    import msvcrt
    def key_pressed():
        return msvcrt.kbhit()
    def get_key():
        return msvcrt.getch().decode('utf-8', errors='ignore')
    class TerminalInput:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
else:
    import termios
    import tty
    import select
    def key_pressed():
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        return bool(dr)
    def get_key():
        return sys.stdin.read(1)
    class TerminalInput:
        def __enter__(self):
            self.fd = sys.stdin.fileno()
            self.old_settings = termios.tcgetattr(self.fd)
            tty.setcbreak(self.fd)
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)

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

def process_line(line):
    while True:
        if line.startswith("!"):
            args = line[1:].strip().split(" ")
            assert len(args)>2
            argv = [vars.get("["+arg.strip()+"]", arg.strip()) for arg in args][:2]
            if str(vars.get(argv[1],argv[1])) == str(vars.get(argv[0],argv[0])):
                return
            line = " ".join(args[2:])
            continue
        if line.startswith("@"):
            args = line[1:].strip().split(" ")
            assert len(args)>2
            argv = [vars.get("["+arg.strip()+"]", arg.strip()) for arg in args][:2]
            if str(vars.get(argv[1],argv[1])) != str(vars.get(argv[0],argv[0])):
                return
            line = " ".join(args[2:])
            continue
        if line.startswith(">"):
            args = line[1:].strip().split(" ")
            assert len(args)>2
            argv = [vars.get("["+arg.strip()+"]", arg.strip()) for arg in args][:2]
            if int(vars.get(argv[1],argv[1])) <= int(vars.get(argv[0],argv[0])):
                return
            line = " ".join(args[2:])
            continue
        if line.startswith("<"):
            args = line[1:].strip().split(" ")
            assert len(args)>2
            argv = [vars.get("["+arg.strip()+"]", arg.strip()) for arg in args][:2]
            if int(vars.get(argv[1],argv[1])) >= int(vars.get(argv[0],argv[0])):
                return
            line = " ".join(args[2:])
            continue
        if line.startswith("="):
            line = line[1:].split()
            assert len(line)==2
            var = "["+line[1]+"]"
            value = vars.get("["+line[0]+"]", line[0])
            value = vars.get(line[0], line[0])
            try:
                value = int(value)
            except:
                assert value[0]=="\"" and value[-1]=="\"" and len(value)>=2, value
                value = value[1:-1]
            vars[var] = value
            return
        if line.startswith("?"):
            line = line[1:].split()
            assert len(line)==2
            var = "["+line[1]+"]"
            value = vars.get(line[0], line[0])
            try:
                value = int(value)
                if value < 0:
                    value = -random.randint(0, -value)
                else:
                    value = random.randint(0, value)
            except:
                raise Exception("Only numbers can get random values")
            vars[var] = value
            return
        if line.startswith("+"):
            line = line[1:].split()
            assert len(line)==2
            var = "["+line[1]+"]"
            vars[var] += int(vars.get(line[0], line[0]))
            return
        if line.startswith("-"):
            line = line[1:].split()
            assert len(line)==2
            var = "["+line[1]+"]"
            vars[var] -= int(vars.get(line[0], line[0]))
            return
        if line.startswith("*"):
            line = line[1:].split()
            assert len(line)==2
            var = "["+line[1]+"]"
            vars[var] *= int(vars.get(line[0], line[0]))
            return
        if line.startswith("/"):
            line = line[1:].split()
            assert len(line)==2
            var = "["+line[1]+"]"
            vars[var] /= int(vars.get(line[0], line[0]))
            return
        break
        
    if line.startswith("^"):
        args = line[1:].strip().split(" ", 2)
        args = [vars.get("["+arg.strip()+"]", arg.strip()) for arg in args]
        assert isinstance(args[1], str)
        line = args[1]*int(args[0])
    for var, value in vars.items():
        line = line.replace(var, str(value))
    return line

lines = list()
printed = dict()
ui = list()
def draw(max_lines=20,fewer_lines=0, skipping = False):
    max_lines -= fewer_lines
    print(clear_screen)
    ui_lines = 0
    accum = ""
    for line in ui:
        line = process_line(line)
        if line is None:
            continue
        if line.endswith("[noend]"):
            accum += line
            continue
        print((accum+line).replace("[noend]", "")+vars["[reset]"])
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
        print()
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
                    skipping = print_with_skip(text, delay)
                else:
                    print(text)
            else:
                count_lines += 1
                print(text)
        else:
            count_lines += 1
    #assert not accum
    return skipping

declaring_ui = False
waiting_for = ""
restarts = True
while restarts:
    declaring_ui = False
    restarts = False
    skipping = False
    with open("book.st") as file:
        for line in file:
            if line[-1]=="\n":
                line = line[:-1]
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                line = line[1:].strip()
                if line==waiting_for:
                    waiting_for = ""
                    skipping = False
            elif waiting_for:
                pass
            elif line == "%":
                declaring_ui = not declaring_ui
            elif line.startswith("`"):
                line = line[1:].strip()
                line = process_line(line)
                assert line is not None
                draw(fewer_lines=1)
                print(vars["[yellow]"]+"["+line+"]"+vars["[reset]"], end="")
                sys.stdout.flush()
                while True:
                    c = readchar.readkey()
                    if c==readchar.key.SPACE or c==readchar.key.ENTER:
                        break
            elif line.startswith("<<<"):
                waiting_for = line[3:].strip()
                waiting_for = process_line(waiting_for)
                if not waiting_for:
                    lines.clear()
                    printed.clear()
                    continue
                assert waiting_for
                options = waiting_for.split(",")
                selection = 0
                while len(options)!=1:
                    opt = ""
                    for i, option in enumerate(options):
                        if i==selection:
                            opt += vars["[yellow]"]
                        opt += "["+option+"] "
                        if i==selection:
                            opt += vars["[reset]"]
                    draw(fewer_lines=1)
                    print(opt, end="")
                    sys.stdout.flush()
                    c = readchar.readkey()
                    if c==readchar.key.LEFT:
                        selection -= 1
                        if selection<0:
                            selection = 0
                    if c==readchar.key.RIGHT:
                        selection += 1
                        if selection>=len(options):
                            selection = len(options)-1
                    if c==readchar.key.SPACE or c==readchar.key.ENTER:
                        break
                waiting_for = options[selection]
                assert not declaring_ui
                if waiting_for:
                    restarts = True
                    lines.clear()
                    printed.clear()
                    ui.clear()
                    break
            elif line.startswith(">>>"):
                waiting_for = line[3:].strip()
                waiting_for = process_line(waiting_for)
                assert waiting_for
                options = waiting_for.split(",")
                selection = 0
                while len(options)!=1:
                    opt = ""
                    for i, option in enumerate(options):
                        if i==selection:
                            opt += vars["[yellow]"]
                        opt += "["+option+"] "
                        if i==selection:
                            opt += vars["[reset]"]
                    draw(fewer_lines=1)
                    print(opt, end="")
                    sys.stdout.flush()
                    c = readchar.readkey()
                    if c==readchar.key.LEFT:
                        selection -= 1
                        if selection<0:
                            selection = 0
                    if c==readchar.key.RIGHT:
                        selection += 1
                        if selection>=len(options):
                            selection = len(options)-1
                    if c=='F':
                        vars["[__refresh]"] = vars["[__refresh]"]*2/3
                    if c=='S':
                        if vars["[__refresh]"]==0:
                            vars["[__refresh]"] = 1
                        elif vars["[__refresh]"]<50:
                            vars["[__refresh]"] = vars["[__refresh]"]*3/2
                    if c==readchar.key.SPACE or c==readchar.key.ENTER:
                        break
                waiting_for = options[selection]
                assert not declaring_ui
            else:
                if declaring_ui:
                    ui.append(line)
                else:
                    line = process_line(line)
                    if line is not None:
                        for line in line.split("\n"):
                            lines.append(line)
                            skipping = draw(skipping=skipping)
draw()
