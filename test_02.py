import os
import sys
import random
from datetime import datetime
import glob # For finding files matching a pattern
import traceback # For detailed error logging

# Ensure we have fallback for audio/visual issues if needed
#prefs.hardware['audioLib'] = ['PTB', 'sounddevice', 'pyo','pygame']
from psychopy import locale_setup
from psychopy import prefs
# prefs.hardware['audioLib'] = ['PTB'] # Force PTB if specific backend needed
from psychopy import sound, gui, visual, core, data, event, logging

# --- Experiment Setup ---
# Clear command window (optional, less common in Python scripts)
# print("\033c", end="") # Clears console in some terminals

# --- Basic Settings ---
useKeyboard = True      # Set to False only if using a non-keyboard HID device AND know how to address it
# responseDevice = 'deviceName' # Specify device if useKeyboard = false (more complex setup)
correctKey = 'left'      # PsychoPy key name for "correct" dragon response
incorrectKey = 'right'     # PsychoPy key name for "incorrect" dragon response
escapeKey = 'escape'      # Key to abort the experiment
allowedKeys = [correctKey, incorrectKey, escapeKey]

# Seed the random number generator
random.seed() # Uses system time by default, similar to rng('shuffle')

# --- Participant Info & Counterbalancing ---
expName = 'RhythmicPriming'
expInfo = {
    'Participant ID': 'P01',
    'Session Number': '1',
    'Sentence Set (A or B)': 'A',
}
# Display dialog box to get participant info
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    print("User cancelled the experiment during setup.")
    core.quit()  # User pressed cancel

# Validate Sentence Set
chosen_sentence_set = expInfo['Sentence Set (A or B)'].strip().upper()
if chosen_sentence_set not in ['A', 'B']:
    errorDlg = gui.Dlg(title="Input Error", labelButtonCancel="OK")
    errorDlg.addText(f"Invalid Sentence Set: '{expInfo['Sentence Set (A or B)']}'.\nIt must be A or B.")
    errorDlg.show()
    print(f"Error: Invalid Sentence Set '{expInfo['Sentence Set (A or B)']}'. It must be A or B.")
    core.quit()
expInfo['Sentence Set Val'] = chosen_sentence_set

participantID = expInfo['Participant ID']
sessionNum = expInfo['Session Number']

# --- Stimulus & Timing Parameters ---
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    script_dir = os.getcwd()

stimDir = os.path.join(script_dir, 'stimuli')
audioDir = os.path.join(stimDir, 'audio')
imgDir = os.path.join(stimDir, 'images')
audioFormat = '.wav'

