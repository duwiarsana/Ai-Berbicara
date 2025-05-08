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
  
  // Selalu gunakan model Gemma
  formData.append('model_type', 'gemma');
  
  statusDiv.textContent = `Mengirim rekaman ke Gemma...`;

  fetch('/api/voice', {
    method: 'POST',
    body: formData
  })
    .then(res => res.blob())
    .then(blob => {
      audioReply.src = URL.createObjectURL(blob);
      audioReply.classList.remove('hidden');
      audioReply.play();
      statusDiv.textContent = 'AI menjawab dengan suara.';
    })
    .catch(() => {
      statusDiv.textContent = 'Gagal mendapatkan respon dari AI.';
    });
}
