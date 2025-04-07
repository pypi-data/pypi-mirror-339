import curses
import json
from curses import window

keyCodesDict = {}
with open('codeCharBinding.json', 'r') as file:
    keyCodesDict = json.load(file)

class Binding:
    def __init__(self, key: str, code: int, action):
        self.key = key
        self.code = code
        self.__function = action
    def addAction(self, func):self.__function = func;
    def execute(self):self.__function();

class windowBinding:
    def __init__(self, window: curses.window):
        self.__window = window
        self.__bindings = {}
    def addBinding(self, binding: Binding):
        self.__bindings[binding.code] = binding


class defaultBinding:
    def __init__(self, printPrev, printNext, closeWindow):
        self.__printPrev = printPrev
        self.__printNext = printNext
        self.__closeWindow = closeWindow
        self.__bindings = {
            451: Binding(keyCodesDict["451"], 451, self.__printPrev),
            339: Binding(keyCodesDict["339"], 339, self.__printPrev),
            457: Binding(keyCodesDict["457"], 457, self.__printNext),
            338: Binding(keyCodesDict["338"], 338, self.__printNext),
            27: Binding(keyCodesDict["27"], 27, self.__closeWindow),
        }

    def get_string(self, code):
        try:return self.__bindings[code]
        except:None
