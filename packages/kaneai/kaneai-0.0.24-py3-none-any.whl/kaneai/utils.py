import json
import os
import re
import base64
import time
from pathlib import Path
from urllib.parse import urlparse
import requests
from typing import Dict
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from kaneai.heal import Heal
from .config import BROWSER
from .webdriver_utils import conditions_met, lambda_hooks
from datetime import datetime

# Network monitoring configuration
LAST_ACTION_TIMESTAMP = 0
MAX_NETWORK_WAIT = 10
WAIT_BUFFER = 0.2
NETWORK_REQUEST_EVENTS = ["Network.requestWillBeSent"]
NETWORK_RESPONSE_EVENTS = ["Network.responseReceived", "Network.BlockedReason", "Network.loadingFailed"]
NETWORK_WAIT_FOR_ALL_ACTIONS = False

def set_network_wait_for_all_actions(network_wait_for_all_actions: bool):
    global NETWORK_WAIT_FOR_ALL_ACTIONS
    NETWORK_WAIT_FOR_ALL_ACTIONS = network_wait_for_all_actions

def get_network_wait_for_all_actions() -> bool:
    global NETWORK_WAIT_FOR_ALL_ACTIONS
    return NETWORK_WAIT_FOR_ALL_ACTIONS

def set_last_action_timestamp(timestamp: int):
    global LAST_ACTION_TIMESTAMP
    LAST_ACTION_TIMESTAMP = timestamp

def get_last_action_timestamp() -> int:
    global LAST_ACTION_TIMESTAMP
    return LAST_ACTION_TIMESTAMP

def update_max_network_wait(max_network_wait: float):
    global MAX_NETWORK_WAIT
    MAX_NETWORK_WAIT = max_network_wait

def update_wait_buffer(wait_buffer: float):
    global WAIT_BUFFER
    WAIT_BUFFER = wait_buffer

def process_browser_logs_for_network_events(driver: webdriver.Chrome) -> list:
    """
        Return only logs which have a method that are in (NETWORK_RESPONSE_EVENTS or NETWORK_REQUEST_EVENTS)
        since we're interested in the network events specifically.

        args:
            driver: webdriver.Chrome // Webdriver instance

        returns:
            list // List of network events
    """
    try:
        logs = driver.get_log("performance")
    except Exception as e:
        print(f"[Smart Wait] Error in process_browser_logs_for_network_events: {str(e)}")
        logs = []
    network_events = []
    for entry in logs:
        log = json.loads(entry["message"])["message"]
        if (log["method"] in NETWORK_REQUEST_EVENTS or log["method"] in NETWORK_RESPONSE_EVENTS) and log["params"].get("type") not in ["Other", "Document", "Ping"]:
            network_events.append({"timestamp": entry["timestamp"], "method": log["method"], "requestId": log["params"].get("requestId", ""), "type": log["params"].get("type", "")})
    return network_events

def smart_network_wait(driver: webdriver.Chrome, start_timestamp: int):
    """
        Wait for all network requests to finish.
        This is a blocking call.

        args:
            driver: webdriver.Chrome // Webdriver instance
            start_timestamp: int // Timestamp just before last action was performed
            max_network_wait: int = 10 // Maximum timeout for the wait
            wait_buffer: int = 200 // Buffer to wait for the network requests to finish
    """
    try:
        if BROWSER != "chrome":
            print(f"[Smart Wait] Not supported for {BROWSER}")
            return
        
        start_time = time.time() * 1000
        request_map = {}
        most_recent_network_timestamp = time.time() * 1000

        while True:
            events = process_browser_logs_for_network_events(driver=driver)  # No await needed
            for event in events:
                if event["method"] in NETWORK_REQUEST_EVENTS and event["timestamp"] >= start_timestamp:
                    request_map[event["requestId"]] = {"timestamp": event["timestamp"], "type": event["type"]}
                elif event["method"] in NETWORK_RESPONSE_EVENTS:  # Fixed logical error here
                    if event["requestId"] in request_map:
                        most_recent_network_timestamp = event["timestamp"]
                        del request_map[event["requestId"]]

            if len(request_map) == 0 and (time.time() * 1000 - most_recent_network_timestamp >= WAIT_BUFFER * 1000):
                print(f"[Smart Wait] Waited for: {time.time() * 1000 - start_time} ms")
                return

            if time.time() * 1000 - start_timestamp > MAX_NETWORK_WAIT * 1000:
                print(f"[Smart Wait] Waited for: {time.time() * 1000 - start_time} ms")
                return
    
    except Exception as e:
        print(f"[Smart Wait] Error in smart_network_wait: {str(e)}")

