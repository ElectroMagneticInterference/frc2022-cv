ESCAPE_CODE = "\033["
EC = ESCAPE_CODE


class cursor:
    ESCAPE_CODE = ESCAPE_CODE
    EC = ESCAPE_CODE
    HIDE = lambda: f"{EC}?25l"
    SHOW = lambda: f"{EC}?25h"
    UP = lambda n=1: f"{EC}{n}A"
    DOWN = lambda n=1: f"{EC}{n}B"
    FORWARD = lambda n=1: f"{EC}{n}C"
    BACKWARD = lambda n=1: f"{EC}{n}D"
    NEXT_LINE = lambda n=1: f"{EC}{n}E"
    PREVIOUS_LINE = lambda n=1: f"{EC}{n}F"
    HORIZONTAL_ABSOLUTE = lambda n=1: f"{EC}{n}G"
    MOVE_TO_POSITION = lambda n=1, m=1: f"{EC}{n};{m}H"
    ERASE_IN_DISPLAY = lambda n=0: f"{EC}{n}J"
    ERASE_IN_LINE = lambda n=0: f"{EC}{n}K"
    SCROLL_UP = lambda n=1: f"{EC}{n}S"
    SCROLL_DOWN = lambda n=1: f"{EC}{n}T"
    SAVE_POSITION = lambda: f"{EC}?25h"
    RESTORE_POSITION = lambda: f"{EC}?25h"

    CUU = UP
    CUD = DOWN
    CUF = FORWARD
    CUB = BACKWARD
    CNL = NEXT_LINE
    CPL = PREVIOUS_LINE
    CHA = HORIZONTAL_ABSOLUTE
    CUP = MOVE_TO_POSITION
    ED = ERASE_IN_DISPLAY
    EL = ERASE_IN_LINE
    SCP = SAVE_POSITION
    RCP = RESTORE_POSITION


from thread_generics import freezable, killable

from psutil import Process
from time import sleep
from datetime import datetime
from threading import Thread, main_thread


class performance_logger(Thread, freezable, killable):
    name = "Performance-Logger"
    text_to_print = []
    daemon = True
    log_datetime = False

    def run(self):
        process = Process()
        main = main_thread()
        text_to_print = ""

        print("\033[?25l\n\n")
        while self.alive and main.is_alive():
            if self.frozen:
                sleep(1)
                continue

            if len(self.text_to_print):

                for text in self.text_to_print:
                    text_to_print += (
                        cursor.CHA()
                        + cursor.CUD()
                        + (
                            (datetime.utcnow().isoformat() + " -> ")
                            if self.log_datetime
                            else ""
                        )
                        + text
                        + (" " * (20 - len(text)) if len(text) < 20 else "")
                    )

                self.text_to_print.clear()

            print(
                cursor.CUU() * 4 + text_to_print,
                f"Ram Usage: {round(process.memory_percent(),5)}%     ",
                f"CPU Usage: {round(process.cpu_percent(),5)}%       ",
                f"Threads: {len(process.threads())}       ",
                sep="\n",
            )

            text_to_print = ""

            sleep(1)

    def log(self, *text: str, sep: str | None = ...):

        if sep is not ...:
            result = ""
            for t in text:
                result += str(t) + sep

            self.text_to_print.append(result)
            return

        for t in text:
            self.text_to_print.append(str(t).strip())


"""
PSUEDO CODE:

hide the cursor

loop while alive:
    
    if there are 'requested prints':
    
        foreach text in 'requested prints':

            add 
                move cursor to first colomn
                move cursor down one row
                Datetime -> text 

            to 'text to print'
        
        empty 'requested prints'

    print 
        'text to print'
        performace info
    
move the cursor to newline
show the cursor

END

"""

"""
EXAMPLE:

>>> logger = performance_logger()
>>> logger.start()
Ram Usage: 0.25647%
CPU Usage: 0.0%
>>> logger.log("test")
test
Ram Usage: 0.24568%
CPU Usage: 0.0%
>>> logger.log("test2")
test
test2
Ram Usage: 0.26711%
CPU Usage: 0.0%
>>> logger.log_datetime = True
>>> logger.log("test3")
test
test2
2021-12-24T05:13:14.764688 -> test3
Ram Usage: 0.21356%
CPU Usage: 0.0%


  <> Note: performance statistics and datetimes may be different
"""

# Example:
if __name__ == "__main__":
    logger = performance_logger()

    logger.start()

    sleep(1)

    logger.log("Test")

    sleep(3)

    logger.log("test2")
    logger.log_datetime = True

    logger.log("test3")

    sleep(3)

    logger.log("test4")

    sleep(4)

    exit(0)

"""
Should result in:
```
Test
test2
2021-12-24T05:12:26.750781 -> test3
2021-12-24T05:12:29.867540 -> test4
Ram Usage: 0.2277%     
CPU Usage: 1.5%        
Threads: 15
```
  <> Note: performance statistics and datetimes may be different
"""
