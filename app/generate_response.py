from app.agents import ledning_agent, verksamhet_agent
from app.memory import save_message, get_full_log
from agents import Runner

async def generate_response(user_input: str, user_type: str) -> str:
    save_message(user_type, "user", user_input)
    full_history = get_full_log(user_type)

    agent = ledning_agent if user_type == "ledning" else verksamhet_agent

    result = await Runner.run(agent, input=full_history)


    result = await Runner.run(agent, input=full_history)
    save_message(user_type, "assistant", result.final_output)
    return result.final_output
