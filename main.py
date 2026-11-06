import cv2
import pyautogui
import numpy as np
import time
import serial

print("=" * 50)
print("CHROME DINO AUTOPLAYER")
print("LIGHT + DARK THEME DETECTION")
print("CACTUS + IMPROVED BIRD DETECTION")
print("FASTER SCREEN CAPTURE")
print("IMPROVED JUMP RESPONSE")
print("=" * 50)
print("Switch to Chrome Dino in 5 seconds.")
print("Press Q in the detection window to stop.")
print()

pyautogui.sleep(5)

# Crop settings
CROP_TOP = 550
CROP_BOTTOM = 800
CROP_LEFT = 0
CROP_RIGHT = 1200

# Ground position
GROUND_Y = 215

# Theme detection thresholds
LIGHT_THEME_LIMIT = 160
DARK_THEME_LIMIT = 95

# Noise removal
kernel = np.ones((3, 3), np.uint8)

current_theme = None
frame_count = 0

# Dino position and jump threshold
DINO_X = 200
JUMP_DISTANCE = 450

# Prevent unnecessary jumps
JUMP_COOLDOWN = 0.25
last_jump_time = 0.0
jump_latched = False

# Arduino connection
arduino = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)

print("Arduino Connected Successfully!")

# Bird detection limits
BIRD_MIN_WIDTH = 20
BIRD_MAX_WIDTH = 120
BIRD_MIN_HEIGHT = 10
BIRD_MAX_HEIGHT = 70
BIRD_MIN_ASPECT_RATIO = 1.0


