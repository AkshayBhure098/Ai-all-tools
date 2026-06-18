from translation import TranslateGemmaTranslator
from mongo_client import MongoStorage
import config
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main(pnkc: str, translator):
    logger.info("Starting translation | PNKC=%s", pnkc)

    # Initialize source Mongo
    source_mongo = MongoStorage(
        config.SOURCE_MONGO_URI,
        config.SOURCE_DB_NAME,
        config.SOURCE_COLLECTION
    )

    # Target Mongo (Disabled for now)
    # target_mongo = MongoStorage(
    #     config.MONGO_URI,
    #     config.DB_NAME,
    #     config.COLLECTION_NAME
    # )

    # Fetch summary by PNKC
    document = source_mongo.fetch_summary_by_pnkc(pnkc)

    if not document:
        logger.error("No document found | PNKC=%s", pnkc)
        return None

    summary_text = document.get("summary")

    if not summary_text:
        logger.error("Empty summary | PNKC=%s", pnkc)
        return None

    # Optional skip check (disabled)
    # if target_mongo.translation_exists(pnkc):
    #     logger.info("Translation already exists | PNKC=%s", pnkc)
    #     return

    # Translate
    translated, accepted_text, latency = translator.translate(summary_text)

    logger.info(
        "Translation completed | PNKC=%s | latency=%.2fs",
        pnkc,
        latency
    )

    # Store translation (disabled)
    # target_mongo.upsert_translation(
    #     pnkc=pnkc,
    #     source_text=summary_text,
    #     accepted_text=accepted_text,
    #     translated_text=translated,
    #     latency_sec=latency,
    #     model=config.MODEL_NAME,
    #     src_lang=config.SOURCE_LANG,
    #     tgt_lang=config.TARGET_LANG,
    # )

    return {
        "pnkc": pnkc,
        "source_text": summary_text,
        "translated_text": translated,
        "latency": latency,
    }


# ---------------------------------
# CLI Execution Support
# ---------------------------------
if __name__ == "__main__":
    translator = TranslateGemmaTranslator()
    result = main("US1234567A", translator)
    print(result)
