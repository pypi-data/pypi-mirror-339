from fastapi import HTTPException
from threading import Thread
import time
import re
from typing import Any

from AgentEngine.framework import handle_agent_output_types, AgentText, ActionStep, MemoryStep
from AgentEngine.core.utils.observer import MessageObserver, ProcessType

from AgentEngine.core.agents import CoreAgent
from AgentEngine.core.models import OpenAIModel



def add_message_to_observer(observer:MessageObserver, step_log:ActionStep):
    if not isinstance(step_log, ActionStep):
        return
    step_number = f"Step {step_log.step_number}" if step_log.step_number is not None else ""
    if hasattr(step_log, "error") and step_log.error is not None:
        observer.add_message("", ProcessType.ERROR, str(step_log.error))

    step_footnote = f"{step_number}"
    if hasattr(step_log, "duration"):
        step_duration = f" | Duration: {round(float(step_log.duration), 2)}" if step_log.duration else None
        step_footnote += step_duration
    step_footnote = f"""<span style="color: #bbbbc2; font-size: 12px;">{step_footnote}</span> """
    observer.add_message("", ProcessType.TOKEN_COUNT, step_footnote)



def agent_run_thread(agent: Any, query: str, reset=True):
    total_input_tokens, total_output_tokens = 0, 0
    observer = agent.observer
    try:
        for step_log in agent.run(query, stream=True, reset=reset):
            # 检查是否需要停止
            if agent.should_stop:
                observer.add_message(agent.agent_name, ProcessType.ERROR, "Agent运行被用户中断")
                break
                
            if getattr(agent.model, "last_input_token_count", None) is not None:
                total_input_tokens += agent.model.last_input_token_count
                total_output_tokens += agent.model.last_output_token_count
                if isinstance(step_log, ActionStep):
                    step_log.input_token_count = agent.model.last_input_token_count
                    step_log.output_token_count = agent.model.last_output_token_count

            # 把内容放入到observer
            add_message_to_observer(observer, step_log)

        final_answer = step_log  # Last log is the run's final_answer
        final_answer = handle_agent_output_types(final_answer)

        if isinstance(final_answer, AgentText):
            observer.add_message(agent.agent_name, ProcessType.FINAL_ANSWER, final_answer.to_string())
        else:
            observer.add_message(agent.agent_name, ProcessType.FINAL_ANSWER, str(final_answer))
    except Exception as e:
        print(f"Error in interaction: {str(e)}")
        observer.add_message(agent_name=agent.agent_name,
                             process_type=ProcessType.ERROR,
                             content=f"Error in interaction: {str(e)}")


def agent_run(agent: Any, query: str, reset=True):
    if not isinstance(agent, CoreAgent):
        raise HTTPException(status_code=400, detail="Create Agent Object with CodeAgent")
    if not isinstance(agent.model, OpenAIModel):
        raise HTTPException(status_code=400, detail="Create Model Object with OpenAIModel")
    if not isinstance(agent.observer, MessageObserver):
        raise HTTPException(status_code=400, detail="Create Observer Object with MessageObserver")

    observer = agent.observer

    # 目前已知的遗留问题，当前端主动中断后，该线程不会停止，仍会执行
    thread_agent = Thread(target=agent_run_thread, args=(agent, query, reset))
    thread_agent.start()

    while thread_agent.is_alive():
        cached_message = observer.get_cached_message()
        for message in cached_message:
            yield f"data: {message}\n\n"

        time.sleep(0.2)

    # 确保信息发送完毕
    cached_message = observer.get_cached_message()
    for message in cached_message:
        yield f"data: {message}\n\n"
