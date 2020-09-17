import mido
import sys
import time

class controller:

    def __init__(self):
        self.old_note = 0
        self.port = mido.open_output('iRig MIDI 2 MIDI 1')

    def __del__(self):
        self.port.close()

    def send_note(self, note):
        global old_note

        try:
            if note.note_number != self.old_note:
                msg = mido.Message('note_on', channel=4, note=note.note_number)
                msg2 = mido.Message('note_off', channel=4, note=note.note_number)
                self.port.send(msg)
                time.sleep(1)
                self.port.send(msg2)
                self.old_note = note.note_number

        except Exception as e:
            line = sys.exc_info()[-1].tb_lineno
            exc_type, exc_obj, exc_tb = sys.exc_info()
            pass

    def plot_sound(self):
        return None
