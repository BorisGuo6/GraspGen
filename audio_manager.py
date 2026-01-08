'''
packages

pip install gtts pygame
pip install SpeechRecognition

'''
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from gtts import gTTS
import io
import speech_recognition as sr
import threading
import pyaudio

class AudioManager:
    def __init__(self, max_time=10):
        self.max_time = max_time
        # self.mic = sr.Microphone(device_index=5)
        self.mic = sr.Microphone()
        self.recognizer = sr.Recognizer()
        print("Adjusting for ambient noise... Please wait.")


                
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')

        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
        self.mic.__enter__()
        self.recognizer.adjust_for_ambient_noise(self.mic, duration=1)  # Reduce noise
        self.mic.__exit__(None, None, None)

    def mic_start(self):
        self.mic.__enter__()
        # pass

    def mic_stop(self):
        self.mic.__exit__(None, None, None)
        # pass

    def listen(self):
        # Initialize the recognizer
        
        recognizer = sr.Recognizer()

        # Use the microphone as the audio source
        # with sr.Microphone() as source:
            # print("Adjusting for ambient noise... Please wait.")
            # recognizer.adjust_for_ambient_noise(source, duration=0.3)  # Reduce noise
        
        self.mic.__enter__()
        print("Listening...")
        audio = recognizer.listen(self.mic, timeout=10)  # Capture the audio
        self.mic.__exit__(None, None, None)

        try:
            print("Recognizing...")
            # Use Google Web Speech API to recognize the speech
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError:
            print("Sorry, the service is unavailable.")

        return None

    def record(self, file_name="my_recording.wav"):
        pass

    def speak(self, text):
        tts = gTTS(text=text, lang='en', tld='us', slow=False)
        # Save the speech to a file-like object in memory (BytesIO)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        self.play(audio_fp)

        # Save the speech to a file
        # audio_fp.seek(0)
        # with open("output.mp3", "wb") as f:
        #     f.write(audio_fp.read())

    def play(self, audio_file):
        # Initialize the mixer
        pygame.mixer.init()

        # Load the audio file
        pygame.mixer.music.load(audio_file)

        # Play the audio
        pygame.mixer.music.play()

        # Wait until the music finishes playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(self.max_time)

        '''
        pygame.mixer.init()
        sound = pygame.mixer.Sound(audio_file)
        sound.play()
        pygame.time.wait(int(sound.get_length() * 1000))
        '''

    def speak_async(self, text):
        # Run the speak method in a separate thread
        threading.Thread(target=self.speak, args=(text,), daemon=True).start()

if __name__ == "__main__":
    # audio_manager = AudioManager()
    # audio_manager.speak("Hello, I am converting text to voice using Python and playing it directly!")
    # audio_manager.play("output.mp3")
    # audio_manager.record()
    # audio_manager.listen()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

    # audio_manager.speak("The task is finished. Here is the item.")


    '''
    # find default mic
    import speech_recognition as sr

    # Create a recognizer instance
    recognizer = sr.Recognizer()

    # List all available microphones and their indices
    mic_list = sr.Microphone.list_microphone_names()
    print(mic_list)  # Print to see the list of available devices

    # Find the index of 'USB Composite Device: Audio (hw:2,0)'
    # Suppose it is index 6 in the printed list (this is just an example)

    usb_mic_index = mic_list.index('USB Composite Device: Audio (hw:2,0)')  # Find the actual index

    # Use the USB microphone as the default microphone
    mic = sr.Microphone(device_index=usb_mic_index)

    print("!!!", usb_mic_index)
    '''

    # import speech_recognition as sr
    # for index, name in enumerate(sr.Microphone.list_microphone_names()):
    #     print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))