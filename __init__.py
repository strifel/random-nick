import array
from st3m.application import Application, ApplicationContext
from st3m.ui.colours import PUSH_RED, GO_GREEN, BLACK
from st3m.goose import Dict, Any
from st3m.input import InputState
from ctx import Context
import leds
import random

import json
import math


class Configuration:
    def __init__(self) -> None:
        self.names = ["flow3r"]
        self.pronouns = ["meow/meow"]
        self.size: int = 75
        self.font: int = 5
        self.time: int = 2000

    @classmethod
    def load(cls, path: str) -> "Configuration":
        res = cls()
        try:
            with open(path) as f:
                jsondata = f.read()
            data = json.loads(jsondata)
        except OSError:
            data = {}
        if "names" in data:
            res.names = data["names"]
        if "pronouns" in data:
            res.pronouns = data["pronouns"]
        if "time" in data:
            if type(data["time"]) == float:
                res.time = int(data["time"])
            if type(data["time"]) == int:
                res.time = data["time"]
        if "size" in data:
            if type(data["size"]) == float:
                res.size = int(data["size"])
            if type(data["size"]) == int:
                res.size = data["size"]
        if "font" in data and type(data["font"]) == int:
            res.font = data["font"]
        return res

    def save(self, path: str) -> None:
        d = {
            "names": self.names,
            "pronouns": self.pronouns,
            "size": self.size,
            "font": self.font,
            "time": self.time
        }
        jsondata = json.dumps(d)
        with open(path, "w") as f:
            f.write(jsondata)
            f.close()


class RandomNickApp(Application):
    def __init__(self, app_ctx: ApplicationContext) -> None:
        super().__init__(app_ctx)
        self._ledPhase = 0
        self._led = 0.0
        self._time = 0
        self._filename = "/flash/nick_random.json"
        self._config = Configuration.load(self._filename)
        self._name = random.choice(self._config.names)
        self._pronouns = random.choice(self._config.pronouns)

    def draw(self, ctx: Context) -> None:
        ctx.text_align = ctx.CENTER
        ctx.text_baseline = ctx.MIDDLE
        ctx.font_size = self._config.size
        ctx.font = ctx.get_font_name(self._config.font)

        ctx.rgb(0, 0, 0).rectangle(-120, -120, 240, 240).fill()
        ctx.rgb(*GO_GREEN)

        ctx.move_to(0, -20)
        ctx.save()
        ctx.scale(1, 1)
        ctx.text(self._name)
        ctx.scale(0.8, 1)
        ctx.move_to(0, 20)
        ctx.text(self._pronouns)
        ctx.restore()

        leds.set_hsv(int(self._led), abs(math.sin(self._ledPhase)) * 360, 1, 0.2)

        leds.update()
        # ctx.fill()

    def on_exit(self) -> None:
        self._config.save(self._filename)

    def think(self, ins: InputState, delta_ms: int) -> None:
        super().think(ins, delta_ms)

        self._time += delta_ms
        if self._time >= self._config.time:
            name = random.choice(self._config.names)
            pronouns = random.choice(self._config.pronouns)
            if (name != self._name or pronouns != self._pronouns):
                self._name = name
                self._pronouns = pronouns
                self._time = 0

        self._led += delta_ms / 45
        if self._led >= 40:
            self._led = 0
        self._ledPhase += delta_ms / 1000