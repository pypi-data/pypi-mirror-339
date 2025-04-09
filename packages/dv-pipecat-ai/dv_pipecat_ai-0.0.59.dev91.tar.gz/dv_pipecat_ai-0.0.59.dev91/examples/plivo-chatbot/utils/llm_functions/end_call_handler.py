import asyncio  # noqa: D100
import base64
from typing import Any, Optional

import aiohttp
from env_config import api_config
from fastapi import HTTPException
from starlette.websockets import WebSocket, WebSocketState

from pipecat.frames.frames import (
    TTSSpeakFrame,
)

from ..api_calls import update_webcall_status
from ..generic_functions.cleanup import cleanup_connection


def create_plivo_auth_headers(call_id, stream_id):
    auth_id = api_config.PLIVO_AUTH_ID
    auth_token = api_config.PLIVO_AUTH_TOKEN

    # Create the Basic Auth token
    auth_string = f"{auth_id}:{auth_token}"
    auth_bytes = auth_string.encode("ascii")
    base64_bytes = base64.b64encode(auth_bytes)
    base64_auth = base64_bytes.decode("ascii")
    plivo_url = f"https://api.plivo.com/v1/Account/{auth_id}/Call/{call_id}/Stream/{stream_id}/"
    headers = {
        "Authorization": f"Basic {base64_auth}",
        "Content-Type": "application/json",
    }
    return plivo_url, headers


async def end_call(
    provider,
    call_id,
    stream_id,
    websocket: WebSocket,
    callback_call_id,
    context_aggregator,
    transcript_handler,
    task,
    task_references,
    function_call_monitor,
    logger,
    transport: Optional[Any] = None,
    record_locally=False,
):
    try:
        if provider == "plivo":
            async with aiohttp.ClientSession() as session:
                plivo_url, headers = create_plivo_auth_headers(call_id, stream_id)
                logger.debug(
                    f"Making call to Plivo URL to end call:{plivo_url}", call_id=callback_call_id
                )

                async with session.delete(plivo_url, headers=headers) as response:
                    if response.status == 204:
                        logger.info(
                            "Successfully informed Plivo to end the call.", call_id=callback_call_id
                        )
                        return True
                    else:
                        logger.error(
                            f"Failed to end the call with Plivo. Status: {response.status}",
                            call_id=callback_call_id,
                        )
                        return False
        elif provider == "exotel":
            if websocket.client_state != WebSocketState.DISCONNECTED:
                await websocket.close()
                await cleanup_connection(
                    callback_call_id,
                    context_aggregator,
                    transcript_handler,
                    task,
                    task_references,
                    function_call_monitor,
                    logger,
                    record_locally,
                )
            return True
        elif provider == "custom":
            if websocket.client_state != WebSocketState.DISCONNECTED:
                await websocket.close()
                await cleanup_connection(
                    callback_call_id,
                    context_aggregator,
                    transcript_handler,
                    task,
                    task_references,
                    function_call_monitor,
                    logger,
                    record_locally,
                )
            return True
        elif provider == "livekit":
            # make a call to calling backend with status as completed
            await update_webcall_status(
                call_id=call_id,
                callback_call_id=callback_call_id,
                status="completed",
                sub_status="completed",
                logger=logger,
            )
            # await transport.cleanup()
            await cleanup_connection(
                callback_call_id,
                context_aggregator,
                transcript_handler,
                task,
                task_references,
                function_call_monitor,
                logger,
                record_locally,
            )
            logger.info("successfully closed the webrtc connection!", call_id=callback_call_id)

    except Exception as e:
        print(e)
        logger.exception("End call failed", call_id=callback_call_id)
        return False


async def end_call_function(
    function_name,
    tool_call_id,
    args,
    llm,
    telephony_provider,
    call_id,
    stream_id,
    websocket_client,
    callback_call_id,
    context_aggregator,
    transcript_handler,
    task,
    task_references,
    bot_speaking_frame_monitor,
    final_message_done_event,
    function_call_monitor,
    logger,
    transport: Optional[Any] = None,
):
    logger.debug("End call function called")
    function_call_monitor.append("end_call_called")
    final_message = args["final_message"]
    await llm.push_frame(TTSSpeakFrame(final_message))

    # Set flag to monitor inactivity and start monitoring task
    bot_speaking_frame_monitor.waiting_for_final_message = True
    bot_speaking_frame_monitor.last_frame_time = None

    async def wait_for_bot_speaking_inactivity():
        try:
            while True:
                await asyncio.sleep(0.2)
                if bot_speaking_frame_monitor.last_frame_time is None:
                    continue
                elapsed = (
                    asyncio.get_event_loop().time() - bot_speaking_frame_monitor.last_frame_time
                )
                if elapsed >= 1.5:
                    break
            final_message_done_event.set()
        except asyncio.CancelledError:
            final_message_done_event.set()
            raise

    inactivity_task = asyncio.create_task(wait_for_bot_speaking_inactivity())
    task_references.append(inactivity_task)
    logger.debug("Waiting for final message audio to finish...")
    await final_message_done_event.wait()
    logger.debug("Final message audio has been sent.")

    bot_speaking_frame_monitor.waiting_for_final_message = False

    success = await end_call(
        telephony_provider,
        call_id,
        stream_id,
        websocket_client,
        callback_call_id,
        context_aggregator,
        transcript_handler,
        task,
        task_references,
        function_call_monitor,
        logger,
        transport,
    )
    return success
