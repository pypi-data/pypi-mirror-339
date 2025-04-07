from window import Window;
import curses

try:
    # scr = curses.initscr()
    # curses.echo()
    # curses.cbreak()
    # scr.scrollok(True)
    # dic = {}
    # while True:
    #     code = scr.getch()
    #     value = scr.getkey()
    #     scr.move(0, 0)
    #     scr.clrtobot()
    #     with open('codeCharBinding.json', 'r') as file:
    #         dic = json.load(file)
    #     dic[str(code)] = value
    #     scr.addstr(str(dic))
    #     scr.refresh()
    #     with open('codeCharBinding.json', 'w') as file:
    #         json.dump(dic, file)
    window = Window();
    line = "dasda\nfdssf\ndsfsdf\ndsafsdf\ndsfsd\ndasda\nfdssf\ndsfsdf\ndsafsdf\ndsfsd\ndasda\nfdssf\ndsfsdf\ndsafsdf\ndsfsd\ndasda\nfdssf\ndsfsdf\ndsafsdf\ndsfsd\ndasda\nfdssf\ndsfsdf\ndsafsdf\ndsfsd\ndasda\nfdssf\ndsfsdf\ndsafsdf\ndsfsd\ndasda\nfdssf\ndsfsdf\ndsafsdf\ndsfsd\nLast";
    window.changeLines(line);
    # curses.napms(2000);
    # window.closeWindow();
    # del window;
except Exception or KeyboardInterrupt as e:
    curses.endwin();
    print(e)