import os
# imports deferred to within class to bypass SSL global context crash on import

from dotenv import load_dotenv

load_dotenv()

class VoiceEngine:
    def __init__(self):
        # Aggressively bypass Avast/AVG SSL interception
        import ssl
        import os
        def create_unverified_context(*args, **kwargs):
            return ssl._create_unverified_context(*args, **kwargs)
        ssl.create_default_context = create_unverified_context
        os.environ['PYTHONHTTPSVERIFY'] = '0'

        try:
            from google.cloud import texttospeech
            from google.cloud import speech
            # Requires GOOGLE_APPLICATION_CREDENTIALS to be set in .env
            self.tts_client = texttospeech.TextToSpeechClient()
            self.stt_client = speech.SpeechClient()

            self.enabled = True
        except Exception as e:
            print(f"VoiceEngine disabled: {e}")
            self.enabled = False
            return

        self.voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", 
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
            name="en-US-Neural2-F" # Empathetic sounding voice
        )
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

    def speak(self, text, output_filename="narration.mp3"):
        if not self.enabled:
            return None
        synthesis_input = texttospeech.SynthesisInput(text=text)
        response = self.tts_client.synthesize_speech(
            input=synthesis_input, voice=self.voice, audio_config=self.audio_config
        )
        with open(output_filename, "wb") as out:
            out.write(response.audio_content)
        return output_filename
