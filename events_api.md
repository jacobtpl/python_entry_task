# Event Manager REST API Documentation
---

## Authentication
To authenticate, send the HTTP request with a header field `token`, with a valid JWT obtained from the Login endpoint.

If authorization is not provided for a query that requires it, then `401 UNAUTHORIZED` will be returned.

##Login Performance
500 concurrent logins in 9 seconds ≈ 18ms per login query

---

# Login

Used to obtain a JWT for a registered user.

**URL** : `/sessions/`

**Method** : `POST`

**Auth required** : NO

**Data constraints**

```json
{
    "username": "[valid email address]",
    "password": "[password in plain text]"
}
```

**Data example**

```json
{
    "username": "teojpl",
    "password": "Garena.com"
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "token": "93144b288eb1fdccbe46d6fc0f241a51766ecd3d"
}
```

## Error Response

**Condition** : If 'username' and 'password' combination is wrong.

**Code** : `400 BAD REQUEST`


---

# Get Events

Show all events in a queried time frame and containing a specified tag. Query is returned in pages of size at most 20.

**URL** : `/events/`

**URL Parameters** :

* `offset` the index of the first page to be queried (required field)
* `page_size` the page size to be returned (max 20)
* `tag` to return events which contain this string in their tag
* `start` to return events starting after this time (in serialized Python datetime format)
* `end` to return events ending before this time (in serialized Python datetime format)

**Method** : `GET`

**Auth required** : YES

**Permissions required** : None

**Data constraints** : `{}`

## Success Responses

Returns list of events in JSON format, starting from the most recent.

**Code** : `200 OK`

**Returned Fields** :

* `event_id` The unique ID of the event
* `name` The name of the event
* `description` The description of the event
* `tags` The tags of the event
* `start` The start time of the event (in serialized Python datetime format)
* `end` The end time of the event (in serialized Python datetime format)
* `created` Timestamp when event was first created (in serialized Python datetime format)
* `updated` Timestamp when event was last updated (in serialized Python datetime format)
* `images` A list of links to attached images
* `likes` A list of user IDs of users who have liked this event
* `participants` A list of user IDs of users who are participating in this event
* `comments` A list of comment IDs of comments on this event (ordered by time, most recent first)

**Example Parameters** :

* `offset: 0`
* `page_size: 3`
* `tag: Food`
* `start: 2018-01-27T12:00:00.000Z`
* `end: 2018-12-27T12:00:00.000Z`

**Example Content** :

```json
[
    {
        "event_id": 449370,
        "name": "Striders on the Storm",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        "tags": "Food & Drink",
        "start": "2018-09-27T13:44:50.417Z",
        "end": "2018-09-27T13:44:50.417Z",
        "created": "2018-06-04T16:39:50.417Z",
        "updated": "2018-06-04T16:39:50.417Z",
        "images": [],
        "likes": [
            151,
            698,
            376,
            562
        ],
        "participants": [
            995
        ],
        "comments": []
    },
    {
        "event_id": 274068,
        "name": "Belch Blanket Babylon",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        "tags": "Food & Drink",
        "start": "2018-09-27T12:52:10.414Z",
        "end": "2018-09-27T12:52:10.414Z",
        "created": "2018-06-04T16:39:47.414Z",
        "updated": "2018-06-04T16:39:47.414Z",
        "images": ["house.png"],
        "likes": [],
        "participants": [
            761,
            210
        ],
        "comments": []
    },
    {
        "event_id": 957790,
        "name": "Conundrum Grand",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        "tags": "Food & Drink",
        "start": "2018-09-27T10:21:20.502Z",
        "end": "2018-09-27T10:21:20.502Z",
        "created": "2018-06-04T16:39:59.502Z",
        "updated": "2018-06-04T16:39:59.502Z",
        "images": ["apple.png"],
        "likes": [],
        "participants": [
            802
        ],
        "comments": []
    }
]
```

---

# Create Event

Show all events in a queried time frame and containing a specified tag. Query is returned in pages of size at most 20.

**URL** : `/events/`

**URL Parameters** :

* `offset` the index of the first page to be queried (required field)
* `page_size` the page size to be returned (max 20)
* `tag` to return events which contain this string in their tag
* `start` to return events starting after this time (in serialized Python datetime format)
* `end` to return events ending before this time (in serialized Python datetime format)

**Method** : `GET`

**Auth required** : YES

**Permissions required** : Admin

**Data constraints** : `{}`

**URL** : `/events/`

