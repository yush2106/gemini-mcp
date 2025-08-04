# gemini-mcp
### This project contain both mcp server and mcp client implementation examples.
### Create a mcp server with all of the tools or functions, first.
### Then, build a mcp client to connect the mcp server, use Google Gemini LLM with tools which are on the mcp server and answer user questions.

## Reference
For biginers, we could learn the mcp structure and process in the repository of <a href="https://github.com/microsoft/mcp-for-beginners">mcp-for-beginners</a> on Github.

The example of this repository, we use Google Gemini to answer user questions with tools on mcp server. Check the <a href="https://ai.google.dev/gemini-api/docs/function-calling">Function calling with the Gemini API</a>, it has offered some function calling examples and mcp client examples with calling Gemini.

## Installation
<pre lang="bash">
pip install mcp
pip install -q -U google-genai
pip install dotenv
</pre>
Use the following command when your package manager is Poetry.
<pre lang="bash">
poetry add mcp
poetry add google-genai
poetry add dotenv
</pre>

## Usage
First of all, you should create your own API key.

You could sign in your google account on
<a href="https://aistudio.google.com">Google AI Studio</a>, then click `Get API key` to generate a new API key for Gemini LLM usage.

Create a `.env` file, the file content should define the `GOOGLE_API_KEY` parameter.

.env file content
<pre lang="bash">
GOOGLE_API_KEY="API-key-from-Google-AI-Studio"
</pre>

Execute the mcp client.
<pre lang="bash">
python client.py
</pre>

## Talk to LLM on mcp client with tools.
<pre lang="bash">
You: convert 19 to binary value
Assistant:  The binary value of 19 is 0b10011.

You: convert 19 to hex value
Assistant:  The hexadecimal value of 19 is 0x13.

You: "101101" shift right
Assistant:  The binary value "101101" shifted right by one bit position is "00010110".

You: "101101" shift left
Assistant:  The binary value "101101" shifted to the left is "01011010".

You: exit
Bye!

MCP client terminated.
</pre>