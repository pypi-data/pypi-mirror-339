from langchain_core.tools import Tool
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor
from langchain_openai import AzureChatOpenAI
import trafilatura
import requests

# Load environment variables from a .env file
load_dotenv()

# Function to perform a search using the SearxNG search engine
def searxng_search(query: str) -> str:
    """
    This function performs a search using the SearxNG search engine.

    Parameters:
    - query: The search query string.

    Functionality:
    1. Sends a GET request to the SearxNG API with the query and specified parameters.
    2. Extracts the top 10 search results from the API response.
    3. Formats the results into a readable string containing the title, URL, and content of each result.

    Returns:
    - A formatted string of search results or an error message if the search fails.
    """
    base_url = "https://searxng.vbi-server.com"  # Base URL for the SearxNG instance
    params = {
        "q": query,  # Query string
        "format": "json",  # Response format
        "language": "en",  # Language for the search results
        "categories": "general"  # Search categories
    }

    try:
        # Send a GET request to the SearxNG API
        response = requests.get(f"{base_url}/search", params=params, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()  # Parse the JSON response

        # Extract the top 5 results
        results = data.get("results", [])[:10]
        if not results:
            return "No relevant results found."  # Return a message if no results are found

        # Format the results into a readable string
        return "\n\n".join([f"{r['title']}\n{r['url']}\n{r['content']}" for r in results])

    except Exception as e:
        # Handle exceptions and return an error message
        return f"Error during search: {str(e)}"
    
def draw_from_url(url: str) -> str:
    """
    This function retrieves and extracts the main content from a given URL.

    Parameters:
    - url: The URL to fetch and extract content from.

    Functionality:
    1. Fetches the content of the URL using the `trafilatura` library.
    2. Extracts the main content while excluding comments and tables.
    3. Limits the extracted content to 8000 characters for brevity.

    Returns:
    - The extracted content as a string or an error message if the process fails.
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            extracted = trafilatura.extract(downloaded, include_comments=False, include_tables=False)
            return extracted[:8000] if extracted else "Unable to extract useful content."
        else:
            return "Unable to retrieve content from the URL."
    except Exception as e:
        return f"Error accessing {url}: {str(e)}"


# Function to perform fact-checking using the AzureChatOpenAI model
def fact_check(llm: AzureChatOpenAI , claims: str) -> str:
    """
    This function performs fact-checking on a list of claims using a language model (LLM) and tools.

    Parameters:
    - llm: The AzureChatOpenAI language model used for processing.
    - claims: A string containing the claims to be fact-checked.

    Functionality:
    1. Defines two tools:
       - `search_tool`: Uses the SearxNG search engine to find relevant information.
       - `draw_tool`: Extracts detailed content from URLs if search results are insufficient.
    2. Binds the tools to the LLM for enhanced functionality.
    3. Constructs a detailed query for fact-checking, including instructions and guidelines.
    4. Creates an agent with the tools and query to process the claims.
    5. Executes the agent and returns the fact-checking results.

    Returns:
    - A string containing the fact-checking results in Markdown format.
    """
    # Create a search tool using the SearxNG search function
    search_tool = Tool.from_function(
        name="search_tool",
        description="Search for factual information from the internet to verify the authenticity of statements.",
        func=searxng_search
    )

    draw_tool = Tool.from_function(
        name="draw_tool",
        description="Used to retrieve and extract the main content of a URL if search_tool does not provide sufficient information.",
        func=draw_from_url
    )

    tools = [search_tool,draw_tool]

    # Bind the search tool to the language model
    llm_with_tools = llm.bind_tools(tools)

    # Define the query for fact-checking
    query = """
    <verification_task>
        <role>You are an assistant for fact-checking information.</role>
        <instruction>
            Use the tool <tool>search_tool</tool> to verify whether the statements below are <b>true or false</b>, 
            then <b>explain clearly</b> by <b>citing specific evidence from reliable sources</b>.
            If the information from <tool>search_tool</tool> is <b>not detailed enough</b> to draw a conclusion, you can use <tool>draw_tool</tool> to retrieve full content from any URL in the search results.
        </instruction>
        
        <tool_usage>
            <description>How to use <code>search_tool</code> and <code>draw_tool</code>:</description>

            <search>
                <tool><b>search_tool</b></tool> is used to find sources related to the statement to be verified.
                Returns a list of <code>results</code>, which can be reformatted as:
                <format>
                    "\\n\\n".join([f"{r['title']}\\n{r['url']}\\n{r['content']}" for r in results])
                </format>
            </search>

            <draw>
                <tool><b>draw_tool</b></tool> is used to extract detailed content from a webpage, based on a URL in the results of <code>search_tool</code>.
                Only use when the information from <code>search_tool</code> is <b>ambiguous, unclear, or too short</b> to draw a conclusion.
                For example, if <code>search_tool</code> only provides a title and a short description, but you need the original content to verify data or context, call <code>draw_tool</code> with the corresponding URL.
            </draw>
        </tool_usage>

        <guidelines>
            <step>1. If the statement contains <b>numbers, dates, names, or specific events</b>, prioritize verifying the <b>accuracy of those details</b>.</step>
            <step>2. If the statement does not contain specific numbers, verify the <b>overall accuracy of the content</b>.</step>
            <step>
                3. <b>Only use reliable sources</b>, for example:
                <sources>
                    <source>Official news websites (.vn, .com, .net, .org, .gov, .edu)</source>
                    <source>Government websites, international organizations, research institutes</source>
                    <source>Do not use Wikipedia or user-contributed sites</source>
                </sources>
            </step>
            <step>4. If <b>verification is not possible</b>, state clearly <i>Unable to verify</i> and explain why.</step>
        </guidelines>

        <note>
            When processing information related to time, note that the current date is April 2025.  
            For proper names, especially common or ambiguous ones, search with context or related information (such as organization, field, specific role) to ensure correct identification.
        </note>

        <output_format>
            For each statement, return the result in Markdown format:
            - **Statement:** The content to be verified
            - **Result:** ✅ True / ❌ False / ⚠️ Unable to verify
            - **Source:** (URL or name of a reliable source)
            - **Evidence:** (Specific citation from the source to explain the conclusion)
        </output_format>

        <example>
            - **Statement:** The Earth is flat.
            - **Result:** ❌ False
            - **Source:** https://www.nasa.gov/mission_pages/planetearth/shape
            - **Evidence:** According to NASA, satellite images show that the Earth is spherical, not flat.
        </example>

        <claims>
            <!-- Below is the list of statements to be verified, each statement on one line -->
            <insert_here>
    """ + claims + """
            </insert_here>
        </claims>
    </verification_task>
    """

    # Create a chat prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are very powerful assistant, but don't know current events",
            ),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    # Define the agent with the prompt and tools
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
    )

    # Create an agent executor to run the agent
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)
    response = agent_executor.invoke({"input": query})
    markdown_output = response["output"]
    print(markdown_output)
    return markdown_output

# Main function to execute the fact-checking
if __name__ == "__main__":

    from langchain_openai import AzureChatOpenAI
    import os
    import extract_module

    # Initialize the AzureChatOpenAI model with API credentials and settings
    llm = AzureChatOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        model="o3-mini", 
        api_version="2024-12-01-preview",
        # temperature=0.7,
        # max_tokens=16000
    )

    pdf_path = "data/tc13.pdf"

    text = extract_module.extract_text(pdf_path)
    # print(text)
    claims = extract_module.extract_claim(llm,text)
    print(claims)
    # Perform fact-checking and print the result
    fact_check(llm,claims)