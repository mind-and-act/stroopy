# Stroopy
A simple Stroop Task programmed using PsychoPy 

[![IMAGE ALT TEXT HERE](https://i.ytimg.com/vi/re8i-CZwREI/0.jpg)](https://www.youtube.com/watch?v=re8i-CZwREI)


## Instructions
- [x] English
- [x] French


Instructions (both English and French) are found in the file ``instructions.ini``. This file is read and parsed by some
functions. The set up of the functions is that Swedish - SwedishEnd words will mark where the swedish instructions are.
The words ending with START and END marks where the scripts (i.e., the functions) will find instructions:

- instructions - The instructions on how to perform the task - the first that will show
- practice - How to start the experiment (i.e., press SPACE) - the first that will show (on the bottom of the screen)
- test - After practice trials - informing that the test part starts and questions should be asked now
- done - Telling participants that the experiment is done

## Stimuli
- [x] English
- [x] Swedish (stimuli translated in the script. Not optimal)
- More languages? Feel free to add your own languages. Perhaps
  the function for translating to Swedish need to remove and languages
  fetched elsewhere.

Feel free to contribute with other languages.

As for now to add more languages add a language in the list on line 21 (['Français', 'English']). After this is done
you need to follow how the ``instructions.ini`` file is set up. Also, the translation function needs to be updated.

---------
