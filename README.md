# MovementReminder
A simple program I wrote for myself that reminds me to get up and move around a little bit, then quizzes me on Japanese words that I should know. I set up a Task Scheduler task to run this every 30 minutes.

## Features
- Console-based prompts for movement, such as "Stand up. Cross your fingers together and stretch your arms over your head. Take deep breaths and walk around a bit." and "[w]ith feet shoulder-width apart, stretch down to your toes. Hold it, release it, repeat a few times."
- Gentle encouragement of learning
- Customizable "JapaneseQuiz.txt"
- DisableSchedule (sample included) to stop the program from running at inconvenient times (perhaps during scheduled work/class/etc hours)
- Custom flags for altering DisableSchedule
- Custom-made Romaji to Hiragana converter for my quizzes
- "override" when you don't know an answer
- **WARNING** You will need a file called "JapaneseQuiz.txt" and one called "DisableSchedule.txt" next to (in the same folder as) MovementReminder.py, even if you don't plan on learning Japanese or disabling the program. If you want to use the program differently, edit the code yourself ;)

## Use
In general, MovementReminder.py should be ran alone, with the command `py <filepath>` where `filepath` is the path to where MovementReminder.py is located on the computer (for example, "C:\Users\Owner\Downloads\MovementReminder.py"). For other purposes, flags can be appended to the end of this command. See the next section for more information.
You may also want to set up a schedule for the program to execute. On my Windows machine, I used the Task Scheduler to run the program every 30 minutes. [Here](https://www.youtube.com/watch?v=HAOP0HZeDJg) is a video that might help with that. If you are not on Windows, I cannot help.
The Romaji to Hiragana converter is fairly robust, but might not accept every style of writing Romaji. Using Hiragana, if possible, is best. If you must use Romaji, review the code I wrote in the function "romajiToHiraganaSimple()". Do not use characters with diacritics; write "ou" or "aa" instead of "о̄" or "ā". Note that, in order to make "っし" or "っち", you will have to write "ssi" or "tti"; "sshi", "cchi", and "tchi" do not work. For "っしゃ" or similar, use "ssya". Alternatively, "q" will always be substituted for "っ", so "qsha" would give "っしゃ". 

## Flags
Using any of the below will prevent the main program from running. Multiple flags can be used consecutively.
- `--addDisable <x>` if `x` is an integer, this will tell the program to close immediately after opening `x` times. Useful for interaction with the Task Scheduler; in my case, if I'm going to be playing games with friends for, say, four hours, and I don't want my program getting in the way, I might run `py <filepath> --addDisable 8` to add 8 disables to my DisableSchedule. Then, the next 8 times the Task Scheduler calls on the program, it will close immediately. Running 8 times every half-hour would take four hours, so the next time the program does not immediately close will be after 4 hours.
- `--addDisable <timeBlock>` if `timeBlock` is formatted correctly, this will append the given `timeBlock` to the DisableSchedule. This is a proper, scheduled disable; it will repeat every week over the same timespan until it is manually deleted from DisableSchedule.txt. The format is as follows: `WxHH:MM-HH:MM`, where `W` is the weekday as an integer (0 = Monday, 6 = Sunday), and `HH:MM` is hours/minutes for the start and end time.
- `--help` Prints information on how to use the program.