def get_download_folder():
    """Returns the system's Downloads folder path and ensures it exists."""
    if os.name == "nt":  # Windows
        downloads_path = Path(os.path.join(os.environ["USERPROFILE"], "Downloads"))
    else:  # macOS and Linux
        downloads_path = Path(os.path.expanduser("~/Downloads"))

    # Ensure the folder exists
    downloads_path.mkdir(parents=True, exist_ok=True)

    return downloads_path

def download_files(media_list):
    """Downloads files from the given list to the system's Downloads folder."""
    download_folder = get_download_folder()
    
    for media in media_list:
        file_url = f"https://{media['media_url']}"
        file_name = media['name']
        file_path = download_folder / file_name
        
        try:
            response = requests.get(file_url, stream=True)
            response.raise_for_status()
            
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            
            print(f"Downloaded: {file_name} -> {file_path}")
        except requests.RequestException as e:
            print(f"Failed to download {file_name}: {e}")

def get_downloads_file_path(file_name):
    """Returns the full path to a file in the system's Downloads folder."""
    if file_name is None:
        raise ValueError("file_name cannot be None")
    
    if os.name == "nt":  # Windows
        downloads_path = Path(os.path.join(os.environ["USERPROFILE"], "Downloads"))
    else:  # macOS and Linux
        downloads_path = Path(os.path.expanduser("~/Downloads"))

    return str(downloads_path / file_name)

def get_prev_operation_wait_time(operation_index: str) -> float:
    """Get the wait time between previous operation end and current operation start."""
    wait_time = 0
    try:
        from .config import get_metadata
        metadata = get_metadata()
        prev_op_index = str(int(operation_index) - 1)
        prev_op_end_time = metadata.get(prev_op_index, {}).get('operation_end', '')
        curr_op_start_time = metadata[operation_index].get('operation_start', '')
        
        if prev_op_end_time and curr_op_start_time:
            # Define the datetime format
            format = "%Y-%m-%d %H:%M:%S.%f"
            
            # Convert strings to datetime objects
            datetime1 = datetime.strptime(prev_op_end_time, format)
            datetime2 = datetime.strptime(curr_op_start_time, format)
            
            # Calculate the difference in seconds
            wait_time = (datetime2 - datetime1).total_seconds()
    except Exception as e:
        print(f"Error getting prev operation wait time: {e}")
    
    return wait_time

def get_operation_wait_time(operation_index: str, default_wait_time: float = 10, max_additional_wait_time: float = 120) -> float:
    """Calculate total wait time for an operation including explicit wait and additional wait based on previous operation."""
    wait_time: float = 0
    try:
        from .config import get_metadata
        metadata = get_metadata()
        op_data = metadata.get(operation_index, {})
        explicit_wait = float(op_data.get('explicit_wait', 0))
        wait_time = explicit_wait
        
        # Get additional wait time depending on prev operation end time
        additional_wait = default_wait_time
        prev_op_wait_time = get_prev_operation_wait_time(operation_index)
        if prev_op_wait_time > additional_wait:
            additional_wait = prev_op_wait_time
            
        # Limit additional wait time
        additional_wait = min(additional_wait, max_additional_wait_time)
        wait_time += additional_wait
    except Exception as e:
        print(f"Error getting wait time: {e}")
        wait_time += default_wait_time
    
    return wait_time

def access_value(mapping, path):
    """Access a nested value in a mapping using a dot-notation path."""
    try:
        keys = path.split('.')
        value = mapping
        for key in keys:
            while '[' in key and ']' in key:
                base_key, index = key.split('[', 1)
                index = int(index.split(']')[0])
                value = value[base_key] if base_key else value
                value = value[index]
                key = key[key.index(']') + 1:]
            if key:
                value = value[key]

        return str(value)
    except (KeyError, IndexError, ValueError, TypeError):
        return path
    
def get_variable_value(value: str, variables: dict) -> str:
    """Replace variable placeholders in a string with their values."""
    matches = re.findall(r'\{\{(.*?)\}\}', value)
    new_value = value
    if matches:
        for match in matches:
            new_value = new_value.replace("{{"+match+"}}", access_value(variables, match))
    return new_value

def canvas_autoheal_wrapper(operation_index, driver):
    response = Heal(operation_index, driver).coordinate(operation_index=operation_index)
    response_data = response.json()
    x = response_data["coordinate"][0]
    y = response_data["coordinate"][1]
    return x,y

