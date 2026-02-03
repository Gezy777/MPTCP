#!/usr/bin/env python3
"""
MPQUIC演示启动脚本
"""

import asyncio
import subprocess
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import os

console = Console()

def show_banner():
    """显示欢迎横幅"""
    banner = """
    ███╗   ███╗██████╗ ██████╗ ██╗   ██╗ ██████╗██╗ ██████╗
    ████╗ ████║██╔══██╗██╔══██╗██║   ██║██╔════╝██║██╔════╝
    ██╔████╔██║██████╔╝██████╔╝██║   ██║██║     ██║██║     
    ██║╚██╔╝██║██╔═══╝ ██╔══██╗██║   ██║██║     ██║██║     
    ██║ ╚═╝ ██║██║     ██║  ██║╚██████╔╝╚██████╗██║╚██████╗
    ╚═╝     ╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚═╝ ╚═════╝
    
    [bold cyan]多路径QUIC传输演示程序[/bold cyan]
    """
    
    console.print(Panel.fit(banner, border_style="cyan"))
    
    info_table = Table(show_header=False, box=None)
    info_table.add_row("版本", "1.0.0")
    info_table.add_row("协议", "MPQUIC over UDP")
    info_table.add_row("实现", "aioquic (Python)")
    info_table.add_row("作者", "MPQUIC Demo Team")
    
    console.print(Panel(info_table, title="系统信息", border_style="blue"))
    console.print()

def run_simple_test():
    """运行简单测试"""
    console.print("[bold yellow]🔧 运行简单测试...[/bold yellow]")
    
    # 创建测试目录
    import os
    os.makedirs("demo_files", exist_ok=True)
    
    # 创建测试文件
    test_content = "这是MPQUIC传输测试文件\n" * 100
    with open("demo_files/test.txt", "w", encoding="utf-8") as f:
        f.write(test_content)
    
    console.print("[green]✓[/green] 测试文件已创建")
    
    # 检查依赖
    try:
        import aioquic
        console.print(f"[green]✓[/green] aioquic 版本: {aioquic.__version__}")
    except ImportError:
        console.print("[red]✗[/red] 未找到aioquic，请运行: pip install aioquic")
        return False
        
    return True

async def main():
    """主函数"""
    show_banner()
    
    # 运行简单测试
    if not run_simple_test():
        return
    
    # 选择运行模式
    table = Table(title="运行模式", show_header=True, header_style="bold magenta")
    table.add_column("选项", style="cyan")
    table.add_column("描述")
    table.add_column("命令", style="green")
    
    table.add_row("1", "启动服务器", "python mpquic_server.py")
    table.add_row("2", "启动客户端", "python mpquic_client.py")
    table.add_row("3", "自动测试", "同时运行服务器和客户端")
    table.add_row("4", "清理文件", "删除生成的证书和测试文件")
    table.add_row("Q", "退出", "")
    
    console.print(table)
    
    while True:
        choice = console.input("\n[bright_white]请选择 (1-4, Q): [/bright_white]").strip().upper()
        
        if choice == "1":
            console.print("[yellow]启动服务器...[/yellow]")
            subprocess.run([sys.executable, "mpquic_server.py"])
            
        elif choice == "2":
            console.print("[yellow]启动客户端...[/yellow]")
            subprocess.run([sys.executable, "mpquic_client.py"])
            
        elif choice == "3":
            console.print("[yellow]运行自动测试...[/yellow]")
            
            # 在后台启动服务器
            import threading
            
            def run_server():
                subprocess.run([sys.executable, "mpquic_server.py"], 
                              stdout=subprocess.DEVNULL, 
                              stderr=subprocess.DEVNULL)
            
            server_thread = threading.Thread(target=run_server)
            server_thread.daemon = True
            server_thread.start()
            
            console.print("[green]✓[/green] 服务器已启动")
            time.sleep(2)  # 等待服务器启动
            
            # 运行客户端
            console.print("[yellow]启动客户端进行测试...[/yellow]")
            subprocess.run([sys.executable, "mpquic_client.py"])
            
        elif choice == "4":
            console.print("[yellow]清理文件...[/yellow]")
            import glob
            import shutil
            
            files_to_remove = ["certificate.pem", "private.key", "demo_files"]
            for pattern in files_to_remove:
                if os.path.exists(pattern):
                    if os.path.isdir(pattern):
                        shutil.rmtree(pattern)
                    else:
                        os.remove(pattern)
                    console.print(f"[green]✓[/green] 已删除: {pattern}")
            
        elif choice == "Q":
            console.print("[yellow]👋 再见！[/yellow]")
            break
            
        else:
            console.print("[red]无效选择，请重试[/red]")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]程序已终止[/yellow]")