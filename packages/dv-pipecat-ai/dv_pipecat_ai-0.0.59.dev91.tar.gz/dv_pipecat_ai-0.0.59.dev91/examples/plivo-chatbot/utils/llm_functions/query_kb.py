import random
import time

from weaviate.classes.query import Filter


async def query_knowledge_base(
    function_name,
    tool_call_id,
    arguments,
    tts,
    pre_query_phrases,
    kb_name_to_id_map,
    weaviate_client,
    collection_name,
    result_callback,
    function_call_monitor,
    logger,
):
    function_call_monitor.append("query_knowledge_base_called")
    phrase = random.choice(pre_query_phrases)
    await tts.say(phrase)
    logger.debug(f"Querying knowledge base for question: {arguments['question']}")
    question = arguments["question"]
    formatting_instructions = (
        "Format the result in a concise answer. The number of words should be less than 50 words. "
        "Answer only to the query which user asked and don't add anything extra. "
        "Also convert numbers to words as needed. query-> "
    )
    formatting_instructions += question
    kb_id = kb_name_to_id_map[arguments["rag_file_name"]]
    start = time.perf_counter()

    collection = weaviate_client.collections.get(collection_name)
    answer = (
        await collection.generate.near_text(
            query=question,
            limit=4,
            grouped_task=formatting_instructions,
            filters=Filter.by_property("knowledge_base_id").equal(kb_id),
        )
    ).generated

    if answer is None:
        logger.debug("kb_id not found on weaviate!")
        answer = "I am sorry I couldn't find anything!"
    end = time.perf_counter()
    logger.debug(f"Time taken: {end - start:.2f} seconds")
    await result_callback(answer)