def perform_assertion(operand1, operator, operand2, operation_index, intent, driver):
    """Perform assertion with hard assertion support and variable handling."""
    from .config import get_metadata
    metadata = get_metadata()
    operation_metadata = metadata.get(str(operation_index), {})
    hard_assertion = operation_metadata.get('hard_assertion', False)
    print(f"Performing assertion: '{hard_assertion}'")
    
    # Handle variable substitution from sub_instruction_obj
    sub_instruction_obj = operation_metadata.get('sub_instruction_obj', {})
    if isinstance(sub_instruction_obj, str):
        sub_instruction_obj = json.loads(sub_instruction_obj)
    
    is_string_to_float = operation_metadata.get('string_to_float', False)
    variables = metadata.get('variables', {})
    
    if isinstance(sub_instruction_obj, dict) and 'json' not in operator:
        if 'variable' in sub_instruction_obj:
            if 'operand1' in sub_instruction_obj['variable']:
                new_value = get_variable_value(sub_instruction_obj['variable']['operand1'], variables)
                if is_string_to_float:
                    operand1 = string_to_float(new_value)
                else:
                    operand1 = new_value.lower()
            if 'operand2' in sub_instruction_obj['variable']:
                new_value = get_variable_value(sub_instruction_obj['variable']['operand2'], variables)
                if is_string_to_float:
                    operand2 = string_to_float(new_value)
                else:
                    operand2 = new_value.lower()

    is_replace = operation_metadata.get('is_replace', False)
    if is_replace:
        operand2 = operation_metadata.get('expected_value')
        operator_name = operation_metadata.get("operator")
        intent = f"assert if {operand1} is {operator_name} {operand2}"

    if is_string_to_float:
        operand1 = string_to_float(operand1)
        operand2 = string_to_float(operand2)

    # Handle JSON-specific operators first.
    json_ops = {
        "json_key_exists",
        "json_keys_count",
        "json_array_length",
        "json_array_contains",
        "json_value_equals"
    }
    if operator in json_ops:
        if operator == "json_key_exists":
            return operand2 in operand1.keys()
        elif operator == "json_keys_count":
            return len(operand1.keys()) == int(operand2)
        elif operator == "json_array_length":
            return len(operand1) == int(operand2)
        elif operator == "json_array_contains":
            # Match original behavior: return True if found, else None.
            return True if operand2 in operand1 else None
        elif operator == "json_value_equals":
            return operand1 == operand2

    # Map standard operators to their corresponding assertion checks.
    assertion_map = {
        "==": lambda a, b: (a == b, f"Expected {a} to equal {b}"),
        "!=": lambda a, b: (a != b, f"Expected {a} to not equal {b}"),
        "true": lambda a, b: (bool(a) is True, f"Expected true, got {a}"),
        "false": lambda a, b: (bool(a) is False, f"Expected false, got {a}"),
        "is_null": lambda a, b: (a is None, "Expected operand to be None"),
        "not_null": lambda a, b: (a is not None, "Expected operand to be not None"),
        "contains": lambda a, b: (b in a, f"Expected {b} to be in {a}"),
        "not_contains": lambda a, b: (b not in a, f"Expected {b} to not be in {a}"),
        ">": lambda a, b: (a > b, f"Expected {a} to be greater than {b}"),
        "<": lambda a, b: (a < b, f"Expected {a} to be less than {b}"),
        ">=": lambda a, b: (a >= b, f"Expected {a} to be greater than or equal to {b}"),
        "<=": lambda a, b: (a <= b, f"Expected {a} to be less than or equal to {b}"),
        "length_equals": lambda a, b: (len(a) == b, f"Expected length of {a} to be {b}"),
        "type_equals": lambda a, b: (type(a) == b, f"Expected type of {a} to be {b}")
    }

    try:
        # Perform assertion if operator is recognized.
        if operator in assertion_map:
            condition, error_msg = assertion_map[operator](operand1, operand2)
            assert condition, error_msg
        # For unrecognized operators, assume the assertion passes.
        lambda_hooks(driver, f"Assertion passed: '{intent}'")
        return True
    except AssertionError as e:
        lambda_hooks(driver, f"Assertion failed: '{intent}' - {str(e)}")
        print(f"Assertion check failed: '{intent}' - {str(e)}")
        if hard_assertion:
            status = "failed"
            driver.execute_script(f"lambda-status={status}")
            raise e

