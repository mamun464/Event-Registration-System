
# Event Registration System Documentaion

The Event Registration System efficiently manages events, covering creation, enrollment, and deregistration. It includes seamless user authentication, enabling easy login and registration. Organizers effortlessly create events, while participants can quickly register, ensuring a smooth experience throughout.




## 🚀 About Me
Mamunur Rashid  
Software Developer (Trainee)  
Red Dot Digital || Robi Axiata Ltd  
Cell: 01767213613  
Email: mrashid.uiu.cse@gmail.com  
Github: [mamun464](https://github.com/mamun464)

## Installation

Install my-project with Python-3.9.0

```bash
  python -m venv [your ENV name]

  /.[your ENV name]/bin/activate

  pip install -r requirements.txt

  python manage.py runserver
```
    
## API Reference

#### Login User-Endpoint

```http
  POST /api/user/login/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `phone_no` | `string` | **Required**. Registerd phone_no  |
| `password` | `string` | **Required**. User's password  |


#### User Registration-API_Endpoint

```http
  POST /api/user/register/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `email` | `string` | **Required**. Registerd email  |
| `fullName` | `string` | **Required**. Registerd Full Name  |
| `phone_no` | `string` | **Required**. Registerd phone_no  |
| `password` | `string` | **Required**. Password  |
| `password2` | `string` | **Required**. Confirm Password  |

#### User's Event Registration-API_Endpoint

```http
  POST /api/user/event-register/?{slot_id}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Access_Token` | `string` | **Required**. Your User's Access_Token |
| `slot_id` | `integer` | **Required**. Slot Id for Registration a event |

#### User's Event Deregistration-API_Endpoint

```http
  DELETE /api/user/event-deregister/?{slot_id}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Access_Token` | `string` | **Required**. Your User's Access_Token |
| `slot_id` | `integer` | **Required**. Slot Id for De-Registration a event |

#### User's all Enrolled Events List -API_Endpoint

```http
  GET /api/user/events/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Access_Token` | `string` | **Required**. Your User's Access_Token |


#### Event Create -API_Endpoint

```http
  POST /api/events/create/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `title` | `string` | **Required**. Event Title |
| `description` | `string` | **Required**. Event description |
| `date` | `date` | **Required**. Event Date |
| `time` | `time` | **Required**. Event time |
| `location_name` | `string` | **Required**. Event Location Name |
| `slots` | `list/array` | **Required**. At list one Slot must be need to create a event. But You can create multile slots |
| `start_time` | `time` | **Required**. start_time of the even. it will be in the event slot. attribute |
| `end_time` | `time` | **Required**. end_time of the even. it will be in the event slot. attribute |
| `end_time` | `time` | **Required**. end_time of the even. it will be in the event slot. attribute |
| `total_seat` | `integer` | **Required**. end_time of the even. it will be in the event slot. attribute |

Example of body:

{
  "title": "Sylhet Folk Fusion",
  "description": "Bangladesh",
  "date": "2023-10-05",
  "time": "20:00:00",
  "location_name": "Hazrat Shah Jalal International Airport",
  "slots": [
    {
      "start_time": "20:30:00",
      "end_time": "22:00:00",
      "total_seat": 50
    }
  ]
}



#### All Event Details For Dashboard -API_Endpoint

```http
  GET /api/events/list/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
|  |  | **Nothing to Required**. |


#### Single Event Details by Event_id -API_Endpoint

```http
  GET /api/events/{event_id}/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `event_id` | `integer` | **Required**. Specific event_id |


#### Single Event Delete by Event_id -API_Endpoint

```http
  DELETE /api/events/delete/{event_id}/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `event_id` | `integer` | **Required**. Specific event_id |


#### Event Info Update -API_Endpoint

```http
  PUT /api/events/update/{event_id}/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `event_id` | `integer` | **Required**. Specific event_id |
| `title` | `string` | **Optonal**. Event Title |
| `description` | `string` | **Optonal**. Event description |
| `date` | `date` | **Optonal**. Event Date |
| `time` | `time` | **Optonal**. Event time |
| `location_name` | `string` | **Optonal**. Event Location Name |


#### Search Event -API_Endpoint
You can Search Event by Title,Description or location_name. If pass empty field then give you all event details.

```http
  GET /api/events/search/?query={Search_key}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Search_key` | `string` | **Optonal**. Search_key Can be anything. |



## Screenshots

![Postman Screenshots](https://i.ibb.co/cwB7k6s/ERS-API.png)

