# Write your code here :-)
from adafruit_circuitplayground import cp

import time

# DEAD_TIME is estimated based on trail and error to make songs sound better
# There is probably a better way to manipulate the speaker turning on/off more controlably
DEAD_TIME = 0.1 #fixed time between speaker turning off and turning back on again even when no pause is commanded

# used to encode songs
note_frequencies = {
    #real frequencies are 1/100 of values here

    'A2': 11000, 'A#/Bb2': 11654, 'B2': 12347, 'C3': 13081, 'C#/Db3': 13859, 'D3': 14683,
    'D#/Eb3': 15556, 'E3': 16481, 'F3': 17461, 'F#/Gb3': 18500, 'G3': 19600, 'G#/Ab3': 20765,

    'A3': 22000, 'A#/Bb3': 23308, 'B3': 24694, 'C4': 26163, 'C#/Db4': 27718, 'D4': 29366,
    'D#/Eb4': 31113, 'E4': 32963, 'F4': 34923, 'F#/Gb4': 36999, 'G4': 39200, 'G#/Ab4': 41530,

    'A4': 44000, 'A#/Bb4': 46616, 'B4': 49388, 'C5': 52325, 'C#/Db5': 55437, 'D5': 58733,
    'D#/Eb5': 62225, 'E5': 65925, 'F5': 69846, 'F#/Gb5': 73999, 'G5': 78399, 'G#/Ab5': 83061,

    'A5': 88000, 'A#/Bb5': 93233, 'B5': 98777, 'C6': 104650, 'C#/Db6': 110873, 'D6': 117466,
    'D#/Eb6': 124451, 'E6': 131851, 'F6': 139691, 'F#/Gb6': 147998, 'G6': 156798, 'G#/Ab6': 166122,

    'A6': 176000, 'A#/Bb6': 186466
    }

# also used to encode songs
note_durations = {
    's': 0.0625, #sixteenth note - avoid using
    'e': 0.125, #eight note
    'es': 0.1875, #dotted eigth note
    'q': 0.25, #quarter note
    'qe': 0.375, #dotted quarter note
    'h': 0.50, #half note
    'he': 0.625,
    'hq': 0.75, #dotted half note
    'w': 1.00, #whole note
    'wq': 1.25,
    'wh': 1.50, #dotter whole note
    'dw': 2.00 #double whole note
    }

# songs encoded using note_frequencies and note_durations, which get called by play_song()
jingle_bells = [200, #bpm
                'D4-q', 'B4-q', 'A4-q', 'G4-q', 'D4-hq', #Dashing through the snow
                'D4-e', 'D4-e', 'D4-q', 'B4-q', 'A4-q', 'G4-q', 'E4-w', #on a one horse open sleigh
                'E4-q', 'C5-q', 'B4-q', 'A4-q', 'F#/Gb4-hq', 'rest-e', 'F#/Gb4-e', #o'er the fields we go
                'D5-q', 'D5-q', 'C5-q', 'A4-q', 'B4-hq', 'rest-e', 'D4-q', #Laughting all the way

                'D4-q', 'B4-q', 'A4-q', 'G4-q', 'D4-hq', 'rest-e', 'D4-e', #bells on bob-tail ring
                'D4-q', 'B4-q', 'A4-q', 'G4-q', 'E4-hq', 'rest-e', #making spirits bright
                'E4-q', 'C5-q', 'B4-q', 'A4-q', 'D5-q', 'D5-q', 'D5-q', 'D5-q', #What fun it is to right and sing a
                'E5-q', 'D5-q', 'C5-q', 'A4-q', 'G4-h' #sleighting song tonight
                ]

rudolph = [150, #bpm
           'G4-q', 'A4-e', 'G4-e', 'E4-q', 'C5-q', 'A4-q', 'G4-hq', #rudolph the red-nosed reindeer
           'G4-e', 'A4-e', 'G4-e', 'A4-e', 'G4-q', 'C5-q', 'B4-w', #had a very shiny nose
           'F4-q', 'G4-e', 'F4-e', 'D4-q', 'B4-q', 'A4-q', 'G4-hq', #and if you ever saw it
           'G4-e', 'A4-e', 'G4-e', 'A4-e', 'G4-q', 'A4-q', 'E4-w' #you would even say it glows
           ]

