# 📄 Resume Analyzer AI Service

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688.svg)
![Gemini AI](https://img.shields.io/badge/AI-Google_Gemini-orange.svg)
![Pydantic](https://img.shields.io/badge/Validation-Pydantic-e92063.svg)

A production-ready backend service designed to parse, evaluate, and extract actionable insights from candidate resumes. By leveraging natural language processing and Google's Gemini API, this service automates the initial screening process and provides deep, structured feedback for candidates.

---

## ✨ Core Features & Capabilities

* **Intelligent Document Extraction:** Seamlessly reads and extracts raw text from uploaded resume files, regardless of complex formatting (`document_reader.py`).
* **Dual-Tier Analysis Engine:** 
  * **Basic Tier:** Handles core resume parsing, skill extraction, and initial screening.
  * **Premium Tier:** Executes a deep-dive evaluation, generating constructive, non-sugar-coated feedback tailored to modern industry standards.
* **Context-Aware AI Feedback:** Uses the Google Gemini API to understand nuances in candidate experience and evaluate them against real-world tech requirements.
* **Structured Data Responses:** Ensures that all AI outputs are strictly formatted into predictable JSON schemas using Pydantic, preventing application crashes from hallucinated or malformed LLM responses.

---

## 🧠 Architecture & Design Reasoning

This project is built with a highly modular architecture. Here is the reasoning behind the structural design choices:

1. **FastAPI Framework (`main.py` & `routes/`)** 
   * **Why:** FastAPI provides native asynchronous support, which is critical when waiting for external API calls (like the Gemini LLM) and handling file I/O operations. It also auto-generates Swagger documentation, making frontend integration effortless.
2. **Tiered Business Logic (`analyser.py` vs. `premium_analyze.py`)** 
   * **Why:** Separating basic and premium analysis into different modules enforces the Single Responsibility Principle. It allows developers to scale, tweak, or monetize the heavy premium logic without accidentally breaking the lightweight basic parser.
3. **Dedicated AI Service Layer (`gemini_service.py`)** 
   * **Why:** By wrapping the Gemini API in its own service class, the core application is decoupled from the specific LLM provider. If you ever decide to switch to OpenAI or Anthropic, you only need to update this single file.
4. **Decoupled Prompts (`prompts/`)** 
   * **Why:** AI prompts are essentially the "configuration" of an LLM. Hardcoding them inside routing logic leads to messy code. Storing them in dedicated files allows for easy version control, A/B testing, and fine-tuning.
5. **Strict Data Validation (`schema/`)** 
   * **Why:** LLMs are inherently unpredictable. By enforcing output structures using Pydantic models, the backend guarantees that the frontend receives exactly the data shapes it expects, preventing UI runtime errors.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Framework:** FastAPI
* **AI/LLM:** Google Gemini API
* **Data Validation:** Pydantic
* **Environment Management:** `python-dotenv`

---

## 📁 Project Structure

```text
resume-analyser-ai-service/
├── .env                        # Local environment variables (API Keys)
├── .gitignore                  # Git ignore rules
├── app/                        # Main application package
│   ├── analyser.py             # Logic for basic resume screening
│   ├── document_reader.py      # Utility for extracting raw text from files
│   ├── gemini_service.py       # Wrapper for external AI model interactions
│   ├── main.py                 # FastAPI application initialization and base routes
│   ├── premium_analyze.py      # Heavy-duty logic for in-depth resume evaluation
│   ├── prompts/                # AI prompt engineering templates
│   │   ├── basic_prompt.py
│   │   └── premium_prompt.py
│   ├── routes/                 # API endpoint definitions
│   │   └── premium.py          # Routing for premium tier requests
│   └── schema/                 # Pydantic models for request/response validation
│       ├── basic_schema.py
│       ├── premium.py
│       └── premium_request.py

