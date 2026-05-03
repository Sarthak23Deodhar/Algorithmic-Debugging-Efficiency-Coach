#!/usr/bin/env python3
"""
Algorithmic Debugging & Efficiency Coach - CLI Demo Application

This interactive CLI demonstrates the capabilities of the system by allowing
users to submit code for analysis and view comprehensive results.
"""
import os
import sys
from typing import Optional
from colorama import Fore, Style, init

from services.api_client import APIClient
from services.formatter import OutputFormatter

# Initialize colorama
init(autoreset=True)


class CLIDemo:
    """Interactive CLI demo application."""
    
    def __init__(self):
        """Initialize CLI demo."""
        self.client = APIClient()
        self.formatter = OutputFormatter()
        self.examples_dir = os.path.join(os.path.dirname(__file__), "examples")
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        """Print application banner."""
        banner = f"""
{Fore.CYAN}{Style.BRIGHT}
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║        Algorithmic Debugging & Efficiency Coach - CLI Demo               ║
║                                                                           ║
║        Powered by IBM watsonx.ai & watsonx Orchestrate                   ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
        print(banner)
    
    def print_menu(self):
        """Print main menu."""
        menu = f"""
{Fore.YELLOW}{Style.BRIGHT}Main Menu:{Style.RESET_ALL}

  {Fore.GREEN}1.{Style.RESET_ALL} Analyze Example Code (Buggy Python)
  {Fore.GREEN}2.{Style.RESET_ALL} Analyze Example Code (Inefficient Python)
  {Fore.GREEN}3.{Style.RESET_ALL} Analyze Custom Code
  {Fore.GREEN}4.{Style.RESET_ALL} View Example Files
  {Fore.GREEN}5.{Style.RESET_ALL} Check Service Health
  {Fore.GREEN}6.{Style.RESET_ALL} About This System
  {Fore.RED}0.{Style.RESET_ALL} Exit

"""
        print(menu)
    
    def read_example_file(self, filename: str) -> Optional[str]:
        """
        Read example code file.
        
        Args:
            filename: Name of the example file
            
        Returns:
            File contents or None if file not found
        """
        filepath = os.path.join(self.examples_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            self.formatter.print_error(f"Example file not found: {filename}")
            return None
        except Exception as e:
            self.formatter.print_error(f"Error reading file: {str(e)}")
            return None
    
    def analyze_code(self, code: str, language: str, code_name: str = "Code"):
        """
        Analyze code and display results.
        
        Args:
            code: Source code to analyze
            language: Programming language
            code_name: Name/description of the code
        """
        print(f"\n{Fore.CYAN}Analyzing {code_name}...{Style.RESET_ALL}\n")
        
        # Show code being analyzed
        print(f"{Fore.YELLOW}Code to analyze:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'-' * 80}")
        print(code)
        print(f"{'-' * 80}{Style.RESET_ALL}\n")
        
        # Perform analysis
        self.formatter.print_info("Step 1/4: Running debugging analysis...")
        self.formatter.print_info("Step 2/4: Running efficiency analysis...")
        self.formatter.print_info("Step 3/4: Generating refactored code...")
        self.formatter.print_info("Step 4/4: Triggering automated actions...")
        
        results = self.client.complete_analysis(
            code=code,
            language=language,
            include_refactoring=True,
            include_automation=True
        )
        
        # Display results
        self.formatter.format_complete_analysis(results)
    
    def analyze_buggy_example(self):
        """Analyze the buggy Python example."""
        code = self.read_example_file("buggy_code.py")
        if code:
            self.analyze_code(code, "python", "Buggy Python Example")
    
    def analyze_inefficient_example(self):
        """Analyze the inefficient Python example."""
        code = self.read_example_file("inefficient_code.py")
        if code:
            self.analyze_code(code, "python", "Inefficient Python Example")
    
    def analyze_custom_code(self):
        """Analyze custom user-provided code."""
        print(f"\n{Fore.CYAN}Analyze Custom Code{Style.RESET_ALL}\n")
        
        # Get language
        print(f"{Fore.YELLOW}Select language:{Style.RESET_ALL}")
        print("  1. Python")
        print("  2. C++")
        print("  3. Java")
        
        lang_choice = input(f"\n{Fore.GREEN}Enter choice (1-3):{Style.RESET_ALL} ").strip()
        
        language_map = {
            "1": "python",
            "2": "cpp",
            "3": "java"
        }
        
        language = language_map.get(lang_choice)
        if not language:
            self.formatter.print_error("Invalid language choice")
            return
        
        # Get code input method
        print(f"\n{Fore.YELLOW}Code input method:{Style.RESET_ALL}")
        print("  1. Enter code directly")
        print("  2. Load from file")
        
        input_choice = input(f"\n{Fore.GREEN}Enter choice (1-2):{Style.RESET_ALL} ").strip()
        
        code = None
        code_name = "Custom Code"
        
        if input_choice == "1":
            print(f"\n{Fore.YELLOW}Enter your code (press Ctrl+D or Ctrl+Z when done):{Style.RESET_ALL}")
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                code = "\n".join(lines)
        elif input_choice == "2":
            filepath = input(f"\n{Fore.GREEN}Enter file path:{Style.RESET_ALL} ").strip()
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    code = f.read()
                code_name = os.path.basename(filepath)
            except Exception as e:
                self.formatter.print_error(f"Error reading file: {str(e)}")
                return
        else:
            self.formatter.print_error("Invalid input method choice")
            return
        
        if code:
            self.analyze_code(code, language, code_name)
        else:
            self.formatter.print_error("No code provided")
    
    def view_example_files(self):
        """Display available example files."""
        print(f"\n{Fore.CYAN}Available Example Files:{Style.RESET_ALL}\n")
        
        examples = [
            ("buggy_code.py", "Python code with syntax and logic errors"),
            ("inefficient_code.py", "Python code with O(n²) complexity"),
            ("optimized_code.py", "Optimized Python code with O(n) complexity")
        ]
        
        for filename, description in examples:
            filepath = os.path.join(self.examples_dir, filename)
            if os.path.exists(filepath):
                print(f"{Fore.GREEN}✓{Style.RESET_ALL} {Fore.YELLOW}{filename}{Style.RESET_ALL}")
                print(f"  {description}")
                
                # Show preview
                code = self.read_example_file(filename)
                if code:
                    lines = code.split('\n')[:10]
                    print(f"\n  {Fore.WHITE}Preview (first 10 lines):{Style.RESET_ALL}")
                    for line in lines:
                        print(f"  {Fore.WHITE}{line}{Style.RESET_ALL}")
                    if len(code.split('\n')) > 10:
                        print(f"  {Fore.WHITE}...{Style.RESET_ALL}")
                print()
            else:
                print(f"{Fore.RED}✗{Style.RESET_ALL} {Fore.YELLOW}{filename}{Style.RESET_ALL} (not found)")
                print(f"  {description}\n")
    
    def check_service_health(self):
        """Check and display service health status."""
        print(f"\n{Fore.CYAN}Checking service health...{Style.RESET_ALL}\n")
        
        health_status = self.client.health_check()
        self.formatter.format_health_status(health_status)
    
    def show_about(self):
        """Display information about the system."""
        about_text = f"""
{Fore.CYAN}{Style.BRIGHT}About Algorithmic Debugging & Efficiency Coach{Style.RESET_ALL}