wonderful_time = [100, #bpm
                  'E4-e', 'F4-e', 'G4-qe', 'G4-e', 'C5-e', 'A4-e', 'G4-qe', 'rest-e', #its the most wonderful time
                  'F4-e', 'D4-e', 'C4-hq', #of the year
                  'E4-q', 'F4-e', 'G4-e', 'D4-e', 'E4-e', 'F4-e', 'D4-e', 'D4-e', 'D4-e',
                  'E4-e', 'F4-e', 'G4-e', 'E4-e', 'E4-e', 'E4-e', 'F4-e', 'G4-e', 'A4-e', 'F4-e', 'A4-e', 'C5-hq',
                  'A4-e', 'B4-e', 'A4-e', 'G4-qe', 'G4-e', 'C5-e', 'A4-e', 'G4-h', 'F4-e', 'D4-e', 'C4-e',
                  'E4-e', 'F4-e', 'G4-e', 'C4-e', 'A4-e', 'G4-h', 'E4-e', 'F4-e', 'G4-qe', 'G4-e', 'C5-e',
                  'A4-e', 'G4-qe', 'rest-e', 'F4-e', 'D4-e', 'C4-hq'
                  ]

twelve_days = [120, #bpm
               'C4-e', 'C4-e', 'C4-q', 'F4-e', 'F4-e', 'F4-q', 'E4-e', #on the first day of xmas
               'F4-e', 'G4-e', 'A4-e', 'A#/Bb4-e', 'G4-e', 'A4-h', #my true love gave to me
               'C5-h', 'D5-q', 'B4-q', 'C5-w', #five golden rings
               'C5-e', 'C4-e', 'G4-e', 'A4-e', 'A#/Bb4-q', #four calling birds
               'C5-q', 'G4-e', 'A4-e', 'A#/Bb4-q', #three Fench hens
               'C5-q', 'G4-e', 'A4-e', 'A#/Bb4-q', #two turtle doves
               'A4-e', 'A#/Bb4-e', 'C5-q', 'D5-e', 'A#/Bb4-e', 'A4-e', 'F4-e', 'G4-q', 'F4-hq' #and a partridge and a pear tree
               ]

holly_jolly = [140, #bpm
               'E4-e', 'G4-e', 'C5-q', 'C5-q', 'B4-q', 'B4-q', 'A4-q', 'E4-q', 'rest-q',
               'E4-e', 'G4-e', 'A4-q', 'A4-q', 'G4-q', 'G4-q', 'B3-h', 'rest-h',
               'B4-q', 'B4-q', 'B4-qe', 'A4-e', 'G4-q', 'G4-q', 'G4-qe', 'E4-e',
               'G4-q', 'G4-q', 'F4-q', 'G4-q', 'E4-h', 'rest-q',
               'E4-e', 'G4-e', 'C5-q', 'C5-q', 'B4-q', 'B4-q', 'A4-q', 'E4-q', 'rest-q',
               'E4-e', 'G4-e', 'A4-q', 'A4-q', 'G4-q', 'G4-q', 'B3-h', 'rest-h',
               'B4-q', 'B4-q', 'B4-qe', 'A4-e', 'G4-q', 'G4-q', 'G4-qe', 'E4-e',
               'G4-q', 'G4-q', 'F4-q', 'D4-q', 'C4-h', 'rest-h'
               ]

