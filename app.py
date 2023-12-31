import sys
import logging
from flask import Flask, render_template, request

app = Flask(__name__)

# Custom IP and port
custom_ip = '192.168.1.14'  # Replace with your custom IP address
port = 5000  # Replace with your desired port number


# Configure logging to write to a log file
log_file = '/opt/python_workspace/text_game/game.log'
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,  # Adjust the log level as needed
    format='%(asctime)s - %(levelname)s - %(message)s'
)


# Initial game state
game_state = {
    'current_room': 'start',
    'inventory': [],
    'rooms': {
        'start': {
            'description': 'You are in a dark room. There is a door to the north.',
            'exits': {'north': 'hallway'},
        },
        'hallway': {
            'description': 'You are in a long hallway. There are doors to the north and south.',
            'exits': {'north': 'kitchen', 'south': 'start'},
        },
        'kitchen': {
            'description': 'You are in the kitchen. There is a knife on the table.',
            'exits': {'south': 'hallway'},
            'items': ['knife'],
        },
    }
}

@app.route('/')
def index():
    current_room = game_state['current_room']
    room = game_state['rooms'][current_room]
    return render_template('index.html', room=room)

@app.route('/submit', methods=['POST'])
def submit():
    command = request.form['command'].lower()
    current_room = game_state['current_room']
    room = game_state['rooms'][current_room]

    if command == 'look':
        response = room['description']
    elif command == 'inventory':
        inventory = ', '.join(game_state['inventory'])
        response = f'Inventory: {inventory}'
    elif command.startswith('go '):
        direction = command[3:]
        if direction in room['exits']:
            game_state['current_room'] = room['exits'][direction]
            response = 'You go ' + direction
        else:
            response = 'You can\'t go that way.'
    else:
        response = 'I don\'t understand that command.'

    return render_template('index.html', room=room, response=response)

sys.stdout = sys.stderr = open(log_file, 'a')


if __name__ == '__main__':
    app.run(host=custom_ip, port=port, debug=True)
