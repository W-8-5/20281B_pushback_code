import math

from vex import *


class Robot:
    def __init__(self):
        self.brain = Brain()
        self.controller = Controller()

        self._setup_drivetrain()
        self._setup_auton_selector()
        self._setup_pneumatics()
        self._setup_scoring()

        self.auton = self.auton_blank
        self.team_color = "red"

    # ---------------- SETUP ---------------- #

    def _setup_drivetrain(self):
        self.gear_ratio = (48, 60)
        self.wheel_dia = 3.5
        self.dt_width = 12.5

        self.left_drive = MotorGroup(
            Motor(Ports.PORT11, GearSetting.RATIO_36_1),
            Motor(Ports.PORT12, GearSetting.RATIO_36_1),
            Motor(Ports.PORT13, GearSetting.RATIO_36_1)
        )

        self.right_drive = MotorGroup(
            Motor(Ports.PORT14, GearSetting.RATIO_36_1, True),
            Motor(Ports.PORT15, GearSetting.RATIO_36_1, True),
            Motor(Ports.PORT16, GearSetting.RATIO_36_1, True)
        )

        self.left_drive.set_stopping(BRAKE)
        self.right_drive.set_stopping(BRAKE)

    def _setup_auton_selector(self):
        self.auton_module = Triport(Ports.PORT20)

        self.mode_switch = Limit(self.auton_module.a)
        self.color_switch = Limit(self.auton_module.b)
        self.side_switch = Limit(self.auton_module.c)
        self.type_switch = Limit(self.auton_module.d)
        self.confirm = Limit(self.auton_module.e)

        self.auton_dict = {
            "mode": ["match", "skills"],
            "team_color": ["red", "blue"],
            "setup_side": ["left", "right"],
            "auton_type": ["both", "long", "middle"]
        }

    def _setup_scoring(self):
        self.intake_motor = Motor(Ports.PORT7)
        self.intake_motors = MotorGroup(self.intake_motor)

        self.outtake_motor = Motor(Ports.PORT8)
        self.outtake_motors = MotorGroup(self.outtake_motor)

    def _setup_pneumatics(self):
        self.lift = Pneumatics(self.brain.three_wire_port.g)
        self.lift.close()
        self.hopper = Pneumatics(self.brain.three_wire_port.f)
        self.hopper.close()
        self.cannon = Pneumatics(self.brain.three_wire_port.e)
        self.cannon.close()

    # --------------- AUTON ROUTINES --------------- #

    def drive_correction(self, distance, speed):
        corrections = {
            100: (1, 0),
            75: (1, 0),
            50: (1, 0),
            25: (1, 0)
        }
        m, b = corrections[speed]
        return (distance - b) / m

    def drive(self, inches, speed):
        self.left_drive.set_velocity(speed, PERCENT)
        self.right_drive.set_velocity(speed, PERCENT)

        distance = self.drive_correction(inches, speed)

        wheel_turns = distance / (self.wheel_dia * math.pi)
        motor_turns = wheel_turns * self.gear_ratio[0] / self.gear_ratio[1]

        self.left_drive.spin_for(FORWARD, motor_turns, TURNS, wait=False)
        self.right_drive.spin_for(FORWARD, motor_turns, TURNS)

    def turn_about(self, angle, speed, offset=0):
        self.left_drive.set_velocity(speed, PERCENT)
        self.right_drive.set_velocity(speed, PERCENT)

        rads = math.radians(angle)

        # distances each side travels
        left_dist = (offset + self.dt_width / 2) * rads
        right_dist = (offset - self.dt_width / 2) * rads

        # convert to wheel turns
        left_wheel_turns = left_dist / (3.5 * math.pi)
        right_wheel_turns = right_dist / (3.5 * math.pi)

        # convert to motor turns
        left_motor_turns = left_wheel_turns * self.gear_ratio[0] / self.gear_ratio[1]
        right_motor_turns = right_wheel_turns * self.gear_ratio[0] / self.gear_ratio[1]

        self.left_drive.spin_for(FORWARD, left_motor_turns, TURNS, wait=False)
        self.right_drive.spin_for(FORWARD, right_motor_turns, TURNS)

    def auton_blank(self):
        pass

    def auton_m_l_b(self):
        # DRIVE FORWARD
        self.drive(32, 100)
        # ARC TOWARDS HOPPER
        self.turn_about(-90, 100, -12)
        # HOPPER LOAD
        self.drive(12, 100)
        self.drive(-12, 100)
        # ARC BACKWARDS
        self.turn_about(-90, 100, 12)
        # ARC TOWARDS LONG GOAL
        self.turn_about(-90, 100, -12)
        self.drive(6, 75)
        # REVERSE 24 INCHES
        self.drive(-24, 100)
        # TURN TOWARDS MIDDLE GOAL
        self.turn_about(45, 100)
        # DRIVE TOWARDS MIDDLE
        self.drive(36 * math.sqrt(2), 100)
        # SCORE ON MIDDLE

    def auton_m_l_l(self):
        pass

    def auton_m_l_m(self):
        pass

    def auton_m_r_b(self):
        pass

    def auton_m_r_l(self):
        # DRIVE STRAIGHT
        self.intake_motors.spin(FORWARD, 100, PERCENT)
        self.outtake_motors.spin(FORWARD, 100, PERCENT)
        self.drive(12, 100)
        # ARC TO COLLECT BLOCKS
        self.turn_about(126.87, 50, 12)
        self.intake_motors.stop()
        self.outtake_motors.stop()
        self.hopper.open()
        # ARC TO HOPPER LOADER
        self.turn_about(53.13, 50, 51)
        self.intake_motors.spin(FORWARD, 100, PERCENT)
        self.outtake_motors.spin(FORWARD, 100, PERCENT)
        self.left_drive.set_stopping(COAST)
        self.right_drive.set_stopping(COAST)
        self.drive(2, 100)
        # REVERSE
        self.left_drive.set_stopping(BRAKE)
        self.right_drive.set_stopping(BRAKE)
        self.intake_motors.stop()
        self.outtake_motors.stop()
        self.drive(-12, 100)
        self.hopper.close()
        # ONE POINT TURN
        self.turn_about(90, 100, -12)
        self.turn_about(90, 100, 12)
        # DRIVE FORWARD AND SCORE
        self.lift.open()
        self.drive(6, 100)
        self.intake_motors.spin(FORWARD, 100, PERCENT)
        self.outtake_motors.spin(FORWARD, 100, PERCENT)
        wait(1, SECONDS)
        # KNOCK THE BALLS INTO THE CONTROL ZONE WITH SHOCK CANNON
        self.drive(-6, 50)
        self.lift.close()
        self.drive(6, 100)
        self.cannon.open()

    def auton_m_r_m(self):
        pass

    def skills_auton(self):
        pass

    # ------------- AUTON SELECTION ------------- #

    def print_auton(self, code):
        # Auton MODE
        self.brain.screen.clear_screen()
        self.brain.screen.set_font(FontType.MONO20)
        self.brain.screen.print("AUTON MODE: ", self.auton_dict["mode"][code[0]].capitalize())

        # Team COLOR
        self.brain.screen.next_row()
        self.brain.screen.set_font(FontType.MONO15)
        self.brain.screen.print("TEAM COLOR: ", self.auton_dict["team_color"][code[1]].capitalize())

        # Setup SIDE
        self.brain.screen.next_row()
        self.brain.screen.print("AUTON SIDE: ", self.auton_dict["setup_side"][code[2]].capitalize())

        # Auton TYPE
        self.brain.screen.next_row()
        self.brain.screen.print("AUTON TYPE: ", self.auton_dict["auton_type"][code[3]].capitalize())

    def select_auton(self):
        code = [0, 0, 0, 0]
        last_code = None
        while not self.confirm.pressing():

            if self.mode_switch.pressing():
                code[0] = (code[0] + 1) % len(self.auton_dict["mode"])
                self._wait_release(self.mode_switch)

            elif self.color_switch.pressing():
                code[1] = (code[1] + 1) % len(self.auton_dict["team_color"])
                self._wait_release(self.color_switch)

            elif self.side_switch.pressing():
                code[2] = (code[2] + 1) % len(self.auton_dict["setup_side"])
                self._wait_release(self.side_switch)

            elif self.type_switch.pressing():
                code[3] = (code[3] + 1) % len(self.auton_dict["auton_type"])
                self._wait_release(self.type_switch)

            if code != last_code:
                self.print_auton(code)
                last_code = code.copy()

            wait(20, MSEC)

        self.brain.screen.clear_screen()
        self.brain.screen.set_font(FontType.MONO30)
        self.brain.screen.print(f"{self.auton_dict['mode'][code[0]].capitalize()} | "
                                f"{self.auton_dict['setup_side'][code[2]].capitalize()} | "
                                f"{self.auton_dict['auton_type'][code[3]].capitalize()}")
        self.brain.screen.print("AUTON LOCKED")

        self.team_color = self.auton_dict["team_color"][code[1]]

        if code[0] == 1:
            self.auton = self.skills_auton
        elif code[2:] == [0, 0]:
            self.auton = self.auton_m_l_b
        elif code[2:] == [0, 1]:
            self.auton = self.auton_m_l_l
        elif code[2:] == [0, 2]:
            self.auton = self.auton_m_l_m
        elif code[2:] == [1, 0]:
            self.auton = self.auton_m_r_b
        elif code[2:] == [1, 1]:
            self.auton = self.auton_m_r_l
        elif code[2:] == [1, 2]:
            self.auton = self.auton_m_r_m

    # ------------- DRIVER CONTROL FUNCTIONS ------------- #
    def _drive(self):
        self.right_drive.spin(FORWARD, (self.controller.axis3.position() - self.controller.axis1.position()) / 8.3,
                              VOLT)
        self.left_drive.spin(FORWARD, (self.controller.axis3.position() + self.controller.axis1.position()) / 8.3, VOLT)

    def _intake(self):
        if self.controller.buttonL1.pressing():
            self.intake_motors.spin(FORWARD, 80, PERCENT)
        elif self.controller.buttonL2.pressing():
            self.intake_motors.spin(REVERSE, 50, PERCENT)
        else:
            self.intake_motors.stop()

    def _outtake(self):
        if self.controller.buttonR1.pressing():
            self.outtake_motors.spin(FORWARD, 100, PERCENT)
        elif self.controller.buttonR2.pressing():
            self.outtake_motors.spin(REVERSE, 100, PERCENT)
        else:
            self.outtake_motors.stop()

    def _lift(self):
        if self.lift.value() == 0:
            self.lift.open()
        else:
            self.lift.close()

    def _hopper(self):
        if self.hopper.value() == 0:
            self.hopper.open()
        else:
            self.hopper.close()

    def _cannon(self):
        if self.cannon.value() == 0:
            self.cannon.open()
        else:
            self.cannon.close()

    # ------------- COMPETITION FUNCTIONS ------------- #

    def autonomous(self):
        self.auton()

    def driver_control(self):
        self.controller.buttonB.pressed(self._lift)
        self.controller.buttonA.pressed(self._hopper)
        self.controller.buttonDown.pressed(self._cannon)
        while True:
            self._drive()
            self._intake()
            self._outtake()
            wait(20, MSEC)

    # ------------- HELPERS ------------- #

    @staticmethod
    def _wait_release(switch):
        while switch.pressing():
            wait(10, MSEC)


# Script Code
breakthrough = Robot()
breakthrough.select_auton()

competition = Competition(breakthrough.driver_control, breakthrough.autonomous)
