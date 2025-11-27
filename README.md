# Rewrite AI

A full-stack application that uses AI to rewrite and summarize text content with intelligent processing powered by LangChain.

## Features

- 🤖 AI-powered text summarization using BART model with LangChain
- ⚡ Real-time processing with loading states
- ✅ Input validation and error handling
- 🎨 Modern, responsive UI
- 🔄 Cross-origin support
- 📚 LangChain-powered summarization chains for better text processing
- 🔀 Automatic handling of long texts with map-reduce strategy

## Tech Stack

**Frontend:**
- React 19.2.0
- Axios for API calls
- Modern CSS with gradients and animations

**Backend:**
- Flask (Python)
- **LangChain** - For advanced summarization chains and text processing
- Transformers library with BART model (integrated via LangChain)
- CORS enabled for cross-origin requests

## Setup Instructions

### Backend Setup

1. Navigate to the server directory:
   ```bash
   cd server
   ```

2. Activate the virtual environment:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies (including LangChain):
   ```bash
   pip install -r requirements.txt
   ```
   
   **Note:** On first run, the BART model will be downloaded (approximately 1.6GB).

4. Start the Flask server:
   ```bash
   python app.py
   ```
   
   The server will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the client directory:
   ```bash
   cd client/summerizer
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   ```
   
   The app will run on `http://localhost:3000`

## Usage

1. Open your browser and go to `http://localhost:3000`
2. Paste a news article or long text (minimum 50 characters)
3. Click "Summarize" to get an AI-generated summary
4. The app will show loading states and handle errors gracefully

## API Endpoints

- `POST /summarize` - Summarize text using LangChain
  - Request body: `{"text": "your text here"}`
  - Response: 
    ```json
    {
      "summary": "generated summary",
      "method": "langchain_stuff" | "langchain_map_reduce",
      "chunks_processed": 3 
    }
    ```
  
- `GET /health` - Health check endpoint
  - Response: `{"status": "healthy", "framework": "LangChain"}`

## Project Structure

```
Summerizer/
├── client/
│   └── summerizer/          # React frontend
│       ├── src/
│       │   ├── App.js       # Main component
│       │   └── App.css      # Styling
│       └── package.json
├── server/
│   ├── app.py              # Flask backend with LangChain
│   ├── requirements.txt    # Python dependencies including LangChain
│   └── venv/               # Python virtual environment
└── README.md
```

## Improvements Made

- ✅ Added comprehensive error handling
- ✅ Implemented loading states with animations
- ✅ Added input validation (min/max length)
- ✅ Enhanced UI with modern design
- ✅ Added character counter
- ✅ Made API URL configurable
- ✅ Improved user experience with disabled states
- ✅ **Integrated LangChain for advanced summarization**
  - Uses LangChain's summarization chains
  - Automatic text chunking for long documents
  - Map-reduce strategy for better handling of lengthy articles
  - Better context preservation with chunk overlap

## Testing

Both servers should start without errors:
- Backend: Flask server on port 5000
- Frontend: React dev server on port 3000

The application is now production-ready with proper error handling and user feedback!

## LangChain Integration Details

This project now uses **LangChain** for enhanced text summarization capabilities:

### What LangChain Adds:

1. **Summarization Chains**: Uses LangChain's `load_summarize_chain` which provides more sophisticated summarization workflows

2. **Text Splitting**: Automatically splits long documents into manageable chunks using `RecursiveCharacterTextSplitter` with:
   - Chunk size: 1000 characters
   - Overlap: 200 characters (for context preservation)

3. **Map-Reduce Strategy**: For texts longer than 2000 characters:
   - **Map**: Summarizes each chunk independently
   - **Reduce**: Combines all chunk summaries into a final summary
   - This allows processing documents much longer than the model's token limit

4. **Document Processing**: Uses LangChain's `Document` schema for structured text handling

5. **Flexible Chain Types**:
   - `stuff` chain: For shorter texts (direct summarization)
   - `map_reduce` chain: For longer texts (chunked processing)

### Benefits:
- ✅ Better handling of long documents
- ✅ More structured and maintainable code
- ✅ Easier to extend with additional LangChain features (memory, prompts, etc.)
- ✅ Better context preservation across chunks
