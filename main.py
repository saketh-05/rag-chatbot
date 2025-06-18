# from langchain_ollama.llms import OllamaLLM     --trying to manually connect with ollama serve 
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever
from google.cloud import texttospeech, speech
import time
import random
import sounddevice as sd
import numpy as np
from pydub import AudioSegment

import requests
import json
import traceback

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # change later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

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

def getOllamaResponse(data):
#     if isinstance(data["episode_list"], list):
#         data["episode_list"] = ", ".join(str(ep) for ep in data["episode_list"])
        
    url = "http://localhost:11434/api/generate"
    
    mod_data = {
        "model": "gemma3:4b",
        "prompt": prompt.format(**data),
        "temperature": 1.0,
        "top_p": 0.9,
        "top_k": 40,
        "max_tokens": 250,
        "stream": False
    }
    
    response = requests.post(url, json=mod_data)
    if response.status_code == 200:
        response_data = response.json()
        return response_data["response"]
    
    
#To decode timestamp to datetime
# date_obj = datetime.fromtimestamp(timestamp)
# formatted_date = date_obj.strftime("%d/%m/%Y %H:%M:%S")

ttsclient = texttospeech.TextToSpeechClient()
sttclient = speech.SpeechClient()

# model = OllamaLLM(model="mistral")
# model = OllamaLLM(model="deepseek-r1:1.5b")
# model = OllamaLLM(model="deepseek-r1:7b")

template = """
You are an expert in answering questions about the One Piece episodes

Here are some One Piece episodes: {episode_list}

Here is the question to answer: {question}

If you don't know the answer, say "I don't know".
"""

prompt = ChatPromptTemplate.from_template(template)

# chain = prompt | model

def mainProgramOnly():
    '''
    This function is used to run the main program. It will take the input from the user and return the output from the model.
    '''      
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

            for result in response.results:
                print(result.alternatives[0].transcript)
                question = result.alternatives[0].transcript
            
            if question == "bye":
                print("Exiting...")
                break
            
            print(f"Question: {question}")
            
            # flag = input("Is this the correct question? (y/n): ")
            # if flag == "n":
            #     print("Please edit the prompt and try again.")
            #     question = input("Enter the correct question: ")
            #     print(f"Question: {question}")
                
            
            episode = retriever.invoke(question)
            
            print(f"Episode retrieved: {episode}")
            
            # flag2 = input("Is this the correct episode? (y/n): ")
            # if flag2 == "n":
            #     print("Exiting...")
            #     break
            
            result = getOllamaResponse({"episode_list": [episode], "question": question})
            
            # print("result : ", result)
            
            result_with_think = result.split("</think>")
            result = result_with_think[1].strip()
            # print(f"Formatted Result: {result}")
            
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
            
            with open(f"local-output-audio/output{unique_file_name}-{i}.mp3", "wb") as out:
                out.write(response.audio_content)
                print(f'Audio content written to file "output{unique_file_name}-{i}.mp3"')
            
            output_audio_file = AudioSegment.from_mp3(f"local-output-audio/output{unique_file_name}-{i}.mp3")
            sample_rate = output_audio_file.frame_rate
            output_audio = np.array(output_audio_file.get_array_of_samples(), dtype=np.int16)
            
            if output_audio_file.channels == 2:
                output_audio = output_audio.reshape(-1, 2) 
            
            sd.play(output_audio, samplerate=sample_rate)
            sd.wait()
            
            i += 1
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Traceback:")
            traceback.print_exc()
            break
        
        
def textResponse(text):
    '''
    This function is used to process the text and return the processed text.
    '''   
    
    episode = retriever.invoke(text)
    
    print(f"Episode context retrieved: {episode}")
    
    result = getOllamaResponse({"episode_list": [episode], "question": text})
    
    return result
    
    
@app.get("/")
def read_root():
    return {"Api working": "yes"}


@app.get("/ask-question")
async def read_question(question: str):
    '''
    This function is used to get the question from the user and return the answer from the model.
    '''
    
    try:
        question = question.strip()
        print("Question: ", question)
        result = textResponse(question)
        # print("Result: ", result)
        return {"result": result}
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Traceback:")
        traceback.print_exc()
        

if __name__ == "__main__":
    # mainProgramOnly() # Uncomment this line if you want to run the interactive console version
    uvicorn.run(app, port=8000) # Runs the FastAPI server instead
