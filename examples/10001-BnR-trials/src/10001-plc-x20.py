import asyncio
import os
import sys
from playwright.async_api import async_playwright
from browser_use import Agent, Browser, ChatGoogle

# Add the parent directory to the path so we can import browser_use
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv

load_dotenv()

BROWSER_CHANNEL = os.getenv("BROWSER_CHANNEL")
BROWSER_EXECUTABLE = os.getenv("BROWSER_EXECUTABLE")

# print(f"BROWSER_CHANNEL: {BROWSER_CHANNEL}")
# print(f"BROWSER_EXECUTABLE: {BROWSER_EXECUTABLE}")

async def main():
	# llm = ChatGroq(model='meta-llama/llama-4-maverick-17b-128e-instruct', base_url=os.getenv("GROQ_API_BASE_URL"), api_key=os.getenv("GROQ_API_KEY"))
    # llm = ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct")
    llm = ChatGoogle(model="gemini-2.5-pro", api_key=os.getenv("GEMINI_API_KEY"))
    browser = Browser(
        executable_path='/usr/bin/microsoft-edge-stable',
        profile_directory='Default', 
        headless=False, channel='msedge', keep_alive=True, window_size={'width': 1920, 'height': 1080}
    )
    # START #################################################################################
    # Browser.
    # END   #################################################################################
    task = "Task steps:" \
        " - Open website: https://www.br-automation.com/en/products/plc-systems/ " \
        " - After the page loads completely, Go to the left navigation menu and click on 'PLC systems'" \
        " - When the sub-menu of 'PLC systems' opens up, click on 'X20 System'." \
        " - Now, the table 'Components and Modules' opens up in the middle of this page (You can scroll by one page to reach this table)." \
        " - Click 'X20 PLC' row from this table to expand this row, to show a child table within this row, with approximately five rows for each product items." \
        " - Now, open each of these product item in a new tab, by right-clicking 'Material Number' of each item and selecting 'Open in New Tab' from the right-click browser context menu." \
        " - For each newly opened browser tab, scroll down to the Table containing details of the product item and extract and collect the 'Basic Information' and the 'Technical Data' from each tab and add this data in tabular format in an individual markdown file, Save this markdown file in temp directory with name in the format '<product item name>-<timestamp>.md' with product item name read from the page ." \
        " - Finally, when above stated data from all the tabs are collecting for all of the product items, close all tabs and browser. "
    
	# task = "Search Google for 'ullu web series' and tell me the top 3 results"
	# task = "Search Google for 'what is browser automation' and tell me the top 3 results"
    # agent = Agent(task=task, llm=llm, launch_browser=launch_browser)
    agent = Agent(task=task, llm=llm, browser=browser)
    await agent.run()


if __name__ == '__main__':
	asyncio.run(main())

