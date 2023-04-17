import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Form, Response, Request
from twilio.twiml.messaging_response import MessagingResponse
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

app = FastAPI()

@app.post("/gpt")
async def gptsms(request: Request, Body:str = Form(...)):
    input_msg = Body

    chat = ChatOpenAI(
        api_key=OPENAI_API_KEY, 
        model='gpt-3.5-turbo', 
        temperature=0.9
        )

    prompt = PromptTemplate(
        input_variables=["input"],
        template="{input}",
        )

    # Create chain that takes user input, formats prompt with input, sends to LLM
    chain = LLMChain(llm=chat, prompt=prompt)
    chain_output = chain.run(input_msg)

    response = MessagingResponse() 
    msg = response.message(f"{chain_output}")
    return Response(content=str(response), media_type="application/xml")


if __name__ == "__main__":
    uvicorn.run('main:app', host="localhost", port=3000, reload=True)