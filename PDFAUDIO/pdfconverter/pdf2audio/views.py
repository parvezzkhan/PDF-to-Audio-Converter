from django.shortcuts import render
from django.http import HttpResponse
import tempfile
import os
from PyPDF2 import PdfReader  # Use PdfReader instead of PdfFileReader
from gtts import gTTS

def pdf_to_audio(request):
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']
        
        # Create a temporary directory to store intermediate files
        temp_dir = tempfile.mkdtemp()
        pdf_path = os.path.join(temp_dir, 'input.pdf')
        audio_path = os.path.join(temp_dir, 'output.mp3')
        
        # Save the uploaded PDF file to the temporary directory
        with open(pdf_path, 'wb') as f:
            for chunk in pdf_file.chunks():
                f.write(chunk)
        
        # Extract text from the PDF using PdfReader
        text = ''
        pdf_reader = PdfReader(pdf_path)
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Convert the extracted text to audio
        tts = gTTS(text)
        tts.save(audio_path)

        # Serve the audio file for download
        with open(audio_path, 'rb') as audio_file:
            response = HttpResponse(audio_file.read(), content_type='audio/mpeg')
            response['Content-Disposition'] = 'attachment; filename="output.mp3"'
            return response

    return render(request, 'pdf_to_audio.html')
