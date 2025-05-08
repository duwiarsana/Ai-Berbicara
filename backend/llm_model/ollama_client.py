import requests
import json

def ask_llm(prompt, model="llama3", temperature=0.7):
    """
    Mengirim prompt ke Ollama LLM lokal dan mendapatkan respons.
    
    Args:
        prompt (str): Teks prompt untuk LLM
        model (str): Nama model Ollama (default: llama3)
        temperature (float): Nilai temperature untuk respons (0.0-1.0)
        
    Returns:
        str: Respons dari LLM
    """
    try:
        # Endpoint Ollama lokal
        url = "http://localhost:11434/api/generate"
        
        # Data untuk request
        data = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False
        }
        
        # Kirim request ke Ollama
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "Maaf, saya tidak bisa menjawab saat ini.")
        else:
            return f"Error: Ollama returned status code {response.status_code}"
    
    except Exception as e:
        return f"Error connecting to Ollama: {str(e)}"

# Contoh penggunaan
if __name__ == "__main__":
    response = ask_llm("Jelaskan apa itu kecerdasan buatan dalam bahasa Indonesia.")
    print(response)
