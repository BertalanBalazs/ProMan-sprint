// It is just an idea how you can structure your data during your page is running.
// You can use it for testing purposes by simply copy/paste/run in the Console tab in your browser

let keyInLocalStorage = 'proman-data';

let sampleData = {
    // dynamic statuses: if user adds a new status, post a new object with id and name
    "statuses": [
        {
            "id": 1,
            "name": "New"
        },
        {
            "id": 2,
            "name": "In progress"
        },
        {
            "id": 3,
            "name": "Testing"
        },
        {
            "id": 4,
            "name": "Done"
        }
    ],
    "boards": [
        {
            "id": 1,
            "title": "Test Board 1",
            "is_active": true,
            "user_id": 0, // public,
            "statuses": [1, 2]
        },
        {
            "id": 2,
            "title": "Test Board 2",
            "is_active": true,
            "user_id": 0, // public
            "statuses": [3, 4]
        }
    ],
    "cards": [
        {
            "id": 1,
            "title": "task1",
            "board_id": 1,
            "status_id": 1,
            "order_num": 3
        },
        {
            "id": 2,
            "title": "task2",
            "board_id": 1,
            "status_id": 2,
            "order_num": 2
        },
        {
            "id": 3,
            "title": "task3",
            "board_id": 1,
            "status_id": 4,
            "order_num": 1
        },
        {
            "id": 4,
            "title": "task4",
            "board_id": 2,
            "status_id": 1,
            "order": 3
        },
        {
            "id": 5,
            "title": "task5",
            "board_id": 2,
            "status_id": 2,
            "order_num": 2
        },
        {
            "id": 6,
            "title": "task6",
            "board_id": 2,
            "status_id": 3,
            "order_num": 1
        }
    ],
    "users": [
        {
            "id": 1,
            "username": "Bob",
            "passwordhash": "jaslfjas9t495rgjkher"
        }
    ]
};

localStorage.setItem(keyInLocalStorage, JSON.stringify(sampleData));

