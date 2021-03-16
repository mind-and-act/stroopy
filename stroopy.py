# -*- coding: utf-8 -*-
from psychopy import event, core, data, gui, visual
from fileHandling import *


# noinspection PyDefaultArgument
class Experiment:
    def __init__(self, win_color):
        self.stimuli_positions = [[-.2, 0], [.2, 0], [0, 0]]
        self.win_color = win_color

    def create_window(self):
        color = self.win_color
        win = visual.Window(monitor="testMonitor", color=color, fullscr=False)
        return win

    @staticmethod
    def settings():
        experiment_info = {'Subid': '', 'Age': '', 'Experiment Version': 0.1,
                           'Sex': ['Male', 'Female', 'Other'],
                           'Language': ['Swedish', 'English'], u'date':
                               data.getDateStr(format="%Y-%m-%d_%H:%M")}

        info_dialog = gui.DlgFromDict(title='Stroop task', dictionary=experiment_info,
                                      fixed=['Experiment Version'])
        experiment_info[u'DataFile'] = u'Data' + os.path.sep + u'stroop.csv'

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

        text_stimuli = visual.TextStim(win=window, ori=0, name=name,
                                       text=text, font=u'Arial',
                                       pos=pos,
                                       color=color, colorSpace=u'rgb')
        return text_stimuli

    @staticmethod
    def create_trials(trial_file):
        data_types = ['Response', 'Accuracy', 'RT', 'Sub_id', 'Sex']
        with open(trial_file, 'r') as stimfile:
            _stims = csv.DictReader(stimfile)
            trialz = data.TrialHandler(list(_stims), 1,
                                       method="random")

        [trialz.data.addDataType(data_type) for data_type in data_types]

        return trialz

    @staticmethod
    def present_stimuli(color, text, position, stim):
        _stimulus = stim
        color = color
        position = position
        if settings['Language'] == "Swedish":
            text = swedish_task(text)
        else:
            text = text
        _stimulus.pos = position
        _stimulus.setColor(color)
        _stimulus.setText(text)
        return _stimulus

    def running_experiment(self, trialz, testtype):
        _trials = trialz
        testtype = testtype
        timer = core.Clock()
        stimuli = [self.create_text_stimuli(window) for _ in range(4)]

        for trial in _trials:
            # Fixation cross
            fixation = self.present_stimuli('Black', '+', self.stimuli_positions[2],
                                            stimuli[3])
            fixation.draw()
            window.flip()
            core.wait(.6)
            timer.reset()

            # Target word
            target = self.present_stimuli(trial['colour'], trial['stimulus'],
                                          self.stimuli_positions[2], stimuli[0])
            target.draw()
            # alt1
            alt1 = self.present_stimuli('Black', trial['alt1'],
                                        self.stimuli_positions[0], stimuli[1])
            alt1.draw()
            # alt2
            alt2 = self.present_stimuli('Black', trial['alt2'],
                                        self.stimuli_positions[1], stimuli[2])
            alt2.draw()
            window.flip()

            keys = event.waitKeys(keyList=['x', 'm'])
            resp_time = timer.getTime()
            if testtype == 'practice':
                if keys[0] != trial['correctresponse']:
                    instruction_stimuli['incorrect'].draw()

                else:
                    instruction_stimuli['right'].draw()

                window.flip()
                core.wait(2)

            if testtype == 'test':
                if keys[0] == trial['correctresponse']:
                    trial['Accuracy'] = 1
                else:
                    trial['Accuracy'] = 0

                trial['RT'] = resp_time
                trial['Response'] = keys[0]
                trial['Sub_id'] = settings['Subid']
                trial['Sex'] = settings['Sex']
                write_csv(settings[u'DataFile'], trial)

            event.clearEvents()


def create_instructions_dict(instr):
    start_n_end = [w for w in instr.split() if w.endswith('START') or w.endswith('END')]
    keys = {}

    for word in start_n_end:
        # noinspection RegExpDuplicateCharacterInClass
        key = re.split("[END, START]", word)[0]

        if key not in keys.keys():
            keys[key] = []

        if word.startswith(key):
            keys[key].append(word)
    return keys


def create_instructions(input_, START_, END_):
    instruction_text = parse_instructions(input_, START_, END_)
    print(instruction_text)
    text_stimuli = visual.TextStim(window, text=instruction_text, wrapWidth=1.2,
                                   alignHoriz='center', color="Black",
                                   alignVert='center', height=0.06)

    return text_stimuli


def display_instructions(start_instruction=''):
    # Display instructions

    if start_instruction == 'Practice':
        instruction_stimuli['instructions'].pos = (0.0, 0.5)
        instruction_stimuli['instructions'].draw()

        positions = [[-.2, 0], [.2, 0], [0, 0]]
        examples = [experiment.create_text_stimuli() for _ in positions]
        example_words = ['green', 'blue', 'green']
        if settings['Language'] == 'Swedish':
            example_words = [swedish_task(word) for word in example_words]

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

        instruction_stimuli['practice'].pos = (0.0, -0.5)
        instruction_stimuli['practice'].draw()

    elif start_instruction == 'Test':
        instruction_stimuli['test'].draw()

    elif start_instruction == 'End':
        instruction_stimuli['done'].draw()

    window.flip()
    event.waitKeys(keyList=['space'])
    event.clearEvents()


def swedish_task(word):
    swedish = '+'
    if word == "blue":
        swedish = u"blå"

    elif word == "red":
        swedish = u"röd"

    elif word == "green":
        swedish = u"grön"

    elif word == "yellow":
        swedish = "gul"

    return swedish


if __name__ == "__main__":
    experiment = Experiment(win_color="White")
    settings = experiment.settings()
    language = settings['Language']
    instructions = read_instructions_file("INSTRUCTIONS", language, language + "End")
    instructions_dict = create_instructions_dict(instructions)
    instruction_stimuli = {}

    window = experiment.create_window()

    for instruction, (START, END) in instructions_dict.items():
        instruction_stimuli[instruction] = create_instructions(instructions, START, END)
    # We don't want the mouse to show:
    event.Mouse(visible=False)
    # Practice Trials
    display_instructions(start_instruction='Practice')

    practice = experiment.create_trials('practice_list.csv')
    experiment.running_experiment(practice, testtype='practice')
    # Test trials
    display_instructions(start_instruction='Test')
    trials = experiment.create_trials('stimuli_list.csv')
    experiment.running_experiment(trials, testtype='test')

    # End experiment but first we display some instructions
    display_instructions(start_instruction='End')
    window.close()
