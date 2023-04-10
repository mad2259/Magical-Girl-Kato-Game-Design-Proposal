# The Dating Sim Engine was written by PyTom, 
# with updates added by Andrea Landaker (qirien),
# and contributions by Edmund Wilfong (Pneumonica)
#
# For support, see the Lemma Soft forums thread:
# http://lemmasoft.renai.us/forums/viewtopic.php?f=51&t=31571
#
# It is released under the MIT License - see DSE-LICENSE.txt
#
#
# This is the main part of the program, where you setup your schedule and
# the options for the user. You can change the stats, periods, and choices
# here; just make sure they match up with the events setup in
# dse-events.rpy.  You can even have different time periods (months, instead
# of times of day, for example).

# Set up a default schedule.
init python:
    register_stat("Strength", "strength", hidden=True)
    register_stat("Intelligence", "intelligence", hidden=True)
    register_stat("Friendship with Shreya", "friendship with Shreya", 10, 100)
    register_stat("Friendship wiht Christine", "friendship with Christine", 10, 100)
    register_stat("Relaxation", "relaxation", hidden=True)

    dp_period("Morning", "morning_act")
    dp_choice("Attend Class", "class")
    dp_choice("Cut Class", "cut")
    
    # This is an example of an event that should only show up under special circumstances
    dp_choice("Fly to the Moon", "fly", show="strength >= 100 and intelligence >= 100")

    dp_period("Afternoon", "afternoon_act")
    dp_choice("study", "study")
    dp_choice("Hang Out", "hang")

    dp_period("Evening", "evening_act")
    dp_choice("Exercise", "exercise")
    dp_choice("Play Games", "play")

    
# This is the entry point into the game.
label start:

    # Initialize the default values of some of the variables used in
    # the game.
    $ day = 0

    # Declare the characters
    define k = Character(_('Kato'), color="#a6f5a6")
    define M = Character(_('Mom'), color="#f5a6f1")
    define D = Character(_('Dad'), color="#a6cbf5")

    # Show a default background.
    scene bg backseat of car
    with dissolve
    
    #start the background music playing
    play music "car-music.mp3"
    play sound "driving-ambience.mp3"

    # The script here is run before any event.

    k "Ugh I can't believe we're still 2 HOURS AWAY!"

    k "we've been driving FOOORRRREEEVVVEEERRRR."

    M "I thought you brought that Nintendo of yours, why aren't you playing that?"

    D "If they play any more of that thing, their brain will rot right out of their ear."

    k "Hey! I heard that!"

    D "*chuckles* I'm just playing with ya, kid. I know you gotta get as much screen time in before the school year starts."

    M "Speaking of the school year..."

    k "Don't you da-"

    M "Have you thought about what Dr. Collard said? About making friends?"

    menu:

        "What should I do?"

        "Play your games and ignore Mom":

            jump ignore

        "try and appeal to Mom's protective instincts": 

            jump protective

        "beg and barter":
            jump beg

label ignore: 

    k "... *begins playing on their Nintendo, ignoring their mom*" 

    M "Don't ignore me!! This is really important!"
    
    M "Will you use any of your therapists advice? You know, he specializes in this sort of thing."

    k "*groans* His ideas are stupid"

    k "and it's not that easy."

    k "Besides, no one will like me there anyway."

    k "No one ever does."

    M "Oh honey... I know things were hard at your old school."

    M "But this is a fresh start! Things will be different for you this year. I just know it."

    D "And hey think of this-- remember that episode of Sailor Moonpie when--"

    k "THEIR HIGH SCHOOL GOT TRANSFER RIN!!!"

    k "He was a transfer student who was the SON OF SATAN"

    k "DOES THIS MEAN I'M THE SON OF SATAN!?"

    D "Uh, well-"

    k "that's"

    k "so"

    k "COOL!"

    k "MWAHAHAHAHA!!!!"

    k "YES!!!!"

    k "My peers will fear my satanic powers!!"

    k "They shall bow before me!!!"

    M "honey that's no-"

    k "I, Kato WILL BE"

    k "CONQUERING MIDDLE SCHOOL!!!"

    show bg gcs full campus transformed redo

    # We jump to day to start the first day.
    jump day

label protective:

    show bg gcs full campus transformed redo

    # We jump to day to start the first day.
    jump day

label beg:

    show bg gcs full campus transformed redo

    # We jump to day to start the first day.
    jump day


# This is the label that is jumped to at the start of a day.
label day:

    # Increment the day it is.
    $ day += 1

    # We may also want to compute the name for the day here, but
    # right now we don't bother.

    "It's day %(day)d."

    # Here, we want to set up some of the default values for the
    # day planner. In a more complicated game, we would probably
    # want to add and remove choices from the dp_ variables
    # (especially dp_period_acts) to reflect the choices the
    # user has available.

    $ morning_act = None
    $ afternoon_act = None
    $ evening_act = None
    $ narrator("What should I do today?", interact=False)
    window show
    

    # Now, we call the day planner, which may set the act variables
    # to new values. We call it with a list of periods that we want
    # to compute the values for.
    call screen day_planner(["Morning", "Afternoon", "Evening"])
    window auto
    
    # We process each of the three periods of the day, in turn.
label morning:

    # Tell the user what period it is.
    centered "Morning"

    # Set these variables to appropriate values, so they can be
    # picked up by the expression in the various events defined below. 
    $ period = "morning"
    $ act = morning_act
    
    # Execute the events for the morning.
    call events_run_period

    # That's it for the morning, so we fall through to the
    # afternoon.

label afternoon:

    # It's possible that we will be skipping the afternoon, if one
    # of the events in the morning jumped to skip_next_period. If
    # so, we should skip the afternoon.
    if check_skip_period():
        jump evening

    # The rest of this is the same as for the morning.

    centered "Afternoon"

    $ period = "afternoon"
    $ act = afternoon_act

    call events_run_period


label evening:
    
    # The evening is the same as the afternoon.
    if check_skip_period():
        jump night

    centered "Evening"

    $ period = "evening"
    $ act = evening_act
    
    call events_run_period


label night:

    # This is now the end of the day, and not a period in which
    # events can be run. We put some boilerplate end-of-day text
    # in here.

    centered "Night"

    "It's getting late, so I decide to go to sleep."

    # We call events_end_day to let it know that the day is done.
    call events_end_day

    # And we jump back to day to start the next day. This goes
    # on forever, until an event ends the game.
    jump conclusion

label conclusion: 

    "Thank you for playing the demo of Magical Girl Kato presents: Conquering Middle School!"
         

