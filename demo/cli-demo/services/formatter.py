"""Output formatter for CLI display with colors and structured output."""
from typing import Dict, Any, List
from colorama import Fore, Style, init

# Initialize colorama for Windows support
init(autoreset=True)


class OutputFormatter:
    """Format analysis results for CLI display."""
    
    @staticmethod
    def print_header(text: str, char: str = "="):
        """Print a formatted header."""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{char * 3} {text} {char * 3}{Style.RESET_ALL}")
    
    @staticmethod
    def print_subheader(text: str):
        """Print a formatted subheader."""
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}{text}{Style.RESET_ALL}")
    
    @staticmethod
    def print_success(text: str):
        """Print success message."""
        print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")
    
    @staticmethod
    def print_error(text: str):
        """Print error message."""
        print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")
    
    @staticmethod
    def print_warning(text: str):
        """Print warning message."""
        print(f"{Fore.YELLOW}⚠ {text}{Style.RESET_ALL}")
    
    @staticmethod
    def print_info(text: str):
        """Print info message."""
        print(f"{Fore.BLUE}ℹ {text}{Style.RESET_ALL}")
    
    @staticmethod
    def format_diagnostic_summary(debugging_results: Dict[str, Any]) -> str:
        """
        Format diagnostic summary section.
        
        Args:
            debugging_results: Results from debugging engine
            
        Returns:
            Formatted diagnostic summary string
        """
        if debugging_results.get("error"):
            return f"{Fore.RED}Error: {debugging_results.get('message', 'Unknown error')}{Style.RESET_ALL}"
        
        bugs = debugging_results.get("bugs", [])
        explanation = debugging_results.get("explanation", "No issues detected.")
        
        output = []
        
        if bugs:
            output.append(f"{Fore.RED}Found {len(bugs)} issue(s):{Style.RESET_ALL}")
            for i, bug in enumerate(bugs, 1):
                bug_type = bug.get("type", "Unknown")
                line = bug.get("line", "?")
                message = bug.get("message", "No description")
                severity = bug.get("severity", "medium")
                
                severity_color = {
                    "critical": Fore.RED,
                    "high": Fore.LIGHTRED_EX,
                    "medium": Fore.YELLOW,
                    "low": Fore.LIGHTYELLOW_EX
                }.get(severity, Fore.WHITE)
                
                output.append(f"\n  {i}. {severity_color}[{severity.upper()}]{Style.RESET_ALL} {bug_type} at line {line}")
                output.append(f"     {message}")
        else:
            output.append(f"{Fore.GREEN}No bugs detected!{Style.RESET_ALL}")
        
        output.append(f"\n{Fore.CYAN}Explanation:{Style.RESET_ALL}")
        output.append(f"{explanation}")
        
        return "\n".join(output)
    
    @staticmethod
    def format_complexity_breakdown(efficiency_results: Dict[str, Any]) -> str:
        """
        Format complexity breakdown section.
        
        Args:
            efficiency_results: Results from efficiency analyzer
            
        Returns:
            Formatted complexity breakdown string
        """
        if efficiency_results.get("error"):
            return f"{Fore.RED}Error: {efficiency_results.get('message', 'Unknown error')}{Style.RESET_ALL}"
        
        time_complexity = efficiency_results.get("time_complexity", {})
        space_complexity = efficiency_results.get("space_complexity", {})
        
        current_time = time_complexity.get("current", "Unknown")
        target_time = time_complexity.get("target", "Unknown")
        current_space = space_complexity.get("current", "Unknown")
        target_space = space_complexity.get("target", "Unknown")
        
        output = []
        output.append(f"{Fore.YELLOW}Current Time Complexity:{Style.RESET_ALL} {Fore.RED}{current_time}{Style.RESET_ALL}")
        output.append(f"{Fore.YELLOW}Current Space Complexity:{Style.RESET_ALL} {Fore.RED}{current_space}{Style.RESET_ALL}")
        output.append(f"{Fore.YELLOW}Target Time Complexity:{Style.RESET_ALL} {Fore.GREEN}{target_time}{Style.RESET_ALL}")
        output.append(f"{Fore.YELLOW}Target Space Complexity:{Style.RESET_ALL} {Fore.GREEN}{target_space}{Style.RESET_ALL}")
        
        # Add patterns detected
        patterns = efficiency_results.get("patterns", [])
        if patterns:
            output.append(f"\n{Fore.CYAN}Inefficient Patterns Detected:{Style.RESET_ALL}")
            for pattern in patterns:
                pattern_name = pattern.get("name", "Unknown")
                description = pattern.get("description", "")
                output.append(f"  • {Fore.YELLOW}{pattern_name}{Style.RESET_ALL}: {description}")
        
        return "\n".join(output)
    
    @staticmethod
    def format_optimization_path(efficiency_results: Dict[str, Any]) -> str:
        """
        Format optimization path section.
        
        Args:
            efficiency_results: Results from efficiency analyzer
            
        Returns:
            Formatted optimization path string
        """
        if efficiency_results.get("error"):
            return f"{Fore.RED}Error: {efficiency_results.get('message', 'Unknown error')}{Style.RESET_ALL}"
        
        optimization_steps = efficiency_results.get("optimization_steps", [])
        recommended_strategy = efficiency_results.get("recommended_strategy", "General optimization")
        
        output = []
        output.append(f"{Fore.CYAN}Recommended Strategy:{Style.RESET_ALL} {Fore.GREEN}{recommended_strategy}{Style.RESET_ALL}")
        
        if optimization_steps:
            output.append(f"\n{Fore.CYAN}Step-by-Step Guide:{Style.RESET_ALL}")
            for i, step in enumerate(optimization_steps, 1):
                if isinstance(step, dict):
                    title = step.get("title", f"Step {i}")
                    description = step.get("description", "")
                    output.append(f"\n  {Fore.YELLOW}Step {i}:{Style.RESET_ALL} {title}")
                    output.append(f"  {description}")
                else:
                    output.append(f"\n  {Fore.YELLOW}Step {i}:{Style.RESET_ALL} {step}")
        else:
            output.append(f"\n{Fore.GREEN}Code is already optimized!{Style.RESET_ALL}")
        
        return "\n".join(output)
    
    @staticmethod
    def format_automated_actions(automation_results: Dict[str, Any]) -> str:
        """
        Format automated actions section.
        
        Args:
            automation_results: Results from watsonx Orchestrate
            
        Returns:
            Formatted automated actions string
        """
        if automation_results.get("error"):
            return f"{Fore.RED}Error: {automation_results.get('message', 'Unknown error')}{Style.RESET_ALL}"
        
        output = []
        
        # Documentation
        documentation = automation_results.get("documentation", {})
        doc_status = documentation.get("status", "unknown")
        doc_files = documentation.get("files", [])
        
        if doc_status == "success":
            output.append(f"{Fore.GREEN}✓ Documentation updated:{Style.RESET_ALL}")
            for file in doc_files:
                output.append(f"  • {file}")
        else:
            output.append(f"{Fore.YELLOW}⚠ Documentation: {doc_status}{Style.RESET_ALL}")
        
        # Tickets
        tickets = automation_results.get("tickets", {})
        ticket_status = tickets.get("status", "unknown")
        ticket_ids = tickets.get("ticket_ids", [])
        
        if ticket_status == "success":
            output.append(f"\n{Fore.GREEN}✓ Tickets created:{Style.RESET_ALL}")
            for ticket_id in ticket_ids:
                output.append(f"  • {ticket_id}")
        else:
            output.append(f"\n{Fore.YELLOW}⚠ Tickets: {ticket_status}{Style.RESET_ALL}")
        
        # Learning path
        learning_path = automation_results.get("learning_path", {})
        learning_status = learning_path.get("status", "unknown")
        topics = learning_path.get("topics", [])
        
        if learning_status == "success":
            output.append(f"\n{Fore.GREEN}✓ Learning path generated:{Style.RESET_ALL}")
            for topic in topics:
                output.append(f"  • {topic}")
        else:
            output.append(f"\n{Fore.YELLOW}⚠ Learning path: {learning_status}{Style.RESET_ALL}")
        
        return "\n".join(output)
    
    @staticmethod
    def format_complete_analysis(results: Dict[str, Any]):
        """
        Format and print complete analysis results.
        
        Args:
            results: Complete analysis results from API client
        """
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 80}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'ANALYSIS RESULTS':^80}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'=' * 80}{Style.RESET_ALL}")
        
        # Language and code info
        language = results.get("language", "Unknown")
        print(f"\n{Fore.YELLOW}Language:{Style.RESET_ALL} {language}")
        
        # Diagnostic Summary
        OutputFormatter.print_header("DIAGNOSTIC SUMMARY")
        debugging_results = results.get("debugging", {})
        print(OutputFormatter.format_diagnostic_summary(debugging_results))
        
        # Complexity Breakdown
        OutputFormatter.print_header("COMPLEXITY BREAKDOWN")
        efficiency_results = results.get("efficiency", {})
        print(OutputFormatter.format_complexity_breakdown(efficiency_results))
        
        # Optimization Path
        OutputFormatter.print_header("THE OPTIMIZATION PATH")
        print(OutputFormatter.format_optimization_path(efficiency_results))
        
        # Automated Actions
        if results.get("automation"):
            OutputFormatter.print_header("AUTOMATED ACTIONS")
            automation_results = results.get("automation", {})
            print(OutputFormatter.format_automated_actions(automation_results))
        
        # Refactored Code
        if results.get("refactoring") and not results["refactoring"].get("error"):
            OutputFormatter.print_header("REFACTORED CODE")
            refactored_code = results["refactoring"].get("refactored_code", "")
            explanation = results["refactoring"].get("explanation", "")
            
            print(f"\n{Fore.CYAN}Explanation:{Style.RESET_ALL}")
            print(explanation)
            
            print(f"\n{Fore.CYAN}Refactored Code:{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{refactored_code}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 80}{Style.RESET_ALL}\n")
    
    @staticmethod
    def format_health_status(health_status: Dict[str, bool]):
        """
        Format and print service health status.
        
        Args:
            health_status: Dictionary of service names and their health status
        """
        OutputFormatter.print_header("SERVICE HEALTH STATUS")
        
        all_healthy = all(health_status.values())
        
        for service, is_healthy in health_status.items():
            service_name = service.replace("_", " ").title()
            if is_healthy:
                OutputFormatter.print_success(f"{service_name}: Online")
            else:
                OutputFormatter.print_error(f"{service_name}: Offline")
        
        print()
        if all_healthy:
            OutputFormatter.print_success("All services are operational!")
        else:
            OutputFormatter.print_warning("Some services are unavailable. Please check service status.")

# Made with Bob
