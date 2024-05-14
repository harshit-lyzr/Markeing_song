import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent,Task
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from PIL import Image
from lyzr_automata.tasks.task_literals import InputType, OutputType

st.set_page_config(
    page_title="Brand Song Lyrics Generator",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

image = Image.open("lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Brand Song Lyrics Generator")
st.sidebar.markdown("## Welcome to the Brand Song Lyrics Generator!")
st.sidebar.markdown("This App Harnesses power of Lyzr Automata to generate Lyrics for your Next Marketing. You Need to input Your Brand Name, Description,Idea and Language and This app will generate Lyrics for your brand.")

api = st.sidebar.text_input("Enter our OPENAI API KEY Here",type="password")

if api:
    openai_model = OpenAIModel(
        api_key=api,
        parameters={
            "model": "gpt-4-turbo-preview",
            "temperature": 0.2,
            "max_tokens": 1500,
        },
    )
else:
    st.sidebar.error("Please Enter Your OPENAI API KEY")


def lyrics_writer(name, description, idea, language):
    marketing_agent = Agent(
        prompt_persona="You Are Expert Marketing Manager",
        role="Marketing Expert",
    )

    song_task = Task(
        name="JS API Integration",
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=openai_model,
        agent=marketing_agent,
        log_output=True,
        instructions=f"""Your Are an Expert Marketing Officer and Part Time Lyrics Writer. Your Task is to Generate a Lyrics for Given Details:
        Product Name: {name}
        Product Description: {description}
        Idea for Song: {idea}
        Language: {language}
        """,
    )

    output = LinearSyncPipeline(
        name="Generate Lyrics",
        completion_message="Lyrics Generated!",
        tasks=[
            song_task
        ],
    ).run()
    return output[0]['task_output']


name = st.text_input("Brand Name", placeholder="Samsung")
description = st.text_input("Description", placeholder="We are selling Phones which is best in the world")
idea = st.text_input("Idea for Song")
language = st.text_input("Language", placeholder="Italian")

if api and st.button("Generate"):
    solution = lyrics_writer(name, description, idea, language)
    st.markdown(solution)

