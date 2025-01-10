# PDF Slack Bot

## Overview

The PDF Slack Bot is a robust solution for handling PDF files directly within Slack. It enables users to upload PDF files and interact with them by asking questions directly related to the document content. This bot integrates seamlessly with Slack to streamline document handling and improve productivity.

---

## Features

- **Upload PDF Files**: Mention the bot (e.g., `@pdf-bot`) in Slack to upload a PDF.
- **Answer Questions**: Use the `/ask` command to query information directly from the uploaded documents.

---

## Prerequisites

Before setting up the PDF Slack Bot, ensure the following:

1. **Slack Workspace**:
   - Admin permissions to install a Slack App.
2. **Environment**:
   - Python 3.8+
   - Virtual Environment (optional but recommended).
3. **Dependencies**:
   - `Slack SDK`
   - `PyPDF2` (or an equivalent PDF parsing library).
   - `Langchain` (for advanced processing, optional).
   - `OpenAI API` (for AI-based features).

---

## Setup Instructions

### 1. Clone the Repository

```bash
$ git clone https://github.com/MohammedFaizer/pdf_slack_bot.git
$ cd pdf_slack_bot
```

### 2. Set Up the Environment

```bash
$ python3 -m venv venv
$ source venv/bin/activate  # On Windows: venv\Scripts\activate
$ pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project directory and add the following:

```
SLACK_BOT_TOKEN=<Your Slack Bot Token>
SLACK_SIGNING_SECRET=<Your Slack Signing Secret>
OPENAI_API_KEY=<Your OpenAI API Key>
```

### 4. Run the Bot

```bash
$ python manage.py runserver
```

---

## Usage

1. **Add the Bot to Slack**:
   - Invite the bot to your desired channel with `/invite @pdf-bot`.
2. **Upload a PDF**:
   - Mention the bot (e.g., `@pdf-bot`) and upload a PDF file in a channel or DM where the bot is present.
3. **Interact with the Bot**:
   - Use the `/ask` command to ask questions directly about the content of the uploaded PDF.

