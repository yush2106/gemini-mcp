#import mcp package
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

#import LLM package
import os
from dotenv import load_dotenv
import asyncio
from google import genai
from google.genai import types

load_dotenv()  #load environment variables
google_api_key = os.getenv("GOOGLE_API_KEY")

#Google Gemini client
gemini_client = genai.Client(api_key=google_api_key)
model_name = "gemini-2.5-flash"  #model name

#start MCP Server
server_params = StdioServerParameters(
  command="python",
  args=["src/mcp_server/server.py"],
  env=None
)

async def llm_chat():
  async with stdio_client(server_params) as (read, write):  #run MCP server
    async with ClientSession(read, write) as session:
      await session.initialize()  # Initialize the connection between client and server

      print("\n")
      print("Enter your questions (type 'exit' or '\\q' to quit):")
      
      while True:
        user_input = input("You: ").strip()  #user input question
        if not user_input or user_input.lower() in ("exit", "\\q", "quit"):
          print("Bye!")
          break
        
        try:
          #Define user prompt
          prompts = [
            types.Content(
              role="user", parts=[types.Part(text=user_input)]
            )
          ]
          #Send request to the model with MCP function declarations
          response = await gemini_client.aio.models.generate_content(
            model=model_name,
            contents=prompts,
            config=types.GenerateContentConfig(
                tools=[session],  # uses the session, will automatically call the tool
                system_instruction=[
                  "You are a helpful assistant.",
                  "You answer user questions kindly.",
                ],
                temperature=0.0,
            ),
          )
          print("Assistant: ", response.text)
        except Exception as err:
          print("Gemini error:", str(err))
          continue
      print("\n")
      print("MCP client terminated.")

if __name__ == "__main__":
  asyncio.run(llm_chat())