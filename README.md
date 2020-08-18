## Sleep-In-Peace

A simple taskbar tool to stop(SIGSTOP) and continue(SIGCONT) a running process by clicking on its window. 

Can be used to pause power-hungry browsers and IDEs when don't want to close them. 

What it does is equivalent to  `xprop _NET_WM_PID | cut -d' ' -f3 | xargs kill -STOP` and `-CONT`. 

PIDs of paused processes are at `/tmp/sleepinpeace.txt`. This is not always reliable, but may help if anything goes wrong: Ctrl-Alt-F\* to console and `kill -CONT ` these manually. 

**Requirements:** 

xprop

python3-pyqt5

**Warning:** 

Use as your own risk. For example, click on desktop or task bar will pause some parts of your desk environment. And all actions done on paused window will have effect when the window is resumed. Try to pause VM may trap your mouse inside it. Try to pause `xfce4-terminal` will pause all terminal windows, while things running inside are untouched. 



