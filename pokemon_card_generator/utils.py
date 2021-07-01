def get_file_contents(filename):
    """Given a filename,
    return the contents of that file
    """
    try:
        with open(filename, "r") as f:
            # It's assumed our file contains a single line,
            # with our API key
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)
