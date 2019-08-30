from pygame import midi
import time
from threading import Thread
from enum import Enum


class Launchpad:

    def __init__(self, inputID, outputID):
        midi.init()
        # print(midi.get_device_info(inputID))
        self.midiInput = midi.Input(inputID)
        self.midiOutput = midi.Output(outputID)

    def inputRecived(self, button):
        pass

    def listen(self, refreshTime):
        while True:
            if self.midiInput.poll():
                midi = self.midiInput.read(1)
                self.inputRecived(LaunchpadButton(midi))
            time.sleep(refreshTime)

    def startListening(self, refreshTime=0.1):
        Thread(target=self.listen, args=(refreshTime,)).start()

    def setButtonLight(self, row, column, state):
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
        for i in range(0, 9):
            for j in range(0, 10):
                self.setButtonLight(i, j, False)

    def testLights(self):
        for i in range(0, 9):
            for j in range(0, 10):
                self.setButtonLight(i, j, True)

        time.sleep(1)

        for i in range(0, 9):
            for j in range(0, 10):
                self.setButtonLight(i, j, False)


class LaunchpadButton:

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
    GRAY = 0
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
