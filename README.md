# VoiceBench

### A Low-Latency Event-Driven Voice AI Platform for Adaptive Topic-Focused Oral Assessment

> A research-oriented voice AI platform that simulates real-time oral assessments through natural voice conversations. VoiceBench combines streaming speech recognition, adaptive questioning, conversational memory, and automated evaluation to create a low-latency interview experience across any learning domain—from computer science to science, aptitude, languages, and general knowledge.

VoiceBench is an event-driven voice AI assessment platform designed to bridge the gap between traditional text-based AI systems and real-time spoken interactions. Instead of relying on typed responses, the platform conducts adaptive voice conversations that continuously evaluate a learner's understanding while dynamically adjusting question difficulty.

The system employs a streaming architecture consisting of Speech-to-Text (STT), a conversational orchestration engine, Large Language Models (LLMs), and Text-to-Speech (TTS) synthesis to minimize interaction latency and create a natural interview experience. Every interview session is automatically evaluated, scored, and archived, enabling detailed performance analytics and longitudinal learning assessment.

![Python](https://img.shields.io/badge/Python-3.11+-blue)

![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)

![React](https://img.shields.io/badge/React-Frontend-61DAFB)

![Deepgram](https://img.shields.io/badge/Deepgram-STT-6E56CF)

![Groq](https://img.shields.io/badge/Groq-Llama--3.3--70B-orange)

![Edge TTS](https://img.shields.io/badge/Edge-TTS-0078D4)

![WebSockets](https://img.shields.io/badge/WebSocket-Streaming-success)

![Architecture](https://img.shields.io/badge/Architecture-Event--Driven-ff6b35)

![License](https://img.shields.io/badge/License-MIT-yellow)

![Status](https://img.shields.io/badge/Status-Active-success)

![Latency](https://img.shields.io/badge/Latency-Real--Time-brightgreen)

![Interview](https://img.shields.io/badge/Assessment-Topic--Adaptive-blueviolet)

---

## Technical Overview

| Category | Specification |
|-----------|---------------|
| Project Type | Event-Driven Voice AI Assessment Platform |
| Primary Language | Python 3.11 |
| Backend Framework | FastAPI |
| Frontend Framework | React |
| Communication Protocol | REST API + WebSockets |
| Speech-to-Text Engine | Deepgram Streaming API |
| Large Language Model | Groq API (Llama 3.3 70B Versatile) |
| Text-to-Speech Engine | Microsoft Edge TTS |
| Voice Processing | Real-Time Streaming Pipeline |
| State Management | Custom Event-Driven Interview State Machine |
| Deployment | Render (Backend) + Vercel (Frontend) |
| Data Storage | PostgreSQL |
| Authentication | JWT Authentication |

---

# 🏗 System Architecture

VoiceBench is built on a **low-latency event-driven architecture** that enables continuous real-time voice interaction. Each component is independently responsible for speech processing, interview orchestration, AI reasoning, and voice synthesis, resulting in a modular and scalable conversational pipeline.

<p align="center">
<img src="images/VoiceBench_Architecture.png" width="100%">
</p>

<p align="center">
<b>Figure 1.</b> End-to-end event-driven architecture powering real-time adaptive voice conversations.
</p>

---

### ⚙️ Architectural Principles

- ⚡ Event-Driven Processing
- 🎙 Continuous Voice Streaming
- 🧠 Adaptive Interview Orchestration
- 🔄 Modular AI Service Integration
- 📡 Real-Time Response Generation
- 💾 Persistent Conversation History

---

### 🧩 Core Components

| Layer | Responsibility |
|--------|----------------|
| 🎤 Client | Captures user voice and streams audio |
| 🗣 Deepgram STT | Real-time speech recognition |
| ⚙ FastAPI Engine | Interview orchestration & state management |
| 🤖 Groq Llama 3.3 70B | Adaptive question generation |
| 🔊 Microsoft Edge TTS | Natural speech synthesis |
| 🗄 Supabase | Session persistence & interview history |

---

# 🔄 Voice Processing Pipeline

VoiceBench processes every conversation through a streaming voice pipeline that continuously transforms speech into contextual AI interactions while maintaining interview state and minimizing response latency.

<p align="center">
<img src="images/Voice_Pipeline.png" width="100%">
</p>

<p align="center">
<b>Figure 2.</b> End-to-end event-driven architecture powering real-time adaptive voice conversations.
</p>
---

### 🚀 Pipeline Characteristics

- ⚡ Streaming speech recognition
- 🧠 Context-aware AI reasoning
- 🎯 Adaptive follow-up questioning
- ⏱ Automatic silence recovery
- 🔄 Continuous conversational flow
- 🎙 Natural voice playback
