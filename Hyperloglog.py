import math

class Hyperloglog:
    def __init__(self, bit_size:int,p:int):
        self.p = int(p)
        self.bit_size = bit_size
        self.m = 2**self.p
       ## p = p if p is not None else math.log(m)
        self.alpha_m = self._get_alpha_m()
        self.remainder = ""
        self.binary_list = []
        self.max_zeroes = 0
        ##self.binary =bin(self.bit_size)    
    def _get_alpha_m(self):
        m = self.m
        match m:
            case 16:
                return 0.673
            case 32:
                return 0.697
            case 64:
                return 0.709
            case _ if self.m >= 128:
                return 0.7213 / (1 + 1.079 / m)
            case _:
                raise ValueError("Unsupported value for m. Only m >= 16 is supported.")

    def _trim_binary(self):
        binary_representation = bin(self.bit_size)[2:]
        len_binary = len(binary_representation)
        print (len_binary)
        remainder = int(len_binary % self.p)
        ##print(binary_representation)        
        remainder_index = len_binary - remainder
        remainder = binary_representation[remainder_index:len_binary]
        binary_representation = binary_representation[0:remainder_index]
        return binary_representation,remainder

    def _get_registar(self,binary):
        counter = 0
        ##binary = self.binary
        p = int(self.p)
        firstCount = True
        binary_list = []
        for i in range(0,len(binary),p):
            if firstCount:
                group = binary[0:p]
                binary_list.append(group)
                print(group)
                counter = p
                firstCount = False
            #not sure if include plus 1
            group = binary[counter:counter+p]
            binary_list.append(group)
            counter += p 
            print(group)
        return binary_list
    
    def _count_max_zeroes(self,remainder,binary_list):
        max_zero = 0
        for i in range(0,len(remainder),1):
            print(i)
            if remainder[i] == '0':
                max_zero += 1
            else:
                break
        for el in binary_list:
            counter = 0
            for i in el:
                if i == '0':
                    counter +=1
                else:
                    break
            if counter > max_zero:
                max_zero = counter
        return max_zero    
        
        
    def _estimate_cardinality(self):
        binary_rep,remainder = self._trim_binary()
        self.remainder = remainder
        print(len(binary_rep))
        binary_list = self._get_registar(binary_rep)
        max_leading_zeroes = self._count_max_zeroes(binary_list=binary_list,remainder=remainder)
        print(max_leading_zeroes)
        cardinality = self.alpha_m * (self.m**2) * 2**-max_leading_zeroes
        return cardinality

bit_size = 256
p = 0
min_p= math.log2(16)
#10000000
h = Hyperloglog(bit_size,min_p)
print(h._estimate_cardinality())


#23536.35633560112
h = Hyperloglog(bit_size,8)
print(h._estimate_cardinality())

#8.352083396687618 * 10^76
h = Hyperloglog(bit_size,256/2)
print(h._estimate_cardinality())


#1.2744267878246487 10^72
h = Hyperloglog(bit_size, 120)
print(h._estimate_cardinality())

