"""Interactive example of the form processing framework with user input via console."""

import asyncio
import os
from typing import List
from datetime import datetime
import questionary
from pydantic import BaseModel, Field
from pydantic2.agents import FormProcessor, BaseFormModel, FormData
from pydantic2.agents.utils.logging_config import SimpleLogger, LogConsole
import nest_asyncio

nest_asyncio.apply()

# Create a logger using our SimpleLogger class
logger = SimpleLogger("examples.interactive_form")
logger.set_agents_logs_visible(True)

console = LogConsole(
    name="examples.interactive_form"
)


# Create nested 3rd level models
class ContactInfo(BaseModel):
    """Contact information."""
    email: str = Field(default="", description="Email contact")
    phone: str = Field(default="", description="Phone number")
    website: str = Field(default="", description="Website")


class MarketInfo(BaseModel):
    """Market information."""
    size: str = Field(default="", description="Market size")
    growth_rate: float = Field(default=0.0, description="Market growth rate in %")
    competitors: List[str] = Field(default_factory=list, description="List of competitors")


class StartupForm(BaseFormModel):
    """Form for collecting startup information."""
    name: str = Field(default="", description="Startup name")
    description: str = Field(default="", description="Product/service description")
    industry: str = Field(default="", description="Industry/sector")
    problem_statement: str = Field(default="", description="Problem that the startup solves")
    market: MarketInfo = Field(default_factory=MarketInfo, description="Market information")
    contact: ContactInfo = Field(default_factory=ContactInfo, description="Contact information")


def get_user_input() -> str:
    """Get input from user with questionary."""
    response = questionary.text("\n💬 Your answer (type 'exit' to quit):").ask()
    if response is None:  # User pressed Ctrl+C
        return "exit"
    return response


def create_progress_bar(percentage: int, width: int = 20) -> str:
    """Create a text-based progress bar."""
    filled_width = int(width * percentage / 100)
    bar = "█" * filled_width + "░" * (width - filled_width)
    return bar


class InteractiveFormSession:
    """Class to handle the interactive form session."""

    def __init__(self):
        self.processor = None
        self.processor_session_id = None
        self.logger = logger.bind(session_id=f"session_{datetime.now().strftime('%Y%m%d%H%M%S')}")

    def setup(self):
        """Initialize the processor with user preferences."""
        # Get API key from environment
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            self.logger.error("OPENROUTER_API_KEY environment variable not set")
            print("\n❌ OPENROUTER_API_KEY environment variable is not set. Please set it and try again.")
            return False

        # Setting Russian language as default
        role_prompt = """
        Speak with the user in their language and be concise.
        Ask specific questions about the startup.
        Be sarcastic and communicate in Pelevin's style.
        """

        # Initialize processor
        try:
            self.logger.info("Initializing FormProcessor...")
            self.processor = FormProcessor(
                form_class=StartupForm,
                api_key=api_key,
                model_name="openai/gpt-4o-2024-11-20",
                completion_threshold=100,  # Set lower threshold to trigger analytics
                role_prompt=role_prompt,
                verbose=True  # Enable detailed logging
            )
            self.logger.info("Form processor initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize processor: {e}")
            print(f"\n❌ Processor initialization error: {e}")
            return False

    async def initialize_session(self):
        """Initialize session asynchronously."""
        if not self.processor:
            self.logger.error("Processor not initialized")
            return None

        self.processor_session_id = await self.processor.start_session("interactive_user")
        self.logger = self.logger.bind(processor_session_id=self.processor_session_id)
        self.logger.success("Session started successfully")

        # Get initial response
        form_data = await self.processor.get_form_state(self.processor_session_id)
        initial_message = form_data.session_info.metadata.next_message_ai or "Hello! I'll help you fill out the startup form. Let's begin!"

        # Show initial form state before greeting
        console.print_json(message="Initial form data", data=form_data.session_info.user_form.model_dump())

        # Then AI greeting
        print(f"\n🤖 {initial_message}")

        return form_data

    async def process_user_message(self, user_message):
        """Process a single user message."""
        if not self.processor or not self.processor_session_id:
            self.logger.error("Processor or session not initialized")
            return None

        self.logger.info(f"Processing user message: {user_message}")
        response = await self.processor.process_message(user_message, str(self.processor_session_id))

        # Show progress
        progress = response.session_info.metadata.progress
        progress_bar = create_progress_bar(progress)
        print(f"\n📊 Form completion: {progress_bar} {progress}%")

        # Always show current form data BEFORE AI response
        console.print_json(message="Session info", data=response.session_info.model_dump())

        # Show AI response AFTER form data output
        print(f"\n🤖 {response.session_info.metadata.next_message_ai}")

        return response

    async def handle_form_completion(self, response: FormData):
        """Handle form completion if achieved."""
        if not response:
            return False

        if response.system.completion_achieved:
            self.logger.success("Form reached completion threshold!")

            if response.analytics:
                print("\n📈 Form analysis completed!")
                return True

        return False


async def async_main():
    """Asynchronous main function."""
    print("🚀 Starting interactive form filling example\n")
    print("This example allows you to interactively fill out a startup form through dialogue.")
    print("Type 'exit' at any time to exit the dialogue.\n")

    # Initialize session
    session = InteractiveFormSession()
    if not session.setup():
        return

    try:
        # Initialize session asynchronously
        await session.initialize_session()

        # Main loop (handled synchronously to avoid questionary asyncio issues)
        user_message = get_user_input()

        while user_message.lower() not in ['exit', 'quit', 'q']:
            # Process message asynchronously
            response = await session.process_user_message(user_message)

            if not response:
                print("\n❌ Failed to process message")
                break

            # Check if form is complete
            form_completed = await session.handle_form_completion(response)

            if form_completed and response.analytics:
                # Using a direct approach without questionary for analytics display
                print("\n📈 Form analysis completed!")
                show_analytics = input("Show analytics? (y/n): ").lower().startswith('y')
                if show_analytics:
                    console.print_json(message="Form analytics", data=response.analytics.model_dump())

                # And for continuation question
                continue_conversation = input("Would you like to continue the conversation? (y/n): ").lower().startswith('y')
                if not continue_conversation:
                    print("\n👋 Thanks for filling out the form!")
                    break

            # Get next user message
            user_message = get_user_input()

        print("\n👋 Ending dialogue. Thank you for your time!")

    except Exception as e:
        logger.exception(f"Error during conversation: {e}")
        print(f"\n❌ An error occurred: {e}")


def main():
    """Main entry point for the interactive form example."""
    try:
        asyncio.run(async_main())
        print("\n✅ Example completed")
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted. Shutting down.")
    except Exception as e:
        logger.exception(f"Unhandled error: {e}")
        print(f"\n❌ An unhandled error occurred: {e}")


if __name__ == "__main__":
    main()
