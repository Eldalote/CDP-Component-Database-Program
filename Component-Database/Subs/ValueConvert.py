class ValueConvert():
    """Collection of functions for the conversion of values between Short notation and database notatation, and to get a verbose representation"""

    #ISO multipliers list, for lookups. (Name[0], Shortdisplay(resistor)[1], shortdisplay(other)[2], shortlookup[3], exponent[4], value[5])
    iso_multipliers = (
                        ('Pico',  'p','p','p', -12, 0.000000000001),
                        ('Nano',  'n','n','n', -9, 0.000000001),
                        ('Micro', 'µ','µ','u', -6, 0.000001),
                        ('Milli', 'm','m','m', -3, 0.001),
                        ('',      'R','.','R', 0, 1),
                        ('Kilo',  'k','k','k', 3, 1000),
                        ('Mega',  'M','M','M', 6, 1000000),
                        ('Giga',  'G','G','G', 9, 1000000000)
                        )
    #how wide is the storage value for the database (value >= 1, and without decimals) (for proper sorting reasons)
    db_store_width = 20

    component_units = {"Resistor": "Ohm",
                       "Capacitor": "Farad",
                       "Inductor": "Henry"}
    component_symbols = {"Resistor": "Ω",
                         "Capacitor": "F",
                         "Inductor": "H"}

    def _is_number(self, input):
        """Checks if the given input is a processable number. 
        Processable numbers are positive integers, positive decimal numbers (but not the full range of floating point numbers such as "NaN" or infinite)
        :param input: String. The input to be checked.
        :return: Boolean
        """
        return input.isdigit() or input.replace('.','',1).isdigit()

    def _split_number(self, number):
        """Splits the presented number into three values. Pre, Post, and Exponential
        Pre is the number before the period, post is the number after the period, and Exponential is the exponential of the number. (ex: 1000 is 3, 100 is 2, 0.1 is -1, etc)
        :param number: String. Number to be broken up
        :return: Pre (string, Post (string), Exponential (integer)
        """
        #If it's not actually a number, return nothing
        if self._is_number(number) == False:
            return None, None, None

        #strip leading zeroes. Make sure that if the number is only zeroes, we return 0
        while number[0] == "0":
            if number == "0":
                return "0", "", 0
            number = number[1:len(number)]

        #if number is an integer, return the number as is (with leading zeroes stripped)
        if number.isdigit():
            return number, "", len(number) -1

        #if not, split the number along the period
        split = number.split(".")
        Pre = split[0]
        Post = split[1]

        #it could be that the number was not only zeroes, but still resolved to nothing. (ex: 0. or 000.)
        if Pre == "" and Post == "":
            return "0", "", 0

        #if Pre is blank (if it was only 0's, the 0's were stripped) we are dealing with a number smaller than 1
        if Pre == "":
            Exponent = -1
            #check how many leading zeroes there are in Post
            tempPost = Post
            while tempPost[0] == "0":
                #for every leading zero, decrease the exponent by one.
                Exponent -= 1
                if tempPost == "0":
                    #this also means only zeroes
                    return "0", "", 0
                tempPost = tempPost[1:len(tempPost)]
        #if Pre is not blank, the exponent is the length of Pre -1
        else:
            Exponent = len(Pre) -1

        #Strip trailing zeroes of Post
        if Post != "":
            while Post[-1] == "0":
                #if Post is only zeroes, set it to blank and break
                if Post == "0":
                    Post = ""
                    break
                Post = Post[0:-1]

        #return the values
        return Pre, Post, Exponent

    def short_to_db(self, type, short_value):
        """Turns the short_value input into a value that can be stored in the database
        :param type: String. Type of component (possible types are listed in component units and component symbols)
        :param short_value: String. Short representation of the value. (ex: 100n, 4k7, 1.8M, etc)
        :return: String containing the value formatted in a way that it can be stored in the database. (in a sortable way)
        """
        #Check if the type is correct
        if type in self.component_units:
            pass
        else:
            return "ERROR: Incorrect type"
        #remove blank spaces
        short_value = short_value.replace(" ","")
        #check if the input has anything in it
        if short_value == "":
            return "ERROR: Empty"
        #check if last character in the string is the component symbol, if yes, strip it
        if short_value[-1] == self.component_symbols[type]:
            short_value = short_value[0:-1]
        
        #check if the input is just a number
        if self._is_number(short_value):
            #split it with the split function
            pre, post, exp = self._split_number(short_value)
        else:
            #If not just a number, check if it is a number with a multiplier in there somewhere. Keep note of if that is successful
            success = False           
            #step through the iso multipliers to look for the multiplier symbol
            for iso in self.iso_multipliers:
                #first, check if we get a number if we replace the multiplier symbol with a period. (ex: 4k7 gets 4.7 with "k")
                pointreplace = short_value.replace(iso[3],".",1)
                if self._is_number(pointreplace):
                    #get the split, and break out of the loop
                    pre, post, exp = self._split_number(pointreplace)
                    #the actual exponent is the sum of "exp" and the iso exponent
                    exp += iso[4]
                    #note the successful conversion
                    success = True
                    #and break
                    break
                #if that does not work, check if we get a number if we remove the multiplier symbol. We only get to this one with a decimal number and a multiplier (ex: 1.6k)
                blankreplace = short_value.replace(iso[3],"",1)
                if self._is_number(blankreplace):
                    #do the same things as with the other success
                    pre, post, exp = self._split_number(blankreplace)
                    exp += iso[4]
                    success = True
                    break
            #if we didn't find a match, error out
            if success == False:
                return "ERROR: Unknown or Format error"

        #we now have a pre post and exp, or we errored out.
        #Formatting splits between values smaller than 1, and 1 and up. 
        if exp < 0: #smaller than 1
            #the database value will always start with 0. on a value smaller than 1
            dbVal = "0."
            #add leading zeroes (after the period) equal to minus the exponent -1
            for i in range(0, -exp -1):
                dbVal += "0"
            #if pre is not blank (as with 100m for example)
            if pre != "":
                #add pre and post to the dbval
                dbVal += pre + post
            else:
                #if pre is blank, only add post, but we first need to strip leading zeros of post
                while post[0] == "0":
                    post = post[1:len(post)]
                #Add it to dbval, zeroes stripped
                dbVal += post
            #now strip trailing zeroes (while post can't have trailing zeroes, pre might have)
            while dbVal[-1] == "0":
                dbVal = dbVal[0:-1]
        #if exp is 0 or greater (value 1 or greater):
        else:
            #if post is blank, or the length of pre and post together is less or equal to the exponent +1, formatting is as an integer
            #start with just pre and post
            if post == "" or len(pre) + len(post) <= exp +1:
                dbVal = pre + post
                #add trailing zeroes untill the length is equal to exp + 1
                while len(dbVal) < exp +1:
                    dbVal += "0"
                #then, add leading zeroes untill the length is eqaul to the storage length
                while len(dbVal) < self.db_store_width:
                    dbVal = "0" + dbVal
            #if not, we do have a decimal number, and need to format it slightly differently
            else:
                #first, shift characters from post to pre until the length of pre is equal to exp +1
                while len(pre) < exp + 1:
                    pre += post[0]
                    post = post[1:len(post)]
                #now start dbval with pre and make it match the storage length
                dbVal = pre
                while len(dbVal) < self.db_store_width:
                    dbVal = "0" + dbVal
                #once the whole part of the decimal number is at the correct length, fractional part at the end
                dbVal += "." + post
        #done
        return dbVal

    def db_to_readable(self, type, db_value):
        """Turns the database stored value into a short representation and verbose representation, for readability
        :param type: String. Type of component (possible types are listed in component units and component symbols)
        :param db_value: string with value from the database.
        :return: String, string. Short representation of the database value, verbose representation of the database value
        """
        #start by checking if the db value is an error. The database should never have an error value in it, but short to verbose also uses this function, and that might pass an error value
        if db_value[0:5] == "ERROR":
            #if the error is that the input is empty, just pass two empty strings
            if db_value == "ERROR: Empty":
                return "",""
            else:
                #else pass an empty string for short value, and the error message for the verbose
                return "", db_value

        #not an error, split the db value with the split function
        pre, post, exp = self._split_number(db_value)
        #step through the isos to see which multiplier matches.
        for iso in self.iso_multipliers:
            if exp >= iso[4]:
                mult = iso
                #this always picks the biggest multiplier that fits
        #if the exponent is less than 0, we need to strip leading zeroes of the post
        if exp < 0:
            while post[0] == "0":
                post = post[1:len(post)]

        #then, depending on whether the length of pre is longer or shorter than the desired length, either shift parts to or from post
        #too long:
        while len(pre) > 1 + exp - mult[4]:
            if pre[-1] != "0" or post != "": #as long as the last digit of pre is not a zero, or post isn't empty, shift the last digit from pre to post
                post = pre[-1] + post
            #remove the last digit from pre, either if it has been shifted, or its a 0 and post is empty
            pre = pre[0:-1]
        #too short
        while len(pre) < 1 + exp -mult[4]:
            if post == "": #if post is already empty, just add a 0 to the end of pre
                pre += "0"
            else: #if not, shift the first digit of post to the end of pre
                pre += post[0]
                post = post[1:len(post)]
        #both short and verbose representation start with pre
        short = pre
        verbose = pre
        #now finish verbose:
        if post != "":
            verbose += "." + post
        verbose += " " + mult[0] + self.component_units[type]
        #then finish short
        if type == "Resistor":
            short += mult[1] + post #resistors are simple. This one works with all values
        else:
            #none resistors need different formatting depending on if the post is empty or not
            if post != "":
                if mult[0] == "":
                    short += "." + post + self.component_symbols[type]
                else:
                    short += "." + post + mult[2] + self.component_symbols[type]
            else:
                if mult[0] == "":
                    short += self.component_symbols[type]
                else:
                    short += mult[2] + self.component_symbols[type]
        #we're done, return short and verbose
        return short, verbose

    def short_to_verbose(self, type, short_value):
        """Turns a short representation value into a verbose representation, for readability
        :param type: String. Type of component (possible types are listed in component units and component symbols)
        :param short_value: string. Short representation value as input
        :return: String. Verbose representation of the short input
        """
        #we pull a sneaky. We already have a short to db function, and a function that takes db value and returns a verbose representation. Just use a combination of the two
        db = self.short_to_db(type, short_value)
        short, verbose = self.db_to_readable(type, db)
        return verbose