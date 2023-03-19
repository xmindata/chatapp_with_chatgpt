import openai
import os
import sys
import json
import time
from dotenv import load_dotenv
import gradio

# load the API key from the environment
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

class ChatApp():
    def __init__(self, model="davinci", max_tokens=100, temperature=0.7, top_p=1, frequency_penalty=0,
                 presence_penalty=0, stop=["\n", " Human:", " AI:"]):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.stop = stop
        self.message_history = []

    def chat(self, input_message, role="user"):
      """
      This function is used to chat with the model, it will return the model's response.

      :param input_message:
      :param role:
      :return:
      """
      try:
        self.message_history.append({"role": role, "content": f"{input_message}"})
        completion = openai.ChatCompletion.create(
                                                  engine=self.model,
                                                  model="gpt-3.5-turbo",  # this is "ChatGPT" $0.002 per 1k tokens
                                                  messages=self.message_history
                                                  )
        reply_message = completion.choices[0].message.content
        self.message_history.append({"role": "assistent", "content": f"{reply_message}"})
        return reply_message
      except openai.error.RateLimitError as e:
        print(e)


class gradio_demo():
    """
    This class is used to create a gradio demo for the chat app.
    The app will use the chat function in the ChatApp class to interact.
    the gradio_demo class will be used to create a gradio app.
    """
    def __init__(self):
        self.chat_app = ChatApp()

    def launch(self):
        # self.interface = gradio.Interface(fn=self.chat_app.chat,
        #                                   inputs="text",
        #                                   outputs="text",
        #                                   title="Chat with GPT-3",
        #                                   description="This is a demo of GPT-3. You can chat with the model and it will try to respond to you.",
        #                                   allow_flagging=False,
        #                                   layout="vertical",
        #                                   theme="huggingface",
        #                                   examples=[
        #                                       ["Hi, how are you?"],
        #                                       ["What is your name?"],
        #                                       ["What is your favorite color?"],
        #                                       ["What is your favorite food?"],
        #                                   ]
        #                                   )
        # self.interface.launch()


        # creates a new Blocks app and assigns it to the variable demo.
        with gradio.Blocks() as demo:
            # creates a new Row component, which is a container for other components.
            with gradio.Row():
                # creates a new Textbox component, which is used to collect user input.
                txt = gradio.Textbox(show_label=False, placeholder="Enter text and press enter").style(container=False)
            # sets the submit action of the Textbox to the predict function,
            txt.submit(self.chat_app.chat, txt, gradio.Chatbot())  # submit(function, input, output)
            # txt.submit(lambda :"", None, txt)  #Sets submit action to lambda function that returns empty string

            '''
            sets the submit action of the Textbox to a JavaScript function that returns an empty string. 
            This line is equivalent to the commented out line above, but uses a different implementation. 
            The _js parameter is used to pass a JavaScript function to the submit method.'''
            txt.submit(None, None, txt,
                       _js="() => {''}")  # No function, no input to that function, submit action to textbox is a js function that returns empty string, so it clears immediately.

        demo.launch()

if __name__ == "__main__":
    gradio_demo().launch()