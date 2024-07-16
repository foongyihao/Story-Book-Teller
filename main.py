# imports
import streamlit as st
from openai import OpenAI

# statics
api_key = st.secrets["OPENAI_SECRET"]
client = OpenAI(api_key=api_key)


# methods
def story_ai(msg, client):
  story_response = client.chat.completions.create(
      model='gpt-3.5-turbo',
      messages=[{
          'role':
          'system',
          'content':
          "You are a bestseller story writer. You will tale user's prompt and generate a 100 words short story for adult age 29-30"
      }, {
          'role': 'user',
          'content': f'{msg}'
      }],
      max_tokens=400,
      temperature=0.8)

  story = story_response.choices[0].message.content
  return story

def design_ai(story, client):
  design_response = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[{
        'role': 'system',
        'content': "Based on the story given. You will design a detailed image prompt for the cover image of this story. The image prompt should include the theme of the story with relevant color, suitable for adults. The output should be within 100 characters."
    },{
        'role': 'user',
        'content': f'{story}'
    }],
    max_tokens = 400,
    temperature = 0.8
  )

  design_prompt = design_response.choices[0].message.content
  return design_prompt

def cover_ai(prompt, client):
  cover_response = client.images.generate(
    model='dall-e-2',
    prompt = f'{prompt}',
    size='256x256',
    quality = 'standard',
    n = 1
  )

  image_url = cover_response.data[0].url
  return image_url


# streamlit stuff
st.title("Story Book Teller")

with st.form(' '):
  st.write('This is for user to key in information')
  
  msg = st.text_input(label="Some keywords to generate a story :")
  submitted = st.form_submit_button(label="Submit")

  if submitted:

    with st.status("Generating story..."):
      st.write("Creating a story based on keywords...")
      story = story_ai(msg, client)
      st.write("Designing a cover for the story...")
      refined_prompt = design_ai(story, client)
      st.write("Painting cover...")
      cover = cover_ai(refined_prompt, client)

    st.image(f'{cover}')
    st.write(f'story: \n{story}')

    st.balloons()

    st.toast('Story Generated!', icon='📖')

    
    

