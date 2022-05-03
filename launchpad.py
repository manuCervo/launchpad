from pygame import midi
import time
from threading import Thread
from enum import Enum


class Launchpad:
    """main class for managing launchpad input/output."""

    def __init__(self, inputID=None, outputID=None):
        """
            inputID: the midi input id of your launchpad
            outputID: the midi output id of your launchpad

            you can find out the input and output id with the get_device_info() method from pygame.midi, check out the pygame documentation for more info: https://www.pygame.org/docs/ref/midi.html
        """
        midi.init()
        if inputID is not None:
            self.midiInput = midi.Input(inputID)

        if outputID is not None:
            self.midiOutput = midi.Output(outputID)

    def inputRecived(self, button):
        """this method is meant to be  overridden from outside the class to handle the button events.

        button: LaunchpadButton, contains all the info about the event(its position, and wether it is a press or a release event)
        """
        pass

    def listen(self, refreshTime):
        while True:
            if self.midiInput.poll():
                midi = self.midiInput.read(1)
                self.inputRecived(LaunchpadButton(midi))
            time.sleep(refreshTime)

    def startListening(self, refreshTime=0.1):
        """starts listening for button events, calling the inputRecived method everytime an event occurs

        refreshTime: how many seconds the listener should wait before trying to read the next event
        """
        Thread(target=self.listen, args=(refreshTime,)).start()

    def setButtonLight(self, row, column, state):
        """sets the state of a button light

            row: int, the row of the button
            column: int, the column of the button
            state: could be either a boolean or a Color, in the first case, the light will be turned yellow if the state is true, or it will be turned off. otherwise, the light will be turned in the specified Color
        """
        if isinstance(state, bool):
            if state:
                state = 127
            else:
                state = 0
        else:
            state = state.value
        if row == 0:
            position = column + 104
            data1 = 176
        else:
            position = (row - 1) * 16 + column
            data1 = 144
        self.midiOutput.write_short(data1, position, state)

    def resetLights(self):
        """turns off all the lights"""
        for i in range(0, 9):
            for j in range(0, 10):
                self.setButtonLight(i, j, False)

    def testLights(self):
        """just for testing, turns on and off all the lights,one by one."""
        for i in range(0, 9):
            for j in range(0, 10):
                self.setButtonLight(i, j, True)

        time.sleep(1)

        for i in range(0, 9):
            for j in range(0, 10):
                self.setButtonLight(i, j, False)


class LaunchpadButton:

    """describes a button event

        row: int, the row of the button, going from 0(first on the top) to 8
        column: int, the column of the button, going from 0(first on the left) to 8
        pressed: wether it is a press or a release event
    """

    def __init__(self, midi):
        # midi: [[[144 or 176(top row),position,pressed,0],timestamp]] pressed : 127, not pressed: 0
        position = midi[0][0][1]
        pressed = midi[0][0][2] == 127
        topRow = midi[0][0][0] == 176
        if topRow:
            row = 0
            column = position - 104
        else:
            row = position // 16 + 1
            column = position % 16

        self.row = row
        self.column = column
        self.pressed = pressed


class Color(Enum):

    """
        class containing all the colors that can be used in the setButtonLight method. 
    """
    GRAY = 0
    # GRAY means turning off the light

    RED1 = 1
    RED2 = 2
    RED3 = 3

    GREEN1 = 16
    GREEN2 = 32
    GREEN3 = 48

    YELLOW1 = 17
    YELLOW2 = 33
    YELLOW3 = 50
    YELLOWGREEN = 49

    ORANGE1 = 18
    ORANGE2 = 19
    ORANGE3 = 34
    ORANGE4 = 35
    ORANGE5 = 51