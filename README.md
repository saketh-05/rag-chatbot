
# RAG-chatbot

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/saketh-05/rag-chatbot.git)

## What is this project about?

This project implements a Retrieval-Augmented Generation (RAG) chatbot. It combines the power of large language models with a retrieval mechanism to provide more accurate and context-aware responses. The chatbot is designed to answer questions based on a specific knowledge base, in this case, information about One Piece episodes.

**Key Features:**

*   **RAG Architecture:** Uses a retriever to fetch relevant documents and augments the language model's input for improved responses.
*   **Voice and Text Chat Capabilities:** Supports both voice input (through microphone recording) and text input for user queries.
*   **FastAPI Backend:** Provides a robust and efficient API for handling requests and interacting with the language model.
*   **Next.js Frontend:** Offers a modern and user-friendly interface for interacting with the chatbot.
*   **ChromaDB for Vector Storage:** Uses ChromaDB to store and retrieve document embeddings for efficient semantic search.
*   **Google Cloud Text-to-Speech & Speech-to-Text:** Converts chatbot responses to speech and transcribes user voice input.

## Technologies Used

*   **Backend:**
    *   Python
    *   FastAPI
    *   Langchain
    *   Langchain-Ollama
    *   ChromaDB
    *   Google Cloud Text-to-Speech
    *   Google Cloud Speech-to-Text
    *   Uvicorn
*   **Frontend:**
    *   Next.js
    *   React
    *   Tailwind CSS
    *   Radix UI
    *   Lucide React
*   **Vector Database:**
    *   ChromaDB

## Installation & Setup

### Backend Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/saketh-05/rag-chatbot.git
    cd rag-chatbot
    ```

2.  **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Google Cloud credentials:**

    *   Create a Google Cloud project and enable the Text-to-Speech and Speech-to-Text APIs.
    *   Create a service account and download the JSON key file.
    *   Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of the JSON key file.

    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/google-cloud-key.json"
    ```

### Frontend Setup

1.  **Navigate to the `Frontend` directory:**

    ```bash
    cd Frontend
    ```

2.  **Install the dependencies:**

    ```bash
    npm install
    # or
    yarn install
    # or
    pnpm install
    ```

3.  **Configure environment variables:**

    Create a `.env.local` file in the `Frontend` directory and add any necessary environment variables.  For example, you might need to configure the API endpoint for the backend:

    ```
    NEXT_PUBLIC_API_ENDPOINT=http://localhost:8000
    ```

## How to Run the Project

### Backend

1.  **Activate the virtual environment (if not already active):**

    ```bash
    source venv/bin/activate
    ```

2.  **Run the FastAPI application:**

    ```bash
    uvicorn main:app --reload
    ```

    This will start the server, typically on `http://127.0.0.1:8000`.

### Frontend

1.  **Navigate to the `Frontend` directory:**

    ```bash
    cd Frontend
    ```

2.  **Start the Next.js development server:**

    ```bash
    npm run dev
    # or
    yarn dev
    # or
    pnpm dev
    ```

    This will start the development server, usually on `http://localhost:3000`.

## Usage

1.  **Access the Frontend:** Open your web browser and navigate to `http://localhost:3000`.
2.  **Interact with the Chatbot:** You can now interact with the chatbot using either text input or voice input.
    *   **Text Input:** Type your question in the input field and press the "Send" button.
    *   **Voice Input:** Click the microphone icon to start recording your question. Click the icon again to stop recording and send the audio to the chatbot.
3.  **View the Response:** The chatbot's response will be displayed in the chat window. If the response includes audio, it will be played automatically.

## Folder Structure

```
rag-chatbot/
├── .gitignore
├── chroma_langchain_db/              # ChromaDB database files
│   ├── 50eb7c8b-b88c-45b0-a69b-ded3cc286f94/
│   │   ├── data_level0.bin
│   │   ├── header.bin
│   │   ├── length.bin
│   │   └── link_lists.bin
│   └── chroma.sqlite3
├── Frontend/                        # Next.js frontend application
│   ├── .eslintrc.json
│   ├── .gitignore
│   ├── .next/                        # Next.js build output (omitted for brevity)
│   ├── app/                           # Next.js app directory
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/                    # React components
│   │   └── ui/                        # Radix UI components
│   │       ├── accordion.tsx
│   │       ├── alert-dialog.tsx
│   │       ├── alert.tsx
│   │       ├── aspect-ratio.tsx
│   │       ├── avatar.tsx
│   │       ├── badge.tsx
│   │       ├── breadcrumb.tsx
│   │       ├── button.tsx
│   │       ├── calendar.tsx
│   │       ├── card.tsx
│   │       ├── carousel.tsx
│   │       ├── chart.tsx
│   │       ├── checkbox.tsx
│   │       ├── collapsible.tsx
│   │       ├── command.tsx
│   │       ├── context-menu.tsx
│   │       ├── dialog.tsx
│   │       ├── drawer.tsx
│   │       ├── dropdown-menu.tsx
│   │       ├── form.tsx
│   │       ├── hover-card.tsx
│   │       ├── input-otp.tsx
│   │       ├── input.tsx
│   │       ├── label.tsx
│   │       ├── menubar.tsx
│   │       ├── navigation-menu.tsx
│   │       ├── pagination.tsx
│   │       ├── popover.tsx
│   │       ├── progress.tsx
│   │       ├── radio-group.tsx
│   │       ├── resizable.tsx
│   │       ├── scroll-area.tsx
│   │       ├── select.tsx
│   │       ├── separator.tsx
│   │       ├── sheet.tsx
│   │       ├── skeleton.tsx
│   │       ├── slider.tsx
│   │       ├── sonner.tsx
│   │       ├── switch.tsx
│   │       ├── table.tsx
│   │       ├── tabs.tsx
│   │       ├── textarea.tsx
│   │       ├── toast.tsx
│   │       ├── toaster.tsx
│   │       ├── toggle-group.tsx
│   │       ├── toggle.tsx
│   │       └── tooltip.tsx
│   ├── config/                        # Configuration files
│   │   └── ngrok.yaml
│   ├── hooks/                         # Custom React hooks
│   │   └── use-toast.ts
│   ├── lib/                           # Utility functions
│   │   └── utils.ts
│   ├── next.config.js
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.ts
│   └── types/                         # TypeScript type definitions
│       └── index.ts
├── main.py                          # FastAPI backend application
├── onepiece-epdata.csv                # CSV data of One Piece episodes
├── readme-gen.sh                    # Script to generate this README
└── requirements.txt                 # Python dependencies
```
