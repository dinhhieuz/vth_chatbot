#! 1. Khởi động Rasa server
pushd D:\Năm 4 - Thực tập tốt nghiệp\Project\Chatbot\chatbot_vth
conda activate rasa-chatbot
rasa train && rasa run -m models --endpoints endpoints.yml --credentials credentials.yml --port 5005

# rasa run -m models --endpoints endpoints.yml --port 9999 --credentials credentials.yml

#! 2. Run actions server
pushd D:\Năm 4 - Thực tập tốt nghiệp\Project\Chatbot\chatbot_vth
conda activate rasa-chatbot
rasa run actions --port 5055


#! 3. Run Ngork
pushd D:\Năm 4 - Thực tập tốt nghiệp\Project\Chatbot\chatbot_vth\others
ngrok authtoken 25GxQSVCB2LLMbAGyXSYIE8ROCU_3LPoxRnaf37Xfv3qzKRzo
ngrok http 5005

#---------------------------------------------------------------------------
#! Chạy Rasa local
pushd D:\Năm 4 - Thực tập tốt nghiệp\Project\Chatbot\chatbot_vth
conda activate rasa-chatbot
rasa shell --port 9009

#! Train model rasa
rasa train


# rasa run actions --port 9099