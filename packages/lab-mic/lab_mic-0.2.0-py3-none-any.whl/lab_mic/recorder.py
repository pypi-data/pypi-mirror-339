import base64
import io
import time
import traceback

import ffmpeg
import ipywidgets as widgets
import numpy as np
from IPython.display import display, HTML, Audio
from scipy.io import wavfile
from scipy.signal import resample_poly

AUDIO_HTML_TEMPLATE = """
<div id="audio-interface-{unique_id}">
    <p>Recording Interface:</p>
    <button id="recordButton-{unique_id}">Press to Start Recording</button>
    <p id="status-{unique_id}">Status: Idle</p>
    <div id="preview-{unique_id}"></div>
</div>
<script>
(function() {{
    const unique_id = "{unique_id}";
    const recordButton = document.getElementById('recordButton-' + unique_id);
    const statusDisplay = document.getElementById('status-' + unique_id);
    const previewContainer = document.getElementById('preview-' + unique_id);
    // 尋找 <input> 元素
    const targetInputSelector = ".{css_class_receiver} input";

    var recorder, gumStream;
    var base64data = "";
    var isStopping = false;

    function resetUIOnError(errorMessage) {{
       statusDisplay.textContent = "Status: Error - " + errorMessage;
       recordButton.textContent = "Recording Failed - Retry?";
       recordButton.disabled = false;
       isStopping = false;
       if (gumStream) {{
           try {{
               gumStream.getAudioTracks().forEach(track => track.stop());
           }} catch (e) {{ console.error("Error stopping tracks during reset:", e); }}
       }}
       recorder = null;
    }}

    function handleSuccess(stream) {{
        gumStream = stream;
        const options = {{ mimeType: 'audio/webm;codecs=opus' }};
        try {{
           recorder = new MediaRecorder(stream, options);
        }} catch (e) {{
           try {{
              recorder = new MediaRecorder(stream);
           }} catch (e2) {{
              resetUIOnError("MediaRecorder creation failed.");
              return;
           }}
        }}

        statusDisplay.textContent = "Status: Recording... Press button again to stop.";
        recordButton.textContent = "Stop Recording";
        recordButton.disabled = false;
        isStopping = false;

        recorder.ondataavailable = function(e) {{
            if (e.data.size > 0) {{
                var url = URL.createObjectURL(e.data);
                var preview = document.createElement('audio');
                preview.controls = true;
                preview.src = url;
                previewContainer.innerHTML = '';
                previewContainer.appendChild(preview);

                var reader = new FileReader();
                reader.onerror = function(event) {{
                   base64data = "FILE_READER_ERROR";
                }};
                reader.onloadend = function() {{
                    if (base64data !== "FILE_READER_ERROR") {{
                       base64data = reader.result;
                       // 資料完整後呼叫 sendDataToPython
                       sendDataToPython(base64data);
                    }}
                }};
                reader.readAsDataURL(e.data);
            }}
        }};

        recorder.onstop = function() {{
           isStopping = false;
           try {{
               if (gumStream) {{
                   gumStream.getAudioTracks().forEach(track => {{
                      track.stop();
                   }});
               }}
           }} catch(e) {{
              resetUIOnError("Processing failed after stop.");
           }} finally {{
                 recordButton.disabled = false;
                 recordButton.textContent = "Retry Recording";
           }}
        }};

        recorder.onerror = function(event) {{
           resetUIOnError("Recorder Error: " + event.error.name);
        }};

        try {{
           recorder.start();
        }} catch (e) {{
           resetUIOnError("Failed to start recorder.");
        }}
    }}

    function sendDataToPython(b64Data) {{
       if (!b64Data || typeof b64Data !== 'string' || !b64Data.startsWith('data:')) {{
           resetUIOnError("Invalid data captured.");
           return;
       }}
       const targetInput = document.querySelector(targetInputSelector);
       if (targetInput) {{
           try {{
               targetInput.value = b64Data;
               targetInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
               targetInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
               statusDisplay.textContent = "Status: Audio sent to Python for processing.";
               recordButton.textContent = "Processing in Python...";
               recordButton.disabled = true;
           }} catch(e) {{
               resetUIOnError("Failed to send data to Python.");
           }}
       }} else {{
           resetUIOnError("Could not communicate with Python backend.");
       }}
    }}

    function toggleRecording() {{
        if (isStopping) {{
            return;
        }}

        if (recorder && recorder.state === "recording") {{
            isStopping = true;
            statusDisplay.textContent = "Status: Stopping recording...";
            recordButton.textContent = "Stopping...";
            recordButton.disabled = true;
            try {{
                recorder.stop();
            }} catch(e) {{
                resetUIOnError("Failed to execute stop command.");
            }}
        }} else {{
            statusDisplay.textContent = "Status: Requesting microphone...";
            recordButton.textContent = "Requesting Mic...";
            recordButton.disabled = true;
            previewContainer.innerHTML = '';
            base64data = "";
            navigator.mediaDevices.getUserMedia({{ audio: true }})
                .then(handleSuccess)
                .catch(function(err) {{
                    resetUIOnError("Microphone Error: " + err.name);
               }});
        }}
    }}

    recordButton.onclick = toggleRecording;
}})(); // End isolated scope
</script>
"""


