class AudioRecorder {
    constructor() {
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.stream = null;
        this.audioContext = null;
        this.inputPoint = null;
        this.processor = null;
        this.targetSampleRate = 16000; // Target sample rate for WAV and Whisper
        this.bufferSize = 4096; // Audio processing buffer size
    }

    async startRecording() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });

            // Use Web Audio API for granular control and WAV encoding
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            console.log('AudioContext sample rate:', this.audioContext.sampleRate);

            this.inputPoint = this.audioContext.createGain();
            const audioInput = this.audioContext.createMediaStreamSource(this.stream);
            audioInput.connect(this.inputPoint);

            this.processor = this.audioContext.createScriptProcessor(this.bufferSize, 1, 1);
            this.inputPoint.connect(this.processor);
            this.processor.connect(this.audioContext.destination);

            let recordingBuffer = [];
            let bufferStartTime = this.audioContext.currentTime;

            this.processor.onaudioprocess = (e) => {
                const inputBuffer = e.inputBuffer.getChannelData(0);
                recordingBuffer.push(new Float32Array(inputBuffer));

                const elapsed = this.audioContext.currentTime - bufferStartTime;

                if (elapsed >= 7) { // Send data every 7 seconds
                    let audioData = this.flattenBuffer(recordingBuffer);
                    
                    // Resample to targetSampleRate if necessary
                    if (this.audioContext.sampleRate !== this.targetSampleRate) {
                        console.log(`Resampling from ${this.audioContext.sampleRate} Hz to ${this.targetSampleRate} Hz`);
                        audioData = this.resample(audioData, this.audioContext.sampleRate, this.targetSampleRate);
                    }

                    const wavBlob = this.encodeWAV(audioData, this.targetSampleRate);
                    this.sendAudioChunk(wavBlob);
                    recordingBuffer = [];
                    bufferStartTime = this.audioContext.currentTime;
                }
            };

            this.isRecording = true;
            console.log('Recording started');
        } catch (error) {
            console.error('Error starting recording:', error);
            throw error;
        }
    }

    stopRecording() {
        if (this.isRecording) {
            if (this.stream) {
                this.stream.getTracks().forEach(track => track.stop());
            }
            if (this.processor) {
                this.processor.disconnect();
            }
            if (this.inputPoint) {
                this.inputPoint.disconnect();
            }
            if (this.audioContext) {
                this.audioContext.close();
            }
            this.isRecording = false;
            console.log('Recording stopped');
        }
    }

    async sendAudioChunk(audioBlob) {
        const formData = new FormData();
        formData.append('audio', audioBlob, 'audio.wav'); // Sending as WAV

        try {
            const response = await fetch('/process-audio', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                console.error('Backend error:', errorData);
                this.showError(errorData.error || 'Unknown error from backend');
                return;
            }

            const data = await response.json();
            console.log('Backend response:', data);
            this.updateUI(data);
        } catch (error) {
            console.error('Error sending audio chunk:', error);
            this.showError(error.message || 'Network error');
        }
    }

    updateUI(data) {
        // Update AI response
        const aiResponseElement = document.getElementById('ai-sidekick-text');
        if (aiResponseElement) {
            aiResponseElement.textContent = data.ai_response_sentence;
        }

        // Helper function to get current words from DOM
        const getCurrentWords = (elementId) => {
            const element = document.getElementById(elementId);
            if (!element) return [];
            return Array.from(element.children).map(wordDiv => wordDiv.textContent);
        };

        // Helper function to randomly select n items from array
        const randomSelect = (array, n) => {
            const shuffled = [...array].sort(() => 0.5 - Math.random());
            return shuffled.slice(0, n);
        };

        // Helper function to update word list with random replacement
        const updateWordListWithRandomReplacement = (elementId, newWords) => {
            const element = document.getElementById(elementId);
            if (!element) return;

            const currentWords = getCurrentWords(elementId);
            
            // If no current words, just display all new words
            if (currentWords.length === 0) {
                element.innerHTML = newWords.map(word => `<div class="word">${word}</div>`).join('');
                return;
            }

            // Randomly select 3 words to replace (or less if fewer words available)
            const replaceCount = Math.min(3, currentWords.length, newWords.length);
            const wordsToReplace = randomSelect(currentWords, replaceCount);
            const newWordsToAdd = randomSelect(newWords, replaceCount);

            // Create new word list
            let updatedWords = [...currentWords];
            
            // Replace selected words with new ones
            wordsToReplace.forEach((oldWord, index) => {
                const oldIndex = updatedWords.indexOf(oldWord);
                if (oldIndex !== -1 && newWordsToAdd[index]) {
                    updatedWords[oldIndex] = newWordsToAdd[index];
                }
            });

            // Update DOM
            element.innerHTML = updatedWords.map(word => `<div class="word">${word}</div>`).join('');
        };

        // Update each word list with random replacement
        updateWordListWithRandomReplacement('nouns-list', data.nouns);
        updateWordListWithRandomReplacement('adjectives-list', data.adjectives);
        updateWordListWithRandomReplacement('verbs-list', data.verbs);

        // Append transcription
        if (data.transcription) {
            const transcriptionElement = document.getElementById('transcription-text');
            if (transcriptionElement) {
                transcriptionElement.textContent += (transcriptionElement.textContent ? ' ' : '') + data.transcription;
            }
        }
    }

    showError(message) {
        let errorBox = document.getElementById('error-box');
        if (!errorBox) {
            errorBox = document.createElement('div');
            errorBox.id = 'error-box';
            errorBox.style.color = 'red';
            errorBox.style.margin = '1rem 0';
            errorBox.style.textAlign = 'center';
            document.body.prepend(errorBox);
        }
        errorBox.textContent = message;
    }

    // Helper to flatten the audio buffer
    flattenBuffer(channelBuffer) {
        let result = new Float32Array(this.countAudioSamples(channelBuffer));
        let offset = 0;
        for (let i = 0; i < channelBuffer.length; i++) {
            result.set(channelBuffer[i], offset);
            offset += channelBuffer[i].length;
        }
        return result;
    }

    countAudioSamples(buffer) {
        let count = 0;
        for (let i = 0; i < buffer.length; i++) {
            count += buffer[i].length;
        }
        return count;
    }

    // Basic audio resampling (downsampling for now)
    resample(audioBuffer, originalSampleRate, targetSampleRate) {
        if (originalSampleRate === targetSampleRate) {
            return audioBuffer; // No resampling needed
        }

        const ratio = originalSampleRate / targetSampleRate;
        const newLength = Math.round(audioBuffer.length / ratio);
        const resampledBuffer = new Float32Array(newLength);
        let offsetResult = 0;
        let offsetBuffer = 0;

        while (offsetResult < newLength) {
            const nextOffsetBuffer = Math.round((offsetResult + 1) * ratio);
            let accum = 0;
            let count = 0;
            for (let i = offsetBuffer; i < nextOffsetBuffer && i < audioBuffer.length; i++) {
                accum += audioBuffer[i];
                count++;
            }
            resampledBuffer[offsetResult] = accum / count; // Simple average
            offsetResult++;
            offsetBuffer = nextOffsetBuffer;
        }
        return resampledBuffer;
    }

    // WAV encoding logic (simplified for mono 16-bit PCM)
    encodeWAV(samples, sampleRate) {
        let buffer = new ArrayBuffer(44 + samples.length * 2); // 44 bytes for header + 2 bytes per sample
        let view = new DataView(buffer);

        // RIFF chunk descriptor
        this.writeString(view, 0, 'RIFF');
        view.setUint32(4, 36 + samples.length * 2, true);
        this.writeString(view, 8, 'WAVE');

        // FMT sub-chunk
        this.writeString(view, 12, 'fmt ');
        view.setUint32(16, 16, true);
        view.setUint16(20, 1, true); // PCM format
        view.setUint16(22, 1, true); // Mono
        view.setUint32(24, sampleRate, true);
        view.setUint32(28, sampleRate * 2, true); // Byte rate (SampleRate * NumChannels * BitsPerSample/8)
        view.setUint16(32, 2, true); // Block align (NumChannels * BitsPerSample/8)
        view.setUint16(34, 16, true); // Bits per sample

        // Data sub-chunk
        this.writeString(view, 36, 'data');
        view.setUint32(40, samples.length * 2, true);

        // Write samples
        this.floatTo16BitPCM(view, 44, samples);

        return new Blob([view], { type: 'audio/wav' });
    }

    writeString(view, offset, string) {
        for (let i = 0; i < string.length; i++) {
            view.setUint8(offset + i, string.charCodeAt(i));
        }
    }

    floatTo16BitPCM(output, offset, input) {
        for (let i = 0; i < input.length; i++, offset += 2) {
            let s = Math.max(-1, Math.min(1, input[i]));
            output.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
        }
    }
}

// Initialize recorder
const recorder = new AudioRecorder();

// Handle start/stop button
const startButton = document.getElementById('start-btn');
const statusText = document.getElementById('status-text');

if (startButton) {
    startButton.addEventListener('click', async () => {
        if (!recorder.isRecording) {
            try {
                // Clear transcription box
                const transcriptionElement = document.getElementById('transcription-text');
                if (transcriptionElement) {
                    transcriptionElement.textContent = '';
                }
                await recorder.startRecording();
                startButton.textContent = '⏹ Stop Practice';
                if (statusText) {
                    statusText.style.display = 'block';
                }
            } catch (error) {
                console.error('Failed to start recording:', error);
                recorder.showError('Failed to start recording: ' + error.message);
            }
        } else {
            recorder.stopRecording();
            startButton.textContent = '🎤 Start Practice';
            if (statusText) {
                statusText.style.display = 'none';
            }
        }
    });
} 