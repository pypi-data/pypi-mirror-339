from backchannel import BackchannelProcessor
from hold_detector import HoldDetector
from voicemail_detector import VoicemailDetector

from pipecat.processors.filters.stt_mute_filter import (
    STTMuteConfig,
    STTMuteFilter,
    STTMuteStrategy,
)
from pipecat.processors.two_stage_user_idle_processor import TwoStageUserIdleProcessor
from pipecat.processors.user_idle_processor import UserIdleProcessor


def initialize_stt_mute_strategy(mute_during_intro, mute_while_bot_speaking, pipeline_steps):
    if mute_during_intro or mute_while_bot_speaking:
        # Mute during first speech only
        mute_strategy = {STTMuteStrategy.FUNCTION_CALL}
        if mute_during_intro:
            mute_strategy.add(STTMuteStrategy.MUTE_UNTIL_FIRST_BOT_COMPLETE)
        if mute_while_bot_speaking:
            mute_strategy.add(STTMuteStrategy.ALWAYS)
        stt_mute_filter_config = STTMuteConfig(strategies=mute_strategy)
        stt_mute_filter = STTMuteFilter(config=stt_mute_filter_config)
        pipeline_steps.append(stt_mute_filter)


def initialize_voicemail_detector(
    mute_during_intro,
    mute_while_bot_speaking,
    voicemail_detect,
    pipeline_steps,
    vad_params_bot_silent,
    end_callback,
):
    if mute_during_intro or mute_while_bot_speaking:
        # Processor to handle voicemail and when the user puts the call on hold.
        if voicemail_detect:
            voicemail_detector = VoicemailDetector(
                end_callback=end_callback, vad_params_bot_silent=vad_params_bot_silent
            )
            pipeline_steps.append(voicemail_detector)


def initialize_filler_config(call_config, transport, tts_voice, language, pipeline_steps):
    if call_config.get("filler_config", {}).get("enable_filler_words", False):
        backchannel_processor = BackchannelProcessor(
            transport=transport.output(),
            backchannel_base_dir="fillers",
            voice=tts_voice,
            words=call_config.get("filler_config", {}).get("filler_words", []),
            language=language,
            filler_frequency=call_config.get("filler_config", {}).get("filler_frequency", 0.2),
        )
        pipeline_steps.append(backchannel_processor)


def initialize_hold_detector(call_hold_config, end_callback, pipeline_steps):
    if call_hold_config.get("detect", False):
        hold_detector = HoldDetector(
            end_callback=end_callback, end_count=call_hold_config.get("end_count", 3)
        )
        pipeline_steps.append(hold_detector)


def initialize_user_idle(
    idle_timeout_warning,
    idle_timeout_end,
    end_callback,
    warning_callback,
):
    if idle_timeout_warning == 0 or idle_timeout_warning == idle_timeout_end:
        user_idle = UserIdleProcessor(callback=end_callback, timeout=idle_timeout_end)
    else:
        user_idle = TwoStageUserIdleProcessor(
            warning_timeout=idle_timeout_warning,
            end_timeout=idle_timeout_end,
            warning_callback=warning_callback,
            end_callback=end_callback,
        )

    return user_idle
