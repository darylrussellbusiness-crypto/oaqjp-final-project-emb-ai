import requests
import json

def emotion_detector(text_to_analyse):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
        "Content-Type": "application/json"
    }
    input_json = {
        "raw_document": {
            "text": text_to_analyse
        }
    }

    response = requests.post(url, headers=headers, json=input_json)

    if response.status_code == 200:
        result_dict = json.loads(response.text)
        print("Full API response:", json.dumps(result_dict, indent=2))
        emotions = {
            'anger': 0.0,
            'disgust': 0.0,
            'fear': 0.0,
            'joy': 0.0,
            'sadness': 0.0
        }
        try:
            emotion_scores = result_dict['emotion']['document']['emotion']
            for emotion in emotions.keys():
                emotions[emotion] = emotion_scores.get(emotion, 0.0)
        except KeyError:
            return {**emotions, 'dominant_emotion': None}

        dominant_emotion = max(emotions, key=emotions.get)

        return {**emotions, 'dominant_emotion': dominant_emotion}
    else:
        return None