**Method** : `POST`

**Auth required** : YES

**Permissions required** : Admin

**Data constraints**

```json
{
	"name": The name of the event,
	"description": The description of the event,
	"tags": The tags of the event,
	"start": The start time of the event (in serialized Python datetime format),
	"end": The end time of the event (in serialized Python datetime format)
}
```

**Data example** All fields must be sent.

```json
{
    "name": "Dinner",
    "description": "A fun event",
    "tags": "Food and Drink",
    "start": "2018-01-27T12:00:00Z",
    "end": "2018-12-27T12:00:00Z"
}
```

## Success Responses

**Code** : `200 OK`


---

# Get Event by ID

Shows the event with the specified ID.

**URL** : `/events/<EVENT_ID>/`

**Method** : `GET`

**Auth required** : YES

**Permissions required** : None

**Data constraints** : `{}`

## Success Responses

Returns event details in JSON format.

**Code** : `200 OK`

**Returned Fields** :

* `event_id` The unique ID of the event
* `name` The name of the event
* `description` The description of the event
* `tags` The tags of the event
* `start` The start time of the event (in serialized Python datetime format)
* `end` The end time of the event (in serialized Python datetime format)
* `created` Timestamp when event was first created (in serialized Python datetime format)
* `updated` Timestamp when event was last updated (in serialized Python datetime format)
* `images` A list of links to attached images
* `likes` A list of user IDs of users who have liked this event
* `participants` A list of user IDs of users who are participating in this event
* `comments` A list of comment IDs of comments on this event (ordered by time, most recent first)


**Example Content** :

```json
{
    "event_id": 54,
    "name": "Belfast United in Song",
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    "tags": "Food & Drink",
    "start": "2018-06-30T16:40:06.607Z",
    "end": "2018-06-30T16:40:06.607Z",
    "created": "2018-06-04T16:39:42.607Z",
    "updated": "2018-06-04T16:39:42.607Z",
    "images": [],
    "likes": [
        526,
        795
    ],
    "participants": [
        939,
        447,
        796,
        610
    ],
    "comments": []
}
```

---

# Get User by ID

Shows the user with the specified ID.

**URL** : `/comments/<COMMENT_ID>/`

**Method** : `GET`

**Auth required** : YES

**Permissions required** : None

**Data constraints** : `{}`

## Success Responses

Returns event details in JSON format.

**Code** : `200 OK`

**Returned Fields** :

* `user_id` The unique ID of the user
* `name` The full name of the user
* `username` The username of the user

**Example Content** :

```json
{
    "user_id": 1,
    "name": "Jacob Teo",
    "username": "teojpl"
}
```

---

# Get Comment by ID

Shows the comment with the specified ID.

**URL** : `/comments/<COMMENT_ID>/`

**Method** : `GET`

**Auth required** : YES

**Permissions required** : None

**Data constraints** : `{}`

## Success Responses

Returns event details in JSON format.

**Code** : `200 OK`

**Returned Fields** :

* `comment_id` The unique ID of the comment
* `user` The ID of the user who commented
* `event` The ID of the event that the comment was posted on
* `text` The text of the comment
* `event` The ID of the event that the comment was posted on
* `created` Timestamp when comment was first created (in serialized Python datetime format)
* `updated` Timestamp when comment was last updated (in serialized Python datetime format)

**Example Content** :

```json
{
    "comment_id": 101,
    "user": 451,
    "event": 248934,
    "text": "sell set",
    "created": "2018-05-23T04:52:58.550Z",
    "updated": "2018-09-24T05:24:20.550Z"
}
```
---

# Get Like by ID

Shows the like with the specified ID.

**URL** : `/comments/<COMMENT_ID>/`

**Method** : `GET`

**Auth required** : YES

**Permissions required** : None

**Data constraints** : `{}`

## Success Responses

Returns like details in JSON format.

**Code** : `200 OK`

**Returned Fields** :

* `like_id` The unique ID of the like
* `user` The ID of the user liking the event
* `event` The ID of the event liked

**Example Content** :

```json
{
    "like_id": 101,
    "user": 38,
    "event": 734409
}
```
---

# Get Like by ID

Shows the like with the specified ID.

**URL** : `/comments/<COMMENT_ID>/`

**Method** : `GET`

**Auth required** : YES

**Permissions required** : None

**Data constraints** : `{}`

## Success Responses

Returns like details in JSON format.

**Code** : `200 OK`

**Returned Fields** :

