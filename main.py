import PyPDF2 as pdf
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv(override=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")
if gemini_api_key : 
  print(f"The key loaded and it starts with {gemini_api_key[:8]}")
else:
  print("The key did not load")

client = genai.Client(api_key = gemini_api_key)

linkedin = ""

with open("Profile.pdf" , 'rb') as file:
  reader = pdf.PdfReader(file)
  for page in reader.pages:
    text = page.extract_text()
    if text:
      linkedin+=text   

with open ("summary.txt" , "r") as file:
  summary = file.read()

name = "Aryaman Srivastava"

system_prompt = f"You are acting as {name}. You are answering questions on {name}'s website, \
particularly questions related to {name}'s career, background, skills and experience. \
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer, say so."

system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin}\n\n"
system_prompt += f"With this context, please chat with the user, always staying in character as {name}."

model = "gemini-2.5-flash"

message = input("Enter text")

while(message!="exit"):
  response = client.models.generate_content(
  model=model,
  contents=message,
  config=types.GenerateContentConfig(
  system_instruction=system_prompt,)
  )
  print(response.text)

  message = input("Enter a message")

print("System complete")


  
