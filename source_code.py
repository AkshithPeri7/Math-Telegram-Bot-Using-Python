import os
import re
import time
import json
import math
import logging
import datetime
import requests
from threading import Thread
import uuid  # For generating unique callback IDs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
LOG_DIR = "log"
os.makedirs(LOG_DIR, exist_ok=True)
USER_LOG_FILE = os.path.join(LOG_DIR, "user_logs.txt")
API_URL = f"bot token }"
CALLBACK_DATA = {}
EMOJI = {
    "factorial": "🔢",
    "fibonacci": "📈",
    "isprime": "🔍",
    "sqrt": "√",
    "power": "⏫",
    "gcd": "🔗",
    "lcm": "🔄",
    "success": "✅",
    "error": "❌",
    "warning": "⚠️",
    "info": "ℹ️",
    "math": "🧮",
    "welcome": "👋",
    "help": "❓",
    "calculator": "🔢",
    "formula": "📊",
    "start": "🚀",
    "settings": "⚙️"
}
COMMANDS = {
    "factorial": "Calculate the factorial of a number (e.g., factorial 5)",
    "fibonacci": "Get the Fibonacci sequence up to a number (e.g., fibonacci 10)",
    "isprime": "Check if a number is prime (e.g., isprime 17)",
    "sqrt": "Calculate the square root of a number (e.g., sqrt 16)",
    "power": "Calculate one number raised to the power of another (e.g., power 2 3)",
    "gcd": "Find the greatest common divisor of two numbers (e.g., gcd 12 8)",
    "lcm": "Find the least common multiple of two numbers (e.g., lcm 4 6)",
}

def get_updates(offset=None, timeout=30):
    """
    Get updates from Telegram API.
    
    Args:
        offset (int, optional): Identifier of the first update to be returned.
        timeout (int, optional): Timeout in seconds for long polling.
        
    Returns:
        dict: The decoded API response.
    """
    params = {'timeout': timeout}
    if offset:
        params['offset'] = offset
    
    try:
        response = requests.get(f"{API_URL}/getUpdates", params=params)
        return response.json()
    except Exception as e:
        logger.error(f"Error getting updates: {e}")
        return {'ok': False, 'description': str(e)}

def send_message(chat_id, text, reply_markup=None):
    """
    Send a message via Telegram API.
      Args:
        chat_id (int): Unique identifier for the target chat.
        text (str): Text of the message to be sent.
        reply_markup (dict, optional): Inline keyboard markup or other reply options.
        
    Returns:
        dict: The decoded API response.
    """
    params = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    
    if reply_markup:
        params['reply_markup'] = json.dumps(reply_markup)
    
    try:
        response = requests.post(f"{API_URL}/sendMessage", params=params)
        return response.json()
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return {'ok': False, 'description': str(e)}

def create_inline_keyboard(buttons, columns=2):
    """
    Create an inline keyboard markup structure for Telegram messages.
    
    Args:
        buttons (list): List of button dictionaries, each containing 'text' and 'callback_data'.
        columns (int): Number of columns in the keyboard layout.
        
    Returns:
        dict: Inline keyboard markup structure.
    """
    keyboard = []
    row = []
    
    for i, button in enumerate(buttons):
        row.append(button)
        
        # Start a new row after reaching column limit
        if (i + 1) % columns == 0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    return {'inline_keyboard': keyboard}

def send_photo(chat_id, photo_url, caption=None, reply_markup=None):
    """
    Send a photo via Telegram API.
    
    Args:
        chat_id (int): Unique identifier for the target chat.
        photo_url (str): URL of the photo or local file path.
        caption (str, optional): Caption for the photo.
        reply_markup (dict, optional): Inline keyboard markup or other reply options.
        
    Returns:
        dict: The decoded API response.
    """
    params = {'chat_id': chat_id}
    
    if caption:
        params['caption'] = caption
        params['parse_mode'] = 'HTML'
    
    if reply_markup:
        params['reply_markup'] = json.dumps(reply_markup)
    
    try:
        if photo_url.startswith(('http://', 'https://')):
            params['photo'] = photo_url
            response = requests.post(f"{API_URL}/sendPhoto", params=params)
        else:
            with open(photo_url, 'rb') as photo:
                files = {'photo': photo}
                response = requests.post(f"{API_URL}/sendPhoto", data=params, files=files)
       return response.json()
    except Exception as e:
        logger.error(f"Error sending photo: {e}")
        return {'ok': False, 'description': str(e)}

