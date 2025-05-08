import google.generativeai as genai
import os

def ask_gemini(prompt, model="gemini-1.5-pro", temperature=0.7):
    """
    Mengirim prompt ke Google Gemini API dan mendapatkan respons.
    
    Args:
        prompt (str): Teks prompt untuk LLM
        model (str): Nama model Gemini (default: gemini-1.5-pro)
        temperature (float): Nilai temperature untuk respons (0.0-1.0)
        
    Returns:
        str: Respons dari LLM
    """
    try:
        # Ambil API key dari environment variable
        api_key = os.environ.get("GEMINI_API_KEY")
        
        if not api_key:
            return "Error: GEMINI_API_KEY tidak ditemukan di environment variables"
        
        # Konfigurasi Gemini API
        genai.configure(api_key=api_key)
        
        # Pilih model
        model_obj = genai.GenerativeModel(model_name=model)
        
        # Konfigurasi generasi
        generation_config = {
            "temperature": temperature,
            "top_p": 0.95,
            "top_k": 0,
            "max_output_tokens": 1024,
        }
        
        # Kirim request ke Gemini API
        response = model_obj.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        # Ekstrak teks dari respons
        return response.text
    
    except Exception as e:
        return f"Error connecting to Gemini API: {str(e)}"

# Contoh penggunaan
if __name__ == "__main__":
    os.environ["GEMINI_API_KEY"] = "YOUR_API_KEY_HERE"  # Ganti dengan API key Anda
    response = ask_gemini("Jelaskan apa itu kecerdasan buatan dalam bahasa Indonesia.")
    print(response)
