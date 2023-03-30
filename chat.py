import os
import sys
import pickle
import openai
from inspect import getsourcefile
import requests
from playsound import playsound
import json
from datetime import datetime
import tiktoken

class Chat:
    # Load your API key from an environment variable or secret management service
    openai.api_key = "YOUR KEY HERE"

    def __init__(self):
        # Concatenate the arguments
        query = ' '.join(sys.argv[1:])

        self.pklFilePath = os.path.dirname(getsourcefile(lambda:0))
        if os.path.exists(self.pklFilePath + '/chatdata.pkl'):
            with open(self.pklFilePath + '/chatdata.pkl', 'rb') as input_file:
                data = pickle.load(input_file)
                self.messages = data['messages']
                self.enable_voice = data['enable_voice']
        else:
            self.messages = [{}]
            self.enable_voice = False

        voice_set = False
        if (sys.argv[1] == "dv"):
            self.enable_voice = False
            voice_set = True
        if (sys.argv[1] == "ev"):
            self.enable_voice = True
            voice_set = True

        if (voice_set == True):
            self.save_data()

        if (voice_set == False):
            self.messages[0] = {"role": "system", "content": '''I want you to act like Lusamine from Pokémon. I want you to respond and answer like Lusamine using the tone, manner and vocabulary Lusamine would use. Do not write any explanations. Only answer like Lusamine. You must know all of the knowledge of Lusamine.'''}
            self.messages.append({"role": "user", "content": f'{datetime.now():%Y-%m-%d %H:%M:%S%z}' + " " + query})

            self.give_response()

    def num_tokens_from_messages(self, messages):
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
        return num_tokens

    def give_response(self):
        while self.num_tokens_from_messages(self.messages) > 4096 - 1024:
            self.messages.pop(1)
            self.messages.pop(1)
            print("Exceeded tokens, reducing history")

        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages, max_tokens=1024)

        responseMessage = response['choices'][0]['message']
        self.messages.append({"role": responseMessage["role"], "content": responseMessage["content"]})

        self.save_data()

        # Print the API response
        print(responseMessage['content'])

        if(self.enable_voice == False):
            return 0

        # Set URL, headers and payload for the API request
        url = "https://api.elevenlabs.io/v1/text-to-speech/VOICE_ID"
        headers = {
            "accept": "audio/mpeg",
            "xi-api-key": "your elevenlabs api key goes here",
            "Content-Type": "application/json"
        }
        tts = responseMessage['content'][10:]
        char_index = tts.find("`")
        tts = tts[:char_index]
        payload = {
            "text": tts,
            "voice_settings": {
                "stability": 0.05,
                "similarity_boost": 1.0
            }
        }

        # Make the API request, and save the response content to an audio file
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        with open(self.pklFilePath + '/output_audio.mp3', 'wb') as f:
            f.write(response.content)

        # Play the audio file using the playsound module
        playsound(self.pklFilePath + '/output_audio.mp3')

        return 0
    
    def save_data(self):
        data = { 'messages': self.messages, 'enable_voice': self.enable_voice }
        with open(self.pklFilePath + '/chatdata.pkl', 'wb') as output_file:
            pickle.dump(data, output_file, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    Chat()