def answer_callback_query(callback_query_id, text=None, show_alert=False):
    """
    Answer a callback query from an inline keyboard button.
    
    Args:
        callback_query_id (str): Unique identifier for the query to be answered.
        text (str, optional): Text to show to the user.
        show_alert (bool, optional): If True, shows as an alert instead of notification.
        
    Returns:
        dict: The decoded API response.
    """
    params = {'callback_query_id': callback_query_id}
    
    if text:
        params['text'] = text
    
    params['show_alert'] = show_alert
    
    try:
        response = requests.post(f"{API_URL}/answerCallbackQuery", params=params)
        return response.json()
    except Exception as e:
        logger.error(f"Error answering callback query: {e}")
        return {'ok': False, 'description': str(e)}

def edit_message_text(chat_id, message_id, text, reply_markup=None):
    """
    Edit a message's text.
    
    Args:
        chat_id (int): Unique identifier for the target chat.
        message_id (int): Identifier of the message to edit.
        text (str): New text of the message.
        reply_markup (dict, optional): Inline keyboard markup or other reply options.
        
    Returns:
        dict: The decoded API response.
    """
    params = {
        'chat_id': chat_id,
        'message_id': message_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    
    if reply_markup:
        params['reply_markup'] = json.dumps(reply_markup)
    
    try:
        response = requests.post(f"{API_URL}/editMessageText", params=params)
        return response.json()
    except Exception as e:
        logger.error(f"Error editing message: {e}")
        return {'ok': False, 'description': str(e)}

def calculate_factorial(n):
    """
    Calculate the factorial of a number using math.factorial for efficiency.
    
    Args:
        n (int): The number to calculate factorial for
        
    Returns:
        int: The factorial of n
        
    Raises:
        ValueError: If n is negative or too large
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n > 100:
        raise ValueError("Number too large")
    
    return math.factorial(n)

def calculate_fibonacci(n):
    """
    Calculate the Fibonacci sequence up to n terms.
    
    Args:
        n (int): The number of terms in the Fibonacci sequence
        
    Returns:
        list: The Fibonacci sequence up to n terms
        
    Raises:
        ValueError: If n is negative or too large
    """
    if n < 0:
        raise ValueError("Number of terms cannot be negative")
    if n > 100:
        raise ValueError("Number too large")
    
    sequence = []
    a, b = 0, 1
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    
    return sequence

def is_prime(n):
    """
    Check if a number is prime.
    
    Args:
        n (int): The number to check
        
    Returns:
        bool: True if n is prime, False otherwise
        
    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("Negative numbers cannot be prime")
    
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
        
    return True

def calculate_square_root(n):
    """
    Calculate the square root of a number.
    
    Args:
        n (float): The number to calculate the square root of
        
    Returns:
        float: The square root of n
        
    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("Cannot calculate square root of a negative number")
    
    return math.sqrt(n)

def calculate_power(base, exponent):
    """
    Calculate the power of a number.
    
    Args:
        base (float): The base number
        exponent (float): The exponent
        
    Returns:
        float: The result of base raised to exponent
        
    Raises:
        ValueError: If the operation would result in a complex number
    """
    if base == 0 and exponent < 0:
        raise ValueError("Cannot raise zero to a negative power")
    
    if base < 0 and not exponent.is_integer():
        raise ValueError("Cannot raise negative number to a non-integer power")
    if abs(base) > 100 or abs(exponent) > 100:
        raise ValueError("Numbers too large for calculation")
    
    return math.pow(base, exponent)

def calculate_gcd(a, b):
    """
    Calculate the greatest common divisor of two numbers.
    
    Args:
        a (int): First number
        b (int): Second number
        
    Returns:
        int: The greatest common divisor of a and b
    """
    return math.gcd(abs(int(a)), abs(int(b)))

def calculate_lcm(a, b):
    """
    Calculate the least common multiple of two numbers.
    
    Args:
        a (int): First number
        b (int): Second number
        
    Returns:
        int: The least common multiple of a and b
        
    Raises:
        ValueError: If either number is negative or zero
    """
    if a <= 0 or b <= 0:
        raise ValueError("Cannot calculate LCM for non-positive numbers")
    
    return abs(a * b) // math.gcd(int(a), int(b))

def log_user_interaction(user_id, full_name, text):
    """
    Log user interaction to a file.
    
    Args:
        user_id (int): Telegram user ID
        full_name (str): User's full name
        text (str): Message text
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} | {user_id} | {full_name} | {text}\n"
    
    try:
        with open(USER_LOG_FILE, "a") as log_file:
            log_file.write(log_entry)
    except Exception as e:
        logger.error(f"Failed to write to log file: {e}")

