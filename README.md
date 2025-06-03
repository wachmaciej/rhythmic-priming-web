# Rhythmic Priming Experiment (Web Version)

A web-based version of the rhythmic priming experiment, optimized for iPad use.

## Setup

1. Host these files on a web server or GitHub Pages
2. Ensure all stimuli files are in the correct directories:
   ```
   stimuli/
   ├── audio/
   │   ├── regular.wav
   │   ├── irregular.wav
   │   ├── set a/
   │   │   ├── sent_corr_*.wav
   │   │   └── sent_viol_*.wav
   │   └── set b/
   │       ├── sent_corr_*.wav
   │       └── sent_viol_*.wav
   └── images/
       ├── drum.png
       ├── exclamation.png
       ├── dragon_correct.png
       └── dragon_incorrect.png
   ```

## Installation on iPad

1. Open Safari on your iPad
2. Visit the experiment URL
3. Tap the Share button
4. Select "Add to Home Screen"
5. Tap "Add"

## Usage

1. Launch the app from your iPad home screen
2. Enter participant information
3. Complete practice trials
4. Complete main experiment blocks
5. Data will be saved automatically

## Development

- `index.html` - Main experiment page
- `styles.css` - Styling and layout
- `app.js` - Core experiment logic
- `utils.js` - Helper functions
- `manifest.json` - PWA configuration
- `sw.js` - Service Worker for offline support 