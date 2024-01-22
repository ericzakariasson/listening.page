from text_chunker import TextChunker
import hashlib
from openai import OpenAI
client = OpenAI()
import requests

import streamlit as st


def scrape_url(url):
    response = requests.get(url)
    return response.text


chunker = TextChunker(maxlen=4096)

st.title("Listen to the web")

site_url = st.text_input('URL')

if (site_url):
  html = scrape_url(site_url)
  print("Received HTML")
  chat_completion= client.chat.completions.create(
      messages=[
        {
          "role": "system",
          "content": "You're an agent designed to parse HTML and extract relevant information from it. You'll be given a string of HTML and your task is to extract the text that people want to read. Only output the text. Do not alter the content",
        },
        { 
          "role": "user", 
          "content": html  
        },
      ],
      model="gpt-4-1106-preview"
  )

  print("Received chat completion")

  text = chat_completion.choices[0].message.content

  site_urk_hash = hashlib.md5(site_url.encode())

  i = 0
  print(text)
  chunks = list(chunker.chunk(text))
  for chunk in chunks:
      print(f"Chunk {i + 1}")
      response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=chunk
      )

      audio_path = f"{site_urk_hash}-audio-{i + 1}.mp3"
      response.write_to_file(audio_path)
      st.write(f"Audio ({i + 1}/{len(chunks)})")
      st.audio(audio_path, format='audio/mp3')
      i += 1