# --- SENTENCE TEXT MAPPINGS (MAIN EXPERIMENT) ---
SENTENCE_TEXT_A = {
    "sent_corr_01.wav": "Every year, the woman trims her hair in early June.",
    "sent_corr_02.wav": "Every year, the kid paints many pictures with bright colors.",
    "sent_corr_03.wav": "Every year, the animals take nuts back to their nests.",
    "sent_corr_04.wav": "Every year, the workers taste many meals for the chefs.",
    "sent_corr_05.wav": "Every year, the worker digs the holes in the flowerbed.",
    "sent_corr_06.wav": "Every year, the teacher hangs the decorations in her classroom.",
    "sent_corr_07.wav": "Every year, the moms sniff the flowers in the springtime.",
    "sent_corr_08.wav": "Every day, the brothers cut their dessert into equal pieces.",
    "sent_corr_09.wav": "Every day, the teachers give a little homework after class.",
    "sent_corr_10.wav": "Last year, the children dropped a vase on the floor.",
    "sent_corr_11.wav": "Last year, the animals watched insects on the tree roots.",
    "sent_corr_12.wav": "Last year, the kid locked his keys in the car.",
    "sent_corr_13.wav": "Last year, the people smelled fresh air by the ocean.",
    "sent_corr_14.wav": "Yesterday, the children hummed a song on the playground.",
    "sent_corr_15.wav": "Yesterday, the child touched a hot stove before breakfast.",
    "sent_corr_16.wav": "Yesterday, the teachers checked some math worksheets for mistakes.",
    "sent_corr_17.wav": "Yesterday, the boys baked many cookies with their aunt.",
    "sent_corr_18.wav": "Yesterday, the teacher picked some flowers for her students.",
    "sent_viol_01.wav": "Every year, the sisters braids their hair for Thanksgiving dinner.",
    "sent_viol_02.wav": "Every year, the animal eat grass in the big pasture.",
    "sent_viol_03.wav": "Every year, the student learn many things in his classes.",
    "sent_viol_04.wav": "Every year, the person hear birds in the early spring.",
    "sent_viol_05.wav": "Every year, the mom throw the baseball with her kids.",
    "sent_viol_06.wav": "Every year, the child ask his mom for new toys.",
    "sent_viol_07.wav": "Every day, the dads toasts the bread for their breakfast.",
    "sent_viol_08.wav": "Every day, the moms reads two stories to their children.",
    "sent_viol_09.wav": "Every day, the women knits hats for the little children.",
    "sent_viol_10.wav": "Last year, the child guess some answers on the test.",
    "sent_viol_11.wav": "Last year, the person mail letters at the post office.",
    "sent_viol_12.wav": "Last year, the dads grill some burgers at the picnic.",
    "sent_viol_13.wav": "Last year, the worker use the snowblower in the winter.",
    "sent_viol_14.wav": "Yesterday, the dad dry clean dishes with a towel.",
    "sent_viol_15.wav": "Yesterday, the men punch a bag at the gym.",
    "sent_viol_16.wav": "Yesterday, the animal dip his nose in the pond.",
    "sent_viol_17.wav": "Yesterday, the students fix mistakes on their science homework.",
    "sent_viol_18.wav": "Yesterday, the brother boil water in an iron pot."
}
SENTENCE_TEXT_B = {
    "b_sent_viol_01.wav": "Every year, the woman trim her hair in early June.",
    "b_sent_viol_02.wav": "Every year, the kid paint many pictures with bright colors.",
    "b_sent_viol_03.wav": "Every year, the animals takes nuts back to their nests.",
    "b_sent_viol_04.wav": "Every year, the workers tastes many meals for the chefs.",
    "b_sent_viol_05.wav": "Every year, the worker dig the holes in the flowerbed.",
    "b_sent_viol_06.wav": "Every year, the teacher hang the decorations in her classroom.",
    "b_sent_viol_07.wav": "Every year, the moms sniffs the flowers in the springtime.",
    "b_sent_viol_08.wav": "Every day, the brothers cuts their dessert into equal pieces.",
    "b_sent_viol_09.wav": "Every day, the teachers gives a little homework after class.",
    "b_sent_viol_10.wav": "Last year, the children drop a vase on the floor.",
    "b_sent_viol_11.wav": "Last year, the animals watch insects on the tree roots.",
    "b_sent_viol_12.wav": "Last year, the kid lock his keys in the car.",
    "b_sent_viol_13.wav": "Last year, the people smell fresh air by the ocean.",
    "b_sent_viol_14.wav": "Yesterday, the children hum a song on the playground.",
    "b_sent_viol_15.wav": "Yesterday, the child touch a hot stove before breakfast.",
    "b_sent_viol_16.wav": "Yesterday, the teachers check some math worksheets for mistakes.",
    "b_sent_viol_17.wav": "Yesterday, the boys bake many cookies with their aunt.",
    "b_sent_viol_18.wav": "Yesterday, the teacher pick some flowers for her students.",
    "b_sent_corr_01.wav": "Every year, the sisters braid their hair for Thanksgiving dinner.",
    "b_sent_corr_02.wav": "Every year, the animal eats grass in the big pasture.",
    "b_sent_corr_03.wav": "Every year, the student learns many things in his classes.",
    "b_sent_corr_04.wav": "Every year, the person hears birds in the early spring.",
    "b_sent_corr_05.wav": "Every year, the mom throws the baseball with her kids.",
    "b_sent_corr_06.wav": "Every year, the child asks his mom for new toys.",
    "b_sent_corr_07.wav": "Every day, the dads toast the bread for their breakfast.",
    "b_sent_corr_08.wav": "Every day, the moms read two stories to their children.",
    "b_sent_corr_09.wav": "Every day, the women knit hats for the little children.",
    "b_sent_corr_10.wav": "Last year, the child guessed some answers on the test.",
    "b_sent_corr_11.wav": "Last year, the person mailed letters at the post office.",
    "b_sent_corr_12.wav": "Last year, the dads grilled some burgers at the picnic.",
    "b_sent_corr_13.wav": "Last year, the worker used the snowblower in the winter.",
    "b_sent_corr_14.wav": "Yesterday, the dad dried clean dishes with a towel.",
    "b_sent_corr_15.wav": "Yesterday, the men punched a bag at the gym.",
    "b_sent_corr_16.wav": "Yesterday, the animal dipped his nose in the pond.",
    "b_sent_corr_17.wav": "Yesterday, the students fixed mistakes on their science homework.",
    "b_sent_corr_18.wav": "Yesterday, the brother boiled water in an iron pot."
}
active_sentence_text_map = None
if chosen_sentence_set == 'A':
    active_sentence_text_map = SENTENCE_TEXT_A
elif chosen_sentence_set == 'B':
    active_sentence_text_map = SENTENCE_TEXT_B

# --- DETAILED PRACTICE FEEDBACK TEXTS ---
PRACTICE_FEEDBACK_A = {
    "test_a_sent_corr_01.wav": "This sentence sounded right so it was the HAPPY dragon who said it.",
    "test_a_sent_corr_02.wav": "This sentence sounded right so it was the HAPPY dragon who said it.",
    "test_a_sent_viol_01.wav": "This sentence didn’t sound quite right so it was the CONFUSED dragon who said it.",
    "test_a_sent_viol_02.wav": "This sentence didn’t sound quite right so it was the CONFUSED dragon who said it."     
}
PRACTICE_FEEDBACK_B = {
    "test_b_sent_corr_01.wav": "This sentence sounded right so it was the HAPPY dragon who said it.",
    "test_b_sent_corr_02.wav": "This sentence sounded right so it was the HAPPY dragon who said it.",
    "test_b_sent_viol_01.wav": "This sentence didn’t sound quite right so it was the CONFUSED dragon who said it.",
    "test_b_sent_viol_02.wav": "This sentence didn’t sound quite right so it was the CONFUSED dragon who said it."
}
active_practice_feedback_map = None
if chosen_sentence_set == 'A':
    active_practice_feedback_map = PRACTICE_FEEDBACK_A