while True:

    # 1. Capture ONLY game area (FASTER)
    screenshot = pyautogui.screenshot(
        region=(
            CROP_LEFT,
            CROP_TOP,
            CROP_RIGHT - CROP_LEFT,
            CROP_BOTTOM - CROP_TOP
        )
    )

    image = cv2.cvtColor(
        np.array(screenshot),
        cv2.COLOR_RGB2BGR
    )

    # Game area is already cropped
    game_area = image

    if game_area.size == 0:
        print("ERROR: Invalid crop coordinates.")
        break

    height, width = game_area.shape[:2]

    # 2. Convert to grayscale
    gray = cv2.cvtColor(
        game_area,
        cv2.COLOR_BGR2GRAY
    )

    # 3. Estimate background brightness
    corner_size = 30

    corners = np.concatenate([
        gray[5:corner_size, 5:corner_size].ravel(),
        gray[5:corner_size, width-corner_size:width-5].ravel(),
        gray[height-corner_size:height-5, 5:corner_size].ravel(),
        gray[height-corner_size:height-5,
             width-corner_size:width-5].ravel()
    ])

    background_brightness = float(np.median(corners))

    # 4. Detect theme
    if background_brightness >= LIGHT_THEME_LIMIT:
        current_theme = "LIGHT"

    elif background_brightness <= DARK_THEME_LIMIT:
        current_theme = "DARK"

    elif current_theme is None:
        current_theme = (
            "LIGHT" if background_brightness >= 127
            else "DARK"
        )

    # 5. Normalize image
    if current_theme == "DARK":
        detection_image = cv2.bitwise_not(gray)
    else:
        detection_image = gray.copy()

    # 6. Otsu thresholding
    _, mask = cv2.threshold(
        detection_image,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    # 7. Remove noise
    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        np.ones((2, 2), np.uint8)
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    # 8. Find contours
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    cactus_count = 0
    bird_count = 0

    nearest_distance = float("inf")
    nearest_obstacle = None

    # Ground reference line
    cv2.line(
        game_area,
        (0, GROUND_Y),
        (width - 1, GROUND_Y),
        (180, 180, 180),
        1
    )

    # 9. Classify objects
    for contour in contours:

        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)

        # Ignore Dino's starting area
        if x < 200:
            continue

        # Ignore small noise
        if area < 40:
            continue

        if w < 5 or w > 300:
            continue

        if h < 10 or h > 220:
            continue

        bottom = y + h
        aspect_ratio = w / max(h, 1)

        # CACTUS DETECTION
        if bottom >= GROUND_Y - 20 and h >= 15:

            cactus_count += 1

            distance = x - DINO_X

            if distance >= 0 and distance < nearest_distance:
                nearest_distance = distance
                nearest_obstacle = "CACTUS"

            cv2.rectangle(
                game_area,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                game_area,
                f"CACTUS X:{x} Y:{y}",
                (x, max(y - 8, 15)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1
            )

        # BIRD DETECTION
        elif (
            bottom < GROUND_Y - 20
            and BIRD_MIN_WIDTH <= w <= BIRD_MAX_WIDTH
            and BIRD_MIN_HEIGHT <= h <= BIRD_MAX_HEIGHT
            and aspect_ratio >= BIRD_MIN_ASPECT_RATIO
        ):

            bird_count += 1

            distance = x - DINO_X

            if distance >= 0 and distance < nearest_distance:
                nearest_distance = distance
                nearest_obstacle = "BIRD"

            cv2.rectangle(
                game_area,
                (x, y),
                (x + w, y + h),
                (255, 0, 0),
                2
            )

            cv2.putText(
                game_area,
                f"BIRD X:{x} Y:{y}",
                (x, max(y - 8, 15)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 0, 0),
                1
            )

    # 10. Display nearest obstacle distance
    if nearest_obstacle is not None:

        distance_text = (
            f"Nearest: {nearest_obstacle} "
            f"Distance: {nearest_distance} px"
        )

    else:
        distance_text = "Nearest Obstacle: None"

    cv2.putText(
        game_area,
        distance_text,
        (20, 125),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (0, 255, 255),
        2
    )

    # 11. Improved jump trigger
    jump_candidate = (
        nearest_obstacle == "CACTUS"
        and nearest_distance <= JUMP_DISTANCE
    )

    current_time = time.monotonic()

    if not jump_candidate:
        jump_latched = False

    jump_trigger = (
        jump_candidate
        and not jump_latched
        and current_time - last_jump_time >= JUMP_COOLDOWN
    )

    if jump_trigger:

        status = "JUMP TRIGGERED!"
        status_color = (0, 0, 255)

        last_jump_time = current_time
        jump_latched = True

        # Send command immediately to Arduino
        arduino.write(b'J')

        print(
            f"\nJUMP COMMAND SENT! "
            f"Distance: {nearest_distance} px"
        )

    elif jump_candidate and jump_latched:

        status = "JUMP ALREADY TRIGGERED"
        status_color = (0, 165, 255)

    elif nearest_obstacle == "BIRD":

        status = "BIRD DETECTED - NO JUMP"
        status_color = (255, 0, 0)

    else:

        status = "WAITING"
        status_color = (0, 255, 0)

    cv2.putText(
        game_area,
        status,
        (20, 150),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        status_color,
        2
    )

    # 12. Display theme
    cv2.putText(
        game_area,
        f"Theme: {current_theme}",
        (20, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 165, 255),
        2
    )

    # Display brightness
    cv2.putText(
        game_area,
        f"Brightness: {background_brightness:.1f}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 165, 255),
        1
    )

    # Display cactus count
    cv2.putText(
        game_area,
        f"Cactus: {cactus_count}",
        (20, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

    # Display bird count
    cv2.putText(
        game_area,
        f"Bird: {bird_count}",
        (20, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 0, 0),
        2
    )

    # 13. Show detection windows
    cv2.imshow(
        "Dino - Unified Detection",
        game_area
    )

    cv2.imshow(
        "Normalized Grayscale",
        detection_image
    )

    cv2.imshow(
        "Detection Mask",
        mask
    )

    frame_count += 1

    # 14. Stop using Q
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cv2.destroyAllWindows()

# Close Arduino connection
arduino.close()

print("\n\nDetection stopped.")
print(f"Frames processed: {frame_count}")
print("Automatic jumping: IMPLEMENTED")
print("Arduino integration: IMPLEMENTED")