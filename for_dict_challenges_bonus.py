"""
Пожалуйста, приступайте к этой задаче после того, как вы сделали и получили ревью ко всем остальным задачам
в этом репозитории. Она значительно сложнее.


Есть набор сообщений из чата в следующем формате:

```
messages = [
    {
        "id": "efadb781-9b04-4aad-9afe-e79faef8cffb",
        "sent_at": datetime.datetime(2022, 10, 11, 23, 11, 11, 721),
        "sent_by": 46,  # id пользователя-отправителя
        "reply_for": "7b22ae19-6c58-443e-b138-e22784878581",  # id сообщение, на которое это сообщение является ответом (может быть None)
        "seen_by": [26, 91, 71], # идентификаторы пользователей, которые видели это сообщение
        "text": "А когда ревью будет?",
    }
]
```

Так же есть функция `generate_chat_history`, которая вернёт список из большого количества таких сообщений.
Установите библиотеку lorem, чтобы она работала.

Нужно:
1. Вывести айди пользователя, который написал больше всех сообщений.
2. Вывести айди пользователя, на сообщения которого больше всего отвечали.
3. Вывести айди пользователей, сообщения которых видело больше всего уникальных пользователей.
4. Определить, когда в чате больше всего сообщений: утром (до 12 часов), днём (12-18 часов) или вечером (после 18 часов).
5. Вывести идентификаторы сообщений, который стали началом для самых длинных тредов (цепочек ответов).

Весь код стоит разбить на логические части с помощью функций.
"""
import random
import uuid
import datetime
import pprint

import lorem


def generate_chat_history():
    messages_amount = random.randint(10, 20)
    users_ids = list(
        {random.randint(1, 10000) for _ in range(random.randint(5, 20))}
    )
    sent_at = datetime.datetime.now() - datetime.timedelta(days=100)
    messages = []
    for _ in range(messages_amount):
        sent_at += datetime.timedelta(minutes=random.randint(0, 240))
        messages.append({
            "id": uuid.uuid4(),
            "sent_at": sent_at,
            "sent_by": random.choice(users_ids),
            "reply_for": random.choice(
                [
                    None,
                    (
                        random.choice([m["id"] for m in messages])
                        if messages else None
                    ),
                ],
            ),
            "seen_by": random.sample(users_ids,
                                     random.randint(1, len(users_ids))),
            "text": lorem.sentence(),
        })
    return messages


if __name__ == "__main__":
    messages = generate_chat_history()
    #  pprint.pprint(messages)

# Вывести айди пользователя, который написал больше всех сообщений.

def find_most_messages_user(messages):
    users = {}
    for message in messages:
        if message['sent_by'] not in users:
            users[message['sent_by']] = 1
        else:
            users[message['sent_by']] += 1

    most_num_of_messages = 0
    for user, number_of_messages in users.items():
        if number_of_messages > most_num_of_messages:
            user_id = user
            most_num_of_messages = number_of_messages
    return user_id

print(f'Больше всего сообщений написал пользователь с id: {find_most_messages_user(messages)}')

# Вывести айди пользователя, на сообщения которого больше всего отвечали.

def find_most_answers_user(messages):
    answers = {}
    for message in messages:
        if message['reply_for'] == None:
            continue
        elif message['reply_for'] not in answers:
            answers[message['reply_for']] = 1
        else:
            answers[message['reply_for']] += 1

    most_num_of_messages = 0
    for message, number_of_answers in answers.items():
        if number_of_answers > most_num_of_messages:
            message_id = message
            most_num_of_messages = number_of_answers

    for message in messages:
        if message['id'] == message_id:
            return(message['sent_by'])
print(f'Больше всего отвечали на сообщения пользователя с id: {find_most_answers_user(messages)}')

# Вывести айди пользователей, сообщения которых видело больше всего уникальных пользователей.

def find_most_viewed_user(messages):
    users = {}
    for message in messages:
        if message['sent_by'] not in users:
            users[message['sent_by']] = message['seen_by']
        else:
            users[message['sent_by']] += message['seen_by']
    for id, messages in users.items():
        print(id, len(set(messages)))
find_most_viewed_user(messages)

# Определить, когда в чате больше всего сообщений: утром (до 12 часов), днём (12-18 часов) или вечером (после 18 часов).

def determine_time(messages):
    sent_time = {'утром': 0,
                 'днём': 0,
                 'вечером': 0}
    for message in messages:
        if int(datetime.datetime.strftime(message['sent_at'], '%H')) < 12:
            sent_time['утром'] += 1
        elif 12 <= int(datetime.datetime.strftime(message['sent_at'], '%H')) < 18:
            sent_time['днём'] += 1
        else:
            sent_time['вечером'] += 1
    number_of_message = 0
    for time, number in sent_time.items():
        if number > number_of_message:
            day_time = time
            number_of_message = number
    print(f'Больше всего сообщений пишут {day_time}')

determine_time(messages)

# Вывести идентификаторы сообщений, который стали началом для самых длинных тредов (цепочек ответов).

def create_message_id_dict(messages):
    message_reply = {}
    for message in messages:
        message_reply[message['id']] = message['reply_for']
    return message_reply

def find_message_tree(message_reply, message_id, answers):
    for key, value in message_reply.items():
        if message_id == value:
            answers.append(key)
            find_message_tree(message_reply, key, answers)
    return answers
    
message_reply = create_message_id_dict(messages)

message_tree = {}
for message_id in message_reply:
    answers = []
    message_tree[message_id] = find_message_tree(message_reply, message_id, answers)

num_of_answers = 0
for key, value in message_tree.items():
    if len(value) > num_of_answers:
        num_of_answers = len(value)
        most_reply_id = key
print(most_reply_id)