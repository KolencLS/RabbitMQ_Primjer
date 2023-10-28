from flask import Flask, render_template
import pika
import time

app = Flask(__name__)

# Initialize RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='time_queue')

# Flag to control message creation and consumption
streaming = False

def produce_time_periodically():
    while True:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        channel.basic_publish(exchange='', routing_key='time_queue', body=current_time)
        time.sleep(1)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/toggle_stream')
def toggle_stream():
    global streaming
    streaming = not streaming
    return "on" if streaming else "off"

@app.route('/consume_time')
def consume_time():
    method_frame, header_frame, body = channel.basic_get(queue='time_queue')
    if method_frame:
        message = body.decode('utf-8')
    else:
        message = None
    return message

if __name__ == '__main__':
    app.run(debug=True)
