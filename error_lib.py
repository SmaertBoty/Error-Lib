import minescript as m
import sys

global signature
signature = "[Error Lib]"
data_pointer = "Error-Lib"

def load(file):
    from pathlib import Path
    import json
    DIRPATH = (Path(__file__).parent / "errorlib")
    if not DIRPATH.exists():
        (Path(__file__).parent / "errorlib").mkdir()
    FILEPATH = (Path(__file__).parent / "errorlib" / f"{file}.json")
    if FILEPATH.exists():
        return json.loads(FILEPATH.read_text())
    return {}

def save(file,data):
    from pathlib import Path
    import json
    FILEPATH = (Path(__file__).parent / "errorlib" / f"{file}.json")
    FILEPATH.write_text(json.dumps(data, indent=2))

def command(cmd,args):
    from pathlib import Path
    if cmd == "download":
        import requests
        import ast
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Fetching download sources","color":"yellow"}])
        download_sources = ast.literal_eval(requests.get(f"https://raw.githubusercontent.com/SmaertBoty/{data_pointer}/refs/heads/main/download_sources.txt").text)
        if args[0] != "mappings":
            try:
                mappings = load("mappings")
            except:
                m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Mappings not found!","color":"yellow"}," ",{"text":"[Download mappings]","color":"green","click_event":{"action":"suggest_command","command":f"\\error_lib download mappings"}}])
                return None
        else:
            try:
                m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Downloading mappings","color":"yellow"}])
                mappings = ast.literal_eval(requests.get(f"https://raw.githubusercontent.com/SmaertBoty/{data_pointer}/refs/heads/main/download_sources.txt").text)
                save("mappings",mappings)
            except Exception as e:
                m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Could not download ","color":"yellow"},{"text":"mappings","color":"aqua"},{"text":". Check logs for more info","color":"yellow"}])  
                m.log(e)
            m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Succesfully downloaded mappings","color":"yellow"}])
            return None
        for i in download_sources:
            if i[0] == args[0]:
                for j in mappings:
                    if j[0] == args[0]:
                        args[0] = j[1]
                try:
                    if args[1] == "True":
                        args[1] = True
                    else:
                        args[1] = False
                except:
                    args.append(False)
                m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Downloading ","color":"yellow"},{"text":f"{i[0]}","color":"aqua"}])
                try:
                    file = requests.get(i[1])
                except Exception as e:
                    m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Could not download ","color":"yellow"},{"text":f"{i[0]}","color":"aqua"},{"text":". Check logs for more info","color":"yellow"}])
                    m.log("[Error Lib] " + str(e))
                    return False
                path = Path(__file__).resolve().parent / str(i[0]+".py")
                if not path.exists():
                    with open(path, "wb") as f:
                        f.write(file.content)
                    m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Succesfully downloaded ","color":"yellow"},{"text":f"{i[0]}","color":"aqua"}])
                    return True
                elif not args[1]:
                    m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"File already exists!","color":"yellow"},{"text":" ","color":"gold"},{"text":"[Download anyway]","color":"green","click_event":{"action":"suggest_command","command":f"\\error_lib download {i[0]} True"}}])
                    return False
                elif args[1]:
                    with open(path, "wb") as f:
                        f.write(file.content)
                    m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Succesfully downloaded ","color":"yellow"},{"text":f"{i[0]}","color":"aqua"}])
                    return True
                m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Could not download ","color":"yellow"},{"text":f"{i[0]}","color":"aqua"}])
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":f"File not found! In most cases this means that the database does not contain ","color":"yellow"},{"text":f"{args[0]}","color":"aqua"},{"text":". Please contact ","color":"yellow"},{"text":"@SmartBoty","color":"light_purple"},{"text":" trough ","color":"yellow"},{"text":"discord","color":"aqua","click_event":{"action":"open_url","url":"https://discord.com/channels/930220988472389713/930227498145443840"}}])

    if cmd == "delete":
        path = Path(__file__).resolve().parent / str(args[0]+".py")
        try:
            if args[1] == "True":
                args[1] = True
        except:
            args.append(False)
        if path.exists():
            try:
                path.unlink()
                m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"File ","color":"yellow"},{"text":f"{args[0]}","color":"aqua"},{"text":" succesfully deleted!","color":"yellow"}])
            except Exception as e:
                m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"File ","color":"yellow"},{"text":f"{args[0]}","color":"aqua"},{"text":" could not be deleted! Check logs for more info","color":"yellow"}])
                m.log(e)
        elif not args[1]:
            m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"File does not exist! ","color":"yellow"},{"text":"[Try anyway]","color":"green","click_event":{"action":"suggest_command","command":f"\\error_lib delete {args[0]} True"}}])
        else:
            try:
                path.unlink()
                m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"File ","color":"yellow"},{"text":f"{args[0]}","color":"aqua"},{"text":" succesfully deleted!","color":"yellow"}])
            except Exception as e:
                m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"File ","color":"yellow"},{"text":f"{args[0]}","color":"aqua"},{"text":" could not be deleted! Check logs for more info","color":"yellow"}])
                m.log(e)

