# py C:\Users\Owner\PythonCoding\MovementReminder\MovementReminder.py

import random, sys
from datetime import datetime
from pathlib import Path

def romajiToHiraganaSimple(roma):
    roma = roma.lower()
    # single check for special sequences
    initialCharsImmediate =         ["a",  "i",  "u",  "e",  "o", "fu", "tsu", "dzu", "q"]
    initialCharsImmediateHiragana = ["あ", "い", "う", "え", "お", "ふ", "つ",  "づ",  "っ"]
    # which consonant column are we in?
    consonantSpecial = ["sh", "ch", "j", "dj"] # must use small y-characters for any vowel other than "i" and cannot use "e"
    consonant = ["k", "s", "t", "n", "h", "m", "y", "r", "w", "g", "z", "d", "b", "p"]
    # which vowel row are we in?
    vowelSpecial = ["a", "u", "o", "i", "ya", "yu", "yo"] # index % 4 - a vs ya do the same thing for the special consonants
    vowel = ["a", "i", "u", "e", "o", "ya", "yu", "yo"]
    # basically an expanded Hiragana chart
    hiraChartSpecial = ["しゃちゃじゃぢゃ",
                        "しゅちゅじゅぢゅ",
                        "しょちょじょぢょ",
                        "しちじぢ"] # first 3 rows: index * 2 to index * 2 + 1
    hiraChart = ["かさたなはまやらわがざだばぱ",
                 "きしちにひみ　りゐぎじぢびぴ",
                 "くすつぬふむゆる　ぐずづぶぷ",
                 "けせてねへめ　れゑげぜでべぺ",
                 "こそとのほもよろをごぞどぼぽ",
                 "きゃしゃちゃにゃひゃみゃ　ゃりゃゐゃぎゃじゃぢゃびゃぴゃ",
                 "きゅしゅちゅにゅひゅみゅ　ゅりゅゐゅぎゅじゅぢゅびゅぴゅ",
                 "きょしょちょにょひょみょ　ょりょゐょぎょじょぢょびょぴょ"] # last 3 rows: index * 2 to index * 2 + 1
    result = ""

    # main loop
    while len(roma) != 0:
        skip = False
        # check for n with consonant
        if roma[0] == "n":
            if len(roma) == 1:
                result += "ん"
                break
            for c in consonant:
                if roma[1] == c:
                    skip = True
                    result += "ん"
                    roma = roma[1:]
                    break
            if not skip:
                for c in consonantSpecial:
                    if len(roma) >= len(c) + 1 and roma[1:len(c) + 1] == c:
                        result += "ん"
                        roma = roma[1:]
                        break
            else:
                skip = False
        # see if we can figure the whole Hiragana character out with just one check
        for i in range(len(initialCharsImmediate)):
            c = initialCharsImmediate[i]
            if len(roma) >= len(c) and roma[0:len(c)] == c:
                result += initialCharsImmediateHiragana[i]
                roma = roma[len(c):]
                skip = True
                break
        if skip:
            continue
        # see if we are in a special column (sh ch j dj)
        for i in range(len(consonantSpecial)):
            c = consonantSpecial[i]
            if len(roma) >= len(c) and roma[0:len(c)] == c:
                roma = roma[len(c):]
                for j in range(len(vowelSpecial)):
                    c = vowelSpecial[j]
                    if len(roma) >= len(c) and roma[0:len(c)] == c:
                        if j % 4 == 3:
                            result += hiraChartSpecial[j%4][i]
                        else:
                            result += hiraChartSpecial[j%4][i*2:i*2+2]
                        roma = roma[len(c):]
                        skip = True
                        break
            if skip:
                break
        if skip:
            continue
        # figure out which consonant column we should be in
        for i in range(len(consonant)):
            c = consonant[i] # len(c) always == 1
            if len(roma) >= 1 and roma[0] == c:
                roma = roma[1:]
                # repeated consonant == chiqchai tsu + what it would be normally (or nn + normal for n)
                if len(roma) >= len(c) and roma[0] == c:
                    roma = roma[1:]
                    if c == "n":
                        result += "ん"
                    else:
                        result += "っ"
                # get the vowel (row)
                for j in range(len(vowel)):
                    v = vowel[j]
                    if len(roma) >= len(v) and roma[0:len(v)] == v:
                        if j < 5: # aiueo
                            result += hiraChart[j][i]
                        else: # ya yu yo
                            result += hiraChart[j][i*2:i*2+2]
                        roma = roma[len(v):]
                        skip = True
                        break
                if skip:
                    break
                # single n standing in for nn
                if c == "n":
                    result += "ん"
                    skip = True
                    break
        # failsafe for unrecognized letters
        if not skip:
            roma = roma[1:]
    return result

# debug code
# while True:
#     print(romajiToHiraganaSimple(input("Type romaji\n")))

