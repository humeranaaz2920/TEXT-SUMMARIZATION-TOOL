 print("✓ Model loaded successfully!\n")
        return {"tokenizer": tokenizer, "model": model, "device": device}
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        return None


def preprocess_text(text):
    """Clean and prepare text for summarization"""
    # Remove extra whitespace and newlines
    text = " ".join(text.split())
    return text


def generate_summary(model_data, text, min_length=50, max_length=150):
    """
    Generate a summary of the input text
    
    Args:
        model_data: Dictionary containing tokenizer, model, and device
        text: The input text to summarize
        min_length: Minimum length of summary (words)
        max_length: Maximum length of summary (words)
    
    Returns:
        The generated summary text
    """
    try:
        # Check text length
        if len(text.split()) < 50:
            return "⚠ Warning: Text is too short for effective summarization. Please provide a longer article (50+ words)."
        
        tokenizer = model_data["tokenizer"]
        model = model_data["model"]
        device = model_data["device"]
        
        # Tokenize input text
        inputs = tokenizer.encode(text, return_tensors="pt", max_length=1024, truncation=True)
        if device == 0:
            inputs = inputs.to("cuda")
        
        # Generate summary
        summary_ids = model.generate(
            inputs,
            max_length=max_length,
            min_length=min_length,
            num_beams=4,
            length_penalty=2.0,
            early_stopping=True
        )
        
        # Decode summary
        summary = tokenizer.batch_decode(summary_ids, skip_special_tokens=True)[0]
        return summary
    except Exception as e:
        return f"✗ Error generating summary: {e}"


def display_results(original_text, summary):
    """Display original text and summary in a formatted way"""
    print("\n" + "="*80)
    print("ORIGINAL TEXT")
    print("="*80)
    
    # Wrap and display original text
    wrapped_original = textwrap.fill(original_text, width=80)
    print(wrapped_original)
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    # Wrap and display summary
    wrapped_summary"""
Text Summarization Tool using Hugging Face Transformers
Generates concise summaries from long articles or paragraphs
"""

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import textwrap


def load_summarizer():
    """Load the pre-trained summarization model"""
    print("Loading summarization model (this may take a moment on first run)...")
    try:
        model_name = "facebook/bart-large-cnn"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        
        # Check for GPU availability
        device = 0 if torch.cuda.is_available() else -1
        if device == 0:
            model = model.to("cuda")
            print("✓ Using GPU for faster processing")
        else:
            print("✓ Using CPU (this may be slower)")
        
 = textwrap.fill(summary, width=80)
    print(wrapped_summary)
    
    print("\n" + "="*80)
    print(f"Original length: {len(original_text.split())} words")
    print(f"Summary length: {len(summary.split())} words")
    compression_ratio = len(summary.split()) / len(original_text.split()) * 100
    print(f"Compression ratio: {compression_ratio:.1f}%")
    print("="*80 + "\n")


def get_user_input():
    """Get text input from user"""
    print("Enter your text for summarization (press Enter twice when done):\n")
    lines = []
    empty_line_count = 0
    
    try:
        while True:
            line = input()
            if line == "":
                empty_line_count += 1
                if empty_line_count >= 2:
                    break
            else:
                empty_line_count = 0
                lines.append(line)
    except EOFError:
        pass
    
    return " ".join(lines)


def main():
    """Main function to run the text summarizer"""
    print("\n" + "="*80)
    print("TEXT SUMMARIZATION TOOL")
    print("Powered by Hugging Face Transformers (facebook/bart-large-cnn)")
    print("="*80 + "\n")
    
    # Load the model
    model_data = load_summarizer()
    if model_data is None:
        return
    
    while True:
        # Get user input
        user_text = get_user_input()
        
        if not user_text.strip():
            print("No text provided. Exiting.")
            break
        
        # Preprocess text
        processed_text = preprocess_text(user_text)
        
        # Generate summary
        summary = generate_summary(model_data, processed_text)
        
        # Display results
        display_results(processed_text, summary)
        
        # Ask if user wants to continue
        another = input("Would you like to summarize another text? (yes/no): ").strip().lower()
        if another not in ['yes', 'y']:
            print("\nThank you for using the Text Summarization Tool!")
            break


if __name__ == "__main__":
    main()
