from dotenv import load_dotenv
from crewai import Agent, Task, Crew
import os
from crewai_tools import ScrapeWebsiteTool
from langchain_openai import ChatOpenAI
from crewai_tools import SeleniumScrapingTool
from crewai_tools import PDFSearchTool
import logging
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Load your environment variables, if necessary
load_dotenv()



# Set the environment variables for Ollama integration
# os.environ["OPENAI_API_BASE"] = 'https://ad92-212-58-120-213.ngrok-free.app/v1'
os.environ["OPENAI_API_BASE"] = 'http://localhost:11434/v1'
os.environ["OPENAI_MODEL_NAME"] = 'mistral'  # Adjust based on your available model
# os.environ["OPENAI_API_KEY"] = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMBsidDxE9m/+4xhrz+2lNCwELUAK/D/K813aPJCOXuL'  # May not be needed for local Ollama, set appropriately
os.environ["OPENAI_API_KEY"] = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMBsidDxE9m/+4xhrz+2lNCwELUAK/D/K813aPJCOXuL'

model = ChatOpenAI(model_name=os.environ["OPENAI_MODEL_NAME"], temperature=0.7)

website = [
    'https://ascensiongroup.com/',
    'https://ascensiongroup.com/about',
    'https://ascensiongroup.com/blog',
    'https://ascensiongroup.com/approach/'
]

pdf_urls = [
    "C:/Users/user/Desktop/AscensionGroup/Interviews/Duane_Tursi_interview.pdf",
    "C:/Users/user/Desktop/AscensionGroup/Interviews/Marion_interview.pdf"
]


search_query = [
"Core values"
]
pdf_search_tool = PDFSearchTool(pdf_urls=pdf_urls)

# Example 2: Scrape the entire webpage of a given URL
scrape_tool = SeleniumScrapingTool(website_urls=website,css_element="body")


brand_analyst = Agent(
    role='Brand Analyst',
    goal=f'Analyze  client and market data to extract key brand attributes, values, and differentiators',
    backstory="""An expert in extracting and interpreting key information from digital formats, this agent specializes 
             in analyzing PDF documents and website content. By using advanced NLP techniques, 
            the agent distills essential brand elements from official reports, leadership interviews in PDFs, and comprehensive website narratives. 
            This focused approach helps in forming a solid foundation for subsequent brand strategy development.""",

    verbose=True,
    tools=[scrape_tool,pdf_search_tool],  
)


brand_strategist = Agent(
    role='Brand Strategist',
    goal=f'Develop comprehensive brand platforms and strategies for ',
    backstory=""" With a knack for strategic thinking and creativity, this agent
                combines analytical insights with market trends to develop the brand
                platform elements listed above along with compelling brand narratives and
                strategies""",
    verbose=True,
    allow_delegation=False,
)

content_creator = Agent(
    role='Content Creator',
    goal=f'Generate engaging  storytelling and messaging content',
    backstory=""" A creative, copywriting powerhouse, this agent specializes in
                translating brand platform elements and strategies into captivating stories
                and messages that engage and inspire the target audience""",
    verbose=True,
    allow_delegation=False,
)

persona_developer = Agent(
    role='Persona Developer',
    goal=f'Create detailed buyer personas for  based on market research',
    backstory=""" Understanding the psyche of different market segments, this
                agent crafts detailed personas that help in tailoring brand messaging and
                campaigns to specific audience needs and preferences""",
    verbose=True,
    allow_delegation=False,
)

brand_reviewer = Agent(
    role='Brand Reviewer',
    goal=f'Ensure coherence and alignment of  materials with client objectives',
    backstory=""" With an eye for detail and a deep understanding of branding
                    principles, this agent ensures that every piece of content and strategy
                    aligns with the overarching brand vision and market positioning""",
    verbose=True,
    allow_delegation=False,
)

# Create tasks for your agents
task_analyze = Task(
    description=f"Analyze client content, including key leadership interview transcripts, "
                "existing websites content "
                "results, and competitor  to extract key brand attributes, values, "
                "and differentiators.", 
    expected_output=f"A detailed report with key  brand attributes, values, and differentiators identified.",
    # tools=[tool],  
    agent=brand_analyst,
    
)

task_analyze_pdf = Task(
    description="Analyze PDF documents to extract key information.",
    expected_output="Extracted information from multiple PDF documents.",
    agent=brand_analyst,
    tools=[pdf_search_tool]
)
# Define a task for scraping multiple URLs
task_scrape_website = Task(
    description="Scrape multiple websites to gather data about the client's online presence.",
    expected_output="A collection of texts scraped from multiple websites.",
    tools=[scrape_tool],  # Assigning the multi scrape tool
    agent=brand_analyst
)


# Create a list to hold the results of each scraping task
        
task_strategize = Task(
    description=f"Synthesize insights from the Brand Analyst to develop comprehensive "
                f"brand platforms and strategies for .",
    expected_output=f"A comprehensive brand strategy document for including vision, mission, values, and positioning.",
    agent=brand_strategist,
)

task_create_content = Task(
    description=f"Generate engaging content for  storytelling, persona specific "
                "messaging, and social media channels.",
    expected_output=f"Engaging and well-crafted brand stories and messages for suitable for various media channels.",
    agent=content_creator,
)

task_develop_persona = Task(
    description=f"Develop detailed buyer personas for based on insights and descriptions "
                "from Marketing and Sales leadership, customer survey results, and market research.",
    expected_output=f"Detailed buyer personas for  that accurately reflect the target audience's characteristics and preferences.",
    agent=persona_developer,
)

task_review_brand = Task(
    description=f"Review and refine the  platforms, credos, storytelling, and messaging "
                "to ensure coherence and alignment with client objectives.",
    expected_output=f"A refined and coherent brand platform for that aligns with the client's objectives and market positioning.",
    agent=brand_reviewer,
)

# Instantiate your crew with a sequential process
crew = Crew(
    agents=[brand_analyst, brand_strategist, content_creator, persona_developer, brand_reviewer],
    tasks=[task_scrape_website, task_analyze_pdf,task_strategize, task_create_content, task_develop_persona, task_review_brand],
    verbose=2
)

# Print the results of the scraping process

# Assuming `result` contains the output of each task, iterate and print them
# Loop through the list of URLs and scrape each one

# Start the process
result = crew.kickoff()

print("--------------------------")
print(result)

