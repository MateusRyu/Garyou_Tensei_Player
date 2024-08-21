import curses
from curses.textpad import rectangle
from curses import wrapper
from config_loader import load_config
import subprocess

class WindowTooSmallError(Exception):
    pass

def check_window_size(screen, state):
    height, width = screen.getmaxyx()
    if height < state["min_height"] or width < state["min_width"]:
        curses.halfdelay(5)
        raise WindowTooSmallError(f"Window too small: {height}x{width}. Minimum size required: {state["min_height"]}x{state["min_width"]}.", [height, width, state])
    return [height, width]

def main(screen):
    screen.nodelay(False)
    config = load_config()
    keys = config["keybind"]
    curses.curs_set(0)
    load_colors()

    screen.clear()
    screen.refresh()

    state = {
        "key": 0,
        "cursor_x": 0,
        "cursor_y": 0,
        "min_height": 30,
        "min_width": 80,
    }

    while state["key"] != ord(keys["close_app"]):
        try:
            state = main_looping(screen, state, keys)
        except WindowTooSmallError as e:
            screen.clear()
            print(e.args[0])
            screen.addstr("\nWindow too small: ")
            args = e.args[1]
            state = args[2]

            if state["key"] == ord(keys["close_app"]):
                exit()

            if args[0] < state["min_height"]:
                screen.addstr(str(args[0]), curses.color_pair(2))
            else:
                screen.addstr(str(args[0]))
            screen.addstr(" x ")
            if args[1] < state["min_width"]:
                screen.addstr(str(args[1]), curses.color_pair(2))
            else:
                screen.addstr(str(args[1]))

            screen.addstr(f"\nMinimum size required: {state["min_height"]}x{state["min_width"]}.\n key = {state["key"]}")
            screen.refresh()
            screen.getch()


def main_looping(screen, state, keys):
    screen.clear()
    curses.cbreak()
    height, width = check_window_size(screen, state)

    if state["key"] == curses.KEY_DOWN:
        cursor_y = cursor_y + 1
    elif state["key"] == curses.KEY_UP:
        cursor_y = cursor_y - 1
    elif state["key"] == curses.KEY_RIGHT:
        cursor_x = cursor_x + 1
    elif state["key"] == curses.KEY_LEFT:
        cursor_x = cursor_x -1

    state = limit_cursor(state, 0, width-1, 0, height-1)

    # STRINGS
    title = "Garyou Tensei Player"[:width-1]
    subtitle = "By Mateu Ryu Yamaguchi"[:width-1]
    key_pressed = f"Last key pressed: {state["key"]}"[:width-1]
    status_bar = f"Press '{keys["close_app"]}' to exit | STATUS BAR | Pos: {state["cursor_x"]}, {state["cursor_y"]}"
    if state["key"] == 0:
        key_str = "No key press detected..."[:width-1]

    title_origin_x = get_start_to_center_string(title, width)
    subtitle_origin_x = get_start_to_center_string(subtitle, width)
    key_pressed_origin_x = get_start_to_center_string(key_pressed, width)
    start_y = int((height//2) - 2 )

    size_string = f"Width: {width}, Height: {height}"
    screen.addstr(0, 0, size_string, curses.color_pair(1))

    screen.attron(curses.color_pair(3))
    screen.addstr(height-1, 0, status_bar)
    screen.addstr(height-1, len(status_bar), " " * (width - len(status_bar) - 1))
    screen.attroff(curses.color_pair(3))

    set_attributes_title(screen, True)
    screen.addstr(start_y, title_origin_x, title)
    set_attributes_title(screen, False)

    screen.addstr(start_y + 1, subtitle_origin_x, subtitle)
    screen.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
    screen.addstr(start_y + 5, key_pressed_origin_x, key_pressed)
    screen.move(state["cursor_y"], state["cursor_x"])

    screen.refresh()

    state["key"] = screen.getch()
    return state

def set_attributes_title(screen, trigger):
    if trigger == True:
        screen.attron(curses.color_pair(2))
        screen.attron(curses.A_BOLD)
    else:
        screen.attroff(curses.color_pair(2))
        screen.attroff(curses.A_BOLD)

def get_start_to_center_string(string, width):
    start_position = int((width//2) - (len(string)//2) % 2)
    return start_position

def limit_cursor(state, min_x, max_x, min_y, max_y):
    state["cursor_x"] = max(min_x, state["cursor_x"])
    state["cursor_x"] = min(max_x, state["cursor_x"])
    state["cursor_y"] = max(min_y, state["cursor_y"])
    state["cursor_y"] = min(max_y, state["cursor_y"])
    return state

def load_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)


def display_playlist(screen, playlist_win):
    playlist = subprocess.check_output(['mpc', 'playlist']).decode('utf-8').splitlines()
    playlist_win.addstr(str(playlist))
    playlist_win.clear()
    playlist_win.box()
    max_y, max_x = playlist_win.getmaxyx()

    for i, song in enumerate(playlist[:max_y - 2]):
        playlist_win.addstr(i + 1, 1, song[:max_x - 2])
    playlist_win.refresh()

wrapper(main)
