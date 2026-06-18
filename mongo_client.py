# from pymongo import MongoClient
# from datetime import datetime


# class MongoStorage:

#     def __init__(self, uri: str, db: str, collection: str):
#         self.collection = MongoClient(uri)[db][collection]

#     def save(
#         self,
#         pnkc: str,
#         file_name: str,
#         source_text: str,
#         accepted_text: str,
#         translated_text: str,
#         model: str,
#         src_lang: str,
#         tgt_lang: str,
#         # was_truncated: bool
#     ):
#         self.collection.update_one(
#             {"_id": pnkc},
#             {
#                 "$set": {
#                     "file_name": file_name,
#                     "source_text": source_text,
#                     "accepted_text": accepted_text,
#                     "translated_text": translated_text,
#                     "model": model,
#                     "source_lang": src_lang,
#                     "target_lang": tgt_lang,
#                     # "was_truncated": was_truncated,
#                     "updated_at": datetime.utcnow()
#                 },
#                 "$setOnInsert": {
#                     "created_at": datetime.utcnow()
#                 }
#             },
#             upsert=True
#         )

from pymongo import MongoClient
from datetime import datetime


class MongoStorage:

    def __init__(self, uri: str, db: str, collection: str):
        self.collection = MongoClient(uri)[db][collection]

    def save_section(
        self,
        pnkc: str,
        file_name: str,
        section: str,
        source_text: str,
        accepted_text: str,
        translated_text: str,
        latency_sec: float,
        model: str,
        src_lang: str,
        tgt_lang: str,
    ):
        now = datetime.utcnow()

        self.collection.update_one(
            {"_id": pnkc},
            {
                "$set": {
                    "file_name": file_name,

                    f"{section}.source": source_text,
                    f"{section}.accepted": accepted_text,
                    f"{section}.translated": translated_text,
                    f"{section}.latency_sec": round(latency_sec, 3),
                    f"{section}.updated_at": now,

                    "model": model,
                    "source_lang": src_lang,
                    "target_lang": tgt_lang,
                    "updated_at": now
                },
                "$setOnInsert": {
                    "created_at": now
                }
            },
            upsert=True
        )

    def fetch_summary_by_pnkc(self, pnkc: str):
        return self.collection.find_one(
            {"_id": pnkc},
            {"pnkc": 1, "summary": 1}
        )
    
    def translation_exists(self, pnkc: str):
        return self.collection.find_one({"_id": pnkc}) is not None

    def upsert_translation(self, pnkc, **translation_data):
        self.collection.update_one(
            {"_id": pnkc},
            {
                "$set": {
                    "_id": pnkc,
                    "summary_translation": translation_data
                }
            },
            upsert=True
        )