def handle_start_command(chat_id, user):
    """
    Handle the /start command.
    
    Args:
        chat_id (int): Chat ID
        user (dict): User information
    """
    first_name = user.get('first_name', 'there')
    user_id = user.get('id')
    full_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
    
    logger.info(f"User {user_id} ({full_name}) started the bot")
    log_user_interaction(user_id, full_name, "/start")
    
    message = (
        f"{EMOJI['welcome']} <b>Welcome, {first_name}!</b>\n\n"
        f"{EMOJI['math']} <b>Math Calculator Bot</b> at your service.\n\n"
        "I can perform various mathematical operations. Choose a function below or type a command:"
    )
    
    buttons = []
    for cmd, desc in COMMANDS.items():
        # Create a unique callback ID for each button
        callback_id = f"func_{cmd}_{uuid.uuid4().hex[:8]}"
        
        CALLBACK_DATA[callback_id] = {
            'command': cmd,
            'user_id': user_id
        }
        
        emoji = EMOJI.get(cmd, "🔢")
        buttons.append({
            'text': f"{emoji} {cmd.capitalize()}",
            'callback_data': callback_id
        })
    
    help_callback_id = f"help_{uuid.uuid4().hex[:8]}"
    CALLBACK_DATA[help_callback_id] = {
        'command': 'help',
        'user_id': user_id
    }
    buttons.append({
        'text': f"{EMOJI['help']} Help",
        'callback_data': help_callback_id
    })
    
    keyboard = create_inline_keyboard(buttons, columns=2)
    
    send_message(chat_id, message, reply_markup=keyboard)

def handle_help_command(chat_id, user):
    """
    Handle the /help command.
    
    Args:
        chat_id (int): Chat ID
        user (dict): User information
    """
    user_id = user.get('id')
    full_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
    
    logger.info(f"User {user_id} ({full_name}) requested help")
    log_user_interaction(user_id, full_name, "/help")
   
    message = (
        f"{EMOJI['help']} <b>Math Calculator Bot Help</b>\n\n"
        "I can perform the following mathematical operations:\n\n"
    )
    
    # Add each command with its emoji and description
    for cmd, desc in COMMANDS.items():
        emoji = EMOJI.get(cmd, "🔢")
        message += f"• <b>{emoji} {cmd}</b> - {desc}\n"
    
    message += (
        "\n<b>Examples:</b>\n"
        "• factorial 5\n"
        "• fibonacci 10\n"
        "• isprime 17\n"
        "• sqrt 16\n"
        "• power 2 3\n\n"
        "You can also just send me a number to calculate its factorial (legacy mode)."
    )
buttons = []
    example_values = {
        'factorial': '5',
        'fibonacci': '10',
        'isprime': '17',
        'sqrt': '16',
        'power': '2 3',
        'gcd': '12 8',
        'lcm': '4 6'
    }
    
    for cmd, value in example_values.items():
        # Create a unique callback ID for each button
        callback_id = f"example_{cmd}_{uuid.uuid4().hex[:8]}"
       
        CALLBACK_DATA[callback_id] = {
            'command': cmd,
            'args': value.split(),
            'user_id': user_id
        }
        emoji = EMOJI.get(cmd, "🔢")
        buttons.append({
            'text': f"{emoji} {cmd}({value})",
            'callback_data': callback_id
        })
    back_callback_id = f"back_to_start_{uuid.uuid4().hex[:8]}"
    CALLBACK_DATA[back_callback_id] = {
        'command': 'start',
        'user_id': user_id
    }
    buttons.append({
        'text': f"{EMOJI['start']} Back to Main Menu",
        'callback_data': back_callback_id
    })
    keyboard = create_inline_keyboard(buttons, columns=2)
    send_message(chat_id, message, reply_markup=keyboard)

