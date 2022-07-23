class MDCGen:
    def __init__(self):
        self.f = open(r"./tms4256.mdc", 'w')
        self.f_config = open(r"./mdc_config.txt", 'r')
        self.file_header = \
            """mem_source_15;

pindef

addr(0..8) = i, hex, (1,2,3,4,5,6,7,8,9)
ras_ = i, bin, (48)
cas_ = i, bin, (47)
w_ = i, bin, (46)

d = i, bin, (45)
q = o, bin, (44)

main_f
//ADDR1 as row
//ADDR2 as colum
"""
        self.file_end = """end."""
        self.start_index = lambda num: '\nstart_index({})\n'.format(num)
        self.halt = '  \n halt  (000 111 0 x) \n'
        self.ldar1 = lambda x: " ldar1, {} (000 111 1 x)\n".format(x)
        self.ldar2 = lambda x: " ldar2, {} (000 111 1 x)\n".format(x)
        self.incar1 = "	incar1	(000 111 0 x)\n"
        self.incar2 = "	incar2	(000 111 0 x)\n"
        self.w = \
            lambda x: ''' inc (000 111 1 x) //Init State
 addr1 (000 010 {d} x) //Row Addr
 addr2 (000 000 {d} x) //Col Addr
 inc (000 000 {d} x) //Write D={d}
 inc (000 011 {d} x)
 inc (000 111 1 x)
 inc (000 111 1 x)\n'''.format(d=x)

        self.r = \
            lambda x: ''' inc (000 111 1 x) //Init State
 addr1 (000 011 1 x) //Row Addr
 addr2 (000 001 1 x) //Col Addr
 inc (000 001 1 {q}) //Test Q For L
 inc (000 011 1 x)
 inc (000 111 1 x)
 inc (000 111 1 x)\n'''.format(q='H' if x == 1 else 'L')

    def one_bit_test(self):
        self.f.write(self.file_header)
        content = self.start_index(0) + self.ldar1(1) + self.ldar2(1)
        for i in range(10):
            content += self.w(0) + self.r(0) + self.w(1) + self.r(1)
        content += self.halt
        self.f.write(content)
        self.f.write(self.file_end)

    def __del__(self):
        print("MDC File Generated")
        self.f.close()


if __name__ == "__main__":
    mdcGen_inst = MDCGen()
    mdcGen_inst.one_bit_test()
