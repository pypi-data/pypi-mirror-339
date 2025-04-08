from langchain_core.tools import Tool
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor
import trafilatura
import requests

# Load environment variables from a .env file
load_dotenv()

# Function to perform a search using the SearxNG search engine
def searxng_search(query: str) -> str:
    base_url = "https://searxng.vbi-server.com"  # Base URL for the SearxNG instance
    params = {
        "q": query,  # Query string
        "format": "json",  # Response format
        "language": "vi",  # Language for the search results
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
            return "Không tìm thấy kết quả phù hợp."  # Return a message if no results are found

        # Format the results into a readable string
        return "\n\n".join([f"{r['title']}\n{r['url']}\n{r['content']}" for r in results])

    except Exception as e:
        # Handle exceptions and return an error message
        return f"Lỗi khi tìm kiếm: {str(e)}"
    
def draw_from_url(url: str) -> str:
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            extracted = trafilatura.extract(downloaded, include_comments=False, include_tables=False)
            return extracted[:8000] if extracted else "Không trích xuất được nội dung có ích."
        else:
            return "Không truy xuất được nội dung từ URL."
    except Exception as e:
        return f"Lỗi khi truy cập {url}: {str(e)}"


# Function to perform fact-checking using the AzureChatOpenAI model
def FactCheck(llm , claims: str) -> str:

    # Create a search tool using the SearxNG search function
    search_tool = Tool.from_function(
        name="search_tool",
        description="Tìm kiếm thông tin thực tế từ internet để kiểm tra tính xác thực của phát biểu.",
        func=searxng_search
    )

    draw_tool = Tool.from_function(
        name="draw_tool",
        description="Dùng để truy xuất và trích xuất nội dung chính của một URL nếu search_tool không cung cấp đủ thông tin.",
        func=draw_from_url
    )

    tools = [search_tool,draw_tool]

    # Bind the search tool to the language model
    llm_with_tools = llm.bind_tools(tools)

    # Define the query for fact-checking
    query = """
    <verification_task>
        <role>Bạn là một trợ lý kiểm chứng thông tin.</role>
        <instruction>
            Hãy dùng công cụ <tool>search_tool</tool> để kiểm tra các phát biểu dưới đây là <b>đúng hay sai</b>, 
            sau đó <b>giải thích rõ ràng</b> bằng cách <b>trích dẫn dẫn chứng cụ thể từ nguồn đáng tin cậy</b>.
            Nếu thông tin từ <tool>search_tool</tool> là <b>chưa đủ chi tiết</b> để đưa ra kết luận, bạn có thể dùng thêm <tool>draw_tool</tool> để truy xuất nội dung đầy đủ từ một URL bất kỳ trong kết quả tìm kiếm.
        </instruction>
        
        <tool_usage>
            <description>Cách sử dụng <code>search_tool</code> và <code>draw_tool</code>:</description>

            <search>
                <tool><b>search_tool</b></tool> dùng để tìm các nguồn tin liên quan đến phát biểu cần kiểm chứng.
                Trả về danh sách <code>results</code>, có thể định dạng lại bằng:
                <format>
                    "\\n\\n".join([f"{r['title']}\\n{r['url']}\\n{r['content']}" for r in results])
                </format>
            </search>

            <draw>
                <tool><b>draw_tool</b></tool> dùng để trích xuất nội dung chi tiết từ một trang web, dựa vào URL có trong kết quả của <code>search_tool</code>.
                Chỉ sử dụng khi thông tin từ <code>search_tool</code> là <b>mơ hồ, chưa rõ ràng hoặc quá ngắn</b> để đưa ra kết luận.
                Ví dụ, nếu <code>search_tool</code> chỉ cung cấp tiêu đề và đoạn mô tả ngắn, nhưng bạn cần nội dung gốc để kiểm tra số liệu hoặc ngữ cảnh, hãy gọi <code>draw_tool</code> với URL tương ứng.
            </draw>
        </tool_usage>

        <guidelines>
            <step>1. Nếu phát biểu chứa <b>số liệu, ngày tháng, tên người, sự kiện cụ thể</b>, hãy ưu tiên kiểm tra <b>độ chính xác của các chi tiết đó</b>.</step>
            <step>2. Nếu phát biểu không có số liệu cụ thể, hãy kiểm tra <b>độ chính xác tổng thể của nội dung</b>.</step>
            <step>
                3. <b>Chỉ sử dụng các nguồn tin cậy</b>, ví dụ:
                <sources>
                    <source>Trang báo chí chính thống (.vn, .com, .net, .org, .gov, .edu)</source>
                    <source>Trang chính phủ, tổ chức quốc tế, viện nghiên cứu</source>
                    <source>Không sử dụng Wikipedia hoặc các trang có đóng góp từ người dùng</source>
                </sources>
            </step>
            <step>4. Nếu <b>không thể xác minh</b>, hãy ghi rõ là <i>Không xác minh được</i> và giải thích lý do.</step>
        </guidelines>

        <note>
            Khi xử lý các thông tin có liên quan đến thời gian, cần lưu ý rằng thời điểm hiện tại là tháng 4 năm 2025.  
            Đối với các tên riêng, đặc biệt là những cái tên phổ biến hoặc dễ gây nhầm lẫn, hãy tìm kiếm kèm theo bối cảnh hoặc thông tin liên quan (như tổ chức, lĩnh vực, vai trò cụ thể) để đảm bảo xác định đúng cá nhân.
        </note>

        <output_format>
            Với mỗi phát biểu, hãy trả ra kết quả gồm 3 phần, trình bày bằng Markdown:
            <fields>
                <field><b>Phát biểu:</b> nội dung cần kiểm chứng</field>
                <field><b>Kết quả:</b> ✅ Đúng / ❌ Sai / ⚠️ Không xác minh được</field>
                <field><b>Nguồn tin:</b> (URL hoặc tên nguồn đáng tin cậy)</field>
                <field><b>Dẫn chứng:</b> (Trích dẫn cụ thể từ nguồn để giải thích kết luận)</field>
            </fields>
        </output_format>

        <example>
            <statement><b>Phát biểu:</b> Trái đất là mặt phẳng.</statement>
            <result><b>Kết quả:</b> ❌ Sai</result>
            <source><b>Nguồn tin:</b> https://www.nasa.gov/mission_pages/planetearth/shape</source>
            <evidence><b>Dẫn chứng:</b> Theo NASA, các hình ảnh từ vệ tinh cho thấy Trái đất có hình cầu, không phải mặt phẳng.</evidence>
        </example>

        <claims>
            <!-- Dưới đây là danh sách các phát biểu cần kiểm chứng -->
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
    response = agent_executor.invoke({"input":query})
    with open("output/fact_check_result.txt", "w", encoding = "utf-8") as f:
        f.write(response['output'])
    return response["output"]

# Main function to execute the fact-checking
if __name__ == "__main__":

    from langchain_openai import AzureChatOpenAI
    import os
    import extract


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

    text = extract.extract_text(pdf_path)
    # print(text)
    claims = extract.extract_claim(llm,text)
    print(claims)
    # Perform fact-checking and print the result
    FactCheck(llm,claims)

'''
không update data realtime
tên riêng seach kèm công việc và các thông tin khác tránh nhằm người trùng tên
'''