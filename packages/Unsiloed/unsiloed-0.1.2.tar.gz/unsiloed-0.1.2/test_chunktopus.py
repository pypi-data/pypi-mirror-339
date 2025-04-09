"""
Test script for chunktopus package.
"""

import os
import chunktopus

# Test with a PDF URL
def test_chunktopus():
    try:
        print("Testing chunktopus package...")
        
        # Use the OpenAI API key from the environment
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("Warning: OPENAI_API_KEY not set in environment variables.")
            print("Set it with: export OPENAI_API_KEY='your-api-key'")
            return
            
        # Example PDF file
        pdf_url = "https://omni-demo-data.s3.amazonaws.com/test/cs101.pdf"
        
        # Process the document
        print(f"Processing document from URL: {pdf_url}")
        result = chunktopus.process_sync({
            "filePath": pdf_url,
            "credentials": {
                "apiKey": api_key
            },
            "strategy": "semantic"
        })
        
        # Print results
        print(f"Successfully processed document with {result['strategy']} chunking")
        print(f"Found {result['total_chunks']} chunks")
        print(f"Average chunk size: {result['avg_chunk_size']:.2f} characters")
        
        # Print the first chunk as a sample
        if result['chunks'] and len(result['chunks']) > 0:
            print("\nFirst chunk preview:")
            print(f"Title: {result['chunks'][0]['metadata'].get('title', 'No title')}")
            print(f"Text: {result['chunks'][0]['text'][:200]}...")
        
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"Error during test: {str(e)}")
        
if __name__ == "__main__":
    test_chunktopus() 