import rich.emoji
import time
import rich
import sys
import threading
from rich.live import Live
from rich.progress import Progress
from rich.progress import BarColumn, TextColumn, TaskProgressColumn, TimeRemainingColumn, SpinnerColumn, TimeElapsedColumn
from rich.console import Group
from rich.tree import Tree

from .MCPScanner import MCPScanner


def printer(scanner):
    progress_bars = dict()
    def _draw():
        drawables = []
        if 'paths' not in scanner.result: return Group()
        for path in scanner.result['paths'].keys():
            if path not in progress_bars:
                progress = Progress(SpinnerColumn(), TextColumn(f"[bold]{path}[/bold]" +  " [gray62]{task.description}"))
                progress_bars[path] = (progress, progress.add_task(path))
            progress, task = progress_bars[path]
            
            path_status = scanner.result['paths'][path].get('status', None)
            done = scanner.result['paths'][path].get('done', False)
            progress.update(task, description=path_status, complete=done)

            drawables.append(Tree(progress))
            for server_name, _ in scanner.result['paths'][path].get('servers', {}).items():
                id = f"{path}.{server_name}"
                if id not in progress_bars:
                    progress = Progress(SpinnerColumn(), TextColumn(f"[bold]{server_name}[/bold]" + " [gray62]{task.description}"))
                    progress_bars[id] = (progress, progress.add_task(server_name))
                progress, task = progress_bars[id]

                server_status = scanner.result['paths'][path]['servers'][server_name].get('status', None)
                done = scanner.result['paths'][path]['servers'][server_name].get('done', False)
                progress.update(task, description=server_status, complete=done)
                server = drawables[-1].add(progress)

                tools = scanner.result['paths'][path]['servers'][server_name].get('tools', [])
                tools = list(map(lambda x: (*x, 'tool'), tools))
                prompts = scanner.result['paths'][path]['servers'][server_name].get('prompts', [])
                prompts  = list(map(lambda x: (*x, 'prompt'), prompts))
                resources = scanner.result['paths'][path]['servers'][server_name].get('resources', [])
                resources = list(map(lambda x: (*x, 'resource'), resources))
                for entity, status, type in tools + prompts + resources:
                    if status == 'verified':
                        status = rich.emoji.Emoji('white_heavy_check_mark')
                    elif status == 'failed':
                        status = rich.emoji.Emoji('cross_mark')
                    elif status == 'skipped':
                        pass
                    else:
                        pass
                        #status = ':warn:'
                        #status = rich.emoji.Emoji(status)
                    server.add(f'{type}: {entity.name} {status}')
        return Group(*drawables)

    with Live(_draw(), refresh_per_second=4) as live:
        while scanner.is_running():
            time.sleep(0.25)
            #progress.update(status_progress,
            #                description=f"[grey62]{scanner.result['status']['message']}")
            #live.refresh()
            live.update(_draw())
            live.refresh()
        live.update(_draw())
        live.refresh()
            #task.update(description="")

def main():
    scanner = MCPScanner() 
    # Run the scanner in a separate thread

    printer_thread = threading.Thread(target=printer, args=(scanner, ))
    printer_thread.start()
    scanner.start()
    printer_thread.join()
    
    # TODO handle ctrl-c correctly trhough threading and multiprocessing
    #print_to_terminal(scanner)
    sys.exit(0)
   
if __name__ == "__main__":
    main()