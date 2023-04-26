# redactAI

Private inference over your sensitive data with GPT4. 

RedactAI is an extremely simple starter library
- it takes your sensitive data and questions
- identifies PII and entities and save it into a mapping
- automatically redacts these entities 
- passes this redacted prompt into an off-the-shelf model API (e.g. GPT-4, Claude, Alpaca, whatever you want) 
- receive the redacted answer 
- unredacts it with the saved mapping 

Full example here
![image](https://user-images.githubusercontent.com/131616017/234503659-a0b765b1-cd28-4bba-a9fa-104c4986ec45.png)

# example usage
Sensitive: "Write a two-sentence email headline for "anonone@gmail.com" and "anon@two.com" for Wednesday regarding the upcoming meeting we have about the dangers of AI."
Prompt: ""

Sensitive: "Hello Paulo Santos. The latest statement for your via 4005274213474735 was mailed to 123 Collingwood Street, Seattle, WA 98109."
Prompt: "What address was it mailed to?" 

# limitations 
- If you need the model to ask about specific entities in the text, these get redacted and the model is not going to be able to answer questions about it (Hi, what do you know about Timothee Chamalet?). You can easily make a selective extension yourself if you need a specific entity type to stay unredacted

# known bugs 
- there are some non-deterministic parsing issues sometimes with tokenization 

# extension ideas 

There are a couple directions to extend this, some below - feel free to make PRs or forks. 
- integrations with other off-the-shelf models (right now only calls gpt-4) 
- customize redaction types (redact only email, PII, school, entity) 
- adding in more advanced entity recongition (toy demo with spacy right now) 
- adding in more advanced forms of redacting and encryption