* `like_id` The unique ID of the like
* `user` The ID of the user liking the event
* `event` The ID of the event liked

**Example Content** :

```json
{
    "like_id": 101,
    "user": 38,
    "event": 734409
}
```
---


# Set Like

Set whether a user has liked an event.

**URL** : `/events/likes/`

**Method** : `POST`

**Auth required** : YES

**Permissions required** : None

**Data constraints**

Provide ID of event and the value `like`, which should be 1 if the user likes the event and 0 otherwise.

```json
{
    "event_id": [int],
    "like": [0 or 1]
}
```

**Data example** All fields must be sent.

```json
{
    "event_id": 123,
    "like": 1
}
```

## Success Response

**Code** : `200 OK`


## Error Response

**Condition** : If event does not exist

**Code** : `400 BAD REQUEST`

---

# Get Participation by ID

Shows the participation with the specified ID.

**URL** : `/events/participations/<PARTICIPATION_ID>/`

**Method** : `GET`

**Auth required** : YES

**Permissions required** : None

**Data constraints** : `{}`

## Success Responses

Returns participation details in JSON format.

**Code** : `200 OK`

**Returned Fields** :

* `participation_id ` The unique ID of the participation
* `user` The ID of the user participating in the event
* `event` The ID of the event participated in

**Example Content** :

```json
{
    "participation_id": 101,
    "user": 791,
    "event": 684112
}
```

---
# Set Participation

Set whether a user is participating an event.

**URL** : `/events/participations/`

**Method** : `POST`

**Auth required** : YES

**Permissions required** : None

**Data constraints**

Provide ID of event and the value `participate `, which should be 1 if the user is participating in the event and 0 otherwise.

```json
{
    "event_id": [int],
    "participate": [0 or 1]
}
```

**Data example** All fields must be sent.

```json
{
    "event_id": 123,
    "participate": 1
}
```

## Success Response

**Code** : `200 OK`


## Error Response

**Condition** : If event does not exist

**Code** : `400 BAD REQUEST`

---

# Post Comment

Post a comment on an event.

**URL** : `/comments/`

**Method** : `POST`

**Auth required** : YES

**Permissions required** : None

**Data constraints**

Provide ID of event and the text of the comment to be posted.

```json
{
    "event_id": [int],
    "text": "[text]"
}
```

**Data example** All fields must be sent.

```json
{
    "event_id": 123,
    "text": "Happy birthday!"
}
```

## Success Response

**Code** : `200 OK`


## Error Response

**Condition** : If event does not exist

**Code** : `400 BAD REQUEST`

---

# Database Tables (event_db)

# event_tab

Events in the database

| ID   | Name   | Type  | Comment   |
| ---- | ------ | --------------| ----------|
| 1    | event_id     | int     | Primary Key, auto-increment  |
| 2    | name     | varchar(200)     | Event name |
| 3    | description     | varchar(500)     | Event description  |
| 4    | tags     | varchar(200)      | Tags |
| 5    | start     | datetime     | Start time of event |
| 6    | end     | datetime     | End time of event  |
| 7    | created     | datetime     | Created timestamp |
| 8    | updated     | datetime     | Updated timestamp  |

