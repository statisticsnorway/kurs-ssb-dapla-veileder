import os
from IPython.core.display import HTML, Markdown

def search_text_in_notes(keyword, root_dir, ignore=""):
    result = []
    
    # walk the root dir
    for root, dirs, files in os.walk(root_dir, onerror=None):
        # iterate over the files in the current dir
        for filename in files:
            if (ignore=="") or (not str(filename).endswith(ignore)): 
                # build the file path
                file_path = os.path.join(root, filename)
                try:
                    # open the file for reading
                    with open(file_path, "rb") as f:
                        # read the file line by line
                        for line in f:
                            try:
                                # try to decode the contents to utf-8
                                line = line.decode("utf-8")
                            # decoding failed, skip the line
                            except ValueError:
                                continue
                            # if the keyword exists on the current line create a HTML-objekt with a link
                            if keyword in line:  
                                result.append(Markdown(f"""<a href="{file_path}">{file_path}</a><br>{line}"""))
                                # no need to iterate over the rest of the file
                                break
                # ignore read and permission errors
                except (IOError, OSError):
                    pass
    return result
