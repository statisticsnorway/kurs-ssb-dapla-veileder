import os
from IPython.core.display import display, HTML, Markdown
from IPython.display import clear_output
from ipywidgets import interact, widgets

def search_text_in_notes(keyword, root_dir, ignore_dirs, ignore_files, debug_output=False):
    result = []
    if debug_output: display(">>>> Start debug <<<<<")

    # walk the root dir
    for root, dirs, files in os.walk(root_dir, onerror=None):
        if any(x in root for x in ignore_dirs):
            if debug_output: display("Ignoring folder ["+root+"]")
            continue
                
        if debug_output: display("Searching folder ["+root+"]")

        # iterate over the files in the current dir
        for filename in files:
            # build the file path
            file_path = os.path.join(root, filename)

            if any(y in filename for y in ignore_files): 
                if debug_output: display("Ignoring file ["+file_path+"]")
                continue

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

    if debug_output: display(">>>> End debug <<<<<")
    return result


def handle_submit(sender):
    with result_field:
        result_field.clear_output()
        result = search_text_in_notes(sender.value,root_dir,ignore_folders, ignore_files, False)
        if not result:
            display(f"Vi finner dessverre ingen resultater når du søker etter {sender.value}")
        else:
            for file in result:
                display(file)

                
root_dir = "."
ignore_files = ["-checkpoint.py"]
ignore_folders = [".ipynb_checkpoints"]  

input_field = widgets.Text(
    value='',
    description='Søk i veilder:',
    disabled=False
)
result_field = widgets.Output(layout={'border': '1px solid black'})
display(input_field, result_field)

input_field.on_submit(handle_submit)