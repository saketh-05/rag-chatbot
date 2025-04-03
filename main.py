from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever
from google.cloud import texttospeech, speech
import time
import random
import sounddevice as sd
import numpy as np
from pydub import AudioSegment

'''
Not required for now - 

# def generate_rawdata_from_input_audio(input_audio_file):
#     samplerate = 44100
#     channels = 2
#     process = subprocess.Popen([
#         "ffmpeg", "-i", f"{input_audio_file}", "-f", "s16le", "-acodec", "pcm_s16le",
#         "-ar", str(samplerate), "-ac", str(channels), "-"
#     ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
#     rawdata = process.stdout.read()
#     return rawdata

'''

def generate_timestamp_unique_id():
    timestamp = int(time.time())
    random_no = random.randint(1000, 9999)
    return f"{timestamp}{random_no}"

#To decode timestamp to datetime
# date_obj = datetime.fromtimestamp(timestamp)
# formatted_date = date_obj.strftime("%d/%m/%Y %H:%M:%S")

ttsclient = texttospeech.TextToSpeechClient()
sttclient = speech.SpeechClient()

model = OllamaLLM(model="mistral")
# model = OllamaLLM(model="deepseek-r1:1.5b")
# model = OllamaLLM(model="deepseek-r1:7b")

template = """
You are an expert in answering questions about the One Piece episodes

Here are some One Piece episodes: {episode_list}

Here is the question to answer: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | model

i=1

while True: 
    try:
        print("\n\n---------------------------------------")
        # question = input("Ask your question (q to quit): ")
        input_question = sd.rec(int(10 * 44100), samplerate=44100, channels=2, dtype='int16')
        sd.wait()  
        print("\n\n")
        # if question == "quit":
        #     break
        
        audio_bytes = input_question.tobytes()
        audio = speech.RecognitionAudio(content=audio_bytes)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            audio_channel_count=2,
            language_code="en-US",
        )
        
        response = sttclient.recognize(config=config, audio=audio)
        
        question = ""
        print("Recognized text:")
        for result in response.results:
            print(result.alternatives[0].transcript)
            question = result.alternatives[0].transcript
        
        if question == "bye":
            print("Exiting...")
            break
        
        print(f"Question: {question}")
        
        flag = input("Is this the correct question? (y/n): ")
        if flag == "n":
            print("Exiting...")
            break
        
        episode = retriever.invoke(question)
        
        print(f"Episode retrieved: {episode}")
        
        flag2 = input("Is this the correct episode? (y/n): ")
        if flag2 == "n":
            print("Exiting...")
            break
        
        result = chain.invoke({"episode_list": [episode], "question": question})
        print(result)
        
        synthesis_text = texttospeech.SynthesisInput(text=result)
        
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        response = ttsclient.synthesize_speech(
            input=synthesis_text, voice=voice, audio_config=audio_config
        )
        unique_file_name = generate_timestamp_unique_id()
        
        with open(f"output-audio/output{unique_file_name}-{i}.mp3", "wb") as out:
            out.write(response.audio_content)
            print(f'Audio content written to file "output{unique_file_name}-{i}.mp3"')
        
        output_audio_file = AudioSegment.from_mp3(f"output-audio/output{unique_file_name}-{i}.mp3")
        sample_rate = output_audio_file.frame_rate
        output_audio = np.array(output_audio_file.get_array_of_samples(), dtype=np.int16)
        
        if output_audio_file.channels == 2:
            output_audio = output_audio.reshape(-1, 2) 
        
        sd.play(output_audio, samplerate=sample_rate)
        sd.wait()
        
        i += 1
        
    except Exception as e:
        print(f"An error occurred: {e}")
        break