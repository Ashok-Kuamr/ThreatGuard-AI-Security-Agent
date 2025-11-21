# src/agents/gemini_agent.py
"""
Robust GeminiAnalysisAgent
- Attempts to auto-detect a usable model from the installed Google Generative AI client.
- If no key or no usable model is found, falls back to a safe mock response so pipeline never crashes.
- Uses genai.GenerativeModel(...).generate_content(...) (compatible with many SDK versions).
"""

import os
import time
import json
try:
    import google.generativeai as genai
    HAS_GENAI = True
except Exception:
    HAS_GENAI = False

# Candidate model names to try (ordered from preferred -> fallback)
CANDIDATE_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-flash-latest"
]



class GeminiAnalysisAgent:
    def __init__(self, logger=None):
        self.logger = logger
        self.client_ready = False
        self.model = None
        self.model_name = None

        if not HAS_GENAI:
            if self.logger:
                self.logger.log("[GeminiAgent] google.generativeai package not installed — running in MOCK mode.")
            return

        api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
        if not api_key:
            if self.logger:
                self.logger.log("[GeminiAgent] No API key found in environment — running in MOCK mode.")
            return

        try:
            genai.configure(api_key=api_key)
            # Try to list models first (if SDK supports it)
            try:
                available = []
                if hasattr(genai, "list_models"):
                    # some SDK variants expose list_models()
                    models = genai.list_models()
                    for m in models:
                        # m may be dict-like or object
                        name = getattr(m, "name", None) or (m.get("name") if isinstance(m, dict) else None)
                        if name:
                            available.append(name)
                else:
                    # not supported in this SDK version — set available empty and rely on candidates
                    available = []
            except Exception:
                available = []

            # choose model
            chosen = None
            # prefer any candidate present in available list
            for cand in CANDIDATE_MODELS:
                if available and cand in available:
                    chosen = cand
                    break
            # if none found by listing, try to instantiate candidates (some SDKs will throw on unsupported)
            if not chosen:
                for cand in CANDIDATE_MODELS:
                    try:
                        # attempt to create model object then call no-op to verify
                        model = genai.GenerativeModel(cand)
                        # don't call generate yet; we only assume instantiation means it's present
                        chosen = cand
                        break
                    except Exception:
                        continue

            if not chosen:
                # final fallback: try a very generic name supported by older SDKs
                try:
                    _ = genai.GenerativeModel("models/gemini-1.0-pro")
                    chosen = "models/gemini-1.0-pro"
                except Exception:
                    chosen = None

            if chosen:
                try:
                    self.model = genai.GenerativeModel(model_name=chosen)
                    self.model_name = chosen
                    self.client_ready = True
                    if self.logger:
                        self.logger.log(f"[GeminiAgent] Gemini client initialized using model '{chosen}'.")
                except Exception as e:
                    self.model = None
                    self.client_ready = False
                    if self.logger:
                        self.logger.log(f"[GeminiAgent] Could not initialize model '{chosen}': {e}")
            else:
                if self.logger:
                    self.logger.log("[GeminiAgent] No compatible Gemini model found — running in MOCK mode.")

        except Exception as e:
            if self.logger:
                self.logger.log(f"[GeminiAgent] Error configuring Gemini client: {e}")
            self.client_ready = False

    # Internal safe generate wrapper
    def _generate_safe(self, prompt, max_chars=2000):
        if not self.client_ready or not self.model:
            if self.logger:
                self.logger.log("[GeminiAgent] MOCK generate (no model).")
            time.sleep(0.15)
            return "MOCK: Gemini not available — simulated analysis."

        try:
            # Use generate_content if available
            if hasattr(self.model, "generate_content"):
                resp = self.model.generate_content(prompt)
                # unify response access
                text = getattr(resp, "text", None)
                if text is None:
                    # try dict-like response
                    try:
                        text = resp["candidates"][0]["content"]
                    except Exception:
                        text = str(resp)
                return text[:max_chars]
            else:
                # older/newer SDK may use different method names - try 'generate'
                if hasattr(self.model, "generate"):
                    resp = self.model.generate(prompt)
                    return getattr(resp, "text", str(resp))[:max_chars]
                else:
                    return "MOCK: model has no generate_content method."
        except Exception as e:
            if self.logger:
                self.logger.log(f"[GeminiAgent] Error during generation: {e}")
            return f"ERROR: {e}"

    def analyze_file_with_gemini(self, file_content: str) -> dict:
        prompt = (
            "You are a cybersecurity analyst. Analyze the following file content and:\n"
            "1) Identify possible vulnerabilities or malicious patterns.\n"
            "2) Provide a short severity label (low/medium/high).\n"
            "3) Suggest 3 concise remediation steps.\n\n"
            "File content:\n----START----\n"
            f"{file_content}\n"
            "----END----\n\n"
            "Return a JSON-like short summary and recommendations."
        )
        raw = self._generate_safe(prompt)
        # Try to parse JSON; if not, return raw text in summary
        try:
            parsed = json.loads(raw)
            return parsed
        except Exception:
            return {"severity": "unknown", "summary": raw, "recommendations": ["See summary above."]}

    def analyze_system_with_gemini(self, system_scan: dict) -> dict:
        prompt = (
            "You are a security engineer. Given this system scan result, summarize the top risks and suggest 5 prioritized hardening actions.\n\n"
            f"System scan:\n{json.dumps(system_scan, indent=2)}\n\n"
            "Return a JSON-like object with keys: top_risks, prioritized_actions."
        )
        raw = self._generate_safe(prompt)
        try:
            parsed = json.loads(raw)
            return parsed
        except Exception:
            return {"top_risks": ["unparsed"], "prioritized_actions": [raw]}