last_christmas = [120, #bpm
                  'C#/Db4-qe', 'D#/Eb4-qe', 'G#/Ab3-q', 'D#/Eb4-qe', 'F4-qe',
                  'G#/Ab4-e', 'F4-e', 'C#/Db4-qe', 'D#/Eb4-qe', 'G#/Ab3-wq',
                  'C#/Db4-qe', 'D#/Eb4-qe', 'G#/Ab3-q', 'D#/Eb4-qe', 'F4-qe',
                  'G#/Ab4-e', 'F4-e', 'C#/Db4-qe', 'D#/Eb4-qe', 'G#/Ab3-wq',
                  #'C#/Db4-e', 'rest-e','C#/Db4-e', 'rest-e',
                  'A#/Bb3-e', 'C4-e', 'C#/Db4-e', 'C#/Db4-e', 'D#/Eb4-e', 'C4-q', 'G#/Ab3-w', #we're no strangers to love
                  'A#/Bb3-e', 'A#/Bb3-e', 'C4-e', 'C#/Db4-e', 'A#/Bb3-e', 'rest-e', #you know the rules
                  'G#/Ab3-e', 'G#/Ab4-q', 'G#/Ab4-e', 'D#/Eb4-qe' #and so do I
                  ]

silent_night = [80, #bpm

              'F4-qe', 'G4-e', 'F4-q', 'D4-hq', #silent night
              'F4-qe', 'G4-e', 'F4-q', 'D4-hq', #holy night
              'C5-h', 'C5-q', 'A4-hq', #all is calm
              'A#/Bb4-h', 'A#/Bb4-q', 'F4-h', 'rest-q', #all is bright
              'G4-h', 'G4-q', 'A#/Bb4-qe', 'A4-e', 'G4-q', #'round you Virgin
              'F4-qe', 'G4-e', 'F4-q', 'D4-h', 'rest-q', #Mother and Child
              'G4-h', 'G4-q', 'A#/Bb4-qe', 'A4-e', 'G4-q', #Holy infant so
              'F4-qe', 'G4-e', 'F4-q', 'D4-qe', #tender and mild
              'D4-e', 'F4-e', 'A#/Bb4-e',
              'C5-h', 'C5-q', 'D#/Eb5-qe', 'C5-e', 'A4-q', 'A#/Bb4-hq', 'D5-hq', #sleep in heavenly peace
              'A#/Bb4-q', 'F4-q', 'D4-q', 'F4-qe', 'D#/Eb4-e', 'C4-q', 'A#/Bb3-hq']

white_christmas = [100, #bpm

                'E4-w',                             #I'm
                'F4-q', 'E4-q', 'D#/Eb4-q', 'E4-q', #drea-ming of a
                'F4-w',                             #white
                'F#/Gb4-q', 'G4-h', 'rest-q',         #Christ-mas
                'A4-h', 'B4-q', 'C5-q',             #just like the
                'D5-q', 'C5-q', 'B4-q', 'A4-q',       #ones I used to
                'G4-w'                              #know

                   ]

sleigh_ride = [110, #bpm
                #'rest-h', 'rest-e',
                'A#/Bb5-e', 'A#/Bb5-e', 'A#/Bb5-e',
                'A#/Bb5-e', 'C6-e', 'A#/Bb5-s', 'G5-s',  'D#/Eb5-e',
                'F5-e', 'G5-e', 'F5-s', 'D#/Eb5-s', 'C5-e',
                'A#/Bb4-he', 'A#/Bb4-s',                         #decent
                'C5-s', 'D5-s', 'D#/Eb5-s', 'F5-s', 'G5-s',
                'A#/Bb5-e', 'C6-e', 'A#/Bb5-s', 'G5-s', 'F5-s', 'D#/Eb5-s',
                'F5-e', 'F5-s', 'G5-s', 'F5-s', 'D#/Eb5-s', 'C5-e',
                'D#/Eb5-h'
                ]

holy_night = [100, #bpm
              'E4-qe', 'E4-q', 'E4-e', 'G4-h', 'rest-e', #O Holy Night
              'G4-e', 'A4-q', 'A4-e', 'F4-q', 'A4-e', 'C5-hq', 'G4-q', #The stars are brightly shining
              'G4-e', 'E4-q', 'D4-e', 'C4-qe', 'E4-q', 'F4-q',  #it is the night of our
              'G4-qe', 'F4-q', 'D4-e', 'C4-wh', #saviour's birth
              ]

