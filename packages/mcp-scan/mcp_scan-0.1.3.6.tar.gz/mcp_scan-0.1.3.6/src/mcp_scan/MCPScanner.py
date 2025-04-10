import os
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import json
import os
import asyncio
import multiprocessing as mp
import requests
import ast
import rich

from .surpressIO import SuppressStd 

def format_path_line(path, status):
    text = f"scanning [bold]{path}[/bold] [gray62]{status}[/gray62]"
    return rich.text.Text.from_markup(text)

def format_servers_line(server, status=None):
    text = f"[bold]{server}[/bold]"
    if status:
        text += f" [gray62]{status}[/gray62]"
    return rich.text.Text.from_markup(text)

def format_tool_line(tool, status, type='tool'):
    color = ''
    if status.startswith('failed'):
        color = '[red]'
        status = status.replace('failed', ':cross_mark:')
    elif status.startswith('verified'):
        color = '[green]'
        status = status.replace('verified', ':white_heavy_check_mark:')
    name = tool.name
    if len(name) > 25:
        name = name[:22] + '...'
    name = name + ' ' * (25 - len(name))
    text = f'{type} {color}[bold]{name}[/bold] {status}'
    text = rich.text.Text.from_markup(text)
    return text

WELL_KNOWN_MCP_PATHS = [
   '~/.codeium/windsurf/mcp_config.json', # windsurf
   '~/.cursor/mcp.json', # cursor
   '~/Library/Application Support/Claude/claude_desktop_config.json', # Claude Desktop
]

# TODO locally store hashes
# TODO data kraken

policy = """
from invariant.detectors import prompt_injection

raise "tool description contains prompt injection" if:
    (msg: Message)
    prompt_injection(msg.content)

raise "attempted instruction overwrite" if:
    (msg: Message)
    '<IMPORTANT>' in msg.content
"""

def verify_server(tools, prompts, resources):
    if len(tools) == 0:
        return []
    messages = [
        {'role': 'system',
         'content': f"Tool Name:{tool.name}\nTool Description:{tool.description}"}
        for tool in tools
    ]
    url = "https://explorer.invariantlabs.ai/api/v1/policy/check"
    api_key = os.environ.get('INVARIANT_API_KEY')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + api_key
    }
    data = {
        'messages': messages,
        'policy': policy,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response = response.json()
        with open('policy.txt', 'w') as f:
            json.dump(policy, f)
        json.dump(response, open('response.json', 'w'))
        json.dump(messages, open('messages.json', 'w'))
        results = [(True, 'verified') for _ in tools]
        for error in response['errors']:
            key = ast.literal_eval(error['key'])
            idx = key[1][0]
            results[idx] = (False, 'failed - ' + ' '.join(error['args']))
        return results
    else:
        print(f"Error: {response.status_code}")
        return [(True, 'verified') for _ in tools]

async def check_server(server_config):
    server_params = StdioServerParameters(
            **server_config
    )
    with SuppressStd():
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                try:
                    prompts = await session.list_prompts()
                    prompts = list(prompts.prompts)
                except:
                    prompts = []
                try:
                    resources = await session.list_resources()
                    resources = list(resources.resources)
                except:
                    resources = []
                try :
                    tools = await session.list_tools()
                    tools = list(tools.tools)
                except:
                    tools = []
    # TODO timeout
    return prompts, resources, tools

def run_check_server(server_config):
    # Move your async logic into a synchronous function or adjust your async function.
    return asyncio.run(check_server(server_config))

def scan_config_file(path):
    path = os.path.expanduser(path)
    with open(path, 'r') as f:
        config = json.load(f)
        servers = config.get('mcpServers')
        return servers

class MCPScanner:
    def __init__(self):
        self.paths = WELL_KNOWN_MCP_PATHS
   
    def scan(self, path):
        try:
            servers = scan_config_file(path)
            status = f"found {len(servers)} servers"
        except FileNotFoundError:
            status = f"file not found"
            return
        except json.JSONDecodeError:
            status = f"invalid json"
            return
        finally:
            rich.print(format_path_line(path, status))

        path_print_tree = rich.tree.Tree('│')
        for server_name, server_config in servers.items():
            try:
                prompts, resources, tools = asyncio.run(check_server(server_config))
                status = None
            except Exception as e:
                status = str(e).splitlines()[0] + '...'
                continue
            finally:
                server_print = path_print_tree.add(format_servers_line(server_name, status))
            verification_result = verify_server(tools, prompts, resources)
            for tool, (verified, status) in zip(tools, verification_result):
                server_print.add(format_tool_line(tool, status))
            for prompt in prompts:
                server_print.add(format_tool_line(prompt, 'skipped', type='prompt'))
            for resource in resources:
                server_print.add(format_tool_line(resource, 'skipped', type='resource'))

        if len(servers) > 0:
            rich.print(path_print_tree)
            
    def start(self):
        for i, path in enumerate(self.paths):
            self.scan(path)
            if i < len(self.paths) - 1:
                rich.print('')
