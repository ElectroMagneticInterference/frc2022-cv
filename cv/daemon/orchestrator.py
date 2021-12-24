from thread_generics import killable, freezable, Logging
from threading import Thread
from logging import Logger


class display_thread(freezable, killable, Logging, Thread):
    name = "Display"

    def run(s):
        while s.alive:
            if s.frozen:
                sleep(0)
                continue
            pass


class processing_thead(freezable, killable, Logging, Thread):
    name = "processing"

    def __init__(s, host_name: str, id: str, input: list, output: list, group) -> None:
        s.input = input
        s.output = output
        super().__init__(host_name=host_name, id=id, group=group)

    def run(s):
        while s.alive:
            if s.frozen:
                sleep(0)
                continue
            pass


class capture_thread(freezable, killable, Logging, Thread):
    name = "Capture"
    camera = None

    def __init__(self) -> None:
        super().__init__()

    def run(s):
        while s.alive:
            if s.frozen:
                sleep(0)
                continue
            pass


class cv_orchestrator(freezable, killable, Thread):
    unprocessed_buffer = []
    processed_buffer = []

    def __init__(s, id, camera, group: None = ...) -> None:
        s.id = id
        s.name = f"frc2927-cv.Orchestrator={id}"
        s.logger = Logger(f"frc2927-cv.Orchestrator={id}")

        s.display = display_thread(host_name=s.name, group=group)

        s.processing_theads = [
            processing_thead(
                host_name=s.name,
                id=0,
                input=s.unprocessed_buffer,
                output=s.processed_buffer,
                group=group,
            )
        ]

        s.capture = capture_thread(camera=camera, host_name=s.name, group=group)

        s.group = group

        super().__init__(group=group)

    def freeze(s):
        s.logger.info("Freezing")
        s.display.freeze()
        s.capture.freeze()
        for thread in s.processing_theads:
            thread.freeze()

    def run(s):
        while s.alive:
            if s.frozen:
                sleep(0)
                continue
            pass


"""
PUESDO CODE:
    THE ORCHESTRATOR

# storage
'processed images list'
'unporccessed images list'

# controlling
'display'
'process'
'capture' 


TODO: FINISH SUDO CODE BEFORE PROCEEDING


END
"""

from time import sleep

if __name__ == "__main__":
    orc = cv_orchestrator()

    sleep(10)
