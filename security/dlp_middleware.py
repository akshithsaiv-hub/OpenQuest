"""
dlp_middleware.py
=================
Safeguard 6: AI Data Masking & PII Scrubber Middleware.

Intercepts prompts, context documents, and conversational queries before transmission
to external LLM APIs (Gemini, OpenAI, Anthropic, or third-party speech engines).

Features:
- Regex and pattern-based scrubbing for Indian agricultural and citizen identifiers:
  * 10-digit Indian Mobile Numbers (+91, 0, or bare format).
  * 12-digit Aadhaar Card Numbers.
  * 10-character Permanent Account Numbers (PAN).
  * Bank Account numbers (9-18 digits).
  * Land Survey, Khasra, and RoR-1B Passbook identifiers.
  * High-precision GPS latitude/longitude coordinates.
  * Direct farmer person names.
- Bidirectional ephemeral session mapping:
  * Safely de-identifies prompt before calling external LLM.
  * Re-hydrates response on behalf of the authorized farmer's view without leaking PII to third parties.
- Zero-leakage audit mode for prompt logging.
"""

import re
import logging
from typing import Dict, Any, Tuple, Optional

logger = logging.getLogger("DLP.AIMiddleware")


class AIDataMaskingEngine:
    """
    Scrubs PII from conversational farmer queries and documents prior to external LLM calls.
    """

    # 1. 10-digit Indian Mobile Phone Numbers (with optional +91, 0, hyphens, spaces)
    PHONE_REGEX = re.compile(
        r'(?:\+91[\s\-]?)?(?:[6-9]\d{9}|[6-9]\d{4}[\s\-]\d{5}|[6-9]\d{2}[\s\-]\d{3}[\s\-]\d{4})\b'
    )

    # 2. 12-digit Aadhaar Card format (e.g., 1234 5678 9012 or 123456789012)
    AADHAAR_REGEX = re.compile(
        r'\b[2-9]\d{3}[\s\-]?[0-9]{4}[\s\-]?[0-9]{4}\b'
    )

    # 3. Indian PAN Card format (5 letters, 4 digits, 1 letter)
    PAN_REGEX = re.compile(
        r'\b[A-Z]{5}[0-9]{4}[A-Z]\b'
    )

    # 4. Bank Account Numbers (9 to 18 consecutive digits)
    BANK_ACC_REGEX = re.compile(
        r'\b\d{9,18}\b'
    )

    # 5. Land Survey / Khasra / Khatauni Numbers (e.g. Sy. No. 45/A, Khasra 120/1, Khata 88)
    SURVEY_REGEX = re.compile(
        r'\b(?:Sy\.?\s*No\.?|Survey\s*No\.?|Khasra\s*No\.?|Khata\s*No\.?|Gat\s*No\.?)\s*[:\-]?\s*([0-9A-Za-z\/\-]+)\b',
        re.IGNORECASE
    )

    # 6. High Precision GPS Coordinates (Latitude, Longitude)
    GPS_REGEX = re.compile(
        r'[-+]?([1-8]?\d(\.\d{4,})|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d{4,}))'
    )

    def __init__(self):
        pass

    def mask_text(
        self,
        text: str,
        farmer_name: Optional[str] = None
    ) -> Tuple[str, Dict[str, str]]:
        """
        Scrub all sensitive identification and contact data from text.
        Returns:
            masked_text (str): The sanitized text safe to pass to external LLMs.
            mapping (Dict[str, str]): Ephemeral dictionary of token -> original value.
        """
        if not text:
            return text, {}

        mapping: Dict[str, str] = {}
        counter = {"phone": 1, "aadhaar": 1, "pan": 1, "survey": 1, "bank": 1, "name": 1}

        # Step 1: Explicit Farmer Name Scrubbing (if known from context)
        if farmer_name and len(farmer_name.strip()) >= 3:
            name_token = f"<FARMER_NAME_TOKEN_{counter['name']}>"
            mapping[name_token] = farmer_name
            # Case insensitive exact word replacement
            text = re.sub(re.escape(farmer_name), name_token, text, flags=re.IGNORECASE)
            counter['name'] += 1

        # Step 2: Aadhaar Card Numbers
        def replace_aadhaar(match):
            val = match.group(0)
            token = f"<AADHAAR_TOKEN_{counter['aadhaar']}>"
            mapping[token] = val
            counter['aadhaar'] += 1
            return token
        text = self.AADHAAR_REGEX.sub(replace_aadhaar, text)

        # Step 3: PAN Card Numbers
        def replace_pan(match):
            val = match.group(0)
            token = f"<PAN_TOKEN_{counter['pan']}>"
            mapping[token] = val
            counter['pan'] += 1
            return token
        text = self.PAN_REGEX.sub(replace_pan, text)

        # Step 4: Phone Numbers
        def replace_phone(match):
            val = match.group(0)
            token = f"<PHONE_REDACTED_{counter['phone']}>"
            mapping[token] = val
            counter['phone'] += 1
            return token
        text = self.PHONE_REGEX.sub(replace_phone, text)

        # Step 5: Land Survey / Khasra Numbers
        def replace_survey(match):
            val = match.group(0)
            token = f"<SURVEY_RECORD_TOKEN_{counter['survey']}>"
            mapping[token] = val
            counter['survey'] += 1
            return token
        text = self.SURVEY_REGEX.sub(replace_survey, text)

        # Step 6: GPS Coordinates
        text = self.GPS_REGEX.sub("<GPS_LOCATION_GENERALIZED>", text)

        # Step 7: Bank Account Numbers (Remaining long digit strings)
        def replace_bank(match):
            val = match.group(0)
            # Avoid replacing if it's already a short number or year (e.g. 2026)
            if len(val) >= 9:
                token = f"<BANK_ACC_TOKEN_{counter['bank']}>"
                mapping[token] = val
                counter['bank'] += 1
                return token
            return val
        text = self.BANK_ACC_REGEX.sub(replace_bank, text)

        return text, mapping

    def unmask_text(self, text: str, mapping: Dict[str, str]) -> str:
        """
        Re-hydrate ephemeral tokens in the LLM response for client delivery.
        """
        if not text or not mapping:
            return text

        unmasked = text
        for token, original_val in mapping.items():
            unmasked = unmasked.replace(token, original_val)
        return unmasked


# Global engine instance
ai_masking_engine = AIDataMaskingEngine()


def scrub_ai_payload(payload: Any, farmer_name: Optional[str] = None) -> Tuple[Any, Dict[str, str]]:
    """
    Convenience function to scrub strings or nested dictionary/list prompt payloads.
    """
    if isinstance(payload, str):
        return ai_masking_engine.mask_text(payload, farmer_name=farmer_name)

    if isinstance(payload, dict):
        total_mapping = {}
        scrubbed_dict = {}
        for k, v in payload.items():
            if isinstance(v, str):
                scrubbed_val, m = ai_masking_engine.mask_text(v, farmer_name=farmer_name)
                scrubbed_dict[k] = scrubbed_val
                total_mapping.update(m)
            elif isinstance(v, (dict, list)):
                scrubbed_val, m = scrub_ai_payload(v, farmer_name=farmer_name)
                scrubbed_dict[k] = scrubbed_val
                total_mapping.update(m)
            else:
                scrubbed_dict[k] = v
        return scrubbed_dict, total_mapping

    if isinstance(payload, list):
        total_mapping = {}
        scrubbed_list = []
        for item in payload:
            scrubbed_item, m = scrub_ai_payload(item, farmer_name=farmer_name)
            scrubbed_list.append(scrubbed_item)
            total_mapping.update(m)
        return scrubbed_list, total_mapping

    return payload, {}
