# Import libraries here

# Define data processing classes

# Generic Action class
class Action:

    # Function members
    
    # Execute the action here
    # (): void
    def execute(self):
        print("yay execution")

# Action subclasses here...

# Input processor
class NaturalLanguageProcessor:

    # Function Members

    # (string input): Action[]
    def processInput(self, input):
        # Execute action according to the input
        print("Action here")

# Output controller
class Coach:
    
    # Data members
    # User currentUser

    # Instantiation
    # def __init__(self):
        
    # Function members

    # So I'm confused...
    # How do we call this method if
    # respondToUserInput(input)
    # I feel like we shouldn't have to use "self"

    # Print response to user's input
    # (string input): void
    def respondToUserInput(self, input):
        # Use NaturalLanProcsser 
        print("You said: " + input)
        print("Hello User")

    # Print the help menu of actions
    # (): void
    def printHelpMenu(self):
        print("Help Menu\n----------")
        print("Action <input1>")
