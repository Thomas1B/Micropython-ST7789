'''

Custom LCD DRIVER

Designed to be used along side Russ Hughes' Driver, found here https://github.com/russhughes/st7789_mpy. Read this article for an entire explaination.F

'''


# **************** FONTs ****************
import scripts
import scriptc
import romans
import romanp
import romand
import romancs
import romanc
import meteo
import italiccs
import italicc
import greeks

import vga2_bold_16x32 as large_font_bold
import vga2_16x32 as large_font
import vga2_16x16 as normal_font
import vga2_8x16 as small_font
import vga2_8x8 as extra_small_font

# **************** Other Modules ****************

import st7789
from machine import Pin, SPI
import utime


basic_fonts = [large_font_bold, large_font,
               normal_font, small_font, extra_small_font]


hershey_fonts = [greeks, italicc, italiccs, meteo, romanc,
                 romancs, romand, romanp, romans, scriptc, scripts]

# ********************** User Parameters **************************

# Pins used for LCD
BACKLIGHT_PIN = 10
RESET_PIN = 11
DC_PIN = 12  # Rx (MSIO) pin
CS_PIN = 13  # CSn pin
CLK_PIN = 14  # SCK pin
DIN_PIN = 15  # Tx (MOSI) pin

# LCD Pixel Size
TOTAL_X_PIXELS = 240  # width of LCD in pixels.
TOTAL_Y_PIXELS = 320  # height of LCD in pixels.

# baudrate
BAUDRATE = 6_2500_000


TFA = 0	 # top free area when scrolling
BFA = 0	 # bottom free area when scrolling

# *********************************** *****************************************

# Base Colors
colors = {'BLACK': st7789.BLACK,
          'BLUE': st7789.BLUE,
          'WHITE': st7789.WHITE,
          'RED': st7789.RED,
          'GREEN': st7789.GREEN,
          'CYAN': st7789.CYAN,
          'MAGENTA': st7789.MAGENTA,
          'YELLOW': st7789.YELLOW,
          }


def get_text_width(text: str, font) -> int:
    '''
    Function to calculate the width of a string in pixels.

    Parameters:
        text: string of text.
        font: what font is being used.

    Returns:
        number of pixels in width [integer.]
    '''

    return len(text)*font.WIDTH