def parse_command(text):
    """
    Parse the text to extract command and arguments.
    
    Args:
        text (str): The message text
        
    Returns:
        tuple: (command, arguments)
    """
    # Check for command pattern: command arg1 arg2 ...
    parts = text.lower().strip().split()
    
    if not parts:
        return None, []
    
    command = parts[0]
    args = parts[1:]
  
    return command, args

def handle_mathematical_command(chat_id, user, text):
    """
    Handle mathematical commands from users.
    
    Args:
        chat_id (int): Chat ID
        user (dict): User information
        text (str): Message text
    """
    user_id = user.get('id')
    full_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
    
    logger.info(f"Received message from {user_id} ({full_name}): {text}")
    log_user_interaction(user_id, full_name, text)
    
    # Parse the command and arguments
    command, args = parse_command(text)
    
    try:
        if command and command.isdigit() and not args:
            num = int(command)
            factorial = calculate_factorial(num)
            formatted_factorial = f"{factorial:,}"
            
            message = (
                f"{EMOJI['success']} <b>Factorial Result</b>\n\n"
                f"<code>{num}! = {formatted_factorial}</code>"
            )
            
            new_calc_id = f"back_to_start_{uuid.uuid4().hex[:8]}"
            CALLBACK_DATA[new_calc_id] = {
                'command': 'start',
                'user_id': user_id
            }
            
            keyboard = create_inline_keyboard([
                {
                    'text': f"{EMOJI['calculator']} New Calculation",
                    'callback_data': new_calc_id
                }
            ])
            send_message(chat_id, message, reply_markup=keyboard)
            logger.info(f"Calculated factorial of {num} for user {user_id}")
            return
        
        # Handle specific commands
        if command == "factorial" and len(args) == 1:
            num = int(args[0])
            factorial = calculate_factorial(num)
            formatted_factorial = f"{factorial:,}"
            
            message = (
                f"{EMOJI['factorial']} <b>Factorial Result</b>\n\n"
                f"<code>{num}! = {formatted_factorial}</code>"
            )
            new_calc_id = f"back_to_start_{uuid.uuid4().hex[:8]}"
            CALLBACK_DATA[new_calc_id] = {
                'command': 'start',
                'user_id': user_id
            }
            keyboard = create_inline_keyboard([
                {
                    'text': f"{EMOJI['calculator']} New Calculation",
                    'callback_data': new_calc_id
                }
            ])
            
            send_message(chat_id, message, reply_markup=keyboard)
            
        elif command == "fibonacci" and len(args) == 1:
            num = int(args[0])
            sequence = calculate_fibonacci(num)
            
          
            if len(sequence) > 15:
                # For long sequences, format into multiple lines
                chunks = [sequence[i:i+5] for i in range(0, len(sequence), 5)]
                formatted_sequence = "\n".join([", ".join(map(str, chunk)) for chunk in chunks])
            else:
                formatted_sequence = ", ".join(map(str, sequence))
            
            message = (
                f"{EMOJI['fibonacci']} <b>Fibonacci Sequence</b>\n\n"
                f"First {num} terms:\n"
                f"<code>{formatted_sequence}</code>"
            )
            
            new_calc_id = f"back_to_start_{uuid.uuid4().hex[:8]}"
            CALLBACK_DATA[new_calc_id] = {
                'command': 'start',
                'user_id': user_id
            }
            
            keyboard = create_inline_keyboard([
                {
                    'text': f"{EMOJI['calculator']} New Calculation",
                    'callback_data': new_calc_id
                }
            ])
            
            send_message(chat_id, message, reply_markup=keyboard)
            
        elif command == "isprime" and len(args) == 1:
            num = int(args[0])
            result = is_prime(num)
            
            if result:
                message = (
                    f"{EMOJI['success']} <b>Prime Number Check</b>\n\n"
                    f"<code>{num} is a prime number</code>"
                )
            else:
                message = (
                    f"{EMOJI['error']} <b>Prime Number Check</b>\n\n"
                    f"<code>{num} is not a prime number</code>"
                )
            
            new_calc_id = f"back_to_start_{uuid.uuid4().hex[:8]}"
            CALLBACK_DATA[new_calc_id] = {
                'command': 'start',
                'user_id': user_id
            }
            
            keyboard = create_inline_keyboard([
                {
                    'text': f"{EMOJI['calculator']} New Calculation",
                    'callback_data': new_calc_id
                }
            ])
        elif command == "sqrt" and len(args) == 1:
            num = float(args[0])
            result = calculate_square_root(num)
            
            message = (
                f"{EMOJI['sqrt']} <b>Square Root Result</b>\n\n"
                f"<code>√{num} = {result:.6g}</code>"
            )
            
            new_calc_id = f"back_to_start_{uuid.uuid4().hex[:8]}"
            CALLBACK_DATA[new_calc_id] = {
                'command': 'start',
                'user_id': user_id
            }
            
            keyboard = create_inline_keyboard([
                {
                    'text': f"{EMOJI['calculator']} New Calculation",
                    'callback_data': new_calc_id
                }
            ])
            
            send_message(chat_id, message, reply_markup=keyboard)
            
        elif command == "power" and len(args) == 2:
            base = float(args[0])
            exponent = float(args[1])
            result = calculate_power(base, exponent)
            
            message = (
                f"{EMOJI['power']} <b>Power Operation Result</b>\n\n"
                f"<code>{base}^{exponent} = {result:.6g}</code>"
            )
            new_calc_id = f"back_to_start_{uuid.uuid4().hex[:8]}"
            CALLBACK_DATA[new_calc_id] = {
                'command': 'start',
                'user_id': user_id
            }
            
            keyboard = create_inline_keyboard([
                {
                    'text': f"{EMOJI['calculator']} New Calculation",
                    'callback_data': new_calc_id
                }
            ])
            
            send_message(chat_id, message, reply_markup=keyboard)
            
        elif command == "gcd" and len(args) == 2:
            a = int(args[0])
            b = int(args[1])
            result = calculate_gcd(a, b)
            
            message = (
                f"{EMOJI['gcd']} <b>Greatest Common Divisor</b>\n\n"
                f"<code>GCD({a}, {b}) = {result}</code>"
            )
            
            new_calc_id = f"back_to_start_{uuid.uuid4().hex[:8]}"
            CALLBACK_DATA[new_calc_id] = {
                'command': 'start',
                'user_id': user_id
            }
            
            keyboard = create_inline_keyboard([
                {
                    'text': f"{EMOJI['calculator']} New Calculation",
                    'callback_data': new_calc_id
                }
            ])
            
            send_message(chat_id, message, reply_markup=keyboard)
            
        elif command == "lcm" and len(args) == 2:
            a = int(args[0])
            b = int(args[1])
            result = calculate_lcm(a, b)
            
            message = (
                f"{EMOJI['lcm']} <b>Least Common Multiple</b>\n\n"
                f"<code>LCM({a}, {b}) = {result}</code>"
            )
            
            new_calc_id = f"back_to_start_{uuid.uuid4().hex[:8]}"
            CALLBACK_DATA[new_calc_id] = {
                'command': 'start',
                'user_id': user_id
            }
            
            keyboard = create_inline_keyboard([
                {
                    'text': f"{EMOJI['calculator']} New Calculation",
                    'callback_data': new_calc_id
                }
            ])
            
            send_message(chat_id, message, reply_markup=keyboard)
            
        else:
       
            if command in COMMANDS:
                
                help_callback_id = f"help_{uuid.uuid4().hex[:8]}"
                CALLBACK_DATA[help_callback_id] = {
                    'command': 'help',
                    'user_id': user_id
                }
                
                keyboard = create_inline_keyboard([
                    {
                        'text': f"{EMOJI['help']} Help",
                        'callback_data': help_callback_id
                    }
                ])
                
                send_message(
                    chat_id, 
                    f"{EMOJI['error']} <b>Invalid Format</b>\n\n"
                    f"Invalid format for the '{command}' command.\n\n"
                    f"{COMMANDS[command]}",
                    reply_markup=keyboard
                )
            else:
                # Create help button
                help_callback_id = f"help_{uuid.uuid4().hex[:8]}"
                CALLBACK_DATA[help_callback_id] = {
                    'command': 'help',
                    'user_id': user_id
                }
                
                keyboard = create_inline_keyboard([
                    {
                        'text': f"{EMOJI['help']} Help",
                        'callback_data': help_callback_id
                    }
                ])
                
                send_message(
                    chat_id,
                    f"{EMOJI['error']} <b>Unknown Command</b>\n\n"
                    f"I don't recognize that command. Press the Help button below to see available commands.",
                    reply_markup=keyboard
                )
        
    except ValueError as e:
        # Handle invalid inputs with a styled error message
        # Create help button
        help_callback_id = f"help_{uuid.uuid4().hex[:8]}"
        CALLBACK_DATA[help_callback_id] = {
            'command': 'help',
            'user_id': user_id
        }
        
        keyboard = create_inline_keyboard([
            {
                'text': f"{EMOJI['help']} Help",
                'callback_data': help_callback_id
            }
        ])
        
        send_message(
            chat_id,
            f"{EMOJI['error']} <b>Input Error</b>\n\n"
            f"{str(e)}.\n\nPlease check your input and try again.",
            reply_markup=keyboard
        )
        logger.warning(f"Invalid input from user {user_id}: {text} - {str(e)}")
    
    except Exception as e:
        help_callback_id = f"help_{uuid.uuid4().hex[:8]}"
        CALLBACK_DATA[help_callback_id] = {
            'command': 'help',
            'user_id': user_id
        }
        
        keyboard = create_inline_keyboard([
            {
                'text': f"{EMOJI['help']} Help",
                'callback_data': help_callback_id
            }
        ])
        
        send_message(
            chat_id,
            f"{EMOJI['error']} <b>Unexpected Error</b>\n\n"
            f"An error occurred while processing your request.\n\n"
            f"Please try again with different input values.",
            reply_markup=keyboard
        )
        logger.error(f"Error processing message '{text}' from user {user_id}: {str(e)}")

