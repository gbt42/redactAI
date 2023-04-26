# redactAI

Private inference over your sensitive data with GPT4. 

RedactAI is an extremely simple starter library
- it takes your sensitive data and questions
- identifies PII and entities and save it into a mapping
- automatically redacts these entities 
- passes this redacted prompt into an off-the-shelf model API (e.g. GPT-4, Claude, Alpaca, whatever you want) 
- receive the redacted answer 
- unredacts it with the saved mapping 

# example usage
Sensitive: "Write an email for "janedoe@gmail.com" and "johnsmith@gmail.com for Wednesday regarding the upcoming meeting we have."
Prompt: ""

# limitations 


# extensions 

There are a couple directions to extend this - feel free to make PRs or forks. 
- integrations with other off-the-shelf models (right now only calls gpt-4) 
- customize redaction techniques 
- adding in 