elif chosen_sentence_set == 'B':
    active_practice_feedback_map = PRACTICE_FEEDBACK_B
# --- END DETAILED PRACTICE FEEDBACK TEXTS ---


if chosen_sentence_set == 'A':
    main_sentence_audio_path = os.path.join(audioDir, 'set a')
    main_corr_prefix = 'sent_corr_'
    main_viol_prefix = 'sent_viol_'
    practice_audio_subpath = os.path.join('practice', 'practice a')
    practice_corr_base_1 = 'test_a_sent_corr_01'
    practice_viol_base_1 = 'test_a_sent_viol_01'
    practice_corr_base_2 = 'test_a_sent_corr_02'
    practice_viol_base_2 = 'test_a_sent_viol_02'
elif chosen_sentence_set == 'B':
    main_sentence_audio_path = os.path.join(audioDir, 'set b')
    main_corr_prefix = 'b_sent_corr_'
    main_viol_prefix = 'b_sent_viol_'
    practice_audio_subpath = os.path.join('practice', 'practice b')
    practice_corr_base_1 = 'test_b_sent_corr_01'
    practice_viol_base_1 = 'test_b_sent_viol_01'
    practice_corr_base_2 = 'test_b_sent_corr_02'
    practice_viol_base_2 = 'test_b_sent_viol_02'
else:
    show_error_and_quit("Critical error: Invalid sentence set determined post-validation.", "Config Error")

dynamic_practice_audio_path = os.path.join(audioDir, practice_audio_subpath)

primeFiles = {
    'regular': 'regular.wav',
    'irregular': 'irregular.wav'
}
drumImageFile = 'drum.png'
exclamImageFile = 'exclamation.png'
correctDragonImageFile = 'dragon_correct.png'
incorrectDragonImageFile = 'dragon_incorrect.png'

fixationDuration = 0.5
postPrimePause = 0.5
exclamationDuration = 0.5
postSentencePause = 0.2
responseTimeLimit = 7.0
interTrialInterval = 1.0
feedbackDuration = 0.75

numBlocks = 6
numSentencesPerBlock = 6
numCorrectPerBlock = 3
numViolationPerBlock = 3
if numCorrectPerBlock + numViolationPerBlock != numSentencesPerBlock:
    errorDlg = gui.Dlg(title="Design Error", labelButtonCancel="OK")
    errorDlg.addText('Configuration Error: Number of correct + violation sentences does not match sentences per block.')
    errorDlg.show()
    raise ValueError('Number of correct + violation sentences does not match sentences per block.')
totalTrials = numBlocks * numSentencesPerBlock

outputDir = os.path.join(script_dir, 'data')
if not os.path.exists(outputDir):
    try:
        os.makedirs(outputDir)
    except OSError as e:
        errorDlg = gui.Dlg(title="File System Error", labelButtonCancel="OK")
        errorDlg.addText(f"Could not create data directory:\n{outputDir}\nError: {e}\nPlease check permissions.")
        errorDlg.show()
        core.quit()

dateTimeStr = datetime.now().strftime("%Y%m%d_%H%M%S")
outputFileNameBase = f'{participantID}_session{sessionNum}_set{chosen_sentence_set}_{dateTimeStr}'
outputFileName = os.path.join(outputDir, outputFileNameBase)

thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=script_dir,
    savePickle=True, saveWideText=True,
    dataFileName=outputFileName)

