"""
Steganography methods for the imager application.

This module provides all of the test processing operations (encode, decode) 
that are called by the application. Note that this class is a subclass of Filter. 
This allows us to layer this functionality on top of the Instagram-filters, 
providing this functionality in one application.

Based on an original file by Dexter Kozen (dck10) and Walker White (wmw2)

Nick Trejo nt286
13 November 2022
"""
import a6filter


class Encoder(a6filter.Filter):
    """
    A class that contains a collection of image processing methods
    
    This class is a subclass of Filter.  That means it inherits all of the 
    methods and attributes of that class too. We do that separate the 
    steganography methods from the image filter methods, making the code
    easier to read.
    
    Both the `encode` and `decode` methods should work with the most recent
    image in the edit history.
    """
    
    def encode(self, text):
        """
        Returns True if it could hide the text; False otherwise.
        
        This method attemps to hide the given message text in the current 
        image. This method first converts the text to a byte list using the 
        encode() method in string to use UTF-8 representation:
            
            blist = list(text.encode('utf-8'))
        
        This allows the encode method to support all text, including emoji.
        
        If the text UTF-8 encoding requires more than 999999 bytes or the 
        picture does  not have enough pixels to store these bytes this method
        returns False without storing the message. However, if the number of
        bytes is both less than 1000000 and less than (# pixels - 10), then 
        the encoding should succeed.  So this method uses no more than 10
        pixels to store additional encoding information.
        
        Parameter text: a message to hide
        Precondition: text is a string
        """
        # You may modify anything in the above specification EXCEPT
        # The first line (Returns True...)
        # The last paragraph (If the text UTF-8 encoding...)
        # The precondition (text is a string)
        assert type(text) == str
        
        current = self.getCurrent()
        
        try:
            
            assert len(text) <= 1000000
            assert len(text) <= len(current.getData())
            
            
            self._indicate_encode()

            
            lst = list(text)
            b = list(text.encode('utf-8'))
            pos = 7
            for i in b:
                self._encode_pixel(i, pos)
                pos += 1
            
            self._store_length(len(b))
            
            return True
        
        except AssertionError:
            return False

    
    def decode(self):
        """
        Returns the secret message (a string) stored in the current image. 
        
        The message should be decoded as a list of bytes. Assuming that a list
        blist has only bytes (ints in 0.255), you can turn it into a string
        using UTF-8 with the decode method:
            
            text = bytes(blist).decode('utf-8')
        
        If no message is detected, or if there is an error in decoding the
        message, this method returns None
        """
        # You may modify anything in the above specification EXCEPT
        # The first line (Returns the secret...)
        # The last paragraph (If no message is detected...)
        current = self.getCurrent()
        try:
            assert self._check_for_indicator()

            length = int(str(self._decode_pixel(5)) + str(self._decode_pixel(6)))
            lst = []
            for i in range(length):
                i += 7
                v = self._decode_pixel(i)
                lst.append(v)

            if len(lst) == 0:
                return ''
            else:
                c = bytes(lst).decode('utf-8')
                return str(c)
            
            
        
        except AssertionError:
            return None

    
    # HELPER METHODS
    def _decode_pixel(self, pos):
        """
        Return: the number n hidden in pixel pos of the current image.
        
        This function assumes that the value was a 3-digit number encoded as 
        the last digit in each color channel (e.g. red, green and blue).
        
        Parameter pos: a pixel position
        Precondition: pos is an int with  0 <= p < image length (as a 1d list)
        """
        # This is helper. You do not have to use it. You are allowed to change it.
        # There are no restrictions on how you can change it.
        #assert type(pos) == int and pos >= 0 and pos < len(self.getCurrent())

        rgb = self.getCurrent()[pos]
        red   = rgb[0]
        green = rgb[1]
        blue  = rgb[2]
        return  (red % 10) * 100  +  (green % 10) * 10  +  blue % 10
    

    def _encode_pixel(self, code, pos):
        """
        Encodes a pixel with the value of a unicode character

        This function converts a unicode character of type str into its 
        respective numerical code. If the code is less than 3 digits, this
        function concatenates 0's to the beginning until the str length is 3.

        The function then sets the last digit of the red, green, and blue pixel
        values of pixel in position pos equal to the first, second, and third
        digits of the character code, respectively.

        If any of the new pixel values go past the int limit of 255, the 
        function subtracts 10 from the value(s).

        Parameter code: a code to hide in a pixel
        Precondition: code is an int >= 0 and < 4

        Parameter pos: a pixel position
        Precondition: pos is an int with 0 <= pos < image length (as a 1d list)
        
        """
        assert type(code) == int and code >= 0
        assert type(pos) == int and pos >= 0 and pos < len(self.getCurrent())
        
        current = self.getCurrent()
        
        string = str(code)
        
        if len(string) == 1:
            string = '00' + string
        elif len(string) == 2:
            string = '0' + string

        lst = []
        for i in string:
            lst.append(int(i))
        
        red = current[pos][0]
        green = current[pos][1]
        blue = current[pos][2]

        r = red % 10
        g = green % 10
        b = blue % 10

        r1 = lst[0]
        g1 = lst[1]
        b1 = lst[2]

        if r1 >= r:
            redf = red + (r1 - r)
        elif r > r1:
            redf = red - (r - r1)
        if redf > 255:
            redf -= 10

        if b1 >= b:
            bluef = blue + (b1 - b)
        elif b > b1:
            bluef = blue - (b - b1)
        if bluef > 255:
            bluef -= 10

        if g1 >= g:
            greenf = green + (g1 - g)
        elif g > g1:
            greenf = green - (g - g1)
        if greenf > 255:
            greenf -= 10
        
        current[pos] = (redf, greenf, bluef)


    def _indicate_encode(self):
        """
        Alters the first 5 pixels to indicate the presence of a message

        This functions alters the last digit of the first 5 pixels to 
        indicate that there is a message to decode.
        
        The first check, on the first pixel, sets the last digit of the blue 
        value equal to the last digit of the sum of the last digits of the red 
        and green values
        (ie. (123, 34, 56) becomes (123, 34, 57))

        The second check, on the second pixel, sets the last digit of the blue 
        value equal to the last digit of the absolute value of the difference of 
        the last digits of the red and green values
        (ie. (123, 34, 56) becomes (123, 34, 51))

        The third check, on the third pixel, sets the last digit of the blue 
        value equal to the last digit of the product of the last digits of the 
        red and green values
        (ie. (123, 34, 56) becomes (123, 34, 52))

        The fourth check, on the fourth pixel, sets the last digit of the blue 
        value equal to the last digit of the last digit of the red value raised 
        to the power of the last digit of the green value
        (ie. (123, 34, 56) becomes (123, 34, 51))

        The fifth check counts the number of 0's in the red and green values 
        of the first four pixels and sets the last digit of the blue value of the 
        fifth pixel equal to the first digit of the count
        (ie. (0, 0, 0) (1, 0, 1) (2, 0, 0) (1, 0, 9) (12, 24, 53): (12, 24, 53) 
        becomes (12, 24, 57)

        """

        current = self.getCurrent()
        counter = 0
        for i in range(4):
            for v in range(2):
                if current[i][v] == 0:
                    counter += 1

            r = current[i][0]
            g = current[i][1]
            b = current[i][2]
            if i == 0:
                j = (r + g) % 10
            elif i == 1:
                j = (r - g) % 10
            elif i == 2:
                j = (r * g) % 10
            else:
                j = (r ** g) % 10

            if j >= (b%10):
                m = j - (b % 10)
                b += m
            else:
                m = (b % 10) - j
                b -= m

            if b > 255:
                b -= 10
            
            current[i] = (r, g, b)
        
        blue = current[4][2]
        
        if (counter%10) >= (blue%10):
            l = (counter%10) - (blue%10)
            blue += l
        else:
            l = (blue%10) - (counter%10)
            blue -= l

        if blue > 255:
            blue -= 10
        current[4] = (current[4][0],current[4][1],blue)


    
    def _store_length(self, l):
        """
        Stores the length of the message in the 6th and 7th pixels

        This function takes the length l of the text and encodes each
        digit into the last digit of the 6 values that make up the 2
        pixels  

        Parameter l: the length of the message in pixels
        Precondition: l is an int
        """
        assert type(l) == int

        current = self.getCurrent()
        
        string = str(l)
        while len(string) < 6:
            string = '0' + string
        lst = []
        for i in string:
            lst.append(int(i))

        n = 0
        for pos in range(2):
            pos += 5
            red = current[pos][0]
            green = current[pos][1]
            blue = current[pos][2]

            r = red % 10
            g = green % 10
            b = blue % 10

            r1 = lst[n]
            n += 1
            g1 = lst[n]
            n += 1
            b1 = lst[n]
            n += 1

            if r1 >= r:
                redf = red + (r1 - r)
            elif r > r1:
                redf = red - (r - r1)
            if redf > 255:
                redf -= 10

            if b1 >= b:
                bluef = blue + (b1 - b)
            elif b > b1:
                bluef = blue - (b - b1)
            if bluef > 255:
                bluef -= 10

            if g1 >= g:
                greenf = green + (g1 - g)
            elif g > g1:
                greenf = green - (g - g1)
            if greenf > 255:
                greenf -= 10
            
            current[pos] = (redf, greenf, bluef)
    

    def _check_for_indicator(self):
        """
        Returns True if a message is encoded. False otherwise.

        This function asserts the tests set up by the function
        _indicate_encode. If any of them fail, the function returns
        False. If they all pass, the function returns True.
        """

        current = self.getCurrent()
        r0 = current[0][0]
        g0 = current[0][1]
        b0 = current[0][2]

        r1 = current[1][0]
        g1 = current[1][1]
        b1 = current[1][2]

        r2 = current[2][0]
        g2 = current[2][1]
        b2 = current[2][2]

        r3 = current[3][0]
        g3 = current[3][1]
        b3 = current[3][2]

        b4 = current[4][2]
        counter = 0
        for i in range(4):
            for v in range(2):
                if current[i][v] == 0:
                    counter += 1
                else:
                    pass
        try:
            
            assert (r0%10)+(g0%10)==(b0%10)
            if (r1%10) >= (g1%10):
                assert (r1%10)-(g1%10)==(b1%10)
            elif (g1%10)>(r1%10):
                assert (g1%10)-(r1%10)==(b1%10)
            assert (r2%10)*(g2%10)==(b2%10)
            assert (r3%10)**(g3%10)==(b3%10)
            assert (counter%10) == (b4%10)
            return True
        
        except AssertionError:
            return False




