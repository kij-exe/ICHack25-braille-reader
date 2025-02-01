document.addEventListener("DOMContentLoaded", () => {
    setupStream();
});

function setupStream() {
    navigator.mediaDevices.getUserMedia({
    video : {
        facingMode : { exact : "environment" }
    }
}).then(stream => {
    const video = document.getElementById("video");
    video.srcObject = stream;
    video.play().then(() => {
        takePicture();
    });
}).catch(error => {
    console.error("Error accessing camera:", error);
    say("Please allow access to the camera, this is so that we can read what you are reading.");
});
}

function takePicture() {
    const video = document.getElementById("video");
    const canvas = document.createElement("canvas");
    canvas.setAttribute("display", "none");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    video.srcObject.getTracks().forEach(track => track.stop());
    const dataUrl = canvas.toDataURL("image/jpeg");
    processImage(dataUrl);
}

function processImage(dataUrl) {
    const postUrl = "";
    fetch(postUrl, {
        method : "POST",
        headers : {
            "Content-Type" : "application/json"
        },
        body : JSON.stringify({ image : dataUrl })
    }).then(response => response.json).then(text => {
        if (!("webkitSpeechRecognition" in window)) say("Sorry, your browser can't recognise speech so " +
            "I can't understand what you say. Please switch to a supported one, like Chrome.")
        else startLearning(text);
    });
}

let totalWords = 0;
let correctWords = 0;
let recognition;

async function say(text) {
    await Promise((resolve, reject) => {
        const saidText = SpeechSynthesisUtterance(text);
        saidText.lang = "en-GB";

        saidText.onend = () => {
            resolve();
        };

        saidText.onerror = (event) => {
            reject(event.error);
        };

        speechSynthesis.speak(saidText);
    });
}

async function startLearning(text) {
    const words = text.split(/[!"#$%&'()*+,\-./:;<=>?@[\\\]^_`{|}~\s]/).map(word => word.toLowerCase());
    totalWords = words.length;
    recognition = webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = "en-GB";
    await say("Welcome to the Braille learning service. This is how it will work - " +
        "you read a word, then I will tell you if it was correct or not. " +
        "We can do this until the end of the extract. After that, I will tell you how you did. " +
        "Now, have a go at the first word!");
    for (let word in words) await testWord(word);
    finishingStats();
}

async function testWord(word) {
    let guess = await hearNextWord();
    if (guess == word) {
        correctWords++;
        await say("Well done! That's the correct word.");
    } else {
        await say("Good try, but the correct word was", word);
    };
};

async function hearNextWord() {
    return Promise((resolve, reject) => {
        recognition.start();
        
        recognition.onresult = (event) => {
            recognition.stop();
            resolve(event.results[0][0].transcript.split(/[!"#$%&'()*+,\-./:;<=>?@[\\\]^_`{|}~\s]/)[0].toLowerCase());
        };

        recognition.onerror = (event) => {
            reject(event.error);
        };
    });
}

function finishingStats() { // more analysis, such as the commonly misread letters can be given here.
    say("Nicely done! Out of", totalWords, "you got", correctWords, "correct! See you next time!");
}