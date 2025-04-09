from deepgram import LiveOptions  # noqa: D100
from env_config import api_config

from pipecat.processors.metrics.sentry import SentryMetrics
from pipecat.services.azure import AzureSTTService
from pipecat.services.deepgram import DeepgramSTTService
from pipecat.services.gladia import GladiaSTTService
from pipecat.services.google import (
    GoogleSTTService,
)
from pipecat.transcriptions.language import Language


def initialize_stt_service(stt_provider, language, logger, record_locally=False):
    if stt_provider == "deepgram":
        keywords = []
        if language.startswith("hi"):
            keywords.extend(["हाँ:1.5", "हाँ जी:1.5"])
        elif language.startswith("en"):
            keywords.extend(["ha:1.5", "haan:1.5"])
        live_options = LiveOptions(
            model="nova-2-phonecall" if language.startswith("en") else "nova-2",
            language=language,
            # sample_rate=16000,
            encoding="linear16",
            channels=1,
            interim_results=True,
            smart_format=False,
            numerals=False,
            punctuate=True,
            profanity_filter=True,
            vad_events=False,
            keywords=keywords,
        )
        stt = DeepgramSTTService(
            api_key=api_config.DEEPGRAM_API_KEY,
            live_options=live_options,
            audio_passthrough=record_locally,
            # metrics=SentryMetrics(),
        )
    elif stt_provider == "google":
        logger.debug("Google STT initilaising")
        languages = list({Language(language), Language.EN_IN})
        # list of languages you want to support; adjust if needed
        stt = GoogleSTTService(
            params=GoogleSTTService.InputParams(
                languages=languages, enable_automatic_punctuation=False, model="latest_short"
            ),
            credentials_path="creds.json",  # your service account JSON file,
            location="us",
            audio_passthrough=record_locally,
            # metrics=SentryMetrics(),
        )
        logger.debug("Google STT initiaised")
    elif stt_provider == "azure":
        logger.debug(
            f"Initializing Azure STT. Received language parameter: '{language}' (type: {type(language)})"
        )  # ADDED LOG
        # Explicitly check the condition and log the result
        is_telugu = language == "te-IN"
        additional_langs = [Language.EN_IN] if is_telugu else []
        stt = AzureSTTService(
            api_key=api_config.AZURE_SPEECH_API_KEY,
            region=api_config.AZURE_SPEECH_REGION,
            language=Language(language),
            additional_languages=additional_langs,
            audio_passthrough=record_locally,
            # metrics=SentryMetrics(),
        )
    elif stt_provider == "gladia":
        params = GladiaSTTService.InputParams(language=Language(language))
        stt = GladiaSTTService(
            api_key=api_config.GLADIA_API_KEY,
            params=params,
            audio_passthrough=record_locally,
            # metrics=SentryMetrics(),
        )

    return stt