{Fore.YELLOW}Overview:{Style.RESET_ALL}
An intelligent code analysis system that diagnoses bugs and guides optimization
from brute-force to production-ready solutions.

{Fore.YELLOW}Supported Languages:{Style.RESET_ALL}
  • Python
  • C++
  • Java

{Fore.YELLOW}Core Features:{Style.RESET_ALL}
  • {Fore.GREEN}Debugging Engine:{Style.RESET_ALL} Identifies bugs with execution flow analysis
  • {Fore.GREEN}Efficiency Analyzer:{Style.RESET_ALL} Calculates time/space complexity
  • {Fore.GREEN}watsonx.ai Integration:{Style.RESET_ALL} Generates refactored code
  • {Fore.GREEN}watsonx Orchestrate:{Style.RESET_ALL} Automates documentation, tickets, and learning

{Fore.YELLOW}Architecture:{Style.RESET_ALL}
  • Microservices-based design
  • Containerized core services (Docker/Kubernetes)
  • Serverless watsonx integrations
  • Hybrid data layer (PostgreSQL + Redis + S3)

{Fore.YELLOW}Services:{Style.RESET_ALL}
  • Debugging Engine (port 8001)
  • Efficiency Analyzer (port 8002)
  • watsonx.ai Integration (port 8003)
  • watsonx Orchestrate Integration (port 8004)

{Fore.YELLOW}Target Users:{Style.RESET_ALL}
  • Developers seeking code optimization
  • Students learning algorithms
  • Coding interview candidates
  • Technical educators

{Fore.YELLOW}Technology Stack:{Style.RESET_ALL}
  • Backend: Python (FastAPI), Node.js
  • AI: IBM watsonx.ai, watsonx Orchestrate
  • Database: PostgreSQL, Redis
  • Storage: IBM Cloud Object Storage (S3)
  • Deployment: Docker, Kubernetes, IBM Cloud Functions

For more information, see the project documentation.
"""
        print(about_text)
    
    def run(self):
        """Run the CLI application."""
        while True:
            self.clear_screen()
            self.print_banner()
            self.print_menu()
            
            choice = input(f"{Fore.GREEN}Enter your choice:{Style.RESET_ALL} ").strip()
            
            if choice == "1":
                self.analyze_buggy_example()
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            elif choice == "2":
                self.analyze_inefficient_example()
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            elif choice == "3":
                self.analyze_custom_code()
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            elif choice == "4":
                self.view_example_files()
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            elif choice == "5":
                self.check_service_health()
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            elif choice == "6":
                self.show_about()
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            elif choice == "0":
                print(f"\n{Fore.CYAN}Thank you for using Algorithmic Debugging & Efficiency Coach!{Style.RESET_ALL}\n")
                sys.exit(0)
            else:
                self.formatter.print_error("Invalid choice. Please try again.")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


def main():
    """Main entry point."""
    try:
        app = CLIDemo()
        app.run()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.CYAN}Interrupted by user. Exiting...{Style.RESET_ALL}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()

# Made with Bob