class LCD:
    '''
    Custom class for st7789.ST7789

    Parameters:
        spi: SPI Object.
        TOTAL_X_PIXELS: width of LCD in pixels.
        TOTAL_Y_PIXELS: height of LCD in pixels.
        rotation (default 0): rotates screen, 0 normal, 1 rot 90, 2 rot 180, 3, rot 270.
        options: ex wrapping [st7789.WRAP, st7789.WRAP_V st7789.WRAP_H]
        buffer_size (default 0): more to come...

        BACKLIGHT_PIN: Pin used for backlight.
        RESET_PIN: Pin used for Reset.
        DC_PIN: # Rx (MSIO) pin
        CS_PIN: # CSn pin
        CLK_PIN: = 14  # SCK pin
        DIN_PIN: = 15  # Tx (MOSI) pin
    '''

    def __init__(self,
                 spi,
                 TOTAL_X_PIXELS=TOTAL_X_PIXELS,
                 TOTAL_Y_PIXELS=TOTAL_Y_PIXELS,
                 rotation=0,
                 options=0,
                 buffer_size=0,
                 RESET_PIN=RESET_PIN,
                 CS_PIN=CS_PIN,
                 DC_PIN=DC_PIN,
                 BACKLIGHT_PIN=BACKLIGHT_PIN) -> None:

        self.tft = st7789.ST7789(
            spi,
            TOTAL_X_PIXELS,
            TOTAL_Y_PIXELS,

            reset=Pin(RESET_PIN, Pin.OUT),
            cs=Pin(CS_PIN, Pin.OUT),
            dc=Pin(DC_PIN, Pin.OUT),
            backlight=Pin(BACKLIGHT_PIN, Pin.OUT),

            rotation=rotation,  # 0, 1, 2, 3
            options=options,
            buffer_size=buffer_size
        )

        self.options = options

    def init(self) -> None:
        '''
        Function to initialize LCD object
        '''

        self.tft.init()

    def screen_width(self) -> int:
        '''
        Function to get the LCD Width
        '''
        return self.tft.width()

    def screen_height(self) -> int:
        '''
        Function to get the LCD height
        '''
        return self.tft.height()

    def screen_center(self) -> tuple:
        '''
        Function to get the center.
        '''

        return self._width//2, self._height//2

    def text(self,
             font, text: str,
             xpos: int,
             ypos: int,
             color=colors['WHITE'],
             bg_color=colors['BLACK'],
             ignore_wrap=False) -> None:
        '''
        Function that extends st7789's text func.

        Parameters:
            font: font style.
            text: string for text.
            xpos: x pixel position.
            ypos: y pixel position.
            color: color of text (default white).
            bg_color: background color of text (default black).
            ignore_wrap (default False): bool to ignore class option.
        '''

        start_x, start_y = xpos, ypos

        # Make font size
        font_size = (font.WIDTH, font.HEIGHT)

        # going through each character of the string
        for i, c in enumerate(text):
            self.tft.text(font, c, xpos, ypos, color, bg_color)
            xpos += font_size[0]

            wrap_check = self.options == st7789.WRAP or self.options == st7789.WRAP_H
            if not ignore_wrap and wrap_check:
                if xpos + font_size[0] > self.screen_width():
                    ypos += font_size[1]
                    xpos = start_x

    def center_text(self, font, text, xpos=None, ypos=None, color=colors['WHITE'], background_color=colors['BLACK']) -> None:
        '''
        Function to center text on the LCD.

        Parameters:
            font: font style.
            text: string for text.
            xpos: x pixel position (Optional). 
            ypos: y pixel position (Optional).
            color: color of text (default white).
            bg_color: background color of text (default black).

        '''

        # length of string
        length = 1 if isinstance(text, int) else len(text)

        if xpos == None:
            xpos = self.screen_width() // 2 - length // 2 * font.WIDTH
        if ypos == None:
            ypos = self.screen_height() // 2 - font.HEIGHT // 2

        self.tft.text(font, text, xpos, ypos, color, background_color)

    def fill(self, color=colors['BLACK']) -> None:
        '''
        Function to fill the LCD.

        color: color to fill with (default black).
        '''

        self.tft.fill(color)

    def clear_screen(self, color=colors["BLACK"]) -> None:
        '''
        Function to clear the screen

        '''

        self.tft.fill(color)

    def on(self):
        '''
        Function to turn the screen on, does not initialize.
        '''
        self.tft.on()

    def off(self):
        '''
        Function to turn the screen off, does not de-initialize.
        '''

        self.tft.off()


# ************ Examples ************:


def Hershey_fonts_example():
    print('Example of Hershey Fonts')

    for i, font in enumerate(hershey_fonts, 1):
        # getting file name then printing to terminal
        font_name = font.__file__.strip(".py")
        print(
            f'Font {i}/{len(hershey_fonts)}: {font_name}, Fontsize = ({font.WIDTH}, {font.HEIGHT})'
        )

        # drawing strings to LCD
        screen.tft.draw(
            font, f'Font {i}/{len(hershey_fonts)}:', 20, 150, color)
        screen.tft.draw(font, 'Welcome!   12345', 0, 60, color)
        screen.tft.draw(font, '67890!@#$%^&*', 30, 110, color)
        screen.tft.text(small_font, f'{font_name}', 60,
                        150+small_font.HEIGHT, color)

        utime.sleep(5)
        screen.clear_screen()


def Basic_font_examples():
    print("Basic Fonts Example:")

    for i, font in enumerate(basic_fonts, 1):
        screen.center_text(font, example)
        print(f'Font ({i}/{len(basic_fonts)}): {font.__name__}')
        utime.sleep(3)

        screen.clear_screen()


if __name__ == '__main__':

    import utime

    spi = SPI(id=1, baudrate=BAUDRATE, sck=Pin(CLK_PIN), mosi=Pin(DIN_PIN))
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

    example = 'Hello World!'

    screen.center_text(
        large_font,
        example,
        color=color,
        background_color=bg_color
    )

    screen.fill(bg_color)
    utime.sleep(0.5)

    font = large_font

    screen.text(
        font, 'Hello World! My name is Thomas Bourgeois ', 0, 0)

    screen.text(
        font, 'Hello World! My name is Thomas Bourgeois', 0, 150, ignore_wrap=True)
