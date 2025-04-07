#!/usr/bin/env python3

import os
import sys
import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt
from rich.columns import Columns
from rich.text import Text

from oratools.tools.youtube_downloader import download_youtube_video, download_youtube_audio
from oratools.tools.image_tools import compress_image
from oratools.tools.network_tools import check_website_status, get_public_ip, ping_host, port_scan, lookup_dns
from oratools.tools.file_tools import search_text_in_files
from oratools.tools.system_tools import get_system_info, analyze_disk_usage

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header():
    clear_screen()
    logo = pyfiglet.figlet_format("ORATOOLS", font="slant")
    console.print(f"[yellow]{logo}[/yellow]")
    console.print(Panel("[green]Stuff That I Actually Use A Lot[/green]", expand=False))

def display_menu():
    display_header()
    
    categories = {
        "Download": [
            "Download YouTube Video",
            "Download YouTube Audio",
        ],
        "Media": [
            "Compress Image",
        ],
        "Network": [
            "Check Website Status",
            "Get Public IP",
            "Ping/Latency Check",
            "Port Scanner",
            "DNS Lookup",
        ],
        "System": [
            "System Information",
            "Disk Usage Analysis",
        ],
        "Files": [
            "Search Text in Files",
            "Exit"
        ]
    }

    # Map tool index to function
    tool_map = {}
    index = 1
    
    category_displays = []
    for category, tools in categories.items():
        tool_texts = []
        tool_texts.append(Text(f"[bold cyan]{category}:[/bold cyan]"))
        
        for tool in tools:
            if tool != "Exit":
                tool_map[index] = (category, tool)
                tool_texts.append(Text(f"  [bold green]{index}.[/bold green] {tool}"))
                index += 1
            else:
                exit_index = index
                tool_texts.append(Text(f"  [bold green]{index}.[/bold green] {tool}"))
                index += 1
                
        category_displays.append("\n".join([str(t) for t in tool_texts]))
    
    # Display categories side by side
    console.print(Columns(category_displays))
    console.print()
    
    return tool_map, exit_index

def main():
    while True:
        tool_map, exit_index = display_menu()
        
        try:
            choice = IntPrompt.ask("Select an option", default=exit_index)
            
            if choice < 1 or choice > exit_index:
                console.print("[bold red]Invalid option. Please try again.[/bold red]")
                continue
                
            if choice == exit_index:  # Exit option
                console.print("[bold yellow]Exiting ORATOOLS. Goodbye![/bold yellow]")
                sys.exit(0)
                
            execute_tool(choice, tool_map[choice])
            
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Exiting ORATOOLS. Goodbye![/bold yellow]")
            sys.exit(0)
        except Exception as e:
            console.print(f"[bold red]Error: {str(e)}[/bold red]")
            
        console.print("Press Enter to continue...")
        input()

def execute_tool(choice, tool_info):
    clear_screen()
    category, tool_name = tool_info
    
    if tool_name == "Download YouTube Video":
        url = console.input("[bold]Enter YouTube URL: [/bold]")
        output_path = console.input("[bold]Enter output path (default: current directory): [/bold]")
        if not output_path:
            output_path = os.getcwd()
        
        console.print("[bold cyan]Downloading video...[/bold cyan]")
        result = download_youtube_video(url, output_path)
        console.print(f"[bold green]Download complete: {result}[/bold green]")
        
    elif tool_name == "Download YouTube Audio":
        url = console.input("[bold]Enter YouTube URL: [/bold]")
        output_path = console.input("[bold]Enter output path (default: current directory): [/bold]")
        if not output_path:
            output_path = os.getcwd()
        
        console.print("[bold cyan]Extracting audio...[/bold cyan]")
        result = download_youtube_audio(url, output_path)
        console.print(f"[bold green]Download complete: {result}[/bold green]")
        
    elif tool_name == "Compress Image":
        image_path = console.input("[bold]Enter image path: [/bold]")
        quality = console.input("[bold]Enter quality (1-100, default: 80): [/bold]")
        quality = int(quality) if quality else 80
        
        console.print("[bold cyan]Compressing image...[/bold cyan]")
        result = compress_image(image_path, quality)
        console.print(f"[bold green]Image compressed: {result}[/bold green]")
        
    elif tool_name == "Check Website Status":
        url = console.input("[bold]Enter website URL: [/bold]")
        
        console.print("[bold cyan]Checking website status...[/bold cyan]")
        status, response_time = check_website_status(url)
        console.print(f"[bold]Status:[/bold] {status}")
        console.print(f"[bold]Response time:[/bold] {response_time:.2f} seconds")
        
    elif tool_name == "Get Public IP":
        console.print("[bold cyan]Fetching public IP...[/bold cyan]")
        ip = get_public_ip()
        console.print(f"[bold]Your public IP:[/bold] {ip}")
        
    elif tool_name == "Search Text in Files":
        search_text = console.input("[bold]Enter text to search for: [/bold]")
        search_dir = console.input("[bold]Enter directory to search in (default: current directory): [/bold]")
        if not search_dir:
            search_dir = os.getcwd()
        
        console.print("[bold cyan]Searching...[/bold cyan]")
        results = search_text_in_files(search_text, search_dir)
        
        if results:
            console.print(f"[bold green]Found in {len(results)} files:[/bold green]")
            for file_path, lines in results.items():
                console.print(f"[bold]{file_path}[/bold]")
                for line_num, line in lines:
                    console.print(f"  Line {line_num}: {line.strip()}")
        else:
            console.print("[bold yellow]No matches found.[/bold yellow]")
            
    elif tool_name == "Ping/Latency Check":
        host = console.input("[bold]Enter hostname or IP to ping: [/bold]")
        count = console.input("[bold]Enter number of pings (default: 4): [/bold]")
        count = int(count) if count else 4
        
        console.print(f"[bold cyan]Pinging {host}...[/bold cyan]")
        results = ping_host(host, count)
        for result in results:
            console.print(result)
            
    elif tool_name == "Port Scanner":
        host = console.input("[bold]Enter hostname or IP to scan: [/bold]")
        port_range = console.input("[bold]Enter port range (e.g., 1-100, default: common ports): [/bold]")
        
        console.print(f"[bold cyan]Scanning ports on {host}...[/bold cyan]")
        open_ports = port_scan(host, port_range)
        
        if open_ports:
            console.print("[bold green]Open ports:[/bold green]")
            for port, service in open_ports:
                console.print(f"  {port}/tcp: {service}")
        else:
            console.print("[bold yellow]No open ports found.[/bold yellow]")
            
    elif tool_name == "DNS Lookup":
        domain = console.input("[bold]Enter domain name: [/bold]")
        record_type = console.input("[bold]Enter record type (A, MX, NS, TXT, CNAME, default: A): [/bold]")
        if not record_type:
            record_type = "A"
            
        console.print(f"[bold cyan]Looking up {record_type} records for {domain}...[/bold cyan]")
        records = lookup_dns(domain, record_type)
        
        if records:
            console.print(f"[bold green]{record_type} records for {domain}:[/bold green]")
            for record in records:
                console.print(f"  {record}")
        else:
            console.print(f"[bold yellow]No {record_type} records found.[/bold yellow]")

if __name__ == "__main__":
    main() 