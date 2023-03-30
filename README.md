# ChatGPTBuddy
Talk through the terminal, set necessary context, resend chat history and integrate with elevenlabs for voice.

The script keeps the history until the token quota is exceeded, then it removes the oldest messages except initial system prompt message.

The script adds the users timestamp so ChatGPT can use it to have a feel of the flow of time for the user.

The script is kinda ugly but it is how it is, maybe someone still needs something like this so that's why I uploaded it to GitHub.

# Installation
```
pip install openai requests playsound tiktoken
```

In the script set your API key for openAI, where it says:
```
openai.api_key = "YOUR KEY HERE"
```

Get it here: [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)

# Setting the context
Change this line:
```
self.messages[0] = {"role": "system", "content": '''I want you to act like Lusamine from Pokémon. I want you to respond and answer like Lusamine using the tone, manner and vocabulary Lusamine would use. Do not write any explanations. Only answer like Lusamine. You must know all of the knowledge of Lusamine.'''}
```
In Python, you can use line breaks in a string with '''message''', thus you can simply copy paste your prompt between the '''

That's it, save the file and try it out by calling the script:
```
python3 chat.py Hello Lusamine, can you be my chat buddy?
```
Reminder that certain symbols need to be escaped in bash with an antislash. Such as:
```
python3 chat.py I\'m feeling great, had a lot of fun today\!
```
Same with <, >, | symbols etc.

And for easier chatting, you can add the script to your .bash_aliases file and for example add:
```
alias c="python3 /home/user/ChatGPTBuddy/chat.py "
```


# ElevenLabs voice integration
I chose elevenlabs for the voice cloning, set your API key

First set the voice id you want to use here:
```
# Set URL, headers and payload for the API request
url = "https://api.elevenlabs.io/v1/text-to-speech/VOICE_ID"
```
It is a random string of characters, uppercase, lowercase and numbers

Then set your API key:
```
"xi-api-key": "your elevenlabs api key goes here",
```

Finally in the payload, change the stability and similarity boost, the current settings are what I use but it depends on the voice you cloned:
```
"voice_settings": {
    "stability": 0.05,
    "similarity_boost": 1.0
}
```

And enable voice by calling the script and ev parameter:
```
python3 chat.py ev
```

Then it should work, to disable:
```
python3 chat.py dv
```
