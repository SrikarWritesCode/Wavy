import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
import os

class MeasurementController:
    def __init__(self, output_filename='output.wav', format=pyaudio.paInt16, channels=1, rate=44100, chunk=1024, record_seconds=5):
        self.output_filename = output_filename
        self.format = format
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.record_seconds = record_seconds
        self.frames = []
    
    def record_audio(self):
        self.frames = []  # Ensure frames are reset for each new measurement
        p = pyaudio.PyAudio()
        stream = p.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk)
        print("Recording...")
        for _ in range(0, int(self.rate / self.chunk * self.record_seconds)):
            data = stream.read(self.chunk)
            self.frames.append(data)
        print("Finished recording.")
        stream.stop_stream()
        stream.close()
        p.terminate()
        self.save_wave_file()


    def save_wave_file(self):
        wf = wave.open(self.output_filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def perform_fft_and_plot(self):
        audio, rate = self.read_wav_file(self.output_filename)
        xf, yf = self.perform_fft(audio, rate)
        # self.plot_frequency_spectrum(xf, yf)
        # self.delete_file(self.output_filename)
        return xf, yf

    def read_wav_file(self, filename):
        with wave.open(filename, 'rb') as wf:
            nchannels, sampwidth, framerate, nframes, comptype, compname = wf.getparams()
            frames = wf.readframes(nframes)
            audio = np.frombuffer(frames, dtype=np.int16)
        return audio, framerate

    def perform_fft(self, audio, rate):
        n = len(audio)
        T = 1.0 / rate
        yf = np.fft.fft(audio)
        xf = np.fft.fftfreq(n, T)[:n//2]
        # Filter frequencies to be within 20 Hz to 20,000 Hz
        valid_indices = np.where((xf >= 20) & (xf <= 20000))
        return xf[valid_indices], 2.0/n * np.abs(yf[0:n//2])[valid_indices]

    def plot_frequency_spectrum(self, xf, yf):
        plt.figure()
        plt.plot(xf, yf)
        plt.xscale('log')  # Set x-axis to logarithmic scale
        plt.grid(True, which="both", ls="-")
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude')
        plt.title('Frequency Spectrum')
        plt.xlim(20, 20000)  # Limit x-axis from 20 Hz to 20,000 Hz
        plt.show()

    # def delete_file(self, filename):
    #     os.remove(filename)
    #     print(f"Deleted file: {filename}")

if __name__ == "__main__":
    mc = MeasurementController(record_seconds=5)
    mc.record_audio()
    mc.perform_fft_and_plot()