def resolve(issue,value=None):
    m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Error","color":"red"},{"text":" detected!","color":"yellow"}])
    if issue == "ModuleNotFoundError":
        mappings = load("mappings")
        cause = value
        for i in mappings:
            if i[0] == value:
                cause = i[1]
        cause = cause + " is not downloaded!"
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Cause:","color":"yellow"}," ",{"text":f"{cause}","color":"red"}])
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"[Quick fix]","color":"green","click_event":{"action":"suggest_command","command":f"\\error_lib download {value}"}}])
    elif issue == "unterminated string":
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Cause:","color":"yellow"}," ",{"text":"Missing quote","color":"red"}])
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Fix: ","color":"green"},{"text":f"Make sure that all quotes ( \" and ' ) are closed at line {value}. Note: \" and ' cannot be combined","color":"yellow"}])
    elif issue == "undefined variable":
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Cause:","color":"yellow"}," ",{"text":"Undefined object","color":"red"}])
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Fix: ","color":"green"},{"text":f"Make sure that '{value}' is a valid/imported function or object for the operation","color":"yellow"}])
    elif issue == "non global variable":
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Cause:","color":"yellow"}," ",{"text":"Undefined variable in function","color":"red"}])
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Fix: ","color":"green"},{"text":f"Make sure that you make '{value}' global before the function ('global {value}')","color":"yellow"}])
    elif issue == "non string joining":
        value = "integer" if value == "int" else value
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Cause:","color":"yellow"}," ",{"text":f"Can't join string and {value}","color":"red"}])
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Fix: ","color":"green"},{"text":f"Make sure that you are joining two strings together ('str()')","color":"yellow"}])
    elif issue == "non number operation":
        value = "string" if value == "str" else value
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Cause:","color":"yellow"}," ",{"text":f"Can't do math operations with {value}","color":"red"}])
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Fix: ","color":"green"},{"text":f"Make sure that you are using two numbers ('int()' or 'float()')","color":"yellow"}])
    elif issue == "uncallable variable":
        value = "string" if value == "str" else value
        value = "integer" if value == "int" else value
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Cause:","color":"yellow"}," ",{"text":f"Cannot call a variable","color":"red"}])
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Fix: ","color":"green"},{"text":f"Make sure that you are only calling functions '()' or that the object you are trying to call is not {value}","color":"yellow"}])
    elif issue == "cant iterate None":
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Cause:","color":"yellow"}," ",{"text":f"Cannot iterate None","color":"red"}])
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Fix: ","color":"green"},{"text":f"Make sure that the value of it is not None       ('if not None:')","color":"yellow"}])
    elif issue == "invalid for int":
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Cause:","color":"yellow"}," ",{"text":f"Can't transform {value} to integer","color":"red"}])
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Fix: ","color":"green"},{"text":f"Make sure that '{value}' can be turned into an integer","color":"yellow"}])
    elif issue == "wrong amount of values to unpack":
        value2 = ""
        if isinstance(value,list):
            value2 = f"({value[1]})"
            value = value[0]
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Cause:","color":"yellow"}," ",{"text":f"Wrong amount of values provided","color":"red"}])
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Fix: ","color":"green"},{"text":f"Make sure that the list/tuple has exactly as many values ({value}), as you are trying to get {value2}","color":"yellow"}])
    elif issue == "attribute error":
        value[0] = "string" if value[0] == "str" else value[0]
        value[0] = "integer" if value[0] == "int" else value[0]
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Cause:","color":"yellow"}," ",{"text":f"'{value[0]}' does not have an attribute called '{value[1]}'","color":"red"}])
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Fix: ","color":"green"},{"text":f"Make sure that you are using '{value[1]}' with the correct object, not '{value[0]}'","color":"yellow"}])
    elif issue == "import error":
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Cause:","color":"yellow"}," ",{"text":f"'{value[0]}' does not have a function called '{value[1]}'","color":"red"}])
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Fix: ","color":"green"},{"text":f"Make sure that the documentation for '{value[0]}' states that '{value[1]}' exists, as a function or class. Alternatively, try updating it to the latest version:","color":"yellow"}])
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"[Quick fix]","color":"green","click_event":{"action":"suggest_command","command":f"\\error_lib download {value[0]}"}}])

