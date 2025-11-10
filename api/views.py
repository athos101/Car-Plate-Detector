from rest_framework.views import APIView
from rest_framework.response import Response
import easyocr
import cv2
import numpy as np
from PIL import Image

class PlateOCRView(APIView):
    def post(self, request):
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({'error': 'Envie uma imagem.'}, status=400)

        image = Image.open(image_file)
        img = np.array(image)

        reader = easyocr.Reader(['en'])  # usa modelo pré-treinado
        results = reader.readtext(img)

        # Junta todos os textos detectados
        texts = [r[1] for r in results]
        joined_text = ' '.join(texts).upper()

        # tenta filtrar formato de placa
        import re
        match = re.search(r'[A-Z]{3}\d[A-Z0-9]\d{2}', joined_text)
        plate_text = match.group(0) if match else joined_text

        return Response({'plate_text': plate_text})
