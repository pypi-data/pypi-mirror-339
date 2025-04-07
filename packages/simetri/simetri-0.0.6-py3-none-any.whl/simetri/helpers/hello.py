import tempfile
import os

import simetri.graphics as sg

def hello():
    """Hello world function."""
    # Open the default web browser to the Simetri website

    canvas = sg.Canvas()

    canvas.text("Helow from simetri.graphics", (0, 0), font_size=20)


    with tempfile.TemporaryDirectory(
            ignore_cleanup_errors=True, delete=True
        ) as tmpdirname:
        file_name = next(tempfile._get_candidate_names())
        file_path = os.path.join(tmpdirname, file_name + ".png")
        print(file_path)
        canvas.save(file_path, show=True, print_output=False)