logFile = logging.LogFile(outputFileName + '.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)

def show_error_and_quit(message, title="Error"):
    errorDlg = gui.Dlg(title=title, labelButtonCancel="OK")
    errorDlg.addText(message)
    errorDlg.show()
    logging.error(message)
    if 'win' in globals() and win is not None:
        win.close()
    core.quit()

print('Loading main stimulus lists...')
logging.info('Loading main stimulus lists...')
correctSentenceFiles = glob.glob(os.path.join(main_sentence_audio_path, f'{main_corr_prefix}*{audioFormat}'))
violationSentenceFiles = glob.glob(os.path.join(main_sentence_audio_path, f'{main_viol_prefix}*{audioFormat}'))

numCorrectNeeded = numBlocks * numCorrectPerBlock
numViolationNeeded = numBlocks * numViolationPerBlock

if len(correctSentenceFiles) < numCorrectNeeded:
    show_error_and_quit(f'Insufficient correct sentence files found in {main_sentence_audio_path}.\nNeed {numCorrectNeeded}, found {len(correctSentenceFiles)}.\nCheck filenames match "{main_corr_prefix}*{audioFormat}".', title="Stimulus Error")
if len(violationSentenceFiles) < numViolationNeeded:
    show_error_and_quit(f'Insufficient violation sentence files found in {main_sentence_audio_path}.\nNeed {numViolationNeeded}, found {len(violationSentenceFiles)}.\nCheck filenames match "{main_viol_prefix}*{audioFormat}".', title="Stimulus Error")

selectedCorrectFiles = random.sample(correctSentenceFiles, numCorrectNeeded)
selectedViolationFiles = random.sample(violationSentenceFiles, numViolationNeeded)

all_correct_sentence_details = []
for f in selectedCorrectFiles:
    all_correct_sentence_details.append({'filename': os.path.basename(f).lower(), 'type': 'correct', 'path': f})

all_violation_sentence_details = []
for f in selectedViolationFiles:
    all_violation_sentence_details.append({'filename': os.path.basename(f).lower(), 'type': 'violation', 'path': f})

print(f'Loaded and selected {numCorrectNeeded} correct and {numViolationNeeded} violation sentences for Set {chosen_sentence_set}.')
logging.info(f'Loaded and selected {numCorrectNeeded} correct and {numViolationNeeded} violation sentences for Set {chosen_sentence_set}.')

random.shuffle(all_correct_sentence_details)
random.shuffle(all_violation_sentence_details)
correct_sentence_idx = 0
violation_sentence_idx = 0

num_regular_blocks = numBlocks // 2
num_irregular_blocks = numBlocks - num_regular_blocks
primeOrder = ['regular'] * num_regular_blocks + ['irregular'] * num_irregular_blocks
random.shuffle(primeOrder)
print(f'Randomized prime order for this participant: {", ".join(primeOrder)}')
logging.info(f'Randomized prime order for this participant: {", ".join(primeOrder)}')
thisExp.addData('prime_order_for_participant', ",".join(primeOrder))

print('Initializing PsychoPy components...')
logging.info('Initializing PsychoPy components...')
try:
    win = visual.Window(
        size=[1024, 768], fullscr=True, screen=0,
        winType='pyglet', allowGUI=False, allowStencil=False,
        monitor='testMonitor', color=[0.7, 0.95, 0.7], colorSpace='rgb',
        blendMode='avg', useFBO=True,
        units='pix')
except Exception as e:
    show_error_and_quit(f"Failed to create PsychoPy window.\nError: {e}\n\nPlease check graphics drivers and PsychoPy installation.", title="Display Error")

expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0
    logging.warning("Frame rate estimation failed. Using 60 Hz default.")

globalClock = core.Clock()
rtClock = core.Clock()

try:
    drumStim = visual.ImageStim(win, image=os.path.join(imgDir, drumImageFile), units='pix')
    exclamStim = visual.ImageStim(win, image=os.path.join(imgDir, exclamImageFile), units='pix')
    correctDragonStim = visual.ImageStim(win, image=os.path.join(imgDir, correctDragonImageFile), units='pix')
    incorrectDragonStim = visual.ImageStim(win, image=os.path.join(imgDir, incorrectDragonImageFile), units='pix')
except Exception as e:
    logging.error(f"Error loading image: {e}. Check image paths and files in {imgDir}")
    show_error_and_quit(f"Error loading image: {e}\nCheck image paths and files in {imgDir}", title="Image Loading Error")

drumScaleFactor = 1.0
exclamScaleFactor = 0.5
origDrumWidth, origDrumHeight = drumStim.size
drumStim.size = (origDrumWidth * drumScaleFactor, origDrumHeight * drumScaleFactor)
logging.info(f"Scaled drum image size to: {drumStim.size}")
origExclamWidth, origExclamHeight = exclamStim.size
exclamStim.size = (origExclamWidth * exclamScaleFactor, origExclamHeight * exclamScaleFactor)
logging.info(f"Scaled exclamation mark image size to: {exclamStim.size}")

win_width, win_height = win.size
xCenter, yCenter = 0, 0
dragonWidth, dragonHeight = correctDragonStim.size
dragonWidth *= 0.8
dragonHeight *= 0.8
correctDragonStim.size = (dragonWidth, dragonHeight)
incorrectDragonStim.size = (dragonWidth, dragonHeight)
imageSpacing = 100
correctDragonPos = [xCenter - dragonWidth/2 - imageSpacing/2, yCenter]
incorrectDragonPos = [xCenter + dragonWidth/2 + imageSpacing/2, yCenter]
correctDragonStim.pos = correctDragonPos
incorrectDragonStim.pos = incorrectDragonPos
drumStim.pos = (xCenter, yCenter)
exclamStim.pos = (xCenter, yCenter)

fixationCross = visual.TextStim(win, text='+', height=60, color='black', pos=(xCenter, yCenter))
instructionTextStim = visual.TextStim(win, text='', height=30, wrapWidth=win_width*0.8, color='black', alignText='center', pos=(xCenter, yCenter))
feedbackTextStim = visual.TextStim(win, text='', height=40, color='red', pos=(xCenter, yCenter - dragonHeight/2 - 50))
blockBreakTextStim = visual.TextStim(win, text='', height=40, wrapWidth=win_width*0.8, color='black', alignText='center', pos=(xCenter, yCenter))
detailedPracticeFeedbackStim = visual.TextStim(win, text='', height=24, 
                                             wrapWidth=win_width*0.85, 
                                             color='black', alignText='left',
                                             pos=(xCenter, yCenter))

# --- Instructions ---
print('Displaying initial instructions (leading to practice)...')
logging.info('Displaying initial instructions (leading to practice)...')
initial_instruction_text = (
    "Welcome to the Dragon Game!\n\n"
    "When you see the DRUMS, listen to the music.\n"
    "Then, when you see the EXCLAMATION MARK, listen to the sentence.\n"
    "Decide if the sentence sounds GOOD or WRONG.\n\n"
    "Press LEFT ARROW KEY if it sounds good\n"
    "and the happy dragon on the left side of the screen said it.\n\n"
    "Press RIGHT ARROW KEY if it sounds wrong\n"
    "and the puzzled dragon on the right side of the screen said it.\n\n"
    "Let’s do a short practice session first!\n"
    "After each practice sentence, we’ll show you if you were right or\n"
    "wrong and explain why.\n\n"
    "Press any key when you’re ready to start the PRACTICE."
)
instructionTextStim.text = initial_instruction_text
instructionTextStim.draw()
win.flip()
event.waitKeys()
core.wait(0.5)

# <<<--- START: PRACTICE SESSION CODE --- >>>
print('Setting up practice session...')
logging.info('Setting up practice session...')

practice_sets_definition = [
    {'prime_type': 'regular', 'sentences_info': [{'filename_base': practice_corr_base_1, 'type': 'correct'}, {'filename_base': practice_viol_base_1, 'type': 'violation'}]},
    {'prime_type': 'irregular', 'sentences_info': [{'filename_base': practice_corr_base_2, 'type': 'correct'}, {'filename_base': practice_viol_base_2, 'type': 'violation'}]}
]
random.shuffle(practice_sets_definition)

practice_trials_structured = []
for p_set in practice_sets_definition:
    prime_type_for_practice = p_set['prime_type']
    actual_prime_audio_file_for_practice = os.path.join(audioDir, primeFiles[prime_type_for_practice])
    if not os.path.exists(actual_prime_audio_file_for_practice):
        show_error_and_quit(f"Practice prime audio file not found: {actual_prime_audio_file_for_practice}", title="Practice File Error")
    random.shuffle(p_set['sentences_info'])
    for sent_info in p_set['sentences_info']:
        fname = sent_info['filename_base'] + audioFormat
        fpath = os.path.join(dynamic_practice_audio_path, fname)
        if not os.path.exists(fpath):
            show_error_and_quit(f"Practice audio file not found: {fpath}\nPlease check the '{dynamic_practice_audio_path}' folder.", title="Practice File Error")
        practice_trials_structured.append({
            'prime_type': prime_type_for_practice,
            'prime_audio_file': actual_prime_audio_file_for_practice,
            'sentence_filename': fname.lower(), # Ensure filename is stored as lower for lookup
            'sentence_type': sent_info['type'],
            'sentence_path': fpath
        })

practiceCorrectnessFeedbackStim = visual.TextStim(win, text='', height=35, pos=(xCenter, yCenter - dragonHeight / 2 - 90), wrapWidth=win_width * 0.8)
current_practice_prime_sound = None
last_played_prime_file = None
practice_trial_counter = 0

for p_trial_data in practice_trials_structured:
    practice_trial_counter += 1
    print(f'    Practice Trial {practice_trial_counter}/{len(practice_trials_structured)}')
    logging.info(f'    Practice Trial {practice_trial_counter}/{len(practice_trials_structured)}')
    if last_played_prime_file != p_trial_data['prime_audio_file']:
        if current_practice_prime_sound is not None:
             current_practice_prime_sound.stop()
        print(f"  Presenting practice musical prime: {p_trial_data['prime_type']} ({os.path.basename(p_trial_data['prime_audio_file'])})")
        logging.info(f"  Presenting practice musical prime: {p_trial_data['prime_type']} ({os.path.basename(p_trial_data['prime_audio_file'])})")
        try:
            current_practice_prime_sound = sound.Sound(p_trial_data['prime_audio_file'], stereo=True, hamming=True)
            practicePrimeDurationActual = current_practice_prime_sound.getDuration()
            if practicePrimeDurationActual is None or not isinstance(practicePrimeDurationActual, (int, float)) or practicePrimeDurationActual <= 0:
                logging.warning(f"Could not get valid duration for practice prime: {p_trial_data['prime_audio_file']}. Using fallback 5.0s.")
                practicePrimeDurationActual = 5.0
        except Exception as e:
            logging.error(f"Error loading practice prime audio: {p_trial_data['prime_audio_file']} - {e}")
            show_error_and_quit(f"Error loading practice prime audio: {p_trial_data['prime_audio_file']}\n{e}", title="Practice Audio Error")
        drumStim.draw()
        win.flip()
        current_practice_prime_sound.play()
        print(f"    Practice prime playing ({practicePrimeDurationActual:.3f} s)...")
        logging.info(f"    Practice prime playing ({practicePrimeDurationActual:.3f} s)...")
        core.wait(practicePrimeDurationActual - 0.05)
        current_practice_prime_sound.stop()
        last_played_prime_file = p_trial_data['prime_audio_file']
        win.flip()
        core.wait(postPrimePause)
    
    p_sentenceFile = p_trial_data['sentence_path']
    p_sentenceType = p_trial_data['sentence_type']
    p_sentenceID = p_trial_data['sentence_filename'] # This is already lowercased during practice_trials_structured creation
    
    print(f'      Sentence ({p_sentenceType}): {p_sentenceID}')
    logging.info(f'      Sentence ({p_sentenceType}): {p_sentenceID}')
    fixationCross.draw()
    win.flip()
    core.wait(fixationDuration)
    exclamStim.draw()
    win.flip()
    core.wait(exclamationDuration)
    print('      Playing practice sentence...')
    logging.info('      Playing practice sentence...')
    try:
        p_sentenceSound = sound.Sound(p_sentenceFile, stereo=True, hamming=True)
        p_sentenceDurationActual = p_sentenceSound.getDuration()
        if p_sentenceDurationActual is None or not isinstance(p_sentenceDurationActual, (int, float)) or p_sentenceDurationActual <= 0:
            logging.warning(f"Could not get valid duration for practice sentence: {p_sentenceFile}. Using fallback 3.0s.")
            p_sentenceDurationActual = 3.0
    except Exception as e:
        logging.error(f"Error loading practice sentence audio: {p_sentenceFile} - {e}")
        show_error_and_quit(f"Error loading practice sentence audio: {p_sentenceFile}\n{e}", title="Practice Audio Error")
    p_sentenceSound.play()
    print(f"      Practice sentence playing ({p_sentenceDurationActual:.3f} s)...")
    logging.info(f"      Practice sentence playing ({p_sentenceDurationActual:.3f} s)...")
    core.wait(p_sentenceDurationActual)
    core.wait(postSentencePause)
    print('      Waiting for practice response...')
    logging.info('      Waiting for practice response...')
    correctDragonStim.draw()
    incorrectDragonStim.draw()
    rtClock.reset()
    event.clearEvents(eventType='keyboard')
    win.flip()
    p_response = event.waitKeys(keyList=allowedKeys, timeStamped=rtClock)
    p_responseKey = None
    p_rt = None
    p_responseDragon = 'NA'
    p_keyName, p_rt = p_response[0]
    p_responseKey = p_keyName
    if p_keyName == escapeKey:
        logging.critical('Experiment aborted by user during practice.')
        print('\nExperiment aborted by user during practice.')
        raise KeyboardInterrupt("Experiment aborted by user via Escape key during practice.")
    elif p_keyName == correctKey:
        p_responseDragon = 'correct'
    elif p_keyName == incorrectKey:
        p_responseDragon = 'incorrect'
    print(f'      Practice Response: {p_responseDragon} ({p_responseKey}) | RT: {p_rt:.4f} s')
    logging.info(f'      Practice Response: {p_responseDragon} ({p_responseKey}) | RT: {p_rt:.4f} s')
    is_attempt_correct = False
    if (p_sentenceType == 'correct' and p_responseDragon == 'correct') or \
       (p_sentenceType == 'violation' and p_responseDragon == 'incorrect'):
        is_attempt_correct = True
    if is_attempt_correct:
        practiceCorrectnessFeedbackStim.text = 'Correct!'
        practiceCorrectnessFeedbackStim.color = [0,0.6,0]
    else:
        practiceCorrectnessFeedbackStim.text = 'That was not the expected answer.'
        practiceCorrectnessFeedbackStim.color = 'darkred'
    correctDragonStim.draw()
    incorrectDragonStim.draw()
    practiceCorrectnessFeedbackStim.draw()
    win.flip()
    core.wait(feedbackDuration * 1.8)

    # --- Display detailed feedback pop-up ---
    detailed_feedback_text_to_show = "Detailed feedback not found for this sentence." 
    if active_practice_feedback_map is not None:
        detailed_feedback_text_to_show = active_practice_feedback_map.get(p_sentenceID, # p_sentenceID is already lowercase
                                                                       "Detailed feedback not found for ID: " + p_sentenceID)
    detailedPracticeFeedbackStim.setText(detailed_feedback_text_to_show)
    detailedPracticeFeedbackStim.draw()
    win.flip()
    event.waitKeys() 
    # --- END NEW ---

    win.flip() 
    core.wait(interTrialInterval)

# --- Practice Session End Instructions ---
practiceEndText = (
    "Practice session finished.\n"
    "You did a great job identifying the dragons!\n\n"
    "Now it’s time for the real game.\n"
    "This time, there won’t be any explanations, just listen carefully\n"
    "and decide which dragon is speaking.\n\n"
    "Remember:\n"
    "Press LEFT ARROW KEY\n"
    "for GOOD sentences (happy dragon)\n\n"
    "Press RIGHT ARROW KEY\n"
    "for WRONG sentences (puzzled dragon)\n\n"
    "Press any key when you’re ready to start the REAL GAME."
)
instructionTextStim.text = practiceEndText
instructionTextStim.draw()
win.flip()
event.waitKeys()
core.wait(0.5)

print('Practice session complete. Starting main experiment...')
logging.info('Practice session complete. Starting main experiment...')
# <<<--- END: PRACTICE SESSION CODE --- >>>

trialCounter = 0
try:
    for block in range(numBlocks):
        currentBlockNum = block + 1
        print(f'Starting Block {currentBlockNum} of {numBlocks}...')
        logging.info(f'Starting Block {currentBlockNum} of {numBlocks}...')
        thisExp.addData('block_num', currentBlockNum)

        currentPrimeType = primeOrder[block]
        print(f'  Prime Type: {currentPrimeType}')
        logging.info(f'  Prime Type: {currentPrimeType}')
        thisExp.addData('block_prime_type', currentPrimeType)

        primeAudioFile = os.path.join(audioDir, primeFiles[currentPrimeType])
        if not os.path.exists(primeAudioFile):
            logging.error(f"Prime audio file not found: {primeAudioFile}")
            raise FileNotFoundError(f"Prime audio file not found: {primeAudioFile}")

        current_block_correct_sentences = all_correct_sentence_details[correct_sentence_idx : correct_sentence_idx + numCorrectPerBlock]
        correct_sentence_idx += numCorrectPerBlock
        current_block_violation_sentences = all_violation_sentence_details[violation_sentence_idx : violation_sentence_idx + numViolationPerBlock]
        violation_sentence_idx += numViolationPerBlock
        blockSentences = current_block_correct_sentences + current_block_violation_sentences
        random.shuffle(blockSentences)
        num_actually_correct = sum(1 for s in blockSentences if s['type'] == 'correct')
        num_actually_violation = sum(1 for s in blockSentences if s['type'] == 'violation')
        print(f'  Sentences for block {currentBlockNum}: {num_actually_correct} correct, {num_actually_violation} violation. Order randomized.')
        logging.info(f'  Sentences for block {currentBlockNum}: {num_actually_correct} correct, {num_actually_violation} violation. Order randomized.')

        print('  Presenting musical prime...')
        logging.info('  Presenting musical prime...')
        try:
            primeSound = sound.Sound(primeAudioFile, stereo=True, hamming=True)
            primeDurationActual = primeSound.getDuration()
            if primeDurationActual is None or not isinstance(primeDurationActual, (int, float)) or primeDurationActual <= 0:
                logging.warning(f"Could not get valid duration for prime: {primeAudioFile}. Using fallback 5.0s.")
                primeDurationActual = 5.0
        except Exception as e:
            logging.error(f"Error loading prime audio: {primeAudioFile} - {e}")
            print(f"\nError loading prime audio: {primeAudioFile}")
            raise e
        drumStim.draw()
        win.flip()
        primeSound.play()
        print(f"  Prime playing ({primeDurationActual:.3f} s)...")
        logging.info(f"  Prime playing ({primeDurationActual:.3f} s)...")
        core.wait(primeDurationActual - 0.05)
        primeSound.stop()
        win.flip()
        core.wait(postPrimePause)

        for trialInBlock, currentSentence in enumerate(blockSentences):
            currentTrialInBlockNum = trialInBlock + 1
            trialCounter += 1
            print(f'        Trial {currentTrialInBlockNum}/{numSentencesPerBlock} (Overall: {trialCounter})')
            logging.info(f'        Trial {currentTrialInBlockNum}/{numSentencesPerBlock} (Overall: {trialCounter})')
            thisExp.addData('trial_num_overall', trialCounter)
            thisExp.addData('trial_in_block', currentTrialInBlockNum)
            thisExp.addData('prime_type_trial', currentPrimeType)
            
            sentenceFile = currentSentence['path']
            sentenceType = currentSentence['type']
            sentenceID = currentSentence['filename'] # This is already .lower()
            
            thisExp.addData('sentence_id', sentenceID)
            thisExp.addData('sentence_type', sentenceType)

            current_sentence_text = "TEXT NOT FOUND" 
            if active_sentence_text_map is not None:
                current_sentence_text = active_sentence_text_map.get(sentenceID, "TEXT NOT FOUND FOR ID") 
            
            if current_sentence_text == "TEXT NOT FOUND FOR ID":
                logging.warning(f"Sentence text not found for ID: {sentenceID} in chosen set {chosen_sentence_set}")
            thisExp.addData('sentence_text', current_sentence_text)
            
            print(f'          Sentence ({sentenceType}): {sentenceID}')
            logging.info(f'          Sentence ({sentenceType}): {sentenceID}')
            
            fixationCross.draw()
            win.flip()
            core.wait(fixationDuration)
            exclamStim.draw()
            win.flip()
            core.wait(exclamationDuration)
            print('          Playing sentence...')
            logging.info('          Playing sentence...')
            try:
                sentenceSound = sound.Sound(sentenceFile, stereo=True, hamming=True)
                sentenceDurationActual = sentenceSound.getDuration()
                if sentenceDurationActual is None or not isinstance(sentenceDurationActual, (int, float)) or sentenceDurationActual <= 0:
                    logging.warning(f"Could not get valid duration for sentence: {sentenceFile}. Using fallback 3.0s.")
                    sentenceDurationActual = 3.0
            except Exception as e:
                logging.error(f"Error loading sentence audio: {sentenceFile} - {e}")
                print(f"\nError loading sentence audio: {sentenceFile}")
                raise e
            sentenceSound.play()
            print(f"          Sentence playing ({sentenceDurationActual:.3f} s)...")
            logging.info(f"          Sentence playing ({sentenceDurationActual:.3f} s)...")
            core.wait(sentenceDurationActual)
            core.wait(postSentencePause)
            print('          Waiting for response...')
            logging.info('          Waiting for response...')
            correctDragonStim.draw()
            incorrectDragonStim.draw()
            rtClock.reset()
            event.clearEvents(eventType='keyboard')
            win.flip()
            responseScreenOnset_global = globalClock.getTime()
            response = event.waitKeys(keyList=allowedKeys, timeStamped=rtClock)
            responseKey = None
            rt = None
            responseDragon = 'NA'
            keyName, reactionTime = response[0]
            rt = reactionTime
            if keyName == escapeKey:
                logging.critical('Experiment aborted by user pressing ESCAPE.')
                print('\nExperiment aborted by user pressing ESCAPE.')
                raise KeyboardInterrupt("Experiment aborted by user via Escape key.")
            elif keyName == correctKey:
                responseKey = keyName
                responseDragon = 'correct'
            elif keyName == incorrectKey:
                responseKey = keyName
                responseDragon = 'incorrect'
            print(f'          Response: {responseDragon} ({responseKey}) | RT: {rt:.4f} s')
            logging.info(f'          Response: {responseDragon} ({responseKey}) | RT: {rt:.4f} s')
            response_accuracy_value = "incorrect"
            if (sentenceType == 'correct' and responseDragon == 'correct') or \
               (sentenceType == 'violation' and responseDragon == 'incorrect'):
                response_accuracy_value = "correct"
            thisExp.addData('response_key', responseKey)
            thisExp.addData('response_dragon', responseDragon)
            thisExp.addData('response_accuracy', response_accuracy_value)
            thisExp.addData('rt', rt)
            thisExp.addData('response_screen_onset_global_time', responseScreenOnset_global)
            thisExp.nextEntry()
            win.flip()
            core.wait(interTrialInterval)

        print(f'Block {currentBlockNum} finished.\n')
        logging.info(f'Block {currentBlockNum} finished.')

        if currentBlockNum < numBlocks:
            if currentBlockNum == 3:
                breakText = (
                    "End of Block 3.\n"
                    "You’re doing a GREAT job identifying the dragons!\n"
                    "There are 3 more Blocks until the end.\n"
                    "Take a short break and continue with the game\n\n"
                    "Press any key to start Block 4."
                )
            else:
                breakText = (f'End of Block {currentBlockNum}.\n\n'
                             f'Take a short break.\n\n'
                             f'Press any key to start Block {currentBlockNum + 1}.')
            blockBreakTextStim.text = breakText
            blockBreakTextStim.draw()
            win.flip()
            event.waitKeys()
            core.wait(0.5)

    print('Experiment Finished!')
    logging.info('Experiment Finished!')
    final_experiment_end_text = (
        "End of the Experiment\n\n"
        "You’ve finished the Dragon Game!\n"
        "Now it’s time to stretch, relax, and get ready for the next part.\n"
        "You’ve done an AMAZING job choosing the right dragons!\n\n"
        "Well Done!"
    )
    instructionTextStim.text = final_experiment_end_text
    instructionTextStim.draw()
    win.flip()
    core.wait(4.0)

except KeyboardInterrupt:
    print("Experiment aborted by user. Proceeding to cleanup.")
    logging.warning("Experiment aborted by user via Escape key.")
except Exception as e:
    print('\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print('!!!!!!!!!!!!! Experiment Error !!!!!!!!!!')
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    logging.error("An unexpected error occurred during the experiment:", exc_info=True)
    print(f"Error Type: {type(e).__name__}")
    print(f"Error message: {e}")
    print("\nTraceback:")
    traceback.print_exc()
    try:
        if 'win' in locals() and win is not None and not win.isClosed:
            errorText = f"An error occurred:\n{type(e).__name__}: {e}\n\nPlease notify the experimenter."
            instructionTextStim.text = errorText
            instructionTextStim.color = 'red'
            instructionTextStim.height = 24
            instructionTextStim.draw()
            win.flip()
            core.wait(5.0)
    except:
        print("Could not display error message in PsychoPy window (window might be closed or unusable).")
finally:
    print('Running cleanup and saving final data...')
    logging.info('Running cleanup and saving final data...')
    if 'win' in locals() and win is not None:
        win.close()
    try:
        if 'thisExp' in locals() and thisExp is not None and thisExp.entries:
            thisExp.saveAsWideText(outputFileName + '.csv', delim=',')
            thisExp.saveAsPickle(outputFileName + '.psydat')
            logging.info(f'Data saved to {outputFileName}.csv and {outputFileName}.psydat')
            print(f'Data saved to:\n  {outputFileName}.csv\n  {outputFileName}.psydat')
        elif 'thisExp' in locals() and thisExp is not None:
            logging.info("No data entries to save for thisExp.")
            print("No data entries to save.")
        else:
            logging.warning("ExperimentHandler object 'thisExp' not found or initialized. Skipping data saving.")
            print("WARNING: ExperimentHandler object 'thisExp' not found. Skipping data saving.")
    except Exception as saveError:
        logging.critical(f"CRITICAL ERROR: Failed to save data! - {saveError}")
        print(f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"!!! CRITICAL WARNING: Could not save final data !!!")
        print(f"!!! Error: {saveError}")
        print(f"!!! Data might be lost. Check logs and permissions.")
        print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
        traceback.print_exc()
    logging.flush()
    print('Cleanup complete. Exiting.')
    core.quit()