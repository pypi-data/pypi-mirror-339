import pyautogui, time


def main():
    count = 0
    while True:
        pyautogui.moveRel(10, 0)
        time.sleep(1)
        pyautogui.moveRel(-10, 0)
        pyautogui.click()
        count += 1
        print(f"tick {count}")
        time.sleep(59)


if __name__ == "__main__":
    main()