def begin_chat_listener():
    with m.EventQueue() as chat_queue:
        chat_queue.register_chat_listener()
        while True:
            event = chat_queue.get()
            if event.type == m.EventType.CHAT:
                string = event.message
                if string.startswith("ModuleNotFoundError: No module named '"):
                    resolve("ModuleNotFoundError",string.replace("ModuleNotFoundError: No module named '","").replace("'",""))
                if string.startswith("SyntaxError: unterminated string literal ("):
                    resolve("unterminated string",string.replace("SyntaxError: unterminated string literal (detected at line ","").replace(")",""))
                if string.startswith("NameError: name '"):
                    resolve("undefined variable",string.replace("NameError: name '","").replace("' is not defined",""))
                if string.startswith("UnboundLocalError: cannot access local variable '"):
                    resolve("non global variable",string.replace("UnboundLocalError: cannot access local variable '","").replace("' where it is not associated with a value",""))
                if string.startswith('TypeError: can only concatenate str (not "'):
                    resolve("non string joining",string.replace('TypeError: can only concatenate str (not "',"").replace('") to str',""))
                if string.startswith("TypeError: unsupported operand type(s) for +: 'int' and '"):
                    resolve("non number operation",string.replace("TypeError: unsupported operand type(s) for +: 'int' and '","").replace("'",""))
                if string.startswith("TypeError: unsupported operand type(s) for +: 'float' and '"):
                    resolve("non number operation",string.replace("TypeError: unsupported operand type(s) for +: 'float' and '","").replace("'",""))
                if string.startswith("TypeError: '"):
                    if not string.startswith("TypeError: 'NoneType'"):
                        resolve("uncallable variable",string.replace("TypeError: '","").replace("' object is not callable",""))
                    else:
                        resolve("cant iterate None")
                if string.startswith("ValueError: invalid literal for int() with base 10: '"):
                    resolve("invalid for int",string.replace("ValueError: invalid literal for int() with base 10: '","").replace("'",""))
                if string.startswith("ValueError: too many values to unpack (expected "):
                    resolve("wrong amount of values to unpack",string.replace("ValueError: too many values to unpack (expected ","").replace(")",""))
                if string.startswith("ValueError: not enough values to unpack (expected "):
                    import re
                    expected, got = map(int, re.findall(r'\d+', "(expected 4, got 3)"))
                    resolve("wrong amount of values to unpack",[expected,got])
                if string.startswith("AttributeError: '"):
                    import re
                    words = re.findall(r"'([^']+)'", string)
                    obj, attribute = words
                    resolve("attribute error",[obj,attribute])
                if string.startswith("ImportError: cannot import name '"):
                    import re
                    words = re.findall(r"'([^']+)'", string)
                    func, module = words
                    resolve("import error",[module,func])

if __name__ == "__main__":
    args = sys.argv
    try:
        a = args[1]
    except:
        a = None
    if a is not None:
        dummy, cmd, *arguments = args
        command(cmd, arguments)
    else:
        from time import sleep
        jobs = m.job_info()
        all_jobs = []
        first = True
        for i in jobs:
            if i.command[0] == "error_lib":
                all_jobs.append(i.job_id)
        if all_jobs != [] and len(all_jobs) > 1:
            m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Closing previous instance...","color":"yellow"}])
            m.execute(f"\killjob {all_jobs[0]}")
            sleep(0.5)
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Warming up...","color":"yellow"}])
        import requests
        import ast
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Downloading mappings","color":"yellow"}])
        mappings = ast.literal_eval(requests.get(f"https://raw.githubusercontent.com/SmaertBoty/{data_pointer}/refs/heads/main/mappings.txt").text)
        save("mappings",mappings)
        m.echo_json([{"text":f"{signature}","color":"gold"}," ",{"text":"Succesfully loaded ErrorLib!","color":"yellow"}])
        begin_chat_listener()