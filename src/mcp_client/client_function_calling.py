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

def find_tool(prompt, tool_list):  #Find the tool to call
  print("FIND TOOLS")
  response = gemini_client.models.generate_content(
    model=model_name,
    contents=prompt,
    config=types.GenerateContentConfig(
      system_instruction=[
        "You are a helpful assistant.",
        "You try to find the available tools",
      ],
      tools=[tool_list],  #Gemini use the MCP tools
      temperature=0.0,
    )
  )
  if response.candidates[0].content.parts[0].function_call:
    function_call = response.candidates[0].content.parts[0].function_call
    print("Function to call:", function_call.name)
    print("Arguments:", function_call.args)
  else:
    print("Tools was not found")
  return response

def call_llm(prompt):  #call LLM ask question
  print("CALLING LLM")
  response = gemini_client.models.generate_content(
    model=model_name,
    contents=prompt,
    config=types.GenerateContentConfig(
      system_instruction=[
        "You are a helpful assistant.",
        "You answer user questions kindly.",
      ],
      temperature=0.0,
    )
  )
  answer_string = response.text
  return answer_string

def convert_to_llm_tool(tool):  #convert tool schema
  tool_schema = {
    "name": tool.name,
    "description": tool.description,
    "parameters": {
      "type": "object",
      "properties": tool.inputSchema["properties"]
    }
  }
  return tool_schema

async def interactive_chat():
  #use STDIO transport to connect MCP Server
  async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
      await session.initialize()  #Initialize the connection

      tools_info = await session.list_tools()  #List available resources
      functions = []
      print("Tools available:")
      for tool in tools_info.tools:
        print(f"{tool.name}: {tool.description}")
        functions.append(convert_to_llm_tool(tool))
      tool_list = types.Tool(function_declarations=functions)
      
      print("\n")
      print("Enter your questions (type 'exit' or '\\q' to quit):")

      while True:
        user_input = input("You: ").strip()
        if not user_input or user_input.lower() in ("exit", "\\q", "quit"):
          print("Bye!")
          break
        
        try:
          #Define user prompt
          contents = [
            types.Content(
              role="user", parts=[types.Part(text=user_input)]
            )
          ]

          response = find_tool(user_input, tool_list)  #Find the tool to call
          tool_call = response.candidates[0].content.parts[0].function_call
          if (tool_call != None):
            tool_name = tool_call.name  #get the tool name
            tool_args = tool_call.args  #get the tool arguments
            result = await session.call_tool(tool_name, tool_args)  #get the result from MCP tool
            print("Result:", result.content)  #print result content
            function_response_part = types.Part.from_function_response(
              name=tool_name,
              response={"result": result},
            )
            contents.append(response.candidates[0].content) # Append the content from the model's response.
            contents.append(types.Content(role="user", parts=[function_response_part])) # Append the function response
          answer_string = call_llm(contents)  #ask question
          print("Assistant:", answer_string)  #answer
        except Exception as err:
          print("Gemini error:", str(err))
          continue

      print("\n")
      print("MCP client terminated.")

if __name__ == "__main__":
  asyncio.run(interactive_chat())