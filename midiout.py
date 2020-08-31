import mido
import sys
import time

old_note = 0

def send_note(note, font, panel, aircraft):
    global old_note
    msg = mido.Message('note_on', channel=4, note=note.note_number)
    msg2 = mido.Message('note_off',channel=4, note=note.note_number)

    try:
        if note.note_number != old_note:
            port = mido.open_output('iRig MIDI 2 MIDI 1')
            port.send(msg)
            time.sleep(1)
            port.send(msg2)
            old_note = note.note_number
    except Exception as e:
        line = sys.exc_info()[-1].tb_lineno
        exc_type, exc_obj, exc_tb = sys.exc_info()
        pass

def plot_sound():
    return None
