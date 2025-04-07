import time
import random
from rich.console import Console
from rich.align import Align

console = Console()

class Trplm:
    """Main Game Class"""
    
    def __init__(self):
        self.menu = Menu()
        self.settings_menu = SettingsMenu()
        self.game_loop()

    def game_loop(self) -> None:
        """Main game loop"""
        user_input = ""

        while user_input not in {'3', 'exit'}:
            self.menu.display_menu()
            user_input = input("Enter: ").strip().lower()

            if user_input == '1':
                self.play_game()
            elif user_input == '2':
                self.settings_menu.display_menu()
            elif user_input not in {'3', 'exit'}:
                console.print("Enter A Valid Response", style="bold red")
                time.sleep(0.7)

        console.clear()

    def play_game(self):
        """Play the game"""
        console.clear()
        
        # Let the user choose between manual or random mode
        while True:
            console.print("[bold red]MENTAL MATH MASTER[/bold red]")
            console.print("(1) Sequential - Choose Starting Number\n(2) Random Questions\n(3) EXIT (or '[yellow]exit[/yellow]')")
            mode = input("Enter: ").strip().lower()
            if mode in {"1", "2"}:
                break
            if mode in {"exit", "3"}:
                return
                
            console.print("Invalid Choice. Enter 1, 2, 3, or '[blue]exit[/blue]'", style="bold red")
            time.sleep(0.7)
            console.clear()

        questions = []
        if mode == "1":
            while True:
                console.clear()
                console.print("[bold red]MENTAL MATH MASTER[/bold red]")
                user_input = input("Sequential Starting Number: ").strip().lower()
                if user_input == "exit":
                    return
                try:
                    user_input = int(user_input)
                    if 2 <= user_input <= 20:
                        break
                    else:
                        console.print("Enter A Number Between 2 and 20, Or Type [yellow]'exit'[/yellow]", style="bold red")
                        time.sleep(1.4)
                except ValueError:
                    console.print("Enter A Number Between 2 and 20, Or Type [yellow]'exit'[/yellow]", style="bold red")
                    time.sleep(1.4)
                        

            num_range = range(user_input, 21)
            questions = [(a, b) for a in num_range for b in range(2, 21)]

        else:  # Random mode
            questions = [(a, b) for a in range(2, 21) for b in range(2, 21)]
            random.shuffle(questions)

        operation = "x"
        start_time = time.time()

        for a, b in questions:
            answer = a * b
            attempts = 0  

            while True:  
                console.clear()
                console.print("[bold red]MENTAL MATH MASTER[/bold red]")
                question_text = f"[bold red]{a} {operation} {b}[/bold red]"
                console.print(Align.left(question_text))

                user_answer = input().strip().lower()

                if user_answer.lower() == "exit":
                    elapsed_time = round(time.time() - start_time)
                    minutes, seconds = divmod(elapsed_time, 60)
                    console.print(f"Time Played: [bold green]{minutes}m {seconds}s[/bold green]")
                    input("Press Enter To Return")
                    return

                if user_answer.isdigit() and int(user_answer) == answer:
                    break  

                attempts += 1
                if attempts == 2:
                    console.print(f"[red]{answer}[/red]")
                    time.sleep(0.7)
                    break  

        elapsed_time = round(time.time() - start_time)
        minutes, seconds = divmod(elapsed_time, 60)
        console.print(f"\n[bold red]Total Time Played:[/bold red] [bold green]{minutes}m {seconds}s[/bold green]")
        input("Press Enter To Return")

class Menu:
    """Main Menu"""
    
    def __init__(self):
        self.title = "MENTAL MATH MASTER"
        self.menu = "(1) PLAY\n(2) SETTINGS\n(3) EXIT (Or '[yellow]exit[/yellow]')"
    
    def display_menu(self) -> None:
        """Display the main menu"""
        console.clear()
        console.print(f"[bold red]{self.title}[/bold red]\n{self.menu}")

class SettingsMenu:
    """Settings Menu"""
    
    def __init__(self):
        self.menu = "(1) OPERATIONS\n(2) TIMER\n(3) QUESTION TYPE\n(4) MAIN MENU"

    def display_menu(self) -> None:
          
        
        while True:
            console.clear()
            console.print(f"[bold red]MENTAL MATH MASTER (SETTINGS)[/bold red]\n{self.menu}")
            user_input = input("Enter: ").strip().lower()

            if user_input in {"4", "exit"}:
                return
            elif user_input == "1":
                console.print("[bold red]Operations Settings Not Implemented Yet[/bold red]\n[bold red]Press Enter To Continue[/bold red]", style="italic")
                input("")
            elif user_input == "2":
                console.print("[bold red]Timer Settings Not Implemented Yet[/bold red]\n[bold red]Press Enter To Continue[/bold red]", style="italic")
                input("")
            elif user_input == "3":
                console.print("[bold red]Question Type Settings Not Implemented Yet[/bold red]\n[bold red]Press Enter To Continue[/bold red]", style="italic")
                input("")
            else:
                console.print("[red]Enter A Valid Response[/red]")
                time.sleep(0.7)


if __name__ == "__main__":
    try:
        Trplm()
    except KeyboardInterrupt:
        console.clear()
 
