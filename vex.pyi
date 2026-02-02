# vex.pyi
# Type stub for VEX V5 Python (editor-only)

# ---------------- Constants ----------------
import math, time

FORWARD: int
REVERSE: int

PERCENT: int
VOLT: int
RPM: int

DEGREES: int
TURNS: int

SECONDS: int
MSEC: int

COAST: int
BRAKE: int
HOLD: int


# ---------------- Enums ----------------

class GearSetting:
    RATIO_36_1: int
    RATIO_18_1: int
    RATIO_6_1: int


class FontType:
    MONO15: int
    MONO20: int
    MONO30: int


# ---------------- Ports ----------------

class Ports:
    PORT1: int
    PORT2: int
    PORT3: int
    PORT4: int
    PORT5: int
    PORT6: int
    PORT7: int
    PORT8: int
    PORT9: int
    PORT10: int
    PORT11: int
    PORT12: int
    PORT13: int
    PORT14: int
    PORT15: int
    PORT16: int
    PORT17: int
    PORT18: int
    PORT19: int
    PORT20: int


# ---------------- Brain ----------------

class Brain:
    def __init__(self): ...

    class Screen:
        def clear_screen(self): ...
        def print(self, *args): ...
        def set_font(self, font: int): ...
        def next_row(self): ...

    screen: Screen

    class ThreeWirePort:
        a: int
        b: int
        c: int
        d: int
        e: int
        f: int
        g: int
        h: int

    three_wire_port: ThreeWirePort


# ---------------- Controller ----------------

class Axis:
    def position(self, units: int = PERCENT) -> int: ...


class Button:
    def pressing(self) -> bool: ...
    def pressed(self, callback): ...


class Controller:
    def __init__(self): ...

    axis1: Axis
    axis2: Axis
    axis3: Axis
    axis4: Axis

    buttonA: Button
    buttonB: Button
    buttonX: Button
    buttonY: Button
    buttonL1: Button
    buttonL2: Button
    buttonR1: Button
    buttonR2: Button
    buttonUp: Button
    buttonDown: Button
    buttonLeft: Button
    buttonRight: Button


# ---------------- Motors ----------------

class Motor:
    def __init__(self, port: int, gear_ratio: int = ..., reversed: bool = False): ...

    def spin(self, direction: int, velocity: float = 0, units: int = PERCENT): ...
    def spin_for(
        self,
        direction: int,
        amount: float,
        units: int,
        wait: bool = True
    ): ...
    def stop(self): ...


class MotorGroup:
    def __init__(self, *motors: Motor): ...

    def spin(self, direction: int, velocity: float = 0, units: int = PERCENT): ...
    def spin_for(
        self,
        direction: int,
        amount: float,
        units: int,
        wait: bool = True
    ): ...
    def set_velocity(self, velocity: float, units: int = PERCENT): ...
    def set_stopping(self, mode: int): ...
    def stop(self): ...


# ---------------- 3-Wire / Triport ----------------

class Triport:
    def __init__(self, port: int): ...
    a: int
    b: int
    c: int
    d: int
    e: int
    f: int
    g: int
    h: int


class Limit:
    def __init__(self, port: int): ...
    def pressing(self) -> bool: ...


class Pneumatics:
    def __init__(self, port: int): ...
    def open(self): ...
    def close(self): ...
    def value(self) -> int: ...


# ---------------- Competition ----------------

class Competition:
    def __init__(self, driver, autonomous): ...


# ---------------- Timing ----------------

def wait(time: float, units: int = SECONDS): ...