def process_updates():
    """
    Main loop for processing Telegram updates.
    """
    logger.info("Starting to process updates...")
    offset = None
    
    while True:
        try:
            # Get updates from Telegram
            result = get_updates(offset)
            
            if result.get('ok'):
                updates = result.get('result', [])
                
                if updates:
                    for update in updates:
                        # Process the update
                        process_update(update)
                    
                        offset = update['update_id'] + 1
            else:
                logger.error(f"Failed to get updates: {result.get('description')}")
                time.sleep(5)
                
        except Exception as e:
            logger.error(f"Error in update processing loop: {e}")
            time.sleep(5)
            
def handle_function_selection(chat_id, user, command):
    """
    Handle when a user selects a function from the main menu.
    
    Args:
        chat_id (int): Chat ID
        user (dict): User information
        command (str): Selected function/command
    """
    user_id = user.get('id')
    
    if command == 'help':
        # User selected help
        handle_help_command(chat_id, user)
        return
    
    if command == 'start':
        # User selected back to start
        handle_start_command(chat_id, user)
        return
    
    if command not in COMMANDS:
        # Invalid command
        send_message(chat_id, f"{EMOJI['error']} Function not found. Please try again.")
        return
    
    emoji = EMOJI.get(command, "🔢")
    description = COMMANDS[command]
    
    if command in ['factorial', 'fibonacci', 'isprime', 'sqrt']:
        
        message = (
            f"{emoji} <b>{command.capitalize()}</b>\n\n"
            f"{description}\n\n"
            f"Enter a number to calculate {command}:"
        )
    elif command in ['power', 'gcd', 'lcm']:
        # These functions take two numbers
        message = (
            f"{emoji} <b>{command.capitalize()}</b>\n\n"
            f"{description}\n\n"
            f"Enter two numbers separated by space (e.g., 2 3):"
        )
    else:
        message = (
            f"{emoji} <b>{command.capitalize()}</b>\n\n"
            f"{description}\n\n"
            f"Please enter the required value(s):"
        )
   session_id = f"session_{command}_{uuid.uuid4().hex[:8]}"
    
    CALLBACK_DATA[session_id] = {
        'command': command,
        'user_id': user_id,
        'awaiting_input': True
    }
    
    cancel_callback_id = f"cancel_{uuid.uuid4().hex[:8]}"
    CALLBACK_DATA[cancel_callback_id] = {
        'command': 'cancel',
        'session_id': session_id,
        'user_id': user_id
    }
    
    keyboard = create_inline_keyboard([
        {
            'text': f"{EMOJI['error']} Cancel",
            'callback_data': cancel_callback_id
        }
    ])
    
    send_message(chat_id, message, reply_markup=keyboard)

