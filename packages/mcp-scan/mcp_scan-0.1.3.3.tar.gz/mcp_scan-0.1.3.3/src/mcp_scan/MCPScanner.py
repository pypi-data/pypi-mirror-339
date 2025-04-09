import os
import sys
from contextlib import redirect_stdout, redirect_stderr
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import json
import os
import asyncio
from termcolor import colored
import itertools
import time
import multiprocessing as mp
import requests
import ast

from .surpressIO import SuppressStd 

WELL_KNOWN_MCP_PATHS = [
   '~/.codeium/windsurf/mcp_config.json', # windsurf
   '~/.cursor/mcp.json', # cursor
   '~/Library/Application Support/Claude/claude_desktop_config.json', # Claude Desktop
]

policy = """
from invariant.detectors import prompt_injection

raise "tool description contains prompt injection" if:
    (msg: Message)
    '<IMPORTANT>' in msg.content
"""


def verify_server(tools):
    if len(tools) == 0:
        return []
    messages = [
        {'role': 'system',
         'content': tool.description}
        for tool, _ in tools
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
    with open('debug.json', 'w') as f:
        json.dump(data, f)
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response = response.json()
        results = [True for _ in tools]
        for error in response['errors']:
            key = ast.literal_eval(error['key'])
            idx = key[0]
            results[idx] = False
        return results
    else:
        print(f"Error: {response.status_code}")
        results = [True for _ in tools]

async def check_server(server_config):
    server_params = StdioServerParameters(
            **server_config
    )
    with SuppressStd():
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                prompts = await session.list_prompts()
                resources = await session.list_resources()
                tools = await session.list_tools()
                prompts = list(prompts.prompts)
                resources = list(resources.resources)
                tools = list(tools.tools)
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
        self._running = False
        self.result = dict()
        
    def _traverse_paths(self):
        active_paths = []
        for path in self.paths:
            is_active_path = False
            try:
                self.result['paths'][path]['servers'] = scan_config_file(path)
                n_servers = len(self.result["paths"][path]["servers"])
                self.result['paths'][path]['status'] = f'found {n_servers} servers'
                if n_servers > 0:
                    active_paths.append(path)
                else:
                    self.result['paths'][path]['done'] = False
            except FileNotFoundError:
                self.result['paths'][path]['status'] = f'File not found'
                self.result['paths'][path]['done'] = True
            except json.JSONDecodeError:
                self.result['paths'][path]['done'] = True
        return active_paths

    def _retrieve_tools(self, active_paths):
        configs = []
        job_results = []
        for path in active_paths:
            servers = self.result['paths'][path]['servers']
            self.result['paths'][path]['status'] = f'{len(servers)} servers - fetching tools'
            for server_name, server_config in servers.items():
                self.result['paths'][path]['servers'][server_name]['status'] = 'fetching tools'
                configs.append((path, server_name, server_config))
        with mp.Pool(processes=1) as pool:
            job_results = pool.map(run_check_server, map(lambda x: x[2], configs))
        n_entity_per_path = {} 
        for (path, server_name, _), (prompts, resources, tools) in zip(configs, job_results):
            self.result['paths'][path]['servers'][server_name]['tools'] = [(t, '') for t in tools]
            self.result['paths'][path]['servers'][server_name]['prompts'] = [(p, '') for p in prompts]
            self.result['paths'][path]['servers'][server_name]['resources'] = [(r, '') for r in resources]
            n_tools = len(tools)
            n_prompts = len(prompts)
            n_resources = len(resources)
            if path not in n_entity_per_path: n_entity_per_path[path] = {}
            if server_name not in n_entity_per_path[path]: n_entity_per_path[path][server_name] = 0
            n_entity_per_path[path][server_name] = n_entity_per_path[path].get(server_name, 0) + n_tools + n_prompts + n_resources
            self.result['paths'][path]['servers'][server_name]['status'] = f'{n_tools} tools, {n_prompts} prompts, {n_resources} resources'

        new_active_paths = []
        active_servers = {}
        for path in active_paths:
            active_servers[path] = []
            for server, count in n_entity_per_path[path].items():
                if count > 0:
                    active_servers[path].append(server)
                else:
                    self.result['paths'][path]['servers'][server]['done'] = True
            if len(active_servers[path]) > 0:
                new_active_paths.append(path)
            else:
                self.result['paths'][path]['done'] = True
        return new_active_paths, active_servers

       

    def start(self):
        if self.is_running(): return
        self._running = True

        self.result['paths'] = {}
        for path in self.paths:
            self.result['paths'][path] = dict()
            self.result['paths'][path]['status'] = 'checking file'

        # traverse the paths for config files and retrieve servers listed there
        # active_paths are those that have a config file and at least one server
        active_paths = self._traverse_paths()

        # retrieve tools
        # active paths have at least one active (reachable) server
        # active servers have at least one tool/prompt/resource
        active_paths, active_servers = self._retrieve_tools(active_paths)


        for path in active_paths:
            self.result['paths'][path]['status'] += ' - verifying'
            for server_name in active_servers[path]:
                self.result['paths'][path]['servers'][server_name]['status'] += ' - verifying'

                tools = self.result['paths'][path]['servers'][server_name]['tools']
                prompts = self.result['paths'][path]['servers'][server_name]['prompts']
                resources = self.result['paths'][path]['servers'][server_name]['resources']
                tools_verified = verify_server(tools)

                for i, (tool, _) in enumerate(self.result['paths'][path]['servers'][server_name]['tools']):
                    self.result['paths'][path]['servers'][server_name]['tools'][i] = (tool, 'verified' if tools_verified[i] else 'failed')
                for i, (prompt, _) in enumerate(self.result['paths'][path]['servers'][server_name]['prompts']):
                    self.result['paths'][path]['servers'][server_name]['prompts'][i] = (prompt, 'skipped')
                for i, (resource, _) in enumerate(self.result['paths'][path]['servers'][server_name]['resources']):
                    self.result['paths'][path]['servers'][server_name]['resources'][i] = (resource, 'skipped')
            
        self._running = False
        
    def is_running(self):
        return self._running
        
    
    
