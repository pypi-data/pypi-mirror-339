from window import Window;

try:
    window = Window();
    line = "dasda\nfdssf\ndsfsdf\ndsafsdf\ndsfsd\ndasda\nfdssf\ndsfsdf\ndsafsdf\ndsfsd\ndasda\nfdssf\ndsfsdf\ndsafsdf\ndsfsd\ndasda\nfdssf\ndsfsdf\ndsafsdf\ndsfsd\ndasda\nfdssf\ndsfsdf\ndsafsdf\ndsfsd\ndasda\nfdssf\ndsfsdf\ndsafsdf\ndsfsd\ndasda\nfdssf\ndsfsdf\ndsafsdf\ndsfsd\nLast";
    window.changeLines(line);
    # curses.napms(2000);
    # window.closeWindow();
    del window;
except Exception as e:
    print(e);