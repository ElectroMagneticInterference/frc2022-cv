class killable:
    alive = True

    def stop(self):
        self.alive = False


class freezable:
    frozen = False

    def toggle_freeze(self):
        self.frozen = not self.frozen

    def freeze(self):
        self.frozen = True

    def unfreeze(self):
        self.frozen = False


from logging import Logger


class Logging:
    def __init__(s, host_name, id: str = ..., group: None = ...) -> None:
        if id != ...:
            s.id = id
            s.name += f"={id}"

        s.name = f"{host_name}.{s.name}"
        s.logger = Logger(s.name)

        super().__init__(group=group)
