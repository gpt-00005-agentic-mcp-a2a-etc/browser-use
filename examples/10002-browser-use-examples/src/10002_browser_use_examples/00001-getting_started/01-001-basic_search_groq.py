import asyncio
import os
import sys
from playwright.async_api import async_playwright

# Add the parent directory to the path so we can import browser_use
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv

load_dotenv()

from browser_use import Agent, Browser, ChatGroq


BROWSER_CHANNEL = os.getenv("BROWSER_CHANNEL")
BROWSER_EXECUTABLE = os.getenv("BROWSER_EXECUTABLE")


async def launch_browser(headless: bool = False, **kwargs):
    async with async_playwright() as p:
        launch_args = kwargs.copy()
        launch_args.setdefault("headless", headless)

        # Prefer channel if provided (msedge). Fallback to executable_path if set.
        if BROWSER_CHANNEL:
            browser = await p.chromium.launch(channel=BROWSER_CHANNEL, **launch_args)
        elif BROWSER_EXECUTABLE:
            browser = await p.chromium.launch(executable_path=BROWSER_EXECUTABLE, **launch_args)
        else:
            browser = await p.chromium.launch(**launch_args)

        return browser


async def main():
	# llm = ChatGroq(model='meta-llama/llama-4-maverick-17b-128e-instruct', base_url=os.getenv("GROQ_API_BASE_URL"), api_key=os.getenv("GROQ_API_KEY"))
    # llm = ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct")
    llm = ChatGroq(model="meta-llama/llama-guard-4-12b")
    browser = Browser(
        executable_path='/usr/bin/microsoft-edge-stable',
        profile_directory='Default', 
        headless=False, channel='msedge', keep_alive=True, window_size={'width': 1920, 'height': 1080}
    )
    task = "Task steps:" \
        "Open website: https://www.br-automation.com/en/products/plc-systems/ " \
        " After the page loads fully, Go to the left navigation menu and click on 'PLC systems', thereafter when the sub-menu opens click 'X20 System'." \
        " Now, the table 'Components and Modules' opens up. Click 'X20 PLC' row from this table to expand it with rows for each product item of this sub-category" \
        " Now, open each of these product item in a new tab, by right-clicking 'Material Number' of each item and selecting 'Open in New Tab' from the right-click context menu. "
        # " Finally, extract the 'Basic Information' and the 'Technical Data' from each tab and add this data in tabular format in an markdown file." \
        # " Provide the summary in a concise bullet-point format."
    
	# task = "Search Google for 'ullu web series' and tell me the top 3 results"
	# task = "Search Google for 'what is browser automation' and tell me the top 3 results"
    # agent = Agent(task=task, llm=llm, launch_browser=launch_browser)
    agent = Agent(task=task, llm=llm, browser=browser)
    await agent.run()


if __name__ == '__main__':
	asyncio.run(main())
