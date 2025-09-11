import asyncio
import os
import sys

# Add the parent directory to the path so we can import browser_use
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from browser_use import Agent, ChatGroq
from dotenv import load_dotenv

load_dotenv()

async def main():
	llm = ChatGroq(model='meta-llama/llama-4-maverick-17b-128e-instruct')
	task = "Search Google for 'Lulu web series' and tell me the top 50 results"
	agent = Agent(task=task, llm=llm)
	await agent.run()


if __name__ == '__main__':
	asyncio.run(main())