def handle_example_execution(chat_id, user, command, args):
    """
    Handle execution of an example command from the help menu.
    
    Args:
        chat_id (int): Chat ID
        user (dict): User information
        command (str): The command to execute
        args (list): Arguments for the command
    """
    text = f"{command} {' '.join(args)}"
    
    handle_mathematical_command(chat_id, user, text)

def handle_callback_query(update):
    """
    Handle callback queries from inline keyboard buttons.
    
    Args:
        update (dict): The update containing a callback query
    """
    callback_query = update.get('callback_query', {})
    callback_query_id = callback_query.get('id')
    callback_data = callback_query.get('data')
    user = callback_query.get('from', {})
    chat_id = callback_query.get('message', {}).get('chat', {}).get('id')
    message_id = callback_query.get('message', {}).get('message_id')
    
    if not callback_data or not chat_id:
        return
    
    user_id = user.get('id')
    full_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
    logger.info(f"Received callback from {user_id} ({full_name}): {callback_data}")
    
    callback_info = CALLBACK_DATA.get(callback_data)
    
    if callback_info:
        # Process different types of callbacks
        command = callback_info.get('command')
        
        answer_callback_query(callback_query_id)
        
        if command == 'cancel':
            # User canceled an operation
            session_id = callback_info.get('session_id')
            if session_id in CALLBACK_DATA:
                del CALLBACK_DATA[session_id]
            
            edit_message_text(
                chat_id, 
                message_id,
                f"{EMOJI['error']} Operation canceled. Use /start to see main menu."
            )
            return
        
        if command == 'help':

            handle_help_command(chat_id, user)
            return
        
        if command == 'start':
            
            handle_start_command(chat_id, user)
            return
        
        if callback_data.startswith('func_'):
            handle_function_selection(chat_id, user, command)
            return
        
        
        if callback_data.startswith('example_'):
            args = callback_info.get('args', [])
            handle_example_execution(chat_id, user, command, args)
            return
    else:
        answer_callback_query(callback_query_id, "This button is no longer active", show_alert=True)