def handle_unresolved_operations(operation_index, driver):
    """Handle unresolved operations using the Vision Agent"""
    from .config import get_metadata, operations_meta_data
    metadata = get_metadata()
    op_data = metadata.get(operation_index, {})
    
    if op_data.get('agent') == "Vision Agent":
        WebDriverWait(driver, 30, poll_frequency=3).until(conditions_met)
        healer = Heal(operation_index, driver)
        response = healer.resolve().json()
        response['locator'] = [response.get('xpath')]
        op_data.update(response)
        operations_meta_data.mark_operation_as_processed(op_data)
        
        # Write updated metadata to file
        with open('operations_meta_data.json', 'w') as f:
            json.dump(metadata, f, indent=4)

def string_to_float(input_string):
    """Convert string to float, handling various formats."""
    # If already a numeric type, return as is
    if isinstance(input_string, (float, int)):
        return input_string

    # Try direct conversion first, which handles scientific notation
    try:
        return float(input_string)
    except ValueError:
        # Handle negative sign
        is_negative = '-' in input_string

        # Filter to keep only digits and decimal point
        a = ''.join(filter(lambda x: x.isdigit() or x == '.', input_string))

        if a == "":
            return 0

        # Apply negative sign if needed
        result = float(a)
        if is_negative:
            result = -result

        return result

def heal_query(driver: webdriver, operation_index: str, outer_html: str) -> str:
    """Perform textual query healing."""
    response = Heal(operation_index, driver).textual_query(outer_html)
    response_dict = json.loads(response.text)

    if 'regex' in response_dict:
        regex_pattern = response_dict.get('regex')
        lambda_hooks(driver, "Regex Autohealed ")
        print("REGEX FROM AUTOMIND: ", regex_pattern)
        return regex_pattern
    elif 'error' in response_dict or response.status_code == 500:
        print("Error encountered, retrying...")
    else:
        print("Error in Getting Regex")
        
    return ""

def vision_query(driver: webdriver.Chrome, operation_index: str):
    """Perform vision query with proper error handling."""
    result = None
    from .config import get_metadata
    metadata = get_metadata()
    op_data = metadata.get(operation_index, {})

    try:
        wait_time = get_operation_wait_time(operation_index)
        if wait_time:
            print(f"Waiting '{wait_time} seconds' before performing vision query....")
            time.sleep(wait_time)

        if not NETWORK_WAIT_FOR_ALL_ACTIONS:
            smart_network_wait(driver=driver, start_timestamp=get_last_action_timestamp())
        set_last_action_timestamp(int(time.time() * 1000))

        response = Heal(operation_index, driver).vision_query()
        print("Vision Response: ", response.text)
        response = json.loads(response.text)
            
        if "error" in response:
            raise RuntimeError(f"Error in vision query: {response['error']}")

        result = response['vision_query']

        if op_data.get('string_to_float', False):
            result = string_to_float(result)

    except Exception as e:
        time.sleep(op_data.get('retries_delay', 0))
        if not op_data.get('optional_flag', False):
            raise e
        elif op_data.get('optional_flag', False):
            print(f"Failed to execute visual_query after. Error: {e}")
        print(f"Retrying visual_query due to Error: {str(e)[:50]}....")

    return result

def execute_js(user_js_code: str, driver: webdriver.Chrome) -> dict:
    """Execute JavaScript code with error handling."""
    try:
        lines_before_user_code = 2

        # Wrap the user's code to capture the return value and handle errors
        wrapped_js_code = f"(function() {{ try {{ return (function() {{ {user_js_code} }})(); }} catch(e) {{ e.stack = e.stack.replace(/<anonymous>:(\\d+):/g, function(match, lineNumber) {{ lineNumber = parseInt(lineNumber) - {lines_before_user_code}; return '<anonymous>:' + lineNumber + ':'; }}); return {{error: e.stack}}; }} }})();"

        if not NETWORK_WAIT_FOR_ALL_ACTIONS:
            smart_network_wait(driver=driver, start_timestamp=get_last_action_timestamp())
        set_last_action_timestamp(int(time.time() * 1000))

        client_response_js = driver.execute_script("return " + wrapped_js_code)

        if isinstance(client_response_js, dict) and 'error' in client_response_js:
            error_stack = client_response_js['error']
            lines = error_stack.split('\n')
            error_message = lines[0].strip()
            error_line = None

            # Extract the line number from the stack trace
            if len(lines) > 1:
                match = re.search(r'<anonymous>:(\d+):', lines[1])
                if match:
                    error_line = int(match.group(1))

            return {
                'value': '',
                'error': error_message,
                'line': error_line
            }
        else:
            # Successful execution
            try:
                json.dumps(client_response_js)
                if client_response_js is None or client_response_js == '':
                    client_response_js = "null"
                return {
                    'value': client_response_js,
                    'error': '',
                    'line': None
                }
            except (TypeError, OverflowError):
                return {
                    'value': str(client_response_js),
                    'error': '',
                    'line': None
                }
    except Exception as e:
        return {
            'value': '',
            'error': str(e),
            'line': None
        }

