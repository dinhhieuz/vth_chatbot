-- Dữ liệu truyền vào
Declare @input_data nvarchar(max) = '
	SELECT 
		id, timestamp, data, 
		'''' as text, ''1900-01-01'' as time_d
	FROM events
	WHERE type_name IN (''user'', ''bot'')   '

-- Tạo bảng ảo lưu kết quả
DECLARE @RESULT_POST TABLE (
	id INT,
	timestamp DATETIME,
	data NVARCHAR(MAX),
	text nvarchar(max),
	time_d DATETIME
)
-- Chuyển đổi USC-2 sang UTF-8 by Python
INSERT INTO @RESULT_POST EXECUTE sp_execute_external_script @language = N'Python'
	, @script = N'
import yaml
import json
from datetime import datetime

for i in range (len(InputDataSet["data"])):
    reply = yaml.safe_load(InputDataSet["data"][i])
    InputDataSet["data"][i] = str(yaml.safe_load(InputDataSet["data"][i]))
    InputDataSet["text"][i] = reply["text"].encode("utf-8", errors="replace").decode("utf-8").replace("?","")
    InputDataSet["time_d"][i] = datetime.fromtimestamp(reply["timestamp"])
    InputDataSet["timestamp"][i] = datetime.fromtimestamp(InputDataSet["timestamp"][i])
OutputDataSet = InputDataSet
'
	, @input_data_1 = @input_data; 

-- Kết quả sau trả về
select 
	e.id, sender_id, type_name, intent_name, action_name, 
	r.timestamp, r.text, r.time_d, r.data 
From events e full join @RESULT_POST r ON e.id = r.id