def process_update(update):
    """
    Process a single update from Telegram.
    
    Args:
        update (dict): The update to process
    """
    if 'callback_query' in update:
        handle_callback_query(update)
        return
    
    if 'message' in update:
        message = update['message']
        
        chat_id = message.get('chat', {}).get('id')
        user = message.get('from', {})
        
        
        if 'text' in message:
            text = message['text']
            
            if text.startswith('/'):
                command = text.split('@')[0].lower()  # Remove bot name if present
                
                if command == '/start':
                    handle_start_command(chat_id, user)
                elif command == '/help':
                    handle_help_command(chat_id, user)
                else:
                    send_message(chat_id, "Unknown command. Try /help for available commands.")
            else:
                handle_mathematical_command(chat_id, user, text)

def main():
    """
    Main function to start the bot.
    """
    try:
        response = requests.get(f"{API_URL}/getMe")
        result = response.json()
        
        if result.get('ok'):
            bot_info = result.get('result', {})
            logger.info(f"Bot activated: @{bot_info.get('username')} ({bot_info.get('first_name')})")
            
            # Start processing updates
            logger.info("Starting to process updates...")
            process_updates()
            
        else:
            logger.error(f"Failed to initialize bot: {result.get('description')}")
            
    except Exception as e:
        logger.error(f"Critical error starting the bot: {e}")
        raise

if __name__ == "__main__":
    main()
