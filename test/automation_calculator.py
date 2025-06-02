#!python3
# -*- coding: utf-8 -*-
# works on windows XP, 7, 8, 8.1 and 10
import os
import sys
import time
import subprocess
import multiprocessing as mp

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # not required after 'pip install uiautomation'
import uiautomation as auto

auto.uiautomation.DEBUG_EXIST_DISAPPEAR = True  # set it to False and try again, default is False
auto.uiautomation.DEBUG_SEARCH_TIME = True  # set it to False and try again, default is False
auto.uiautomation.TIME_OUT_SECOND = 7  # global time out
print('timeout: {}, old {} is not effective'.format(auto.uiautomation.TIME_OUT_SECOND, auto.TIME_OUT_SECOND))
auto.uiautomation.SetGlobalSearchTimeout(6)  # global time out
print('timeout: {}, old {} is not effective'.format(auto.uiautomation.TIME_OUT_SECOND, auto.TIME_OUT_SECOND))

def GifProcess(stopEvent: mp.Event, calcHandle: int):
    calcWindow = auto.ControlFromHandle(calcHandle)
    bmps = []
    intervalMs = 50
    while True:
        if stopEvent.is_set():
            break
        bmps.append(calcWindow.ToBitmap(captureCursor=True))
        time.sleep(intervalMs / 1000)
    auto.GIF.ToGifFile('calc.gif', bmps, [intervalMs]*len(bmps))

def Calc(window, btns, expression):
    expression = ''.join(expression.split())
    if not expression.endswith('='):
        expression += '='
    for char in expression:
        auto.Logger.Write(char, writeToFile=False)
        btns[char].Click(waitTime=0.05)
    time.sleep(0.1)
    window.SendKeys('{Ctrl}c', waitTime=0.1)
    result = auto.GetClipboardText()
    auto.Logger.WriteLine(result, auto.ConsoleColor.Cyan, writeToFile=False)
    time.sleep(1)

def CalcOnWindows10():
    """works on Windows 10.0.19042"""
    char2Id = {
        '0': 'num0Button',
        '1': 'num1Button',
        '2': 'num2Button',
        '3': 'num3Button',
        '4': 'num4Button',
        '5': 'num5Button',
        '6': 'num6Button',
        '7': 'num7Button',
        '8': 'num8Button',
        '9': 'num9Button',
        '.': 'decimalSeparatorButton',
        '+': 'plusButton',
        '-': 'minusButton',
        '*': 'multiplyButton',
        '/': 'divideButton',
        '=': 'equalButton',
        '(': 'openParenthesisButton',
        ')': 'closeParenthesisButton',
    }
    # Desc is not a valid search property, but it can be used for debug printing
    calcWindow = auto.WindowControl(searchDepth=1, ClassName='ApplicationFrameWindow',
                                    Compare=lambda c, d: c.Name == 'Calculator' or c.Name == '计算器', Desc='Calculator Window')
    if not calcWindow.Exists(0, 0):
        subprocess.Popen('calc')
    calcWindow.SetActive()
    calcWindow.GetTransformPattern().Move(40, 40)
    stopEvent = mp.Event()
    process = mp.Process(target=GifProcess, args=(stopEvent, calcWindow.NativeWindowHandle))
    process.start()
    time.sleep(0.1)
    calcWindow.ButtonControl(AutomationId='TogglePaneButton').Click()
    calcWindow.ListItemControl(AutomationId='Scientific').Click()
    calcWindow.ButtonControl(AutomationId='clearButton').Click()
    if 0:
        char2Button = {key: calcWindow.ButtonControl(AutomationId=char2Id[key], Desc='Button ' + key) for key in char2Id}
    else:
        # Run faster because it only walk calc window once
        id2char = {v: k for k, v in char2Id.items()}
        char2Button = {}
        for c, d in auto.WalkControl(calcWindow):
            if c.AutomationId in id2char:
                char2Button[id2char[c.AutomationId]] = c
    Calc(calcWindow, char2Button, '1234 * (4 + 5 + 6) - 78 / 90.8')
    Calc(calcWindow, char2Button, '3*3+4*4')
    Calc(calcWindow, char2Button, '2*3.14159*10')
    stopEvent.set()
    calcWindow.CaptureToImage('calc.png', captureCursor=True)
    char2Button['8'].CaptureToImage('calc_8.png')
    calcWindow.Disappears(1)
    calcWindow.GetWindowPattern().Close()
    calcWindow.Exists(1)
    process.join()
    subprocess.Popen('calc.gif', shell=True)

if __name__ == '__main__':
    
    CalcOnWindows10()
    auto.Logger.Write('\nPress any key to exit', auto.ConsoleColor.Cyan)
    import msvcrt
    while not msvcrt.kbhit():
        time.sleep(0.05)
