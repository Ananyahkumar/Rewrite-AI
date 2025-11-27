from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from transformers import pipeline, AutoTokenizer
import torch

app = Flask(__name__)
CORS(app)

# Initialize the BART model pipeline using HuggingFace
print("Loading BART model... This may take a moment on first run.")
model_name = "facebook/bart-large-cnn"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Create HuggingFace pipeline
hf_pipeline = pipeline(
    "summarization",
    model=model_name,
    tokenizer=tokenizer,
    device=0 if torch.cuda.is_available() else -1  # Use GPU if available
)

# Text splitter for handling long documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  
    chunk_overlap=200,  
    length_function=len,
)

def summarize_with_langchain(text, use_chunking=False):
    """Summarize text using LangChain"""
    if use_chunking and len(text) > 2000:
        # Split the text into chunks
        texts = text_splitter.split_text(text)
        documents = [Document(page_content=text_chunk) for text_chunk in texts]
        
        # Summarize each chunk
        chunk_summaries = []
        for doc in documents:
            # Use the HuggingFace pipeline directly for each chunk since BART handles summarization
            result = hf_pipeline(
                doc.page_content,
                max_length=150,
                min_length=40,
                do_sample=False
            )
            chunk_summaries.append(result[0]["summary_text"])
        
        if len(chunk_summaries) > 1:
            combined_text = " ".join(chunk_summaries)
            # Summarize the combined summaries to get final summary
            result = hf_pipeline(
                combined_text,
                max_length=150,
                min_length=40,
                do_sample=False
            )
            return result[0]["summary_text"], "langchain_map_reduce", len(documents)
        else:
            return chunk_summaries[0], "langchain_map_reduce", 1
    else:
        # Direct summarization for shorter texts
        result = hf_pipeline(
            text,
            max_length=150,
            min_length=40,
            do_sample=False
        )
        return result[0]["summary_text"], "langchain_stuff", 1

@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json()
        text = data.get("text", "")
        if not text.strip():
            return jsonify({"error": "No text provided"}), 400

        # Check text length
        if len(text) < 50:
            return jsonify({"error": "Text should be at least 50 characters long."}), 400

        # Determine if we need chunking
        use_chunking = len(text) > 2000
        
        # Summarize using LangChain
        summary, method, chunks = summarize_with_langchain(text, use_chunking=use_chunking)
        
        response = {
            "summary": summary,
            "method": method
        }
        
        if chunks > 1:
            response["chunks_processed"] = chunks
        
        return jsonify(response)

    except Exception as e:
        print(f"Error during summarization: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Summarization failed: {str(e)}"}), 500


@app.route("/", methods=["GET"])
def index():
    """Root endpoint with API information"""
    return jsonify({
        "message": "AI News Summarizer API",
        "framework": "LangChain with BART model",
        "endpoints": {
            "POST /summarize": "Summarize text content",
            "GET /health": "Health check endpoint"
        },
        "status": "running"
    })

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "framework": "LangChain"})


if __name__ == "__main__":
    print("Starting Flask server with LangChain...")
    app.run(host="0.0.0.0", port=5000, debug=True)
