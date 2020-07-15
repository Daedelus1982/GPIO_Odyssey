# GPIO_Odyssey

I wanted to control the speed of my motor via PWM on my Odyssey SBC and the raspberry pi module didn't work so I made this software PWM code in order to do it.

**Note:** A hardware PWM implementation may produce a cleaner and accurate output but this code is good enough for many.

**Note:** Many thanks to zerrofour4 for this table https://forum.seeedstudio.com/t/gpio-pins-not-responding-in-code/252187/3

Examples
--------

Creating and using a standard GPIO output pin using physical pin numbers

    import odyssey_gpio as GPIO
    
    # get a normal GPIO pin object using just the physical pin number
    std_pin = GPIO.fetch_gpio(23, GPIO.OUT)
    # std_pin is a GPIO pin from the periphery module
    # as we set this pin to output, we can write high or low as normal
    std_pin.write(GPIO.HIGH)
    std_pin.write(GPIO.LOW)
    # then close it when we are done
    std_pin.close()
    
Creating and using a PWM class 
    
    import odyssey_gpio as GPIO
    
    # Create a PWM object, the first argument is the physical pin number,
    # the second argument sets the frequency 
    # (5000hz in this case)
    pwm_pin = GPIO.PWM(24, 5000)
    # start the cycle with initial duty cycle
    pwm_pin.start(40)
    # change the duty cycle and frequency
    pwm_pin.set_duty_cycle(80)
    pwm_pin.set_frequency(2000)
    # clean it up
    pwm_pin.stop()

