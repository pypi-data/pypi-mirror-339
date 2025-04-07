simple pygame plugin for kids.

### Template. Empty window ###

    from pioneergame import Window

    window = Window(1300, 700)  # 1300x700 window

    while True:  # main loop
        window.fill('black')

        window.update(80)  # update 80 times per second
