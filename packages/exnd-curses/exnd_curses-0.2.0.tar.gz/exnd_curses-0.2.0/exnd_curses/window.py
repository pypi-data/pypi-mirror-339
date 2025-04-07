import curses;
from actions import defaultBinding

class Window:
    def __init__(self):
        self.__stdscr = curses.initscr();
        curses.cbreak();
        curses.noecho();
        self.__stdscr.keypad(True);
        self.__lines = "";
        self.__linesCount = 0;
        self.__linePtr = 0;
        self.__getInput = False;
        self.__defaultBinding = defaultBinding(self.__printPrev, self.__printNext, self.__closeWindowKeyPress);
    
    def changeGetInput(self, b: bool):
        self.__getInput = b;
        return b;
    
    def displayText(self, s: str, n: int | None = None):
        if n == None:
            self.__stdscr.move(0, 0);
            self.__stdscr.clrtobot();
        else:
            for i in range(0, n):
                self.__stdscr.move(i, 0)  # Move to the start of the line
                self.__stdscr.clrtoeol()  # Clear to the end of the line
            self.__stdscr.move(0, 0);
        self.__stdscr.addstr(s);
        self.__stdscr.refresh();
    
    def changeLines(self, lines: str):
        self.__lines = lines.splitlines();
        self.__linesCount = len(self.__lines);
        self.__linePtr = 0;
        if self.__stdscr.getmaxyx()[0] >= self.__linesCount:
            lines = ""
            for i in self.__lines:
                lines += (i if len(i) <= (l:=self.__stdscr.getmaxyx()[1]) else i[:l-4]+"...") + "\n";
            self.displayText(lines);
        else:
            lines = ""
            for i in self.__lines[self.__linePtr: self.__stdscr.getmaxyx()[0] + self.__linePtr - 1]:
                lines += (i if len(i) <= (l:=self.__stdscr.getmaxyx()[1]) else i[:l-4]+"...") + "\n";
            lines += "MORE---v";
            self.displayText(lines)
        self.__getInput = True
        self.__nextCharInput()

    def closeWindow(self):
        curses.echo()
        curses.nocbreak()
        self.__stdscr.keypad(False)
        curses.endwin()
        exit()

    def __checkKeyPressAction(self, code: int):
        binding = self.__defaultBinding.get_string(code)
        binding.execute()
        self.__nextCharInput()
    
    def __nextCharInput(self):
        if self.__getInput:
            key = self.__stdscr.getch();
            self.__checkKeyPressAction(key);
    
    def __printNext(self):
        if (self.__linesCount > self.__stdscr.getmaxyx()[0]):
            self.__linePtr = self.__linePtr if self.__linePtr == self.__linesCount - self.__stdscr.getmaxyx()[0] + 1 else self.__linePtr + 1;
            self.__getstr(False if self.__linePtr == self.__linesCount - self.__stdscr.getmaxyx()[0] + 1 else True);
    
    def __printPrev(self):
        if (self.__linesCount > self.__stdscr.getmaxyx()[0]):
            self.__linePtr = 0 if self.__linePtr == 0 else self.__linePtr - 1;
            self.__getstr();
    
    def __closeWindowKeyPress(self):
        self.displayText("Exiting...")
        self.closeWindow();
    
    def __getstr(self, m=True):
        if self.__stdscr.getmaxyx()[0] >= self.__linesCount:
            lines = ""
            for i in self.__lines:
                lines += (i if len(i) <= (l:=self.__stdscr.getmaxyx()[1]) else i[:l-4]+"...") + "\n";
            self.displayText(lines);
        else:
            lines = ""
            for i in self.__lines[self.__linePtr: self.__stdscr.getmaxyx()[0] + self.__linePtr - 1]:
                lines += (i if len(i) <= (l:=self.__stdscr.getmaxyx()[1]) else i[:l-4]+"...") + "\n";
            if m==True:
                lines += "MORE---v";
            self.displayText(lines);
    
