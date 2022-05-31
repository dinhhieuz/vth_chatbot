title Rasa Server : 5005

cd ../../chatbot_vth

conda activate rasa-chatbot && rasa train && rasa run -m models --endpoints endpoints.yml --credentials credentials.yml --port 5005

