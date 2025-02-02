import pygame
import cv2
import numpy as np
import os
import time
from gpiozero import Button, LED
from pipeline.braille_converter import convert_braille_to_english
from pipeline.image_converter import convert_image_to_braille
from pipeline.generate_voice_eleven import text_to_speech

"""
    sounds:
    - select_mode
    - read_mode
    - learn_mode
    - press_to_start
    - continue
    - letter
    - press_to_capture
"""

IMG_PATH = "captured.jpg"
OUT_FILE = "voice.mp3"

pygame.mixer.init()

def play(name, custom = False):
    if not custom:
        name = os.path.join("samples/", name + ".mp3")
    if os.path.exists(name):
        sound = pygame.mixer.Sound(os.path.join(os.getcwd(), name))
        player = sound.play()
        while player.get_busy():
            pygame.time.wait(100)

def letter(l):
    path = os.path.join(os.getcwd(), "samples/", l.upper() + ".wav")
    if os.path.exists(path):
        play(path, True)

def get_mode(read : Button, learn : Button):
    if (read.is_pressed and learn.is_pressed):
        return None
    if (read.is_pressed or learn.is_pressed):
        if read.is_pressed:
            return "read_mode"
        else:
            return "learn_mode"
    return None

btn = Button(14)
flash = LED(23)

read_btn = Button(18)
learn_btn = Button(15)

while True:
    play("select_mode")
    play("press_to_start")

    mode = get_mode(read_btn, learn_btn)
    play(mode)

    while not btn.is_pressed:
        newmode = get_mode(read_btn, learn_btn)
        if mode != newmode:
            if newmode != None:
                mode = newmode
                play(mode)

    cam = cv2.VideoCapture(0)

    play("press_to_capture")
    btn.wait_for_press()

    flash.on()
    time.sleep(1)
    flash.off()
    time.sleep(0.100)
    flash.on()
    time.sleep(0.500)
    print("reading")
    _, image = cam.read()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = image[240-200:240+200, 320-300:320+300]
    image = cv2.addWeighted(image, 1, np.zeros(image.shape, image.dtype), 0, 7)
    cv2.imwrite(IMG_PATH, image)
    cam.release()
    flash.off()

    print("braille")
    try:
        braille_text = convert_image_to_braille(IMG_PATH)
    except Exception as e:
        print(e)
        continue
    print(braille_text)
    print("english")
    try:
        english_text = convert_braille_to_english(braille_text)
    except Exception as e:
        print(e)
        continue
    print(english_text)

    print("read")
    text_to_speech(english_text, output_file=OUT_FILE, voice="cgSgspJ2msm6clMCkdW9")
    play(OUT_FILE, True)

    if mode == "learn_mode":
        play("press_to_start")
        btn.wait_for_press()

        for l in english_text:
            play("letter")
            letter(l)
            time.sleep(2)
            play("continue")
            btn.wait_for_press()
    time.sleep(3)