~~~~sql
CREATE TABLE `event_tab` (
  `event_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `description` varchar(500) NOT NULL,
  `tags` varchar(200) NOT NULL,
  `start` datetime(6) NOT NULL,
  `end` datetime(6) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  PRIMARY KEY (`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1000002 DEFAULT CHARSET=utf8;
~~~~

# user_tab

Users in the database

| ID   | Name   | Type  | Comment   |
| ---- | ------ | --------------| ----------|
| 1    | user_id     | int     | Primary Key, auto-increment  |
| 2    | name     | varchar(200)     | Employee name |
| 3    | username     | varchar(64)     | Username, unique  |
| 4    | passhash     | varchar(70)      | SHA-256 hash of password (with salt) |
| 5    | salt     | varchar(32)     | Salt used for hashing |
| 6    | admin     | tinyint     | 1 for admin, 0 for regular user  |
| 7    | created     | datetime     | Created timestamp |
| 8    | updated     | datetime     | Updated timestamp  |

~~~~sql
CREATE TABLE `user_tab` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `username` varchar(64) NOT NULL DEFAULT '',
  `passhash` varchar(70) NOT NULL,
  `salt` varchar(32) NOT NULL,
  `admin` tinyint(1) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=1000001 DEFAULT CHARSET=utf8;
~~~~

# like_tab

Likes in the database

| ID   | Name   | Type  | Comment   |
| ---- | ------ | --------------| ----------|
| 1    | like_id     | int     | Primary Key, auto-increment  |
| 2    | event_id     | int    | ID of event liked, foreign key |
| 3    | user_id     | int     | User ID that liked the event, foreign key |

~~~~sql
CREATE TABLE `like_tab` (
  `like_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`like_id`),
  KEY `like_tab_event_id_b0d36dc1_fk_event_tab_event_id` (`event_id`),
  KEY `like_tab_user_id_4fec33fe_fk_user_tab_user_id` (`user_id`),
  CONSTRAINT `like_tab_event_id_b0d36dc1_fk_event_tab_event_id` FOREIGN KEY (`event_id`) REFERENCES `event_tab` (`event_id`),
  CONSTRAINT `like_tab_user_id_4fec33fe_fk_user_tab_user_id` FOREIGN KEY (`user_id`) REFERENCES `user_tab` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1000001 DEFAULT CHARSET=utf8;
~~~~

# participation_tab

Event participations in the database

| ID   | Name   | Type  | Comment   |
| ---- | ------ | --------------| ----------|
| 1    | participation_id     | int     | Primary Key, auto-increment  |
| 2    | event_id     | int    | ID of event participated in, foreign key |
| 3    | user_id     | int     | User ID that participated in the event, foreign key |

~~~~sql
CREATE TABLE `participation_tab` (
  `participation_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`participation_id`),
  KEY `participation_tab_event_id_4277446c_fk_event_tab_event_id` (`event_id`),
  KEY `participation_tab_user_id_704a6e50_fk_user_tab_user_id` (`user_id`),
  CONSTRAINT `participation_tab_event_id_4277446c_fk_event_tab_event_id` FOREIGN KEY (`event_id`) REFERENCES `event_tab` (`event_id`),
  CONSTRAINT `participation_tab_user_id_704a6e50_fk_user_tab_user_id` FOREIGN KEY (`user_id`) REFERENCES `user_tab` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1000001 DEFAULT CHARSET=utf8;
~~~~

# comment_tab

Comments in the database

| ID   | Name   | Type  | Comment   |
| ---- | ------ | --------------| ----------|
| 1    | comment_id     | int     | Primary Key, auto-increment  |
| 2    | text     | varchar(500)     | Contents of the comment |
| 3    | created     | datetime     | Created timestamp |
| 4    | updated     | datetime     | Updated timestamp  |
| 5    | event_id     | int    | ID of event commented on, foreign key |
| 6    | user_id     | int     | User ID that commented on the event, foreign key |

~~~~sql
CREATE TABLE `comment_tab` (
  `comment_id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(500) NOT NULL,
  `created` datetime(6) NOT NULL,
  `updated` datetime(6) NOT NULL,
  `event_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`comment_id`),
  KEY `comment_tab_event_id_a1b4d8fc_fk_event_tab_event_id` (`event_id`),
  KEY `comment_tab_user_id_bddf6348_fk_user_tab_user_id` (`user_id`),
  CONSTRAINT `comment_tab_event_id_a1b4d8fc_fk_event_tab_event_id` FOREIGN KEY (`event_id`) REFERENCES `event_tab` (`event_id`),
  CONSTRAINT `comment_tab_user_id_bddf6348_fk_user_tab_user_id` FOREIGN KEY (`user_id`) REFERENCES `user_tab` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1000001 DEFAULT CHARSET=utf8;
~~~~

# image_tab

Images in the database

| ID   | Name   | Type  | Comment   |
| ---- | ------ | --------------| ----------|
| 1    | image_id     | int     | Primary Key, auto-increment  |
| 2    | image_path     | varchar(400)    | Path of image on server |
| 3    | event_id     | int    | ID of corresponding event, foreign key |

~~~~sql
CREATE TABLE `image_tab` (
  `image_id` int(11) NOT NULL AUTO_INCREMENT,
  `image_path` varchar(400) NOT NULL,
  `event_id` int(11) NOT NULL,
  PRIMARY KEY (`image_id`),
  KEY `image_tab_event_id_8cecb87d_fk_event_tab_event_id` (`event_id`),
  CONSTRAINT `image_tab_event_id_8cecb87d_fk_event_tab_event_id` FOREIGN KEY (`event_id`) REFERENCES `event_tab` (`event_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1000001 DEFAULT CHARSET=utf8;
~~~~