# parse arguments
disable = False
for i in range(len(sys.argv)):
    if sys.argv[i] == "--addDisable":
        disable = True
        toAdd = sys.argv[i + 1]
        if toAdd.isdigit():
            f = open(Path(__file__).with_name("DisableSchedule.txt"), "r")
            disableSchedule = f.readlines()
            f.close()
            disableSchedule[0] = f"{int(disableSchedule[0].strip()) + int(toAdd)}\n"
            f = open(Path(__file__).with_name("DisableSchedule.txt"), "w")
            f.writelines(disableSchedule)
            f.close()
            print(f"Added {toAdd} skips to the DisableSchedule, for a total of {int(disableSchedule[0].strip())}.")
        elif (toAdd[0] + toAdd[2:4] + toAdd[5:7] + toAdd[8:10] + toAdd[11:13]).isdigit():
            f = open(Path(__file__).with_name("DisableSchedule.txt"), "a")
            f.write(toAdd[0] + " " + toAdd[2:] + "\n")
            f.close()
            print(f"Appended {toAdd} to the end of the DisableSchedule.")
        else:
            print("Unrecognized format for command \'--addDisable\'.\nPlease either enter only an integer or a timeBlock like this:\n0x11:00-13:00")
            print("where the first number is the day of the week (0 -> Monday), followed by an 'x', followed by HH:MM-HH:MM indicating start and end hours and minutes.")
    elif sys.argv[i] == "--help":
        disable = True
        print("Commands:\n--help      \tPrints information on how to use the program.")
        print("--addDisable\tAdds a condition for the program to be disabled. This can be a single integer, which represents a set number of times the program will skip before running again, or a timeBlock formatted as WxHH:MM-HH:MM, where W is the weekday (0 -> Monday) and HH:MM is hours and minutes for the start and end time of the scheduled disable.")
        print("Without either of the above two commands, the main program will run. Both commands will prevent the main program from running.")


if not disable:            
    # Reads the schedule file to check if this program is not supposed to run right now.
    current = datetime.now()
    # weekday (Mon == 0), hour * 60 + minute
    current = [current.weekday(), current.hour * 60 + current.minute]
    f = open(Path(__file__).with_name("DisableSchedule.txt"), "r")
    disableSchedule = f.readlines()
    f.close()
    # remove the first line of the file, since it is just a number and not a timeBlock string
    unscheduledSkipCount = int(disableSchedule.pop(0).strip())
    # check each timeBlock string of the file
    for timeBlock in disableSchedule:
        # does the weekday match?
        if int(timeBlock[0]) != current[0]:
            continue
        # start hour * 60 + min, end hour * 60 + min
        timeBlockAsList = [int(timeBlock[2:4]) * 60 + int(timeBlock[5:7]),int(timeBlock[8:10]) * 60 + int(timeBlock[11:13])]
        if timeBlockAsList[0] <= current[1] and current[1] < timeBlockAsList[1]:
            disable = True
            break
# check the first line of the file, and disable + decrement if it is >0
if not disable and unscheduledSkipCount > 0:
    f = open(Path(__file__).with_name("DisableSchedule.txt"), "w")
    disableSchedule.insert(0, f"{unscheduledSkipCount - 1}\n")
    f.writelines(disableSchedule)
    f.close()
    disable = True

if not disable:
    # Commands the user to take a movement break.
    input("Stand up. Cross your fingers together and stretch your arms over your head. Take deep breaths and walk around a bit. Hit ENTER when done. ")
    input("Now, with feet shoulder-width apart, stretch down to your toes. Hold it, release it, repeat a few times. Hit ENTER when done. ")

    # Read the kanji-hiragana-English quiz file.
    f = open(Path(__file__).with_name("JapaneseQuiz.txt"), "r", encoding='utf-8')
    quiz = f.readlines()
    f.close()

    # shuffle quiz
    for i in range(len(quiz)):
        swapIndex = random.randint(i,len(quiz)-1)
        temp = quiz[i]
        quiz[i] = quiz[swapIndex]
        quiz[swapIndex] = temp

    # Generate quiz questions from the data in the file.
    response = ""
    counter = 0
    while response != "exit":
        # grab the next line with which to test: KANJI,HIRA,ENG or SKIP,HIRA,ENG
        counter += 1
        if counter >= len(quiz):
            counter %= len(quiz)
            for i in range(len(quiz)):
                swapIndex = random.randint(i,len(quiz)-1)
                temp = quiz[i]
                quiz[i] = quiz[swapIndex]
                quiz[swapIndex] = temp
        quizLine = quiz[counter].strip("\t\n ")
        comma2 = quizLine[quizLine.index(",")+1:].index(",") + quizLine.index(",")+1
        quizLine = [quizLine[:quizLine.index(",")], quizLine[quizLine.index(",")+1:comma2], quizLine[comma2+1:]]

        # generate questions and answers
        if quizLine[0] == "SKIP": # no kanji
            questionBank = [f"What is {quizLine[1]} in English? "]
            answerBank = [quizLine[2]]
        else:
            questionBank = [f"What is {quizLine[0]} in Hiragana or Romaji? ",f"What is {quizLine[0]} in English? "]
            answerBank = [quizLine[1],quizLine[2]]

        # ask questions
        for i in range(0,len(questionBank)):
            answer = answerBank[i].lower()
            response = input(questionBank[i]).lower()
            while response != answer and response != "override" and romajiToHiraganaSimple(response) != answer:
                response = input("Try again: ").lower()
            if response == "override":
                print(f"Correct answer is {answer}")

        # go again?
        response = input("Great job! Type EXIT to close the program, or anything else to continue. ").lower()