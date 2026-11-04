
#from httpx import stream
from mcp import ClientSession, StdioServerParameters, types
from mcp.client import stdio
from mcp.client.stdio import stdio_client
#from mcp.client.streamable_http import streamablehttp_client
from mcp.client.streamable_http import streamable_http_client

import asyncio


from pydantic import AnyUrl


# create server parameters for stdio connection
# server_params = StdioServerParameters(
#     command="uv",
#     args = ["run", "mcp", "run", "server.py"],
#  )

server_params = StdioServerParameters(
    command="uv",
    args = ["run", "python", "server.py"],
 )

# create a run function 
async def run():
    async with stdio_client(server_params) as (read,write):
        async with ClientSession(read, write) as session:
            # 1. intialise (create a new client session)
            await session.initialize()
            
            # 2. List available prompts
            prompts = await session.list_prompts()
            print(f"Available Prompts: {[p.name for p in prompts.prompts]}")
            
            # 3. Retrieve a prompt by name
            if prompts.prompts:
                prompt = await session.get_prompt("summarize_note", arguments={"name":"October 12"})
                print(f"Retrieved Prompt :{prompt.messages[0].content}")
            
            # 4. List available tools
            tools = await session.list_tools()
            print(f"Available Tools: {[t.name for t in tools.tools]}")
            
            # 5. Retrieve a tool by name
            result = await session.call_tool(
                "add_note", 
                arguments={
                    "name":"October 13", 
                    "content":"This is a reference note."
                    }
                )
            
            if result.content:
                result_unstructured = result.content[0]

                if isinstance(result_unstructured, types.TextContent):
                    print(f"Result of add_note: {result_unstructured.text}")

            # Read structured response
            result_structured = result.structured_content

            print(f"Structured Result: {result_structured}")
            
            # 6. List available resources
            resources = await session.list_resources()
            print(f"Available Resources: {[r.uri for r in resources.resources]}")

        
            # 7. Retrieve a resource by name
            resource_content = await session.read_resource(f"note://reference")
            content_block = resource_content.contents[0]
            if isinstance(content_block, types.TextContent):
                print(f"Retrieved Resource 'note://reference': {content_block.text}")


            resource_templates = await session.list_resource_templates()

            print(
                "Available Resource Templates:",
                [r.uri_template for r in resource_templates.resource_templates]
            )


            # List static resources
            resources = await session.list_resources()

            print(
                "Available Resources:",
                [r.uri for r in resources.resources]
            )

            # List dynamic resource templates
            resource_templates = await session.list_resource_templates()

            print(
                "Available Resource Templates:",
                [r.uri_template for r in resource_templates.resource_templates]
            )

            for resource in resource_templates.resource_templates:
                    print("Resource URI:", resource.uri_template)

            # Read a resource
            resource_content = await session.read_resource(
                "note://October%2013"
            )



                        
            # 8. Call/run the tool (example: add_note)
            if any(tool.name == "add_note" for tool in tools.tools):
                result = await session.call_tool(
                    "add_note", 
                    arguments={
                        "name": "Test Note", 
                        "content": "This is a test note."
                        }
                    )
                
                print("Result of add_note:", result)
                result_unstructured = result.content[0]
                if isinstance(result_unstructured, types.TextContent):
                    print(f"Tool result: {result_unstructured.text}")
                result_structured = result.structured_content
                print(f"Structured tool result: {result_structured}")

        
        
        
       


# 1. intialise (create a new client session)
# 2. List available propmts
# 3. Retrieve a prompt by name
# 4. List available tools
# 5. Retrieve a tool by name
# 6. list available resources
# 7. Retrieve a resource by name
# 8. call/run the tool

# main method 
# call run


def main():
    asyncio.run(run())


if __name__ == "__main__":

    main()