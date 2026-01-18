def test_create_chat(client):
    response = client.post("/chats/", json={"title": "Test chat"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test chat"


def test_create_chat_empty_title(client):
    response = client.post("/chats/", json={"title": "   "})
    assert response.status_code == 422


def test_send_message(client):
    chat = client.post("/chats/", json={"title": "Chat"}).json()

    response = client.post(
        f"/chats/{chat['id']}/messages/",
        json={"text": "Hello"},
    )

    assert response.status_code == 201
    assert response.json()["text"] == "Hello"


def test_send_message_to_unknown_chat(client):
    response = client.post(
        "/chats/999/messages/",
        json={"text": "Hello"},
    )
    assert response.status_code == 404


def test_get_chat_with_limit(client):
    chat = client.post("/chats/", json={"title": "Chat"}).json()

    for i in range(5):
        client.post(
            f"/chats/{chat['id']}/messages/",
            json={"text": f"msg {i}"},
        )

    response = client.get(f"/chats/{chat['id']}?limit=3")
    messages = response.json()["messages"]

    assert len(messages) == 3
    assert messages[0]["text"] == "msg 2"
    assert messages[-1]["text"] == "msg 4"


def test_delete_chat_cascade(client):
    chat = client.post("/chats/", json={"title": "Chat"}).json()

    client.post(
        f"/chats/{chat['id']}/messages/",
        json={"text": "Hello"},
    )

    response = client.delete(f"/chats/{chat['id']}")
    assert response.status_code == 204

    response = client.get(f"/chats/{chat['id']}")
    assert response.status_code == 404
