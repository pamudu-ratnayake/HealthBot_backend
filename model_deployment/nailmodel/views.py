import csv
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.views import APIView
import pickle
import h5py
from keras.models import model_from_json
from keras.models import load_model
import numpy as np
import cv2


class NailDIdentifier:
    permission_classes = (permissions.AllowAny,)

    description = {
        "Clubbing": "Clubbing is a condition that affects the nails and is often associated with underlying medical conditions such as lung disease, heart disease, and gastrointestinal disorders. While there are no specific treatments for clubbing itself, managing the underlying condition is important. If you suspect that you have clubbing, it is important to see a doctor for proper evaluation and diagnosis. However, here are some basic things you can do until you see a doctor:",
        "Distal Subungual Onychomycosis": "Distal subungual onychomycosis is a fungal infection that affects the nail bed and plate. If you suspect that you have this condition, it is important to see a doctor for proper diagnosis and treatment. However, here are some basic things you can do until you see a doctor:",
        "Healthy Nails": "test is a condition that affects the nails and is often associated with underlying medical conditions such as lung disease, heart disease, and gastrointestinal disorders. While there are no specific treatments for clubbing itself, managing the underlying condition is important. If you suspect that you have clubbing, it is important to see a doctor for proper evaluation and diagnosis. However, here are some basic things you can do until you see a doctor:",
        "Onychomycosis": "Onychomycosis is a fungal infection that affects the nails, usually the toenails. If you suspect that you have this condition, it is important to see a doctor for proper diagnosis and treatment. However, here are some basic things you can do until you see a doctor:",
        "Psoriasis": "Psoriasis is a chronic skin condition that can affect the nails. If you suspect that you have psoriasis, it is important to see a doctor for proper diagnosis and treatment. However, here are some basic things you can do until you see a doctor:"
    }

    steps = {
        "Clubbing": [
            "Maintain good nail hygiene: Keep your nails clean and dry. Avoid using harsh chemicals or abrasive nail products.",
            "Moisturize: Apply moisturizer to your nails and cuticles to prevent dryness.",
            "Stop smoking: Smoking can worsen clubbing, so if you smoke, it is important to quit.",
            "Avoid exposure to cold temperatures: Exposure to cold temperatures can worsen clubbing. Keep your hands warm in cold weather.",
            "Stay hydrated: Drink plenty of water to keep your body hydrated."
        ],
        "Distal Subungual Onychomycosis": [
            "Keep your feet or hands clean and dry: Clean and dry the affected area regularly, and avoid wearing tight shoes or gloves.",
            "Use over-the-counter antifungal creams: You can apply over-the-counter antifungal creams, such as clotrimazole or terbinafine, to the affected area according to the instructions on the packaging.",
            "Trim your nails: Keep your nails trimmed and filed to reduce the thickness of the infected nail.",
            "Wear breathable shoes: Choose shoes that allow air circulation and avoid wearing shoes that trap moisture.",
            "Tea tree oil: Some studies have shown that tea tree oil has antifungal properties and can be effective in treating onychomycosis. You can apply a few drops of tea tree oil to the affected area twice daily."
        ],
        "Healthy Nails": [
            "Keep your feet clean and dry: Clean and dry the affected area regularly, and avoid wearing tight shoes or socks.",
            "Use over-the-counter antifungal creams: You can apply over-the-counter antifungal creams, such as clotrimazole or terbinafine, to the affected area according to the instructions on the packaging.",
            "Trim your nails: Keep your nails trimmed and filed to reduce the thickness of the infected nail."
        ],
        "Onychomycosis": [
            "Keep your feet clean and dry: Clean and dry the affected area regularly, and avoid wearing tight shoes or socks.",
            "Use over-the-counter antifungal creams: You can apply over-the-counter antifungal creams, such as clotrimazole or terbinafine, to the affected area according to the instructions on the packaging.",
            "Trim your nails: Keep your nails trimmed and filed to reduce the thickness of the infected nail.",
            "Wear breathable shoes: Choose shoes that allow air circulation and avoid wearing shoes that trap moisture.",
            "Tea tree oil: Some studies have shown that tea tree oil has antifungal properties and can be effective in treating onychomycosis. You can apply a few drops of tea tree oil to the affected area twice daily."
        ],
        "Psoriasis": [
            "Keep your nails clean and dry: Clean your nails regularly and avoid moisture buildup, which can worsen psoriasis symptoms.",
            "Apply moisturizer: Use a moisturizer on your nails and cuticles to prevent dryness and cracking.",
            "Wear gloves: Wear gloves when you wash dishes or clean to protect your nails from exposure to water and harsh chemicals.",
            "Avoid picking at your nails: Picking at your nails can worsen psoriasis symptoms and increase the risk of infection.",
            "Avoid trauma to your nails: Avoid activities that may cause trauma to your nails, such as excessive manicuring or wearing tight shoes.",
            "Apply topical corticosteroids: You may apply over-the-counter topical corticosteroids, such as hydrocortisone cream, to the affected area according to the instructions on the packaging."
        ]
    }

    @csrf_exempt
    def get_disease_category(request):
        # if request.method == 'POST':
            # data = json.loads(request.body)
            # print("Request recieved!", data['data'])
            print("Request recieved!!")
            print("Request recieved!", request.FILES['image'])
            model_file = h5py.File('D:/Research 4th Year/app/model-deployment/model_deployment/nailmodel/model/nailmodel01.h5', 'r')
            model = load_model(model_file, compile=False)
          
            image_file = request.FILES['image']

            with open('tmp.jpg', 'wb') as f:
                f.write(image_file.read())

                img = cv2.imread("tmp.jpg")
   
                img = cv2.resize(img, (224, 224))

                img = np.array(img, dtype=np.float32)

                img /= 255.0

                img = np.expand_dims(img, axis=0)

                input_data = img


            predicted_category = model.predict(input_data)
            # get the class label with the highest predicted probability
            class_index = np.argmax(predicted_category[0])

            # define a list of class labels
            class_labels = ["Clubbing", "Distal Subungual Onychomycosis", "Healthy Nails", "Onychomycosis", "Psoriasis"]

            # get the class label corresponding to the class index
            class_label = class_labels[class_index]

            # print the class label
            print("Class label: ", class_label)
            # value = {'diseaseName': class_label}

            data = {}
            data['disease'] = class_label
            data['description'] = NailDIdentifier.description.get(class_label, '')
            data['steps'] = NailDIdentifier.steps.get(class_label, '')
            json_data = json.dumps(data)
            # value['category'] = predicted_category[0]
            print(predicted_category)
            return JsonResponse(json_data, safe=False)