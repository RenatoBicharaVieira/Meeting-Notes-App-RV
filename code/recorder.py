"""Two WASAPI streams, bounded queues, and incremental 16 kHz mono WAV files."""
import audioop
import queue
import threading
import time
import wave
import pyaudiowpatch as pa
from meeting_data import save_json


def devices():
    with pa.PyAudio() as audio:
        host = audio.get_host_api_info_by_type(pa.paWASAPI)
        inputs = []
        for i in range(audio.get_device_count()):
            item = audio.get_device_info_by_index(i)
            if item['hostApi'] == host['index'] and item['maxInputChannels'] and not item.get('isLoopbackDevice'):
                inputs.append(item)
        outputs = list(audio.get_loopback_device_info_generator())
        default_output = audio.get_default_wasapi_loopback().get('index') if outputs else None
        return inputs, outputs, host['defaultInputDevice'], default_output


class Track:
    def __init__(self, audio, device, path, origin, microphone=False):
        self.path, self.origin = path, origin
        self.microphone, self.muted = microphone, False
        self.rate = int(device['defaultSampleRate'])
        self.channels = min(2, int(device['maxInputChannels']))
        self.queue = queue.Queue(maxsize=256)
        self.error = None
        self.closed = threading.Event()
        self.frames = 0
        self.audio = audio
        self.stream = audio.open(format=pa.paInt16, channels=self.channels,
            rate=self.rate, input=True, input_device_index=int(device['index']),
            frames_per_buffer=1024, stream_callback=self.callback, start=False)
        self.clock_base = self.stream.get_time()
        self.wall_base = time.perf_counter() - origin
        self.writer = threading.Thread(target=self.write, daemon=True)

    def callback(self, data, count, timing, status):
        if status:
            self.error = 'An audio buffer overflow or device error occurred. Stop and check your audio devices.'
        stamp = timing.get('input_buffer_adc_time', 0)
        if not stamp:
            stamp = timing.get('current_time', self.clock_base) - count / self.rate
        offset = self.wall_base + stamp - self.clock_base
        try:
            self.queue.put_nowait((data, offset, self.microphone and self.muted))
        except queue.Full:
            self.error = 'Audio could not be saved quickly enough. Check available disk space.'
            return None, pa.paAbort
        return None, pa.paContinue

    def start(self):
        self.writer.start()
        self.stream.start_stream()

    def write(self):
        state = None
        try:
            with wave.open(str(self.path), 'wb') as output:
                output.setnchannels(1)
                output.setsampwidth(2)
                output.setframerate(16000)
                while not self.closed.is_set() or not self.queue.empty():
                    try:
                        data, offset, muted = self.queue.get(timeout=.1)
                    except queue.Empty:
                        continue
                    if self.channels == 2:
                        data = audioop.tomono(data, 2, .5, .5)
                    data, state = audioop.ratecv(data, 2, 1, self.rate, 16000, state)
                    if muted:
                        data = bytes(len(data))
                    # Preserve gaps and stream offsets. Small scheduling jitter is ignored.
                    target = max(0, round(offset * 16000))
                    gap = target - self.frames
                    if gap > 640:
                        if gap > 16000 * 4 * 3600:
                            raise RuntimeError('The audio device clock jumped. Recording stopped to preserve timing.')
                        # Loopback devices may emit no callbacks during long silent breaks.
                        remaining = gap
                        while remaining:
                            count = min(remaining, 16000)
                            output.writeframesraw(bytes(count * 2))
                            remaining -= count
                        self.frames += gap
                    elif gap < -640:
                        data = data[min(len(data), -gap * 2):]
                    output.writeframesraw(data)
                    self.frames += len(data) // 2
        except Exception as exc:
            self.error = f'Could not save audio: {exc}'

    def stop(self):
        try:
            if self.stream.is_active():
                self.stream.stop_stream()
        finally:
            self.stream.close()
            self.closed.set()
            if self.writer.ident:
                self.writer.join()


class Recorder:
    def __init__(self, folder, microphone, playback, muted=False):
        self.audio = pa.PyAudio()
        self.folder = folder
        self.origin = time.perf_counter()
        self.tracks = []
        try:
            for name, device, mic in [('microphone', microphone, True), ('system', playback, False)]:
                track = Track(self.audio, device, folder / f'{name}.wav', self.origin, mic)
                track.muted = muted if mic else False
                self.tracks.append(track)
            for track in self.tracks:
                track.start()
        except Exception:
            self.stop()
            raise

    def mute(self, value):
        self.tracks[0].muted = value

    def error(self):
        for track in self.tracks:
            if track.error:
                return track.error
            try:
                if not track.stream.is_active():
                    return 'An audio device stopped responding. The recording has been stopped.'
            except OSError:
                return 'An audio device disconnected. The recording has been stopped.'
        return None

    def stop(self):
        errors = []
        for track in self.tracks:
            try:
                track.stop()
            except Exception as exc:
                errors.append(str(exc))
        self.audio.terminate()
        save_json(self.folder / 'recording.json', {'duration': time.perf_counter() - self.origin,
            'sample_rate': 16000, 'errors': errors + [t.error for t in self.tracks if t.error]})
        return errors
