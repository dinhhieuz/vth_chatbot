# if 'optin' in entry['messaging'][0].keys():
#     if entry['messaging'][0]["optin"]["type"] == 'one_time_notif_req':
#         import random, string 
#         random_word = lambda length: ''.join(random.choice(string.ascii_lowercase) for i in range(length))
#         entry['messaging'][0]['message'] = {
#                         "mid": 'm_{0}-{1}_{2}-{3}'.format(random_word(10), random_word(14), random_word(29), random_word(30)),
#                         "text": entry['messaging'][0]["optin"]["payload"] + ' | ' + entry['messaging'][0]["optin"]["one_time_notif_token"]
#                     }
#         del entry['messaging'][0]['optin'], random_word

# {'id': '100297242401314', 'time': 1653405609755, 'messaging': [{'sender': {'id': '4188549794601171'}, 'recipient': {'id': '100297242401314'}, 'timestamp': 1653405609175, 'postback': {'title': 'Get Started', 'payload': 'GET_STARTED_PAYLOAD', 'mid': 'm_ixXdoVY2J1PCEC3dv51CzKau9u8nzeKyEXfJ3C3nW6oHzldvr5PLd3fp8yEZDAICJSwR0k744kd38NihiYRrKA'}}]}