class LabMic:
    def __init__(self, sampling_rate=16000, frame_duration_ms=30):
        self.sampling_rate = sampling_rate
        self.frame_duration_ms = frame_duration_ms
        self.frame_size = int(self.sampling_rate * (self.frame_duration_ms / 1000.0))
        self.bytes_per_sample = 2
        self.bytes_per_frame = self.frame_size * self.bytes_per_sample

        self.unique_id = f"audio-receiver-{int(time.time())}"
        self.receiver_css_class = f"audio-data-receiver-{self.unique_id}"

        self.recording_result = None
        self.audio_bytes_io = io.BytesIO()

        self.data_receiver = widgets.Text(
            value='',
            description='',
            disabled=False,
            layout=widgets.Layout(display='none'),
            style={'description_width': '0px'}
        )
        self.data_receiver.add_class(self.receiver_css_class)

        self.output_widget = widgets.Output()
        self.start_button = widgets.Button(
            description="Load Recording Interface",
            button_style='success',
            icon='microphone'
        )
        self.start_button.on_click(self.load_recorder_interface)
        self.data_receiver.observe(self._handle_received_data, names='value')

    def load_recorder_interface(self, b=None):
        with self.output_widget:
            self.output_widget.clear_output(wait=True)
            html_content = AUDIO_HTML_TEMPLATE.format(
                unique_id=self.unique_id,
                css_class_receiver=self.receiver_css_class
            )
            display(HTML(html_content))
        print(
            f"Recording interface loaded. Use controls above. Data will be sent to widget with class '{self.receiver_css_class}'.")

    def display(self):
        display(self.start_button)
        display(self.output_widget)
        display(self.data_receiver)

    def _handle_received_data(self, change):
        print("Observer triggered: Received data from JavaScript.")
        base64_data_url = change['new']
        if not base64_data_url or not base64_data_url.startswith('data:audio'):
            print("No valid audio data received or already processed.")
            return

        try:
            header, encoded = base64_data_url.split(',', 1)
            audio_binary = base64.b64decode(encoded)
            print(f"Decoded {len(audio_binary)} bytes. Header: {header}")

            mime_type = header.split(':')[1].split(';')[0]
            input_format = mime_type.split('/')[1]
            print(f"Detected input format: {input_format}")

            print("Converting audio using ffmpeg...")
            process = (ffmpeg
                       .input('pipe:0', f=input_format)
                       .output('pipe:1', format='wav', acodec='pcm_s16le', ac=1, ar=self.sampling_rate)
                       .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True, overwrite_output=True))
            output_bytes, err_bytes = process.communicate(input=audio_binary)
            if err_bytes:
                print("FFmpeg Warning/Error:", err_bytes.decode())
            if not output_bytes:
                raise ValueError("FFmpeg produced no output. Conversion failed.")

            wav_data = bytearray(output_bytes)
            riff_size = len(wav_data) - 8
            wav_data[4:8] = riff_size.to_bytes(4, byteorder='little')
            print(f"Repaired RIFF header with size: {riff_size}")

            original_sr, audio_data = wavfile.read(io.BytesIO(wav_data))
            print(
                f"FFmpeg conversion successful. Original SR: {original_sr} Hz, Shape: {audio_data.shape}, Dtype: {audio_data.dtype}")

            if audio_data.ndim > 1 and audio_data.shape[1] > 1:
                print("Converting stereo to mono...")
                axis_to_average = 1 if audio_data.shape[1] < audio_data.shape[0] else 0
                audio_data = audio_data.mean(axis=axis_to_average).astype(audio_data.dtype)

            if original_sr != self.sampling_rate:
                print(f"Resampling from {original_sr} Hz to {self.sampling_rate} Hz...")
                audio_data = resample_poly(audio_data, self.sampling_rate, original_sr)
                print(f"Resampled Audio Shape: {audio_data.shape}, Dtype: {audio_data.dtype}")

            if audio_data.dtype != np.int16:
                print(f"Converting Dtype {audio_data.dtype} to int16...")
                if np.issubdtype(audio_data.dtype, np.floating):
                    max_val = np.max(np.abs(audio_data))
                    if max_val > 0:
                        audio_data = audio_data / max_val
                    audio_data = np.clip(audio_data * 32767, -32768, 32767).astype(np.int16)
                elif np.issubdtype(audio_data.dtype, np.integer):
                    audio_data = np.clip(audio_data, -32768, 32767).astype(np.int16)
                else:
                    audio_data = audio_data.astype(np.int16)

            self.audio_bytes_io = io.BytesIO()
            wavfile.write(self.audio_bytes_io, self.sampling_rate, audio_data)
            self.audio_bytes_io.seek(0)
            print("Displaying processed audio:")
            display(Audio(data=self.audio_bytes_io.read(), rate=self.sampling_rate))
            self.audio_bytes_io.seek(0)
            self.recording_result = audio_data

        except Exception as e:
            print(f"Error processing audio data: {e}")
            traceback.print_exc()
        finally:
            self.data_receiver.value = ""
            print("Data receiver cleared.")

    def get_result(self):
        return self.recording_result