def execute_api(driver: webdriver.Chrome, method: str, url: str, headers: dict, body: str, params: dict, timeout: int, verify: bool) -> dict:
    """Execute API request with error handling."""
    parsed_url = urlparse(url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        return {'status': 400, 'message': 'Invalid URL'}
    if url.startswith(("wss://", "ws://")):
        return {'status': 400, 'message': 'Websockets not supported'}
    if any(value == 'text/event-stream' for value in headers.values()):
        return {'status': 400, 'message': 'SSE not supported'}

    proxies = {"http": "http://127.0.0.1:22000", "https": "http://127.0.0.1:22000"}
    request_methods = {
        "GET": requests.get,
        "POST": requests.post,
        "PUT": requests.put,
        "DELETE": requests.delete,
        "PATCH": requests.patch
    }

    start = time.time()

    if not NETWORK_WAIT_FOR_ALL_ACTIONS:
        smart_network_wait(driver=driver, start_timestamp=get_last_action_timestamp())
    set_last_action_timestamp(int(start * 1000))

    try:
        response = request_methods.get(method.upper(), lambda *args, **kwargs: None)(
            url, headers=headers, data=body, params=params, timeout=timeout, proxies=proxies, verify=verify
        )
        if response is None:
            return {'status': 400, 'message': 'Unsupported HTTP method'}
    except requests.RequestException as e:
        return {'status': 400, 'message': f"API request failed: {e}"}
    end = time.time()

    test_api_resp = {
        "status" : response.status_code,
        "headers" : response.headers,
        "cookies" : response.cookies,
        "body" : response.content,
        "time" : (end-start)*1000
    }
    
    checker=[]
    for key in test_api_resp:
        checker.append(key)
    for i in range(0,len(checker)):
        key=checker[i]
        try:
            json.dumps(test_api_resp[key])  # Try to serialize the value
        except (TypeError, ValueError):
            if isinstance(test_api_resp[key], bytes):
                try:
                    test_api_resp["response_body"] = json.loads(test_api_resp[key].decode('utf-8'))
                except (TypeError, ValueError):
                    test_api_resp["response_body"] = {"html":test_api_resp[key].decode('utf-8')}
                test_api_resp[key]=list(test_api_resp[key].decode('utf-8'))
            else:
                test_api_resp[key]=[{k:v} for k,v in test_api_resp[key].items()]
            for i in range(0,len(test_api_resp[key])):
                try:
                    json.dumps(test_api_resp[key][i])
                except (TypeError, ValueError):
                    test_api_resp[key][i] = str(test_api_resp[key][i])

    return test_api_resp

def replace_secrets(text: str) -> str:
    """Replace secrets using {{secrets.env.VAR}} format."""
    matches = re.findall(r'\{\{(.*?)\}\}', text)
    for match in matches:
        keys = match.split('.')
        if len(keys) == 3 and keys[0] == 'secrets':
            secret_value = os.getenv(keys[2], '')
            text = text.replace(f"{{{{{match}}}}}", secret_value)
    return text

def replace_secrets_in_dict(d: Dict[str, str]) -> Dict[str, str]:
    """Replace secrets in dictionary values."""
    new_dict = {}
    for k, v in d.items():
        replaced_key = replace_secrets(k)
        replaced_value = replace_secrets(v)
        if replaced_key == 'Authorization' and not replaced_value.startswith('Bearer'):
            username = replaced_value.split(':')[0]
            access_key = replaced_value.split(':')[1]
            replaced_value = f"Basic {base64.b64encode(f'{username}:{access_key}'.encode()).decode()}"
        new_dict[replaced_key] = replaced_value
    return new_dict

def replace_variables_in_script(script: str, variables: dict) -> str:
    """Replace variables in JavaScript code."""
    pattern = r'//Variables start.*?//Variables end\n*'
    find_variables = re.findall(pattern, script, re.DOTALL)
    updated_script = script
    if find_variables:
        updated_variables = ""
        for key, value in variables.items():
            if f"const {key} " in find_variables[0]:
                if isinstance(value, str):
                    value = json.dumps(value)
                    updated_variables += f"const {key} = {value};\n"
                else:
                    value = json.dumps(value)
                    updated_variables += f"const {key} = {value};\n"
        updated_script = script.replace(find_variables[0], f"//Variables start\n{updated_variables}//Variables end\n")
    return updated_script
