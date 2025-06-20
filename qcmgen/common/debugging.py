import os
import re
import debugpy


def handle_debugging():
    debug = os.getenv("debug", None)
    if debug:
        debug_port = 9265
        if re.match("[0-9]+", debug):
            _dp = int(debug)
            if _dp == 0:
                return
            if _dp > 100:
                debug_port = _dp
        debugpy.listen(("0.0.0.0", debug_port))
        print(f"debug is on , please attach a debugger on port {debug_port}")
        debugpy.wait_for_client()
