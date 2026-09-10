import queue
import threading
import wave
from recorder import Track


def test_writer_resamples_stereo_and_preserves_muted_time(tmp_path):
    track = Track.__new__(Track)
    track.path = tmp_path / 'track.wav'
    track.channels, track.rate, track.frames = 2, 48000, 0
    track.error = None
    track.closed = threading.Event()
    track.queue = queue.Queue()
    # One second audible, followed by one second muted, at the same sample rate.
    pcm = (1000).to_bytes(2, 'little', signed=True) * 2 * 48000
    track.queue.put((pcm, 0, False))
    track.queue.put((pcm, 1, True))
    track.closed.set()
    track.write()
    assert track.error is None
    with wave.open(str(track.path), 'rb') as source:
        assert source.getframerate() == 16000
        assert source.getnchannels() == 1
        assert abs(source.getnframes() - 32000) <= 1
        assert any(source.readframes(16000))
        assert not any(source.readframes(16000))


def test_silent_meeting_break_is_padded_without_large_allocation(tmp_path):
    track = Track.__new__(Track)
    track.path = tmp_path / 'break.wav'
    track.channels, track.rate, track.frames = 1, 16000, 0
    track.error = None
    track.closed = threading.Event()
    track.queue = queue.Queue()
    track.queue.put((b'\x01\x00' * 16000, 180, False))
    track.closed.set()
    track.write()
    assert track.error is None
    with wave.open(str(track.path), 'rb') as source:
        assert source.getnframes() == 181 * 16000
        assert not any(source.readframes(180 * 16000))
        assert any(source.readframes(16000))
