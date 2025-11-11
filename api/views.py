from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import easyocr
import numpy as np
from PIL import Image
import re

def upload_page(request):
    return render(request, 'upload.html')

class PlateOCRView(APIView):
    def post(self, request):
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({'error': 'Envie uma imagem.'}, status=400)

        # Carregar e processar a imagem
        image = Image.open(image_file)
        img = np.array(image)
        reader = easyocr.Reader(['en'])
        results = reader.readtext(img)
        texts = [r[1] for r in results]
        joined_text = ' '.join(texts).upper()

        # Regex para placas brasileiras Mercosul e padrão antigo
        # Padrão antigo: 3 letras + 4 números (e.g. ABC1234)
        # Mercosul: 3 letras + 1 número + 1 letra + 2 números (e.g. ABC1D23)
        patterns = [
            r'[A-Z]{3}\d{4}',    # Antigo
            r'[A-Z]{3}\d[A-Z]\d{2}'  # Mercosul
        ]

        plate_text = None
        for pattern in patterns:
            match = re.search(pattern, joined_text)
            if match:
                plate_text = match.group(0)
                break

        # Se não encontrou, retornar texto amigável
        if not plate_text:
            return Response({'plate_text': 'Placa não detectada.'})

        return Response({'plate_text': plate_text})
