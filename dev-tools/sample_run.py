from browser_use import Agent, Browser, BrowserConfig
from langchain_openai import ChatOpenAI
import asyncio


# Structure that stores the action tree of possible actions that 
# can be performed on an app, starting from the root url or a defined 
# page + a given state.
action_tree = {
    "url": "http://host.docker.internal:3011",
    "state": {
        "logged_in": False
    }, # state object of the page, e.g. {"logged_in": True}
    "actions": {
        "click_login_button": {
            "type": "click",
            "selector": "button[name='login']",
        },
        "click_submit_button": {
            "type": "click",
            "selector": "button[name='submit']"
        },
        "navigate_to_about_us_page": {
            "type": "navigate",
            "url": "http://host.docker.internal:3011/about-us",
            "state": {
                "logged_in": True
            },
            "actions": {
                
            }
        },
        "input_username": {
            "type": "input",
            "selector": "input[name='username']",
            "value": "testuser"
        },
        "input_password": {
            "type": "input",
            "selector": "input[name='password']",
            "value": "testpassword"
        },
    }
}

# Example of a test sequence that can be used to test the web app
# should have an expected end result or some sort of check.
# Should also include a good description & metadata so that
# we can better understand when to retest after code changes.
test_sequence_json = {
    "url": "http://host.docker.internal:3011",
    "state": {
        "logged_in": False
    },
    "actions": [
        {
            "click_login_button": {
                "selector": "button[name='login']"
            }
        },
        {
            "input_username": {
                "selector": "input[name='username']",
                "value": "testuser"
            }
        },
        {
            "input_password": {
                "selector": "input[name='password']",
                "value": "testpassword"
            }
        }
    ]
}

# Configure the browser to connect to your Chrome instance
browser = Browser(
    config=BrowserConfig(
        # Specify the path to your Chrome executable
        browser_binary_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # macOS path
        # For Windows, typically: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        # For Linux, typically: '/usr/bin/google-chrome'
    )
)

# Create the agent with your configured browser
agent = Agent(
    task="Navigate to http://host.docker.internal:3011 and list all possible links / actions on the page",
    llm=ChatOpenAI(model='gpt-4o'),
    browser=browser,
)

async def main():
    await agent.run()

    input('Press Enter to close the browser...')
    await browser.close()

if __name__ == '__main__':
    asyncio.run(main())