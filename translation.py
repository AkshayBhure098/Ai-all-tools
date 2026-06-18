import time
import logging
from tracemalloc import start
import torch
from transformers import pipeline
from huggingface_hub import login

logger = logging.getLogger(__name__)


import time
import torch
import logging
from huggingface_hub import login
from transformers import pipeline

from folder_reader import read_txt_folder
from mongo_client import MongoStorage
import config


# -----------------------
# Logging Configuration
# -----------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("TranslateGemmaPOC")


import os


def extract_pnkc(file_name: str) -> str:
    return os.path.splitext(file_name)[0]


class TranslateGemmaTranslator:
    """
    POC-only TranslateGemma translator.
    Character-bound, period-safe, deterministic.
    Messages-only (no prompt).
    """

    def __init__(self):
        logger.info("Initializing TranslateGemma translator")

        login(token=config.HF_TOKEN)

        device = "cuda" if torch.cuda.is_available() else "cpu"

        self.pipe = pipeline(
            task="image-text-to-text",
            model=config.MODEL_NAME,
            device=device,
            dtype=torch.bfloat16,
            token=True
        )

        self.tokenizer = self.pipe.tokenizer
        self.max_ctx = self.tokenizer.model_max_length

        # Business constraint
        self.max_chars = 2000

        # # Defensive token ceiling
        # self.gen_buffer_tokens = 512
        # self.max_text_tokens = min(
        #     1024,
        #     self.max_ctx - self.gen_buffer_tokens
        # )

        # logger.info(
        #     "Model loaded | model=%s | device=%s | max_ctx=%d | "
        #     "max_chars=%d | max_text_tokens=%d",
        #     config.MODEL_NAME,
        #     config.DEVICE,
        #     self.max_ctx,
        #     self.max_chars,
        #     self.max_text_tokens
        # )

    def _extract_complete_text(self, text: str) -> str:
        """
        Extract up to max_chars and rollback to last full stop.
        Deterministic and zero-overhead.
        """
        if not text or not text.strip():
            raise ValueError("Empty input text")

        text = text.strip()

        if len(text) <= self.max_chars:
            return text

        # Hard cut
        text = text[:self.max_chars]

        # Roll back to last complete sentence
        last_dot = text.rfind(".")
        if last_dot != -1:
            text = text[: last_dot + 1]

        return text

    # def translate(self, text: str) -> tuple[str, str]:
    #     """
    #     Returns:
    #         translated_text,
    #         accepted_source_text
    #     """

    #     # ---- CHARACTER-BASED EXTRACTION ----
    #     accepted_text = self._extract_complete_text(text)


    #     # ---- MESSAGES-ONLY PAYLOAD ----
    #     messages = [
    #         {
    #             "role": "user",
    #             "content": [
    #                 {
    #                     "type": "text",
    #                     "source_lang_code": config.SOURCE_LANG,
    #                     "target_lang_code": config.TARGET_LANG,
    #                     "text": accepted_text
    #                 }
    #             ]
    #         }
    #     ]

    #     # ---- MODEL INVOCATION ----
    #     start = time.perf_counter()

    #     result = self.pipe(
    #         text=messages,
    #         max_new_tokens=1500,
    #         do_sample=False
    #     )

    #     latency = time.perf_counter() - start

    #     logger.info(
    #         "Translation completed | latency=%.2fs",
    #         latency
    #     )

    #     translated_text = result[0]["generated_text"][-1]["content"]

    #     return translated_text, accepted_text

    def translate(self, text: str) -> tuple[str, str, float]:
        """
        Returns:
            translated_text,
            accepted_source_text,
            latency_seconds
        """
        # accepted_text = self._extract_complete_text(text)
        
        accepted_text = text
        
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "source_lang_code": config.SOURCE_LANG,
                        "target_lang_code": config.TARGET_LANG,
                        "text": accepted_text
                    }
                ]
            }
        ]

        start = time.perf_counter()

        result = self.pipe(
            text=messages,
            max_new_tokens=1500,
            do_sample=False
        )

        latency = time.perf_counter() - start

        translated_text = result[0]["generated_text"][-1]["content"]

        return translated_text, accepted_text, latency


import time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


class XALMATranslator:
    """
    X-ALMA translation wrapper.
    Deterministic generation, latency tracked.
    """

    def __init__(self, group_id: str = "6"):
        model_name = f"haoranxu/X-ALMA-13B-Group{group_id}"

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto" if self.device == "cuda" else None
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            padding_side="left"
        )
        self.tokenizer.pad_token = self.tokenizer.eos_token

        self.max_chars = 2000

    def _extract_complete_text(self, text: str) -> str:
        if not text or not text.strip():
            raise ValueError("Empty input text")

        text = text.strip()

        if len(text) <= self.max_chars:
            return text

        text = text[:self.max_chars]
        last_dot = text.rfind(".")
        if last_dot != -1:
            text = text[: last_dot + 1]

        return text

    def _build_prompt(self, text: str, source_lang="English", target_lang="Japanese"):
        prompt = f"""<s>[INST] Translate this from {source_lang} to {target_lang}:
{source_lang}: {text}
{target_lang}: [/INST]"""

        chat_style_prompt = [{"role": "user", "content": prompt}]

        return self.tokenizer.apply_chat_template(
            chat_style_prompt,
            tokenize=False,
            add_generation_prompt=True
        )

    def _extract_translated_text(self, full_output: str, target_lang: str = "Japanese") -> str:
        """
        Extract ONLY the translated text from the full model output.
        
        The output contains the prompt and special tokens which we need to remove.
        """
        
        # Look for the target language marker with /INST tag
        target_lang_marker = f"{target_lang}: [/INST]"
        
        if target_lang_marker in full_output:
            # Extract everything after "[/INST]"
            translation = full_output.split(target_lang_marker)[-1].strip()
        else:
            # Fallback
            translation = full_output.split(f"{target_lang}:")[-1].strip()
        
        # Remove special tokens
        translation = translation.replace("[/INST]", "").strip()
        translation = translation.replace("<|end_header_id|>", "").strip()
        translation = translation.replace("</s>", "").strip()
        
        # Remove any remaining language prefixes
        for prefix in ["Japanese:", "English:", "Chinese:", "German:", "Spanish:", "French:"]:
            if translation.startswith(prefix):
                translation = translation[len(prefix):].strip()
        
        return translation


    def translate(self, text: str, source_lang="English", target_lang="Japanese") -> tuple[str, str, float]:
        """..."""
        
        accepted_text = self._extract_complete_text(text)
        full_prompt = self._build_prompt(accepted_text, source_lang, target_lang)
        
        input_ids = self.tokenizer(
            full_prompt,
            return_tensors="pt",
            padding=True,
            truncation=True
        ).input_ids.to(self.device)
        
        start = time.perf_counter()
        
        with torch.no_grad():
            generated_ids = self.model.generate(
                input_ids,
                num_beams=5,
                max_new_tokens=2048,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        latency = time.perf_counter() - start
        
        full_output = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        # ✅ FIXED: Extract only translated text
        translated_text = self._extract_translated_text(full_output, target_lang)
        
        return translated_text, accepted_text, latency
    
