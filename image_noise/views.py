from django.shortcuts import render
from PIL import Image
import random
import io
from django.http import HttpResponse
import base64
import json  
import numpy as np
import cv2
import os
from django.http import JsonResponse
from PIL import UnidentifiedImageError
from io import BytesIO
# Function for super-resolution
import numpy as np
import cv2
import base64
from PIL import Image
from django.http import JsonResponse
import logging

def resize_image(image, size=(400, 400)):
    return image.resize(size)


# Vue pour sauvegarder l'image dessinée
def save_drawing_view(request):
    if request.method == 'POST':
        # Obtenir les données de dessin de la requête
        draw_data = request.POST.get('draw_data')
        if draw_data:
            # Convertir les données de dessin en image
            # Suppose que draw_data est en base64
            draw_data = draw_data.split(',')[1]  # Enlever le préfixe "data:image/png;base64,"
            drawn_image_data = base64.b64decode(draw_data)

            # Sauvegarder l'image dessinée dans la session ou comme fichier
            request.session['drawn_image'] = base64.b64encode(drawn_image_data).decode('utf-8')
            return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")

    return HttpResponse(json.dumps({'status': 'fail'}), content_type="application/json")

def add_strong_noise_to_image(image):
    if image.mode != 'RGB':
        image = image.convert('RGB')  # Convertir en RGB si nécessaire
    pixels = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            if random.random() < 0.3:  # 30% de probabilité d'ajouter du bruit
                r, g, b = pixels[i, j]
                noise = random.randint(-40, 40)  # Intensifier le bruit
                pixels[i, j] = (max(0, min(255, r + noise)),
                                max(0, min(255, g + noise)),
                                max(0, min(255, b + noise)))
    return image





# Configure logging
logger = logging.getLogger(__name__)

def super_resolution_view(request):
    if request.method == 'POST':
        uploaded_image = request.FILES.get('image')

        if uploaded_image:
            try:
                # Log the received file
                logger.info("Received image: %s", uploaded_image.name)

                # Convert uploaded image to OpenCV format using PIL
                image = Image.open(uploaded_image)
                image = image.convert('RGB')  # Ensure RGB format
                img_array = np.array(image)

                logger.info("Image shape: %s", img_array.shape)

                # Resize the image if it's too large
                max_height = 1080  # Set a max height
                max_width = 1920   # Set a max width
                height, width = img_array.shape[:2]

                if height > max_height or width > max_width:
                    scaling_factor = min(max_height / height, max_width / width)
                    new_dimensions = (int(width * scaling_factor), int(height * scaling_factor))
                    img_array = cv2.resize(img_array, new_dimensions)

                logger.info("Resized image shape: %s", img_array.shape)

                # Apply Non-Local Means (NLM) denoising for color images
                enhanced_image = cv2.fastNlMeansDenoisingColored(img_array, None, 10, 10, 7, 21)

                # Convert the result back to PIL format to return as base64
                enhanced_image_pil = Image.fromarray(cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2RGB))
                buffer = BytesIO()
                enhanced_image_pil.save(buffer, format="PNG")
                super_res_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

                # Return JSON response with the enhanced image
                return JsonResponse({'super_res_image_base64': super_res_image_base64})

            except Exception as e:
                logger.error("Error processing image: %s", e, exc_info=True)  # Log full traceback
                return JsonResponse({'error': 'Error processing image'}, status=500)

    # If no image or wrong method, return an error response
    return JsonResponse({'error': 'No image uploaded or invalid request method'}, status=400)





def image_noise_view(request):
    original_image_base64 = None
    noisy_image_base64 = None

    if request.method == 'POST':
        action = request.POST.get('action')
        uploaded_image = request.FILES.get('image')

        if uploaded_image:
            image = Image.open(uploaded_image)
            image = resize_image(image)  # Redimensionner l'image

            # Convertir l'image d'origine en base64 pour l'afficher
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            original_image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

            if action == 'add_noise':
                noisy_image = add_strong_noise_to_image(image.copy())  # Appliquer le bruit sur une copie de l'image

                # Convertir l'image bruitée en base64 pour l'afficher et la stocker dans la session
                buffered_noisy = io.BytesIO()
                noisy_image.save(buffered_noisy, format="PNG")
                noisy_image_base64 = base64.b64encode(buffered_noisy.getvalue()).decode('utf-8')

                # Stocker l'image bruitée dans la session
                request.session['noisy_image'] = noisy_image_base64  # Stocker en base64

            elif action == 'download_with_noise':
                # Récupérer l'image bruitée de la session
                noisy_image_base64 = request.session.get('noisy_image')
                if noisy_image_base64:
                    noisy_image_data = base64.b64decode(noisy_image_base64)

                    # Générer une réponse pour télécharger l'image avec bruit
                    response = HttpResponse(content_type='image/png')
                    response.write(noisy_image_data)
                    response['Content-Disposition'] = 'attachment; filename="noisy_image.png"'
                    return response

    return render(request, 'image_noise.html', {
        'original_image_base64': original_image_base64,
        'noisy_image_base64': noisy_image_base64,
    })



