# -*- coding: utf-8 -*-
import pandas as pd
from psychopy import event, core, data, gui, visual

DATA_DIR = 'data'
TYPE_TEST = 'test'
TYPE_END = 'end'
TYPE_PRACTICE = 'practice'
TRIALS_PRACTICE_FILE = 'practice_list.csv'
TRIALS_TEST_FILE = 'stimuli_list.csv'


# noinspection PyDefaultArgument
class StroopExperiment:

    def __init__(self, win_color):
        self.stimuli_positions = [[-.2, 0], [.2, 0], [0, 0]]
        self.win_color = win_color

    def create_window(self):
        color = self.win_color
        win = visual.Window(monitor="testMonitor", color=color, fullscr=False)
        return win

    @staticmethod
    def settings():
        import os
        experiment_info = {'suid': 1, 'age': 1, 'exp_version': 0.1, 'sex': ['f', 'm'], 'language': ['français', 'english'], u'date': data.getDateStr(format="%Y-%m-%d_%H:%M")}

        info_dialog = gui.DlgFromDict(title='Stroop task', dictionary=experiment_info, fixed=['exp_version'])

        experiment_info[u'data_file'] = DATA_DIR + os.path.sep + f'stroop_{experiment_info["age"]:02d}.csv'

        if info_dialog.OK:
            return experiment_info
        else:
            core.quit()
            return 'Cancelled'

    @staticmethod
    def create_text_stimuli(text=None, pos=[0.0, 0.0], name='', color='Black'):
        """
        Creates a text stimulus,
        :param text:
        :type text:
        :param pos:
        :type pos:
        :param name:
        :type name:
        :param color:
        :type color:
        :return:
        :rtype:
        """

        text_stimuli = visual.TextStim(win=window, ori=0, name=name, text=text, font=u'Arial', pos=pos, color=color, colorSpace=u'rgb')
        return text_stimuli

    @staticmethod
    def create_trials(pract=False, shuffle=True):
        zeTrials = pd.read_csv(TRIALS_PRACTICE_FILE if pract else TRIALS_TEST_FILE)
        zeTrials.index.name = 'index'
        if not pract:  # add output columns
            zeTrials['rt'] = 0.
            zeTrials['response'] = ''
            zeTrials['suid'] = int(settings['suid'])
            zeTrials['sex'] = settings['sex']
            zeTrials['accuracy'] = int(0)

        if shuffle:
            shuffled = zeTrials.sample(len(zeTrials))
            shuffled = shuffled.reset_index(drop=True)
            shuffled.index.name = 'index'
            return shuffled
        return zeTrials

    @staticmethod
    def present_stimuli(color, text, position, stim):
        _stimulus = stim
        color = color
        position = position

        if settings['language'] == "français":
            text = french_task(text)
        else:
            text = text

        _stimulus.pos = position
        _stimulus.setColor(color)
        _stimulus.setText(text)

        return _stimulus

    def running_experiment(self, trialz, testtype):
        timer = core.Clock()
        stimuli = [self.create_text_stimuli(window) for _ in range(4)]
        runTrials = trialz.copy(deep=True)
        for i, trial in trialz.iterrows():
            # Fixation cross
            fixation = self.present_stimuli('Black', '+', self.stimuli_positions[2], stimuli[3])
            fixation.draw()
            window.flip()
            POST_FIXATION_WAIT_DURATION = .6
            core.wait(POST_FIXATION_WAIT_DURATION)
            timer.reset()

            # Target word
            target = self.present_stimuli(trial['colour'], trial['stimulus'], self.stimuli_positions[2], stimuli[0])
            target.draw()

            # alt1
            alt1 = self.present_stimuli('Black', trial['alt1'], self.stimuli_positions[0], stimuli[1])
            alt1.draw()

            # alt2
            alt2 = self.present_stimuli('Black', trial['alt2'], self.stimuli_positions[1], stimuli[2])
            alt2.draw()
            window.flip()

            keys = event.waitKeys(keyList=['x', 'm'])
            resp_time = timer.getTime()

            if testtype == TYPE_PRACTICE:
                if keys[0] != trial['correctresponse']:
                    instructions['incorrect'].draw()

                else:
                    instructions['right'].draw()

                window.flip()
                core.wait(2)

            if testtype == TYPE_TEST:
                if keys[0] == trial['correctresponse']:
                    runTrials.loc[i, 'accuracy'] = 1
                else:
                    runTrials.loc[i, 'accuracy'] = 0

                runTrials.loc[i, 'rt'] = resp_time
                runTrials.loc[i, 'response'] = keys[0]

            event.clearEvents()
        return runTrials


def display_instructions(start_instruction=''):
    """
    Displays the instructions.

    :param start_instruction: the command
    :type start_instruction: str
    """
    # Display instructions

    if start_instruction == TYPE_PRACTICE:
        instructions['instructions'].pos = (0.0, 0.5)
        instructions['instructions'].draw()

        positions = [[-.2, 0], [.2, 0], [0, 0]]
        examples = [strexp.create_text_stimuli() for _ in positions]
        example_words = ['green', 'blue', 'green']
        if settings['language'] == 'français':
            example_words = [french_task(word) for word in example_words]

        for i, pos in enumerate(positions):
            examples[i].pos = pos

            if i == 0:
                examples[0].setText(example_words[i])

            elif i == 1:
                examples[1].setText(example_words[i])

            elif i == 2:
                examples[2].setColor('Green')
                examples[2].setText(example_words[i])

        [example.draw() for example in examples]

        instructions['practice'].pos = (0.0, -0.5)
        instructions['practice'].draw()

    elif start_instruction == TYPE_TEST:
        instructions['test'].draw()

    elif start_instruction == TYPE_END:
        instructions['done'].draw()

    window.flip()
    event.waitKeys(keyList=['space'])
    event.clearEvents()


def french_task(word):
    français = '+'
    if word == "blue":
        français = u"bleu"

    elif word == "red":
        français = u"rouge"

    elif word == "green":
        français = "vert"

    elif word == "yellow":
        français = "jaune"

    return français


def read_instructions(lang):
    global window
    import configparser
    configIn = configparser.ConfigParser()
    configIn.read("instructions.ini")
    configOut = {}
    for ck, cv in configIn[lang].items():
        configOut[ck] = visual.TextStim(window, text=configIn[lang][ck], wrapWidth=1.2, alignHoriz='center', color="Black", alignVert='center', height=0.06)
    return configOut


if __name__ == "__main__":
    strexp = StroopExperiment(win_color="White")
    settings = pd.Series(strexp.settings())
    language = settings['language']

    window = strexp.create_window()
    instructions = read_instructions(language)

    # We don't want the mouse to show:
    event.Mouse(visible=False)
    ##- Practice Trials
    display_instructions(start_instruction=TYPE_PRACTICE)
    practiceTrials = strexp.create_trials(pract=True)
    _ = strexp.running_experiment(practiceTrials, testtype='practice')

    ##- Test trials
    display_instructions(start_instruction=TYPE_TEST)
    testTrials = strexp.create_trials()
    run_trials = strexp.running_experiment(testTrials, testtype='test')
    run_trials.to_csv(settings.data_file, sep='\t')

    # End experiment but first we display some instructions
    display_instructions(start_instruction='end')
    window.close()
