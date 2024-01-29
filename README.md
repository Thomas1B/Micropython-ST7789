# ST7789 LCD Display Driver for Micropython

Designed to be used along side Russ Hughes' Driver, found here https://github.com/russhughes/st7789_mpy. Read this article for an entire explaination.




# Class Description

```
spi = SPI(id=1, baudrate=BAUDRATE, sck=Pin(14), mosi=Pin(15))
screen = LCD(
    spi=spi,
    TOTAL_X_PIXELS=TOTAL_X_PIXELS,
    TOTAL_Y_PIXELS=TOTAL_Y_PIXELS,
    rotation=1,
    buffer_size=0,
    options=st7789.WRAP,
    RESET_PIN=RESET_PIN,
    CS_PIN=CS_PIN,
    DC_PIN=DC_PIN,
    BACKLIGHT_PIN=BACKLIGHT_PIN)
```
#
- `spi`: SPI Object.
- `TOTAL_X_PIXELS`: width of LCD in pixels.
- `TOTAL_Y_PIXELS`: height of LCD in pixels.
- `rotation` (default 0): rotates screen, 0 normal, 1 rot 90, 2 rot 180, 3, rot 270.
- `options`: ex wrapping [st7789.WRAP, st7789.WRAP_V st7789.WRAP_H]
- `buffer_size` (default 0): more to come...
- `BACKLIGHT_PIN`: Pin used for backlight.
- `RESET_PIN`: Pin used for Reset.
- `DC_PIN`: Rx (MSIO) pin
- `CS_PIN`: Sn pin
- `CLK_PIN`: SCK pin
- `DIN_PIN`: Tx (MOSI) pin

## Example
```py
import utime
from machine import Pin, SPI

spi = SPI(id=1, baudrate=BAUDRATE, sck=Pin(14), mosi=Pin(15))
screen = LCD(
    spi=spi,
    TOTAL_X_PIXELS=TOTAL_X_PIXELS,
    TOTAL_Y_PIXELS=TOTAL_Y_PIXELS,
    rotation=1,
    buffer_size=0,
    options=st7789.WRAP,
    RESET_PIN=RESET_PIN,
    CS_PIN=CS_PIN,
    DC_PIN=DC_PIN,
    BACKLIGHT_PIN=BACKLIGHT_PIN)


    screen.init()

    color = colors["CYAN"]
    bg_color = colors['BLACK']
    screen.fill(bg_color)

    screen.text(font, 'Hello World! I hope you are having a great day!', 0, 0)

    utime.sleep(5)
    screen.off()

```