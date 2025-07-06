# micropython script for esp32
# tone generation with buzzer using pwm

import machine
import time
import sys

BUZZER_PIN = 16
BUTTON_PIN = 0

# Tone frequencies
# Common musical notes
C4 = 262
D4 = 294
E4 = 330
F4 = 349
G4 = 392
A4 = 440
B4 = 494
C5 = 523
SILENCE = 1 # buzzer off

NOTES = [C4, D4, E4, F4, G4, A4, B4, C5, SILENCE]
current_note_index = 0

# Duty cycle is usually 50% for symmetric square wave sound
BUZZER_DUTY = 512 # Approximately 50% of 1023

# Button debounce variables
last_button_state = 1
last_button_press_time = 0
DEBOUNCE_TIME = 50

buzzer = machine.PWM(machine.Pin(BUZZER_PIN), freq=SILENCE, duty=BUZZER_DUTY)
button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

def play_notes(freq):
    if freq == SILENCE:
        buzzer.duty(0)
        print("Playing Silence")
    else:
        buzzer.freq(freq)
        buzzer.duty(BUZZER_DUTY)
        print(f"Playing: {freq} Hz")
    time.sleep_ms(100)
    
play_notes(SILENCE)

try:
    while True:
        # detect button press and play notes
        current_time = time.ticks_ms()
        current_button_state = button.value()
        if current_button_state == 0 and last_button_state == 1:
            if time.ticks_diff(current_time, last_button_press_time) > DEBOUNCE_TIME:
                print("Button pressed")
                current_note_index = (current_note_index + 1) % len(NOTES)
                new_freq = NOTES[current_note_index]
                play_notes(new_freq)
                last_button_press_time = current_time
        last_button_state = current_button_state
        time.sleep_ms(10)
except KeyboardInterrupt:
    print("Script terminated")
    sys.exit()
    

