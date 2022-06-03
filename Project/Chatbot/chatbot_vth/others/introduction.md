## Thông tin RASA

1. Version: 
    - Rasa: 2.8.13
    - Python: 3.7.7
    - selenium: 4.1.3
    - pyYAML: 6.0
    - pymssql: 2.2.5

2. Logs:
    - Action:
        rasa run actions -vv >> ./assets/other/log_RasaAction.log 2>&1

3. Custom:
    - Tăng thời gian xữ lý request:
        + Tới địa chỉ: C:\Users\DELL\anaconda3\envs\rasa-chatbot\Lib\site-packages\rasa\core\channels\console.py
        + Tới biến "DEFAULT_STREAM_READING_TIMEOUT_IN_SECONDS": change time

    - Tăng số lượng xữ lý:
        + Tới địa chỉ: C:\Users\DELL\anaconda3\envs\rasa-chatbot\Lib\site-packages\rasa\core\channels\constants.py
        + tới biến " DEFAULT_SANIC_WORKERS " : change number user

4. Note:
    - Không train không dấu: 
        mục đích vì con người nói chuyện với nhau mà không có dấu thì cũng chẳn ai hiểu được nói gì tới bot 

5. Connect:
    - Tại thư mục "Credentials.yml" sẽ có các thông tin của channel, và chúng sẽ dựa vào khóa để tìm thấy file channel phù hợp với liệt kê
    - Ví dụ ở đây là "Facebook" chúng sẽ dựa trên từ khóa này để vào 