song_playlist = {
                 0: jingle_bells,
                 1: last_christmas,
                 2: rudolph,
                 3: wonderful_time,
                 4: twelve_days,
                 5: holly_jolly,
                 6: silent_night,
                 7: white_christmas,
                 8: sleigh_ride,
                 9: holy_night
                 }


def holiday_lights():
    '''
    Used to give the lights more holiday cheer.
    Needs a global called holiday_lights_seed to base alternating light pattern off of and
    also to leave it updated once the fuction is done so that each time it's called, it's a little different.
    '''
    global holiday_lights_seed

    for pixel in range(0,10): #there are 10 pixels

        if holiday_lights_seed % 3 == 0:
            holiday_lights_seed += 1 #increments ths seed so that pixels alternate colors
            cp.pixels[pixel] = 0xff1111 #red
        elif holiday_lights_seed % 3 == 1:
            holiday_lights_seed += 1 #increments ths seed so that pixels alternate colors
            cp.pixels[pixel] = 0x77ff00 #yellow
        else:
            holiday_lights_seed += 1 #increments ths seed so that pixels alternate colors
            cp.pixels[pixel] = 0x00ff11 #green
    holiday_lights_seed += 1 #increments ths seed so that pixels are different on next holiday_lights() call



def play_song(song):
    '''
    This function relies on the Global Variable, DEAD_TIME to compensate for the time it takes to
    change notes with the methods related to getting an sample to play.

    Songs are lists.
    song[0] should be the BPM of the as an int.
    each index following [0] is a string in the form of '<note_name>-<note_length_code>'.
    These strings are split on '-'.
    note_name is used to lookup the note frequency from a dict, unless it is 'rest'
    in which case it does something special for that.
    note_duration is used to lookup the base duration of the note.split
    '''
    global holiday_lights_seed
    cp.pixels.brightness = 0.1

    #beats per minute
    bpm = song[0]

    #seconds per whole note (this is used as the reference for all other note durations)
    whole_note_duration = 4 * (60 / bpm)

    #enable speaker
    cp._speaker_enable.value = True

    for note in song[1:]:

        #switches lights to red/green combinations

        #retreieves the name for the note
        note_name = note.split('-')[0]
        print('playing: '+ note)
        #if the note name exists (not a rest) make sample and play it
        if note_name in note_frequencies.keys():

            holiday_lights()

            frequency = note_frequencies[note_name]
            cp._generate_sample(100)
            cp._sine_wave_sample.sample_rate = int(frequency)
            #print("playing: " + str(cp._sine_wave_sample.sample_rate))
            cp._sample.play(cp._sine_wave_sample, loop=True)

        #retrieves the base duration for the note
        note_length_code = note.split('-')[1]
        base_duration = note_durations[note_length_code]

        #calculations how long the note should play for
        duration = (base_duration * whole_note_duration) - DEAD_TIME

        #ensures that a note can't be too short to play or have a negative duration
        if duration < 0.1:
            print('minimum duration hit!')
            duration = 0.1

        time.sleep(duration)

        #print('Stopping')
        cp._sample.stop()
    cp.pixels.brightness = 0.005

cp.pixels.brightness = 0.005
holiday_lights_seed = 1
button_down_last_loop = False
selection = 0

while True:

    if selection == 10: #if selection has incremented to 10
        selection = 0 #loop back to 0, because 9 is the max

    cp.pixels[selection] = 0x0000FF #turn on selected pixel

    for each in range(0, 10):
        if each == selection: #if each is the current selection...
            continue    #skip it
        cp.pixels[each] = 0xff0000 #turn off pixel

    # checks to see if button was just pressed this loop
    if cp.button_b and not(button_down_last_loop):
        #increments once per press
        selection += 1

    if cp.button_a:
        play_song(song_playlist[selection])

    if cp.button_b:
        button_down_last_loop = True
    else:
        button_down_last_loop = False















