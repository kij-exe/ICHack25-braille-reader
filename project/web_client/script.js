let cameraLoaded = false;
let recognition;

document.addEventListener("DOMContentLoaded", async () => {
    setupStream();
    await say("When ready, say capture to take a photo or say upload to upload a photo of your Braille.");
    setupMicrophone();
});

function setupMicrophone() {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = "en-GB";

    let capturePhrases = ["take", "capture", "image", "snap", "photo", "photograph", "pic", "picture", "ready"];
    let uploadPhrases = ["upload", "attach", "file", "attachment", "send", "post", "put"];

    recognition.start();
        
    recognition.onresult = (event) => {
        recognition.stop();
        let words = [];
        try {
            words = event.results[0][0].transcript.split(/[!"#$%&'()*+,\-./:;<=>?@[\\\]^_`{|}~\s]/);
        } catch (event) {
            console.error(event.error);
        };
        if (words.some(item => capturePhrases.includes(item.toLowerCase()))) {
            if (cameraLoaded) takePicture(); // listen again if camera has not loaded
        } else if (words.some(item => uploadPhrases.includes(item.toLowerCase()))) {
            // this actually does not work due to browser security disallowing the
            // file prompt from showing unless the user themself clicks on something to do this.
            // it is a good security feature but unfortunately disadvantages less-abled people
            // such as the blind - who should also be considered before rolling out features like this.
            uploadImage();
        } else {
            try {
                recognition.start(); // console error says recognition has already started,
                // but it has not - rerecognition only works if this line is left in.
            } catch (_) {}; // stop crashing.
        };
    };
};

function setupStream() {
    navigator.mediaDevices.getUserMedia({
        video : {
            facingMode : { exact : "environment" }
        }
    }).then(stream => {
        const video = document.getElementById("video");
        video.srcObject = stream;
        video.play().then(() => {
            cameraLoaded = true;
        });
    }).catch(error => {
        console.error("Error accessing camera:", error);
        say("Please allow access to the camera, this is so that we can read what you are reading.");
    });
};

function takePicture() {
    if (cameraLoaded) {
        const video = document.getElementById("video");
        video.style.display = "none";
        const buttons = document.getElementsByClassName("button");
        [...buttons].forEach(button => {
            button.style.display = "none";
        });
        const canvas = document.createElement("canvas");
        canvas.style.display = "none";
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const context = canvas.getContext("2d");
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        video.srcObject.getTracks().forEach(track => track.stop());
        const dataUrl = canvas.toDataURL("image/jpeg");
        processImage(dataUrl);
    };
};

function uploadImage() {
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = "image/*";
    fileInput.style.display = "none";

    fileInput.addEventListener("change", (event) => {
        const file = event.target.files[0];
        const reader = new FileReader();
        reader.onload = (e) => {
            const dataUrl = e.target.result;
            const video = document.getElementById("video");
            video.style.display = "none";
            const buttons = document.getElementsByClassName("button");
            [...buttons].forEach(button => {
                button.style.display = "none";
            });
            processImage(dataUrl);
        };
        reader.readAsDataURL(file);
        reader.onerror = (e) => {
            console.error("Error uploading file", e);
            recognition.start();
        };
    });

    fileInput.click();
};

function processImage(dataUrl) {
    const postUrl = "http://172.30.170.92:8000/braille-reader/image-to-english/";
    // Convert Base64 string to binary data
    const byteCharacters = atob(dataUrl.split(',')[1]);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    fetch(postUrl, {
        method : "POST",
        headers : {
            "Content-Type" : "image/jpeg",
        },
        body : byteArray
    }).then(response => response.json()).then(data => {
        if (!("webkitSpeechRecognition" in window)) {say("Sorry, your browser can't recognise speech so " +
            "I can't understand what you say. Please switch to a supported one, like Chrome.");}
        else {startLearning(data["text"]);}
     });
};

let totalWords = 0;
let correctWords = 0;

async function say(text) {
    await new Promise((resolve, reject) => {
        const saidText = new SpeechSynthesisUtterance(text);
        saidText.lang = "en-GB";

        saidText.onend = () => {
            resolve();
        };

        saidText.onerror = (event) => {
            reject(event.error);
        };

        speechSynthesis.speak(saidText);
    });
};

async function startLearning(text) {
    const words = text.split(/[!"#$%&()*+,\./:;<=>?@[\\\]^_`{|}~\s]/).map(word => word.toLowerCase());
    totalWords = words.length;
    await say("Welcome to the Braille learning service. This is how it will work - " +
        "you read a word, then I will tell you if it was correct or not. " +
        "We can do this until the end of the extract. After that, I will tell you how you did. " +
        "Now, have a go at the first word!");
        const userSaid = document.getElementById("userSaid");
        const computerSaid = document.getElementById("computerSaid");
        userSaid.style.display = "block";
        computerSaid.style.display = "block";
    for (let index in words) await testWord(words[index]);
    finishingStats(words);
};

function playBeep() {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    oscillator.type = "sine";
    oscillator.frequency.setValueAtTime(1000, audioContext.currentTime);
    oscillator.connect(audioContext.destination);
    oscillator.start();
    oscillator.stop(audioContext.currentTime + 0.2);
};

async function testWord(word) {
    playBeep();
    let guess = await hearNextWord();
    const userSaid = document.getElementById("userSaid");
    const computerSaid = document.getElementById("computerSaid");
    if (guess == word) {
        userSaid.textContent = "Correct!";
        userSaid.style.color = "green";
        computerSaid.textContent = word;
        correctWords++;
        await say("Well done! That's the correct word.");
    } else {
        userSaid.textContent = "Incorrect! You said " + guess;
        userSaid.style.color = "red";
        computerSaid.textContent = "The correct word was " + word;
        await say("Good try, but the correct word was " + word);
    };
};

async function hearNextWord() {
    return new Promise((resolve, reject) => {
        try {
            recognition.start();
        } catch (e) {
            // ignore failure and allow app to continue
        };
        
        recognition.onresult = (event) => {
            recognition.stop();
            try {
                let words = event.results[0][0].transcript.split(/[!"#$%&()*+,\./:;<=>?@[\\\]^_`{|}~\s]/);
                resolve(words[0].toLowerCase());
            } catch (event) {
                reject(event.error); // probably empty speech
            };
        };

        recognition.onerror = (event) => {
            reject(event.error);
        };
    });
};

function finishingStats(words) { // more analysis, such as the commonly misread letters can be given here.
    say("Nicely done! Out of " + totalWords + " you got " + correctWords + " correct! See you next time!");
    const wordsElem = document.getElementById("answers");
    wordsElem.textContent = words.join(" ");
    wordsElem.style.display = "block";
    const scoreElem = document.getElementById("score");
    scoreElem.textContent = "You got " + correctWords + " words correct out of " +
    totalWords + " words! Well done! Keep up the practise.";
    scoreElem.style.display = "block";
};