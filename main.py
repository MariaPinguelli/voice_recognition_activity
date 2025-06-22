import speech_recognition as sr
from pathlib import Path

def transcribe_audio(audio_file):
    """Transcreve o áudio para texto"""
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            
            try:
                text = recognizer.recognize_google(audio_data, language="en-US")
                return text
            except sr.UnknownValueError:
                return "Não foi possível entender o áudio"
            except sr.RequestError as e:
                return f"Erro no serviço de reconhecimento: {e}"
    except Exception as e:
        return f"Erro ao processar o arquivo: {str(e)}"

def get_audio_files(input_dir):
    """Retorna lista de arquivos de áudio na pasta input"""
    supported_formats = ['.wav', '.aiff', '.flac']
    return [f for f in Path(input_dir).iterdir() if f.suffix.lower() in supported_formats]

def main():
    INPUT_DIR = "input"
    OUTPUT_FILE = "transcricoes.txt"
    
    audio_files = get_audio_files(INPUT_DIR)
    
    if not audio_files:
        print(f"Nenhum arquivo de áudio encontrado na pasta '{INPUT_DIR}'.")
        print(f"Formatos suportados: .wav, .aiff, .flac")
        return
    
    print(f"Encontrados {len(audio_files)} arquivo(s) de áudio para processar:")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_file:
        for audio_file in audio_files:
            print(f"\nProcessando: {audio_file.name}...")
            transcription = transcribe_audio(str(audio_file))
            
            result = f"Arquivo: {audio_file.name}\nTranscrição: {transcription}\n{'-'*50}\n"
            print(result)
            out_file.write(result)
    
    print(f"\nProcessamento concluído! Resultados salvos em '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    main()