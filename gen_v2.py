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
        self.halt = '  \n halt (000 111 1 x)\n'
        self.ldar1 = lambda x: " ldar1, {} (000 111 1 x)\n".format(x)
        self.ldar2 = lambda x: " ldar2, {} (000 111 1 x)\n".format(x)
        self.incar1 = " incar1 (000 111 1 x)\n"
        self.incar2 = "	incar2 (000 111 1 x)\n"
        self.decar1 = "	decar1 (000 111 1 x)\n"
        self.decar2 = " decar2 (000 111 1 x)\n"
        self.comment = lambda x: "\n//{}\n".format(x)
        self.w = \
            lambda x: ''' inc (000 111 1 x) //Init State
 addr1 (000 010 {d} x) //Row Addr
 addr2 (000 000 {d} x) //Col Addr
 inc (000 000 {d} x) //Write D={d}
 inc (000 111 1 x)\n'''.format(d=x)
        self.r = \
            lambda x: ''' inc (000 111 1 x) //Init State
 addr1 (000 011 1 x) //Row Addr
 addr2 (000 001 1 x) //Col Addr
 inc (000 001 1 {q}) //Test Q =? {q}
 inc (000 111 1 x)\n'''.format(q='H' if x == 1 else 'L')

        self.all_diag_loop = \
            lambda num, rw: ''' ldc, 511 (000 111 0 x)
lp1x{num} inc (000 111 0 x)
 ldc, 511 (000 111 0 x)
lp2x{num} '''.format(num=num) + rw + ''' loop, lp2x{num} (000 111 0 x)
 incar1 (000 111 0 x)
 loop, lp1x{num} (000 111 0 x)\n'''.format(num=num)
        self.loop = \
            lambda num, rw, loop_times=511: ''' ldc, {loop_times} (000 111 1 x)
lp_x{num} inc (000 111 1 x)\n'''.format(num=num, loop_times=loop_times) + \
            rw + ''' loop, lp_x{num} (000 111 1 x)\n'''.format(num=num)

    def fun_loop(self):

        mono_r = lambda x: self.r(x) + ''' incar1 (000 111 0 x)\n incar2 (000 111 0 x)\n'''
        mono_w = lambda x: self.w(x) + ''' incar1 (000 111 0 x)\n incar2 (000 111 0 x)\n'''

        # Init All Cell Set 1
        init = self.comment("Init") + self.all_diag_loop(0, mono_w(1))
        # Diag write 0
        diag_w0 = self.comment("Diag Write 0") + self.loop('diag_w0', mono_w(0))
        # Diag read 0
        diag_r0 = self.comment("Diag Read 0") + self.loop('diag_r0', mono_r(0))
        # Background Read 1
        bg_r1 = self.comment("Background Read 1") + self.incar1
        bg_read_tmp = self.loop('bg_lp_inner', mono_r(1))
        bg_r1 += self.loop('bg_r1', bg_read_tmp + self.incar1, 510)
        # Background reset - diag write 1
        bg_w1 = self.comment("Background Reset") + self.loop('bg_w1', mono_w(1))
        # INCAR next diag
        next_diag = self.comment("Move to Next Diag") + self.incar1

        mdc_code = init + self.loop('outer', diag_w0 + diag_r0 + bg_r1 + bg_w1 + next_diag)
        return mdc_code

    def main_gen(self):
        self.f.write(self.file_header)
        # one bit test
        content = self.start_index(0) + self.ldar1(1) + self.ldar2(1)
        for i in range(3):
            content += self.w(1) + self.r(1) + self.w(0) + self.r(0)
        content += self.halt
        self.f.write(content)

        # error test
        content = self.start_index(1) + self.ldar1(1) + self.ldar2(1)
        for i in range(2):
            content += self.w(1) + self.r(0) + self.w(0) + self.r(1)
        content += self.halt
        self.f.write(content)

        # fun_all_loop_test
        content = self.start_index(2) + self.ldar1(0) + self.ldar2(0)
        content += self.fun_loop()
        content += self.halt
        self.f.write(content)

        self.f.write(self.file_end)

    def __del__(self):
        print("MDC File Generated")
        self.f.close()


if __name__ == "__main__":
    mdcGen_inst = MDCGen()
    mdcGen_inst.main_gen()
