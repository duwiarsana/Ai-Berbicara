const recordBtn = document.getElementById('recordBtn');
const statusDiv = document.getElementById('status');
const audioReply = document.getElementById('audioReply');

let mediaRecorder;
let audioChunks = [];

recordBtn.addEventListener('mousedown', startRecording);
recordBtn.addEventListener('mouseup', stopRecording);
recordBtn.addEventListener('mouseleave', stopRecording);

function startRecording() {
  audioChunks = [];
  navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.start();
      statusDiv.textContent = 'Merekam... Lepas tombol untuk selesai.';
      mediaRecorder.ondataavailable = e => {
        audioChunks.push(e.data);
      };
      mediaRecorder.onstop = () => {
        stream.getTracks().forEach(track => track.stop());
        sendAudio();
      };
    })
    .catch(err => {
      statusDiv.textContent = 'Gagal mengakses mikrofon.';
    });
}

function stopRecording() {
  if (mediaRecorder && mediaRecorder.state === 'recording') {
    mediaRecorder.stop();
    statusDiv.textContent = 'Mengirim audio...';
  }
}

function sendAudio() {
  const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
  const formData = new FormData();
  formData.append('audio', audioBlob, 'recording.wav');

  statusDiv.textContent = 'Mengirim rekaman...';

  fetch('http://localhost:5050/api/voice', {
    method: 'POST',
    body: formData
  })
    .then(response => {
      if (!response.ok) {
        return response.json().then(data => {
          throw new Error(data.error || 'Network response was not ok');
        });
      }
      return response.blob();
    })
    .then(blob => {
      const audioUrl = URL.createObjectURL(blob);
      
      // Reset audio element
      audioReply.pause();
      audioReply.currentTime = 0;
      audioReply.src = audioUrl;
      
      // Show audio controls
      audioReply.classList.remove('hidden');
      
      // Play audio
      return audioReply.play()
        .then(() => {
          statusDiv.textContent = 'AI telah merespons. Memutar audio...';
        })
        .catch(error => {
          console.error('Error playing audio:', error);
          statusDiv.textContent = 'Audio siap. Klik play untuk mendengarkan.';
        });
    })
    .catch((error) => {
      console.error('Error:', error);
      statusDiv.textContent = 'Error: ' + error.message;
    });
}
