import chainlit as cl


@cl.on_chat_start
async def start():
    # Sending an action button within a chatbot message
    actions = [
        cl.Action(name="action_button", value="example_value", description="Click me!")
    ]

    await cl.Message(content="Interact with this action button:", actions=actions).send()


@cl.action_callback("action_button")
async def on_action(action: cl.Action):
    print("The user clicked on the action button!")

    return "Thank you for clicking on the action button!"
