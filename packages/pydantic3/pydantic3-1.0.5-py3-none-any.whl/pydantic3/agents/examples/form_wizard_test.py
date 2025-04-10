"""Example that tests the FormWizard functionality."""

import os
import asyncio
import json

from pydantic3.agents.wizards.form import FormWizard
from pydantic3.agents.models.form import FormData


async def print_form_data(form_data: FormData) -> None:
    """Print form data in a formatted way."""
    form_dict = form_data.safe_dict()
    user_form = form_dict.get("user_form", {})

    print("\n📝 Current form data:")
    print(json.dumps(user_form, indent=2, ensure_ascii=False))


async def test_basic_flow() -> None:
    """Test the basic form flow with the wizard."""
    print("\n🧪 Testing basic form wizard flow")

    # Get API key from environment
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY environment variable not set")
        return

    # Create wizard instance
    wizard = FormWizard(api_key=api_key, verbose=True)
    print(f"✅ Created wizard with model: {wizard.model_name}")

    # Start session
    session_id = await wizard.start_session("test_user")
    print(f"✅ Started session: {session_id}")

    # Get initial state
    form_data = await wizard.get_form_state()
    print("✅ Got initial form state")
    print(f"🤖 Initial message: {form_data.session_info.metadata.next_message_ai}")

    # Print initial form data
    await print_form_data(form_data)

    # Test a series of messages
    test_messages = [
        "I'm creating a feedback form for an online store",
        "Our business sells handmade crafts and art supplies",
        "The form will be filled out by customers after they make a purchase",
        "We need to ask about product quality, delivery speed, and overall satisfaction",
        "We want to use a friendly communication style with emojis"
    ]

    # Process each message
    for idx, message in enumerate(test_messages, 1):
        print(f"\n🔄 Processing message {idx}/{len(test_messages)}: '{message}'")

        # Process the message
        response = await wizard.process_message(message)

        # Show progress
        progress = response.session_info.metadata.progress
        print(f"📊 Form completion: {progress}%")

        # Show AI response
        print(f"🤖 {response.session_info.metadata.next_message_ai}")

        # Show updated form data
        await print_form_data(response)

    # Get message history
    messages = await wizard.get_message_history()
    print(f"\n📜 Retrieved {len(messages)} messages from history")

    # Try direct processor method access
    session_info = await wizard.processor_instance.session_manager.get_session_info(session_id)
    print(f"\n✅ Accessed processor directly: session created at {session_info.get('created_at', 'unknown')}")

    # Test __getattr__ method for direct access to processor methods
    try:
        # Используем session_manager напрямую, это точно существует
        latest_state = await wizard.processor_instance.session_manager.get_latest_form_data(session_id)
        print("\n✅ Accessed processor method via session_manager")
        if latest_state:
            print(f"   Form data contains {len(latest_state)} fields")
    except Exception as e:
        print(f"\n❌ Error accessing processor method: {e}")

    print("\n✅ All tests complete")


async def main():
    """Run all tests."""
    try:
        await test_basic_flow()
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        print(traceback.format_exc())


if __name__ == "__main__":
    print("🧪 Starting FormWizard tests")
    asyncio.run(main())
    print("\n�� Tests finished")
