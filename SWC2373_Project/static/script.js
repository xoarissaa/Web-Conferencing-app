// Camera functionality
const cameraButton = document.getElementById('camera-button');
const localVideo = document.getElementById('local-video');

cameraButton.addEventListener('click', async () => {
    if (cameraButton.textContent === 'Turn on Camera') {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            localVideo.srcObject = stream;
            localVideo.play();
            cameraButton.textContent = 'Turn off Camera';
        } catch (error) {
            alert('Unable to access the camera.');
        }
    } else {
        const tracks = localVideo.srcObject.getTracks();
        tracks.forEach((track) => track.stop());
        localVideo.srcObject = null;
        cameraButton.textContent = 'Turn on Camera';
    }
});

// Microphone functionality
const micButton = document.getElementById('mic-button');
let micStream = null;

micButton.addEventListener('click', async () => {
    if (micButton.textContent === 'Turn on Mic') {
        try {
            micStream = await navigator.mediaDevices.getUserMedia({ audio: true });
            micButton.textContent = 'Turn off Mic';
        } catch (error) {
            alert('Unable to access the microphone.');
        }
    } else {
        if (micStream) {
            const tracks = micStream.getTracks();
            tracks.forEach((track) => track.stop());
        }
        micButton.textContent = 'Turn on Mic';
    }
});

// Screen Sharing
document.getElementById('share-screen-button').addEventListener('click', async () => {
    try {
        const screenStream = await navigator.mediaDevices.getDisplayMedia({
            video: true
        });
        document.getElementById('local-video').srcObject = screenStream;
        alert('Screen sharing started!');
    } catch (error) {
        alert('Unable to share the screen.');
        console.error(error);
    }
});

// Chat functionality
const chatForm = document.getElementById('chat-form');
const messagesContainer = document.getElementById('messages');

chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const messageInput = document.getElementById('chat-input');
    const message = messageInput.value.trim();
    if (message) {
        const messageElement = document.createElement('li');
        messageElement.textContent = `You: ${message}`;
        messagesContainer.appendChild(messageElement);
        messageInput.value = ''; // Clear input
    }
});

// Leave meeting functionality
const leaveButton = document.getElementById('leave-meeting-button');
leaveButton.addEventListener('click', () => {
    if (confirm('Are you sure you want to leave the meeting?')) {
        window.location.href = '/dashboard';
    }
});

// Adding new participants to the list
const participantsList = document.getElementById('participants-list');

function addParticipant(fullName) {
    const participant = document.createElement('li');
    participant.textContent = fullName;
    participantsList.appendChild(participant);
}

function loadParticipants(room_id) {
    fetch('/static/meetings.json')
        .then((response) => response.json())
        .then((meetings) => {
            // Find the current meeting by room_id
            const meeting = meetings.find((m) => m.room_id === room_id);
            const participantsList = document.getElementById("participants-list");

            if (meeting && meeting.participants) {
                participantsList.innerHTML = ""; // Clear the list
                
                // Add participants dynamically
                meeting.participants.forEach((participant) => {
                    const listItem = document.createElement("li");
                    listItem.textContent = `${participant.name} (${participant.email})`;
                    participantsList.appendChild(listItem);
                });
            }
        })
        .catch((error) => console.error("Error loading participants:", error));
}

// Call the function with the room_id from the template
const roomId = "{{ room_id }}";
loadParticipants(roomId);


document.getElementById('turn-on-camera').addEventListener('click', function () {
    const video = document.createElement('video');
    video.setAttribute('autoplay', true);
    video.setAttribute('muted', true); // Avoid feedback noise

    navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((stream) => {
            video.srcObject = stream;
            document.getElementById('video-area').appendChild(video);
        })
        .catch((error) => {
            console.error('Error accessing the camera:', error);
            alert('Unable to access the camera. Please check permissions or try again.');
        });
});

