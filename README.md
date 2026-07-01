# 🎙️ Voice AI Interview Agent – AI-Powered Stateful Interview System

The Voice AI Interview Agent is a full-stack AI system that simulates real technical interviews through a complete Speech → AI → Speech pipeline.

Unlike traditional interview practice tools that rely on static Q&A or post-interview feedback, this system runs a **stateful, dynamic interview session** where each response influences the next question, evaluation, and difficulty progression in real time.

The system is designed to behave like a real interviewer — adaptive, contextual, and continuously evaluating performance throughout the session instead of only at the end.

---

## 🚨 Problem Statement

Most existing interview preparation tools fail in three critical ways:

* Static question flows with no conversational intelligence
* Generic feedback generated only after the interview ends
* No adaptation based on user performance or response quality

This results in a passive learning experience that does not simulate real interview pressure, reasoning, or adaptability.

---

## 💡 Solution

This system introduces a **stateful AI interview engine** that:

* Conducts real-time adaptive interviews
* Evaluates every response individually
* Tracks difficulty progression dynamically
* Maintains full session memory across turns
* Generates structured feedback at both micro and macro levels

The goal is to simulate an **actual technical interviewer**, not a chatbot.

---

## ⚙️ Key Features

### 🎙️ Real-Time Voice Interview Pipeline

User speech is converted into text, processed by AI, and converted back into speech for natural conversational flow.

### 🧠 Dynamic Question Generation

Each next question is generated based on:

* Previous answer quality
* Current difficulty level
* Interview progression state

### 📊 Per-Response Evaluation System

Every answer is evaluated independently with:

* Individual scoring
* Qualitative feedback
* Difficulty tagging

### 🗄️ Persistent Interview State

All interview sessions are stored in PostgreSQL, including:

* Questions asked
* User responses
* Scores and evaluations
* Session progression state

### 🔊 Speech Output Engine

AI-generated questions are converted into natural speech using TTS for a realistic interview experience.

### 📈 Final Session Analysis

At the end of the interview, the system generates:

* Overall performance score
* Strength analysis
* Weakness identification
* Personalized improvement suggestions
* Learning tags
* Interview difficulty assessment

---

## ⚙️ System Architecture

User (Speech Input)
↓
Speech-to-Text (Deepgram)
↓
FastAPI Backend (Interview Orchestrator)
↓
Groq LLM (Evaluation + Next Question Generation)
↓
PostgreSQL (Session + State Storage)
↓
Edge-TTS (Text-to-Speech)
↓
Audio Output to User

---

## 🔄 Request Flow

User starts interview session
↓
Backend initializes interview state
↓
User speaks answer
↓
Speech converted to text (STT)
↓
LLM evaluates response + assigns score
↓
State updated in PostgreSQL
↓
LLM generates next question dynamically
↓
Question converted to speech (TTS)
↓
Next interview cycle continues
↓
Final session triggers full analysis report

---

## ⚙️ Tech Stack

### Backend

* FastAPI – Core backend framework
* PostgreSQL – Session and state storage
* SQLAlchemy – ORM layer
* Groq LLM – Answer evaluation + question generation
* Deepgram – Speech-to-Text engine
* Edge-TTS – Text-to-Speech engine

### AI Layer

* LLM-based evaluation engine
* Stateful prompt orchestration
* Dynamic difficulty progression logic
* Structured response parsing

### Core Concepts Used

* Stateful AI orchestration
* Multi-step LLM pipelines
* Real-time conversational systems
* Event-driven backend design

---

## 🧠 Challenges Faced

### 1. Maintaining Interview State Across Turns

The hardest problem was ensuring continuity between multiple user responses without losing context or resetting evaluation logic.

### 2. Separating Per-Answer vs Final Evaluation

Initially, feedback was too generic. Splitting micro-evaluation (per answer) and macro-evaluation (full session) significantly improved accuracy and usefulness.

### 3. Latency in Voice Pipeline

Speech-to-text + LLM + TTS introduced delay. Orchestration optimization became critical.

### 4. Consistent Evaluation Formatting

LLM responses were inconsistent until strict structured prompting was enforced.

---

## 📌 Key Learnings

* Voice AI systems are primarily orchestration problems, not model problems
* Stateful design is significantly harder than stateless chat systems
* Structured prompting is essential for production-grade AI systems
* Real-time systems require strict control over latency and pipeline ordering
* Separating evaluation layers improves output quality dramatically

---

## 🚀 Future Improvements

* Real-time streaming voice conversation (low latency pipeline)
* Web-based frontend interview interface
* Emotion and confidence detection from voice
* Interview replay and analytics dashboard
* Multi-language interview support
* Resume-aware interview personalization

---

## 👤 Author

**Geethika Nagasri Tammineni**

Aspiring Software Engineer | Backend + AI Systems Builder

Focused on building production-grade AI systems that combine LLMs, voice interfaces, and scalable backend architecture.

---
