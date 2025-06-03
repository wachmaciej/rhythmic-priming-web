import { config, state, loadAudio } from './app.js';

// Participant Info Dialog
export function getParticipantInfo() {
    return new Promise((resolve) => {
        const dialog = document.createElement('div');
        dialog.className = 'participant-dialog';
        dialog.innerHTML = `
            <form id="participant-form">
                <div class="form-group">
                    <label for="participantId">Participant ID:</label>
                    <input type="text" id="participantId" required pattern="P[0-9]{2}" placeholder="P01">
                </div>
                <div class="form-group">
                    <label for="sessionNumber">Session Number:</label>
                    <input type="number" id="sessionNumber" required min="1" value="1">
                </div>
                <div class="form-group">
                    <label for="sentenceSet">Sentence Set:</label>
                    <select id="sentenceSet" required>
                        <option value="A">Set A</option>
                        <option value="B">Set B</option>
                    </select>
                </div>
                <button type="submit" class="response-button">Start</button>
            </form>
        `;

        const stimulusDisplay = document.getElementById('stimulus-display');
        stimulusDisplay.appendChild(dialog);

        const form = document.getElementById('participant-form');
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const info = {
                participantId: document.getElementById('participantId').value,
                sessionNumber: document.getElementById('sessionNumber').value,
                sentenceSet: document.getElementById('sentenceSet').value
            };
            dialog.remove();
            resolve(info);
        });
    });
}

// Load Stimuli
export async function loadStimuli() {
    const audioFiles = {
        primes: {
            regular: 'stimuli/audio/regular.wav',
            irregular: 'stimuli/audio/irregular.wav'
        },
        practice: {
            A: {
                correct: [
                    'stimuli/audio/practice/practice a/test_a_sent_corr_01.wav',
                    'stimuli/audio/practice/practice a/test_a_sent_corr_02.wav'
                ],
                violation: [
                    'stimuli/audio/practice/practice a/test_a_sent_viol_01.wav',
                    'stimuli/audio/practice/practice a/test_a_sent_viol_02.wav'
                ]
            },
            B: {
                correct: [
                    'stimuli/audio/practice/practice b/test_b_sent_corr_01.wav',
                    'stimuli/audio/practice/practice b/test_b_sent_corr_02.wav'
                ],
                violation: [
                    'stimuli/audio/practice/practice b/test_b_sent_viol_01.wav',
                    'stimuli/audio/practice/practice b/test_b_sent_viol_02.wav'
                ]
            }
        }
    };

    // Preload all audio files
    const loadPromises = [];
    
    // Load primes
    for (const prime of Object.values(audioFiles.primes)) {
        loadPromises.push(loadAudio(prime));
    }

    // Load practice files for both sets
    for (const set of ['A', 'B']) {
        for (const type of ['correct', 'violation']) {
            for (const file of audioFiles.practice[set][type]) {
                loadPromises.push(loadAudio(file));
            }
        }
    }

    // Wait for all files to load
    await Promise.all(loadPromises);
}

// Generate Block Trials
export function generateBlockTrials() {
    const trials = [];
    const primeTypes = ['regular', 'irregular'];
    
    // Create correct trials
    for (let i = 0; i < config.numCorrectPerBlock; i++) {
        trials.push({
            primeType: primeTypes[Math.floor(Math.random() * 2)],
            isCorrect: true,
            sentenceFile: `sent_corr_${String(i + 1).padStart(2, '0')}.wav`
        });
    }

    // Create violation trials
    for (let i = 0; i < config.numViolationPerBlock; i++) {
        trials.push({
            primeType: primeTypes[Math.floor(Math.random() * 2)],
            isCorrect: false,
            sentenceFile: `sent_viol_${String(i + 1).padStart(2, '0')}.wav`
        });
    }

    // Shuffle trials
    return shuffleArray(trials);
}

// Run Practice Trials
export async function runPracticeTrials() {
    const practiceTrials = [
        {
            primeType: 'regular',
            isCorrect: true,
            sentenceFile: `test_${state.sentenceSet.toLowerCase()}_sent_corr_01.wav`,
            feedback: "This sentence sounded right so it was the HAPPY dragon who said it."
        },
        {
            primeType: 'irregular',
            isCorrect: false,
            sentenceFile: `test_${state.sentenceSet.toLowerCase()}_sent_viol_01.wav`,
            feedback: "This sentence didn't sound quite right so it was the CONFUSED dragon who said it."
        }
    ];

    for (const trial of practiceTrials) {
        await runPracticeTrial(trial);
    }
}

// Run Practice Trial
export async function runPracticeTrial(trialData) {
    await runTrial(trialData);
    
    // Show detailed feedback
    const feedbackArea = document.getElementById('feedback-area');
    feedbackArea.textContent = trialData.feedback;
    await new Promise(resolve => setTimeout(resolve, 3000));
    feedbackArea.textContent = '';
}

// Save Data
export async function saveData() {
    const filename = `${state.participantId}_session${state.sessionNumber}_set${state.sentenceSet}_${getTimestamp()}.json`;
    const dataStr = JSON.stringify(state.data, null, 2);
    
    // Create blob and download
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Show Block Break
export async function showBlockBreak() {
    if (state.currentBlock < config.numBlocks - 1) {
        const breakScreen = document.createElement('div');
        breakScreen.className = 'break-screen';
        breakScreen.innerHTML = `
            <h2>Break Time!</h2>
            <p>You've completed block ${state.currentBlock + 1} of ${config.numBlocks}.</p>
            <p>Take a short break if you need one.</p>
            <button class="response-button">Continue</button>
        `;

        const stimulusDisplay = document.getElementById('stimulus-display');
        stimulusDisplay.appendChild(breakScreen);

        await new Promise(resolve => {
            breakScreen.querySelector('button').addEventListener('click', () => {
                breakScreen.remove();
                resolve();
            });
        });
    }
}

// Show Completion Screen
export function showCompletionScreen() {
    const completionScreen = document.createElement('div');
    completionScreen.className = 'completion-screen';
    completionScreen.innerHTML = `
        <h2>Experiment Complete!</h2>
        <p>Thank you for participating!</p>
        <p>Your data has been saved.</p>
    `;

    const stimulusDisplay = document.getElementById('stimulus-display');
    stimulusDisplay.innerHTML = '';
    stimulusDisplay.appendChild(completionScreen);
}

// Show Error Screen
export function showErrorScreen(error) {
    const errorScreen = document.createElement('div');
    errorScreen.className = 'error-screen';
    errorScreen.innerHTML = `
        <h2>An Error Occurred</h2>
        <p>Please contact the experimenter.</p>
        <p class="error-details">${error.message}</p>
    `;

    const stimulusDisplay = document.getElementById('stimulus-display');
    stimulusDisplay.innerHTML = '';
    stimulusDisplay.appendChild(errorScreen);
}

// Utility Functions
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

function getTimestamp() {
    const now = new Date();
    return now.toISOString().replace(/[:.]/g, '-').slice(0, -5);
}

// Export functions
export {
    getParticipantInfo,
    loadStimuli,
    generateBlockTrials,
    runPracticeTrials,
    saveData,
    showBlockBreak,
    showCompletionScreen,
    showErrorScreen
}; 