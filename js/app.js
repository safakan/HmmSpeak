// Configurable content - easy to modify
const PRACTICE_CONTENT = {
    ai_sidekick_text: [
        "Try describing your favorite childhood memory in detail.",
    ],
    nouns: [
        "adventure", "opportunity", "challenge", "experience", "memory", "tradition", "culture"
    ],
    adjectives: [
        "fascinating", "incredible", "remarkable", "outstanding", "magnificent", "extraordinary", "brilliant"
    ],
    verbs: [
        "explore", "discover", "achieve", "create", "inspire", "motivate", "encourage"
    ]
};

let isListening = false;
let updateInterval;

document.addEventListener('DOMContentLoaded', () => {
    initializeContent();
});

function initializeContent() {
    // Initialize AI sidekick text
    const aiSidekickText = document.getElementById('ai-sidekick-text');
    aiSidekickText.textContent = PRACTICE_CONTENT.ai_sidekick_text[0];

    // Initialize vocabulary lists
    updateWordList('nouns-list', PRACTICE_CONTENT.nouns);
    updateWordList('adjectives-list', PRACTICE_CONTENT.adjectives);
    updateWordList('verbs-list', PRACTICE_CONTENT.verbs);
}

function showSection(section) {
    const practiceSection = document.getElementById('practice-section');
    const aboutSection = document.getElementById('about-section');
    const navButtons = document.querySelectorAll('.nav-btn');
    const aiSidekickBox = document.querySelector('.ai-sidekick-box');

    // Update navigation buttons
    navButtons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');

    if (section === 'practice') {
        practiceSection.classList.remove('hidden');
        aboutSection.classList.remove('active');
        // Scroll AI Sidekick box to a position with larger offset (e.g., 120px from top)
        const yOffset = -100; // increased offset for navbar height
        const y = aiSidekickBox.getBoundingClientRect().top + window.pageYOffset + yOffset;
        window.scrollTo({ top: y, behavior: 'smooth' });
    } else {
        practiceSection.classList.add('hidden');
        aboutSection.classList.add('active');
        aboutSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

function togglePractice() {
    const startBtn = document.getElementById('start-btn');
    const statusText = document.getElementById('status-text');

    isListening = !isListening;

    if (isListening) {
        startBtn.textContent = '🔴 Stop Practice';
        startBtn.className = 'start-btn stop';
        statusText.style.display = 'block';
        startContentUpdates();
    } else {
        startBtn.textContent = '🎤 Start Practice';
        startBtn.className = 'start-btn start';
        statusText.style.display = 'none';
        stopContentUpdates();
    }
}

function startContentUpdates() {
    updateInterval = setInterval(() => {
        updateSuggestion();
        updateVocabulary();
    }, 8000);
}

function stopContentUpdates() {
    if (updateInterval) {
        clearInterval(updateInterval);
    }
}

function updateSuggestion() {
    const suggestionText = document.getElementById('ai-sidekick-text');
    const randomSuggestion = PRACTICE_CONTENT.ai_sidekick_text[
        Math.floor(Math.random() * PRACTICE_CONTENT.ai_sidekick_text.length)
    ];
    suggestionText.textContent = randomSuggestion;
}

function updateVocabulary() {
    updateWordList('nouns-list', PRACTICE_CONTENT.nouns);
    updateWordList('adjectives-list', PRACTICE_CONTENT.adjectives);
    updateWordList('verbs-list', PRACTICE_CONTENT.verbs);
}

function updateWordList(listId, words) {
    const list = document.getElementById(listId);
    const shuffled = [...words].sort(() => Math.random() - 0.5);
    const selected = shuffled.slice(0, 6);
    
    list.innerHTML = selected.map(word => 
        `<div class="vocab-word">${word}</div>`
    ).join('');
}

function shuffleArray(array) {
    return [...array].sort(() => Math.random() - 0.5);
} 