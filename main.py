from fastapi import FastAPI
from pydantic import BaseModel
import os
import spacy
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import uuid
import json
import en_core_web_sm
import openai
from dotenv import load_dotenv

openai.api_key = os.getenv("OPENAI_API_KEY")

async def generate_text(prompt):
    # TODO change the model
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message["content"]

# Load the NER model 
# TODO change the NER
nlp = en_core_web_sm.load()

app = FastAPI()

# Set up CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "https://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EntityDetector:
    def __init__(self):
        self.entity_registry_names = []
        self.entity_registry_types = []
        self.entity_name_map = {}
        self.entity_type_map = {}
        self.full_uuid_map = {}

    def detect_entities(self, txt):
        # Perform NER detection on some text
        doc = nlp(txt)
        # Iterate over the entities in the document
        for ent in doc.ents:
            # Add the entity to the registry
            self.entity_registry_names.append(ent.text)
            # Access the label of the entity to extract its type
            self.entity_registry_types.append(ent.label_)

        for token in doc:
            if token.like_email and token.text not in self.entity_registry_names:
                self.entity_registry_names.append(token.text)
                self.entity_registry_types.append("EMAIL")
             
        return (self.entity_registry_names, self.entity_registry_types)

    def map_items(self): 
        # Iterate over the items in the entity registry
        for item_name, item_type in zip(self.entity_registry_names, self.entity_registry_types):
            # Map the item to a uuid
            item_uuid = str(uuid.uuid4())
            # Add the mapped item to the dictionary
            self.entity_name_map[item_uuid] = item_name
            self.entity_type_map[item_uuid] = item_type
            self.full_uuid_map[item_name] = item_uuid + " ( " + item_type + " ) "

    def redact(self, txt, prompt):
        # TODO fix format
        custom_replace = "Assume brackets may contain entity information. After this"
        ending = "Remove all the entity information in the output txt."
        for entity, uuidstr in self.full_uuid_map.items():
            txt = txt.replace(entity, uuidstr)
        for uuidstr, entity in self.entity_name_map.items():
            prompt = prompt.replace(entity, uuidstr)
        txtprocess = txt+ '\n' + custom_replace+ '\n' + prompt+ '\n' + ending 
        self.txtprocess = txtprocess
        return txtprocess

    def unredact(self, outputtxt):
        for uuidstr, entity in self.entity_name_map.items():
            outputtxt = outputtxt.replace(uuidstr, entity)
        return outputtxt

    def clear_values(self):
        self.entity_registry_names = []
        self.entity_registry_types = []
        self.entity_name_map = {}
        self.entity_type_map = {}
        self.full_uuid_map = {}
        self.txtprocess = None

@app.get("/")
async def root():
    return {"message": "hello world!"}

@app.post("/redact")
async def redact(request: dict):
    inputtxt = request.get("sensitive")
    prompttxt = request.get("question")
    detector = EntityDetector()
    detector.detect_entities(inputtxt + prompttxt)
    detector.map_items()
    txtprocess = detector.redact(inputtxt, prompttxt)
    return {"redacted": txtprocess, "mapping": json.dumps(detector.entity_name_map)}

@app.post('/answer')
async def answer(request: dict):
    # fix this later to get it from the endpoint
    inputtxt = request.get("sensitive")
    prompttxt = request.get("question")
    detector = EntityDetector()
    detector.detect_entities(inputtxt + prompttxt)
    detector.map_items()
    txtprocess = detector.redact(inputtxt, prompttxt)
    print(txtprocess)
    redacted_answer = await generate_text(txtprocess)
    finalanswer = detector.unredact(redacted_answer) 
    detector.clear_values()
    return {"unredacted": finalanswer, "redacted": redacted_answer}

@app.get("/path/{path_id}")
async def demo_get_path_id(path_id: int):
    return {"message": f"This is /path/{path_id} endpoint, use post request to retrieve result"}