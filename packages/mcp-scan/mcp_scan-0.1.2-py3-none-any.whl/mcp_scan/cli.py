import resource
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import json
import os
import asyncio
from termcolor import colored
from alive_progress import alive_bar
import sys
import tempfile
import io
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO

# Inspired from the following SO answer
# https://stackoverflow.com/questions/24277488/in-python-how-to-capture-the-stdout-from-a-c-shared-library-to-a-variable/57677370#57677370
import io
import os
import sys
import tempfile


class SuppressStd(object):
    """Context to capture stderr and stdout at C-level.
    """

    def __init__(self):
        self.orig_stdout_fileno = sys.__stdout__.fileno()
        self.orig_stderr_fileno = sys.__stderr__.fileno()
        self.output = None

    def print(self, *args, **kwargs):
        # Redirect the print to the original stdout
        print(*args, **kwargs, file=sys.__stdout__)

    def __enter__(self):
        # Redirect the stdout/stderr fd to temp file
        self.orig_stdout_dup = os.dup(self.orig_stdout_fileno)
        self.orig_stderr_dup = os.dup(self.orig_stderr_fileno)
        self.tfile = tempfile.TemporaryFile(mode='w+b')
        os.dup2(self.tfile.fileno(), self.orig_stdout_fileno)
        os.dup2(self.tfile.fileno(), self.orig_stderr_fileno)

        # Store the stdout object and replace it by the temp file.
        self.stdout_obj = sys.stdout
        self.stderr_obj = sys.stderr
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        return self

    def __exit__(self, exc_class, value, traceback):

        # Make sure to flush stdout
        print(flush=True)

        # Restore the stdout/stderr object.
        sys.stdout = self.stdout_obj
        sys.stderr = self.stderr_obj

        # Close capture file handle
        os.close(self.orig_stdout_fileno)
        os.close(self.orig_stderr_fileno)

        # Restore original stderr and stdout
        os.dup2(self.orig_stdout_dup, self.orig_stdout_fileno)
        os.dup2(self.orig_stderr_dup, self.orig_stderr_fileno)

        # Close duplicate file handle.
        os.close(self.orig_stdout_dup)
        os.close(self.orig_stderr_dup)

        # Copy contents of temporary file to the given stream
        #self.tfile.flush()
        #self.tfile.seek(0, io.SEEK_SET)
        #self.output = self.tfile.read().decode()
        #self.tfile.close()

WELL_KNOWN_MCP_PATHS = [
   '~/.codeium/windsurf/mcp_config.json', # windsurf
   '~/.cursor/mcp.json', # cursor
   '~/Library/Application Support/Claude/claude_desktop_config.json', # Claude Desktop
]

async def check_server(server_name, server_config):
    with SuppressStd() as suppress:
        server_params = StdioServerParameters(
                **server_config
        )
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(
                read,
                write
            ) as session:
                await session.initialize()
                prompts = await session.list_prompts()
                resources = await session.list_resources()
                tools = await session.list_tools()
                prompts = list(prompts.prompts)
                resources = list(resources.resources)
                tools = list(tools.tools)
        return prompts, resources, tools

def scan(path):
    try:
        path = os.path.expanduser(path)
        with open(path, 'r') as f:
            config = json.load(f)
            print(colored(f"{path}", 'cyan', attrs=['bold']), end='')
            servers = config.get('mcpServers')
            print(colored(f" {len(servers)} servers", 'cyan'))
    except FileNotFoundError as e:
        #print(colored(f"File not found: {path}", 'red'))
        return
    except json.JSONDecodeError as e:
        print(colored(f"\tError decoding JSON from file: {path}", 'red'))
        return

    if servers:
        for server_name, server_config in servers.items():
            print(colored(f"\t+ {server_name}", 'yellow', attrs=['bold']))
            try: 
                #with alive_bar(1, spinner='dots', bar=None, title="Checking server") as bar:
                prompts, resources, tools = asyncio.run(check_server(server_name, server_config))
                #    bar()
                for prompt in prompts:
                    print(colored(f"\t\t+ prompt: {prompt.name}", 'yellow'))
                for resource in resources:
                    print(colored(f"\t\t+ resource: {resource.name}", 'yellow'))
                for tool in tools:
                    print(colored(f"\t\t+ tool: {tool.name}", 'yellow'))
            except Exception as e:
                print(colored(f"Error connecting to {server_name}: {e}", 'red'))
                continue

def main():
    for path in WELL_KNOWN_MCP_PATHS:
        #print(f"Checking {path}")
        scan(path)

if __name__ == "__main__":
    main()