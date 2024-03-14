#!/bin/env python3
from flyer_maker import social_media, stable_diffusion 
from flyer_maker.flyer_maker import make_flyer_from_image
from flyer_maker.flyer import FlyerData
import time
import threading
import os
import signal
import sys

def signal_handler(sig, frame):
    """
    Kill all threads when Ctrl+C is pressed.
    """
    global response_received_event
    response_received_event.set()
    exit()

def progress_feedback(response_received_event, timeout):
    print("Requesting images to stable diffussion", end="")
    steps = timeout
    for _ in range(steps):
        if (response_received_event.is_set()):
            print("Done")
            return
        time.sleep(timeout/steps)
        print(".", end="", flush=True),
    print("Timeout")

def main(metro_path: str,
         output_dir: str,
         timeout: int):

    feedback_thread = threading.Thread(
            target=progress_feedback,
            args=(response_received_event,timeout))
    feedback_thread.start()

    makespacemadrid_data = FlyerData(
                title = "MakeSpace - AI Lab #2",
                subtitle = "Python con IAs autoalojadas",
                date = "Día 20 de Marzo",
                timeframe = "19:00-21:00",
                place= "Calle Ruiz Palacios 7",
                metro = "Tetuán")
    
    images = stable_diffusion.get_images(
            url="https://1111.makespacemadrid.org",
            prompt="hackerspace cyberpunk city steampunk",
            img_size=social_media.Sizes["Facebook"]['Landscape'],
            batch_size=1,
            timeout=timeout)

    response_received_event.set()
    feedback_thread.join()
    
    for i, base in enumerate(images):
        flyer = make_flyer_from_image(
                    flyer_data=makespacemadrid_data,
                    metro_path=metro_path,
                    base=base)
        
        flyer.save(f"{output_dir}/out_{i}.png", "PNG")
        flyer.show()

response_received_event = threading.Event() 
response_received_event.clear()
signal.signal(signal.SIGINT, signal_handler)
if __name__ == "__main__":
    pwd = os.path.dirname(os.path.realpath(__file__))
    metro_logo = f"{pwd}/data/logo/Logotipo-Metro_Principal_RGB_0.png"
    output_dir = "./"
    timeout = 170
    main(metro_path=metro_logo,
         output_dir=output_dir,
         timeout=timeout)
