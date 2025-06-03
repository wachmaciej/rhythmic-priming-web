// Experiment Configuration
export const config = {
    fixationDuration: 500,
    postPrimePause: 500,
    exclamationDuration: 500,
    postSentencePause: 200,
    responseTimeLimit: 7000,
    interTrialInterval: 1000,
    feedbackDuration: 750,
    numBlocks: 6,
    numSentencesPerBlock: 6,
    numCorrectPerBlock: 3,
    numViolationPerBlock: 3
};

// Experiment State
export const state = {
    participantId: '',
    sessionNumber: '',
    sentenceSet: '',
    currentBlock: 0,
    currentTrial: 0,
    data: [],
    audioContext: null,
    audioBuffers: new Map(),
    isRunning: false
};

// DOM Elements
const stimulusDisplay = document.getElementById('stimulus-display');
const responseArea = document.getElementById('response-area');
const feedbackArea = document.getElementById('feedback-area');

// Initialize Audio Context
export async function initAudioContext() {
    state.audioContext = new (window.AudioContext || window.webkitAudioContext)();
}

// Load Audio File
export async function loadAudio(url) {
    if (state.audioBuffers.has(url)) {
        return state.audioBuffers.get(url);
    }

    const response = await fetch(url);
    const arrayBuffer = await response.arrayBuffer();
    const audioBuffer = await state.audioContext.decodeAudioData(arrayBuffer);
    state.audioBuffers.set(url, audioBuffer);
    return audioBuffer;
}

// Play Audio
export async function playAudio(buffer) {
    const source = state.audioContext.createBufferSource();
    source.buffer = buffer;
    source.connect(state.audioContext.destination);
    source.start(0);
    return new Promise(resolve => {
        source.onended = resolve;
    });
}

// Show Fixation Cross
export function showFixation() {
    stimulusDisplay.innerHTML = '<div class="fixation">+</div>';
    return new Promise(resolve => setTimeout(resolve, config.fixationDuration));
}

// Show Image
export function showImage(imagePath) {
    return new Promise((resolve) => {
        const img = new Image();
        img.src = imagePath;
        img.className = 'stimulus-image';
        img.onload = () => {
            stimulusDisplay.innerHTML = '';
            stimulusDisplay.appendChild(img);
            resolve();
        };
    });
}

// Get Response
export function getResponse() {
    return new Promise((resolve) => {
        const happyButton = document.createElement('button');
        const confusedButton = document.createElement('button');
        
        happyButton.className = 'response-button';
        confusedButton.className = 'response-button';
        
        happyButton.textContent = 'Happy Dragon';
        confusedButton.textContent = 'Confused Dragon';
        
        responseArea.innerHTML = '';
        responseArea.appendChild(happyButton);
        responseArea.appendChild(confusedButton);

        const timeoutId = setTimeout(() => {
            resolve({ response: null, rt: null });
        }, config.responseTimeLimit);

        const startTime = performance.now();

        const handleResponse = (response) => {
            clearTimeout(timeoutId);
            const rt = performance.now() - startTime;
            responseArea.innerHTML = '';
            resolve({ response, rt });
        };

        happyButton.addEventListener('click', () => handleResponse('happy'));
        confusedButton.addEventListener('click', () => handleResponse('confused'));
    });
}

// Show Feedback
export function showFeedback(isCorrect) {
    const feedbackImage = isCorrect ? 'dragon_correct.png' : 'dragon_incorrect.png';
    return showImage(feedbackImage);
}

// Run Trial
export async function runTrial(trialData) {
    // Show fixation cross
    await showFixation();

    // Play prime
    const primeBuffer = await loadAudio(trialData.primeAudio);
    await playAudio(primeBuffer);
    await new Promise(resolve => setTimeout(resolve, config.postPrimePause));

    // Show exclamation mark
    await showImage('exclamation.png');
    await new Promise(resolve => setTimeout(resolve, config.exclamationDuration));

    // Play sentence
    const sentenceBuffer = await loadAudio(trialData.sentenceAudio);
    await playAudio(sentenceBuffer);
    await new Promise(resolve => setTimeout(resolve, config.postSentencePause));

    // Get response
    const { response, rt } = await getResponse();

    // Show feedback
    const isCorrect = (response === 'happy' && trialData.isCorrect) || 
                     (response === 'confused' && !trialData.isCorrect);
    await showFeedback(isCorrect);

    // Save data
    state.data.push({
        block: state.currentBlock,
        trial: state.currentTrial,
        prime: trialData.primeType,
        sentence: trialData.sentenceFile,
        isCorrect: trialData.isCorrect,
        response: response,
        rt: rt,
        accuracy: isCorrect ? 1 : 0
    });

    // Inter-trial interval
    await new Promise(resolve => setTimeout(resolve, config.interTrialInterval));
}

// Start Experiment
export async function startExperiment() {
    try {
        await initAudioContext();
        
        // Get participant info
        const info = await getParticipantInfo();
        state.participantId = info.participantId;
        state.sessionNumber = info.sessionNumber;
        state.sentenceSet = info.sentenceSet;

        // Load stimuli
        await loadStimuli();

        // Run practice trials
        await runPracticeTrials();

        // Run main experiment
        for (state.currentBlock = 0; state.currentBlock < config.numBlocks; state.currentBlock++) {
            const blockTrials = generateBlockTrials();
            for (state.currentTrial = 0; state.currentTrial < blockTrials.length; state.currentTrial++) {
                await runTrial(blockTrials[state.currentTrial]);
            }
            await showBlockBreak();
        }

        // Save data
        await saveData();

        // Show completion screen
        showCompletionScreen();

    } catch (error) {
        console.error('Experiment error:', error);
        showErrorScreen(error);
    }
}

// Initialize experiment when page loads
document.addEventListener('DOMContentLoaded', () => {
    const startButton = document.createElement('button');
    startButton.textContent = 'Start Experiment';
    startButton.className = 'response-button';
    startButton.addEventListener('click', startExperiment);
    
    stimulusDisplay.appendChild(startButton);
}); 