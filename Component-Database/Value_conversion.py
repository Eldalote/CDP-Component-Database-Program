class ValueConvert:
    """Class for the conversion of short notation to real value of components, and vise versa"""
    
    #ISO multipliers list, for lookups. (Name, Shortdisplay(resistor), shortdisplay(other), shortlookup(resistor), shortlookup(other), value, exponent)
    iso_multipliers = (('Pico',  'p','p','p','p', 0.000000000001, -12),
                       ('Nano',  'n','n','n','n', 0.000000001, -9),
                       ('Micro', 'µ','µ','u','u', 0.000001, -6),
                       ('Milli', 'm','m','m','m', 0.001, -3),
                       ('',      'R','.','R','.', 1, 0),
                       ('Kilo',  'k','k','k','k', 1000, 3),
                       ('Mega',  'M','M','M','M', 1000000, 6),
                       ('Giga',  'G','G','G','G', 1000000000, 9))
    #How wide should the real value be for storage (for sorting reasons)
    realvalue_store_width = 20
    
    def real_to_short_resistor(self, RealValue):
        """Converts the presented RealValue to short notation for the user, and the verbose value
        :param RealValue: string with the real value of the component, only feed this data from the database. Invalid user input could result in errors.
        :return: tuple of (Short representation, verbose representation)
        """
        #A value of zero ohm should be stored as "Zero". We check for empty string anyway.        
        if RealValue == "Zero" or RealValue == "":
            return ("0R","Zero Ohm")
        #If the real value starts with "0." we know we are dealing with a "small value" (less than 1 ohm)
        elif RealValue[0:2] == "0.":
            return self.__rts_res_small(RealValue[2:len(RealValue)])
        #if not, it is a "big value" (1 ohm and up)
        else:
            return self.__rts_res_big(RealValue)
    
    def __rts_res_big(self,value):
        """Sub-function of the real to short resistor convertor, for "Big values"
        :Param value: the real value
        :return: tuple of (Short representation, verbose representation)
        """
        #first we strip off the leading zeroes with a while loop
        while value[0] == "0":
            value = value[1:len(value)]      
        #if value is only digits, we can just convert it to an integer, and work with that.
        if value.isdigit():
            intvalue = int(value)
            #Step through the iso_multipliers, and check if the value fits in that multiplier range
            for mult in ValueConvert.iso_multipliers:                            
                if intvalue >= mult[5] and intvalue < mult[5]*1000:
                    #when we find the right multiplier, store some values for later use
                    multiplier = mult[5]
                    symbol = mult[1]
                    word = mult[0]
                    break
            #if the value is larger than 1000 times the largest in the list, we didnt find a matching one in the list, and so we assign the largest now.
            if intvalue >= ValueConvert.iso_multipliers[len(ValueConvert.iso_multipliers)-1][5]:
                multiplier = ValueConvert.iso_multipliers[len(ValueConvert.iso_multipliers)-1][5]
                symbol = ValueConvert.iso_multipliers[len(ValueConvert.iso_multipliers)-1][1]
                word = ValueConvert.iso_multipliers[len(ValueConvert.iso_multipliers)-1][0]
            #the first part of the representation (the part before the dividing symbol) is a string of the integer rounded value of the value divided by the multiplier
            first_part = str(int(intvalue/multiplier))
            #the remainder is the part after the dividing symbol, we get that by taking the integer value of the remainder of the same division 
            remainder = int(intvalue%multiplier)
            #special case, if we are dealing with resistors in the "1 ohm" range, to get the right remainder, we need to multiply and divide by 1000 (remainder of 14.7/1 is 0.7, we need to get "7" as the answer in this case).
            if multiplier == 1:
                remainder = int((intvalue*1000)%1000)
            
            if remainder != 0:
                #in a loop, we strip the trailing zeroes of the remainder
                while remainder%10 == 0:
                    remainder = int(remainder / 10)
                #and then formate the outputs correctly
                shortvalue = first_part + symbol +str(remainder)
                verbose = first_part + '.' + str(remainder) + " " + word +"Ohm"
            else:
                #if the remainder is 0, the formatting is simpler
                shortvalue = first_part + symbol
                verbose = first_part + " " + word +"Ohm"
            return(shortvalue, verbose)
        #if the value is not only digits, we are dealing with a decimal value in the 1 ohm range.
        else:
            #Just split by "." and format accordingly
            parts = value.split(".")
            shortvalue = parts[0]+"R"+parts[1]
            return(shortvalue, value+" Ohm")


    def __rts_res_small(self,value):
        """Sub-function of the real to short resistor convertor, for "Small values"
        :Param value: the real value
        :return: tuple of (Short representation, verbose representation)
        """
        #First, we determine the exponent of the value.
        exponent = 0
        while value[0] == '0':
            #for each '0' at the start of the value, we strip that '0' and decrease the exponent by 1
            exponent -= 1
            value = value[1:len(value)]
        #if the exponent is smaller than the smallest in the iso list, we can't deal with that right now.
        #note: This shouldn't happen, since the value should only be stored in the db if converted by this class, which uses the same iso table.
        if exponent <= iso_multipliers[0][6]:
            return("ERROR", "Out of bounds")
        #we step the the iso table again, to check which one matched, this time by exponent
        for mult in ValueConvert.iso_multipliers:
            if exponent > mult[6]:
                #shift is how many spaces we have to shift the number to get to the right value. 0.1 is 100 milli, not 1 milli, so we have to shift 2
                shift = exponent - mult[6] 
                symbol = mult[1]
                word = mult[0]
        #now, the first part are the first (shift) digits
        first_part = value[0:shift]
        #if the digits are fewer than the number we need (for example 0.1 is 100m, but comes into the function as just 1) we need to padd zeroes to the end.
        while len(first_part) < shift:
            first_part += "0"
        #the remainder are the digits after (shift)
        remainder = value[shift:len(value)]
        #now format it properly, and return
        if remainder != "":
            short = first_part + symbol + remainder
            verbose = first_part + "." + remainder + " " + word + "Ohm"
        else:
            short = first_part + symbol
            verbose = first_part + " " + word + "Ohm"
        return(short, verbose)
    
    
    def short_to_real_resistor(self, ShortRepresentation):
        """Converts the presented ShortRepresentation to a string containing the real value for storage in the database, as well ass a verbose representation
        :param ShortRepresentation: The short representation of the value of the resistor, like 4k7
        :return: A tuple as (Real value string, verbose representation)
        """
        #if the input is zero, return zero
        if ShortRepresentation == "0" or ShortRepresentation == "0R":
            return ("Zero", "Zero Ohm")
        #if the input is just digits, return the sub function for just numerical
        if ShortRepresentation.isdigit():
            return self.__str_res_num(ShortRepresentation)
        #Now we check all the iso multipliers, to see what symbol is used
        for iso in ValueConvert.iso_multipliers:
            breakpoint = ShortRepresentation.find(iso[3])
            #check if the symbol was found, 
            if breakpoint != -1:
                #if yes, see if it is a "large" (>=1) or a "small" (<1) value, and return the proper sub function
                if iso[6] >= 0:
                    return self.__str_res_big(ShortRepresentation[0:breakpoint], ShortRepresentation[breakpoint +1 : len(ShortRepresentation)], iso)
                else:
                    return self.__str_res_small(ShortRepresentation[0:breakpoint], ShortRepresentation[breakpoint +1 : len(ShortRepresentation)], iso) 
        #if that all hasn't worked so far, return an error with "Unknown value" as the error message.
        return("ERROR", "Unknown value")          
    
    def __str_res_big(self, pre, post, iso):
        """Sub function of the short to real resistor function, for "Big" (>=1) values 
        :param pre: The part before the symbol break (symbol break is the 'k' in 4k7)
        :param post: the part after the symbol break
        :param iso: correct tuple from the iso_multipliers table
        :return: A tuple as (Real value string, verbose representation)
        """
        #Start with creating the verbose representation
        #if post is blank, the formatting is very simple
        if post == "":
            verbose = pre + " " + iso[0] + "Ohm" 
        #if post is not blank, but also not just digits, something is wrong, and we error out.
        elif post.isdigit() == False:
            return ("ERROR","Invalid formatting")
        #else, format it slightly longer
        else:
            verbose = pre + "." + post + " " + iso[0] + "Ohm"
        
        #now we start formatting the realvalue
        #first, the pre must always be only digits, and not blank (0k7 should be 700R) else error out
        if pre.isdigit() == False:
            return ("ERROR","Invalid formatting")
        #if iso[0] (the name of the multiplier) is blank, we are dealing with the 1 ohm range.
        if iso[0] == "":
            #if post is empy, realvalue is just pre, if post is present, realvalue is pre.post
            if post == "":
                realvalue = pre
            else:
                realvalue = pre + "." + post
        #if we are not in the 1 ohm range, just paste pre and post together to get realvalue (for now)
        else:
            realvalue = pre + post
        #Now add trailing zeroes, by checking if the length is shorter than the exponent + 1 ("1000" has exponent of 3, length of 4)
        while len(realvalue) < (iso[6] +1):
            realvalue += "0"
        #then add leading zeroes for database sorting perposes and return
        while len(realvalue) < realvalue_store_width:
            realvalue = "0" + realvalue 
        
        return (realvalue, verbose)


    def __str_res_small(self, pre, post, iso):
        """Sub function of the short to real resistor function, for "small" (<1) values 
        :param pre: The part before the symbol break (symbol break is the 'm' in 4m7)
        :param post: the part after the symbol break
        :param iso: correct tuple from the iso_multipliers table
        :return: A tuple as (Real value string, verbose representation)
        """
        #verbose formatting is the same as with the "big" subfunction
        if post == "":
            verbose = pre + " " + iso[0] + "Ohm"
        elif post.isdigit() == False:
            return ("ERROR","Invalid formatting")
        else:
            verbose = pre + "." + post + " " + iso[0] + "Ohm" 
        #then realvalue formatting
        #pre must always be only digits, and not blank, else error out
        if pre.isdigit() == False:
            return ("ERROR","Invalid formatting")
        #since we are dealing with values below 1 ohm, the period is in front of the values anyway
        realvalue = pre + post
        #if the length of pre is too long, that is invallid formatting
        if len(pre) > 3:
            return ("ERROR","Invalid formatting")
        #calculate the number of leading zeroes we need, by using the negative of the exponent, minus the current length
        leadingzeroes = (0 - iso[6]) - len(pre)
        #and then add the leading zeroes
        for i in range(0,leadingzeroes):
            realvalue = "0" +realvalue
        #after that, add the "0." to the front
        realvalue = "0." + realvalue    
        #also strip trailing zeroes, in case the user entered too many zeroes in the input, and then return
        while realvalue[len(realvalue)-1] == "0":
            realvalue = realvalue[0:len(realvalue)-1]       
        return (realvalue, verbose)


    def __str_res_num(self, short):
        """Sub function of the short to real resistor function, 1 ohm range values, with only numerical input 
        :param short: The numerical input        
        :return: A tuple as (Real value string, verbose representation)
        """
        #this one is very simple. Just format it, and padd it with leading zeroes, and return.
        verbose = short + " Ohm"
        realvalue = short
        while len(realvalue) < realvalue_store_width:
            realvalue = "0" + realvalue    
        return (realvalue, verbose)
