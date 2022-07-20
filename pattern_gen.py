import sys


class MdcGenerator:
    def __init__(self):
        self.f = open(r".\tms4256.mdc", "w")
        self.file_header = \
            """mem_source_15;
pindef

addr(0..8) = i, hex, (1,2,3,4,5,6,7,8,9)
ras_ = i, bin, (46)
cas_ = i, bin, (45)
w_ = i, bin, (44)

d = i, bin, (35)
q = o, bin, (36)

main_f
//ADDR1 as row
//ADDR2 as colum
"""

        self.file_end = """end."""
        self.start_index = lambda num: '\nstart_index({})\n'.format(num)
        self.halt = '  halt  (000 111 0 x) \n'
        self.w0 = \
            '''  addr1   (000 110 0 x)
  inc     (000 010 0 x)
  addr2   (000 010 0 x)
  inc     (000 000 0 x)
  inc     (000 111 1 x)
  '''
        self.w1 = \
            '''  addr1   (000 110 1 x)
  inc     (000 010 1 x)
  addr2   (000 010 1 x)
  inc     (000 000 1 x)
  inc     (000 111 1 x)
  '''
        self.r0 = \
            '''  addr1   (000 111 0 x)
  inc     (000 011 0 x)
  addr2   (000 011 0 x)
  inc     (000 001 0 L)
  inc     (000 111 1 x)
  '''
        self.r1 = \
            '''  addr1   (000 111 x x)
  inc     (000 011 x x)
  addr2   (000 011 x x)
  inc     (000 001 x H)
  inc     (000 111 1 x)
  '''
        self.incar1 = "	incar1	(000 110 0 x)\n"
        self.incar2 = "	incar2	(000 110 0 x)\n"
        self.code_other = \
            '''
    start_index(1)    //VOH
      //AAA RCW DQ
      inc   (000 110 1 x)
      inc   (000 010 1 x)
      inc   (000 000 1 x) //写入000处 1
      inc   (000 111 1 x)
      inc   (000 111 1 x)
      inc   (000 011 1 x)
      inc   (000 001 1 x)
      halt  (000 001 1 x)
    
    start_index(2)   //VOL
      //AAA RCW DQ
      inc   (000 110 0 x)
      inc   (000 110 0 x)
      inc   (000 010 0 x)
      inc   (000 000 0 x) //写入000处 0
      inc   (000 111 0 x)
      inc   (000 111 0 x)
      inc   (000 011 0 x)
      inc   (000 001 0 x)
      halt  (000 001 0 x) 
    
    
    start_index(3)  //IIL
      //AAA RCW DQ
      inc   (111 111 1 x)
      inc   (111 111 1 x)
      inc   (111 111 1 x)
      inc   (111 111 1 x)
      halt  (111 111 1 x)
    
    start_index(4)  //IIH
      //AAA RCW DQ
      inc   (000 000 0 x)
      inc   (000 000 0 x)
      inc   (000 000 0 x)
      inc   (000 000 0 x)
      halt  (000 000 0 x)
    
    start_index(5)  //IO
      //AAA RCW DQ
      INC   (xxx x1x x x)
      INC   (xxx x1x x x)
      INC   (xxx x1x x x)
      INC   (xxx x1x x x)
      HALT  (xxx x1x x x)
    
    
    
    start_index(6)    //IDD1-W
      //AAA RCW DQ
      INC   (000 110 0 x)
      INC   (000 010 0 x)
      INC   (000 000 0 x)
      HALT  (000 010 0 x) 
    
    START_INDEX(7)    //IDD1-Re
      //AAA RCW DQ
      INC   (000 111 0 x)
      INC   (000 011 0 x)
      INC   (000 001 0 x)
      HALT  (000 011 0 x)
    
    start_index(8)   //IDD2-Wr
      //AAA RCW DQ
      INC   (000 110 0 x)
      INC   (000 010 0 x)
      INC   (000 000 0 x)
      INC   (000 010 0 x)
      HALT  (000 110 0 x)
    
    START_INDEX(9)    //IDD2-Re
      //AAA RCW DQ
      INC   (000 111 0 x)
      INC   (000 011 0 x)
      INC   (000 001 0 x)
      INC   (000 011 0 x)
      HALT  (000 111 0 x)
    
    start_index(10)  //IDD3
      //AAA RCW DQ
      LDF   (000 101 0 x)
    A1 INC  (000 011 0 x)
      INC   (000 111 0 x)  
      JMP,A1 (000 011 0 x)
      HALT  (000 111 0 x)
    
    start_index(11)   //page Re
      //AAA RCW DQ
      LDF   (000 111 0 x)
    C1 INC  (000 011 0 x)
      INC   (000 001 0 x)
      JMP,C1 (000 011 0 x)  
      HALT  (000 011 0 x)
    
    start_index(12)   //page Wr
      //AAA RCW DQ
      LDF   (000 110 0 x)
    D1 INC  (000 010 0 x)
      INC   (000 000 0 x)
      JMP,D1 (000 010 0 x)  
      HALT  (000 010 0 x)
     '''
        self.code_fun_loop = \
            '''
      //功能测试
      ldar1, 0	(000 110 0 x)
      ldar2, 0	(000 110 0 x)
    
      ldc, 511	(000 110 0 x)  //写1
    lp1	inc	(000 110 0 x) //对所有单元格写1
      ldc, 511	(000 110 0 x)
    lp2 addr1   (000 110 1 x)
      inc     (000 010 1 x)
      addr2   (000 010 1 x)
      inc     (000 000 1 x)
      inc     (000 111 1 x)
      incar1	(000 110 0 x)
      incar2	(000 110 0 x)
      loop, lp2	(000 110 0 x)
        incar1	(000 110 0 x)
      loop, lp1	(000 110 0 x)
    
    
      ldar1, 0	(000 110 0 x)
      ldar2, 0	(000 110 0 x)
      ldc, 511  (000 110 0 x)
    f inc     (000 110 0 x) //对角线大循环
    
      ldc, 511 (000 110 0 x) //当前对角线写0
    a addr1   (000 110 0 x)
      inc     (000 010 0 x)
      addr2   (000 010 0 x)
      inc     (000 000 0 x)
      inc     (000 111 1 x)
      incar1	(000 110 0 x)
      incar2	(000 110 0 x)
      loop, a	(000 110 0 x)
    
      ldc, 511 (000 110 0 x)
    b addr1   (000 111 0 x) //读取数据进行验证--对角线
      inc     (000 011 0 x)
      addr2   (000 011 0 x)
      inc     (000 001 0 L)
      inc     (000 111 1 x)
      incar1	(000 110 0 x)
      incar2	(000 110 0 x)
      loop, b	(000 110 0 x)
    //刷新
    // inc     (000 10x x x)
    // addr1   (000 11x x x)
    // inc     (000 01x x x)
    //读1
      ldc, 511     (000 110 x x)//读取数据进行验证--背景
    c incar1	(000 110 x x) 
      ldc, 511     (000 110 x x)
    d addr1   (000 111 x x)
      inc     (000 011 x x)
      addr2   (000 011 x x)
      inc     (000 001 x H)
      inc     (000 111 1 x)
      incar1	(000 110 x x)
      incar2	(000 110 x x)
      loop, d	(000 110 x x)
    //刷新
    // inc     (000 10x x x)
    // addr1   (000 11x x x)
    // inc     (000 01x x x)
      loop, c  (000 110 x x)
    
    //补1
      //incar1	(000 110 x x)
    
      ldc, 511 (000 110 x x)
    e addr1   (000 110 1 x)
      inc     (000 010 1 x)
      addr2   (000 010 1 x)
      inc     (000 000 1 x)
      inc     (000 111 1 x)
      incar1	(000 110 x x)
      incar2	(000 110 x x)
      loop, e	(000 110 x x)
    
        incar1	(000 110 x x) //转移到下一个对角线
      loop, f	(000 110 x x)
    
      '''

    def diagonal_line(self, line_n):
        code_diag_write = \
            '''
  //第{a}条对角线写0
  ldar1, 0	(000 110 0 x)
  ldar2, {col}	(000 110 0 x)
  ldc, 511 (000 110 0 x) //当前对角线写0
w{a}  addr1  (000 110 0 x)
  inc     (000 010 0 x)
  addr2   (000 010 0 x)
  inc     (000 000 0 x)
  inc     (000 111 1 x)
  incar1	(000 110 0 x)
  incar2	(000 110 0 x)
  loop, w{a}	(000 110 0 x)
'''.format(col=line_n, a=line_n)
        code_diag_clear = \
            '''
  //第{a}条对角线置1
  ldar1, 0	(000 110 0 x)
  ldar2, {col}	(000 110 0 x)
  ldc, 511 (000 110 0 x) //当前对角线写1
x{a}  addr1  (000 110 1 x)
  inc     (000 010 1 x)
  addr2   (000 010 1 x)
  inc     (000 000 1 x)
  inc     (000 111 1 x)
  incar1	(000 110 0 x)
  incar2	(000 110 0 x)
  loop, x{a}	(000 110 0 x)
'''.format(col=line_n, a=line_n)
        code_diag_read = \
            '''
  //第{x}条对角线--读取验证
  ldar1, 0	(000 110 0 x)
  ldar2, {col}	(000 110 0 x)
  ldc, 511 (000 110 0 x)
rdiag{x} addr1   (000 111 0 x) //读取数据进行验证--对角线
  inc     (000 011 0 x)
  addr2   (000 011 0 x)
  inc     (000 001 0 L)
  inc     (000 111 1 x)
  incar1	(000 110 0 x)
  incar2	(000 110 0 x)
  loop, rdiag{x}	(000 110 0 x)
'''.format(col=line_n, x=line_n)
        code_background_read = \
            '''
  //第{x}条对角线--读取背景验证
  ldar1, 0	(000 110 0 x)
  ldar2, {col}	(000 110 0 x)
  ldc, 511     (000 110 x x)//读取数据进行验证--背景
bg1r{x} incar1	(000 110 x x) 
  ldc, 511     (000 110 x x)
bg2r{x} addr1   (000 111 x x)
  inc     (000 011 x x)
  addr2   (000 011 x x)
  inc     (000 001 x H)
  inc     (000 111 1 x)
  incar1	(000 110 x x)
  incar2	(000 110 x x)
  loop, bg2r{x}	(000 110 x x)
  loop, bg1r{x}	(000 110 x x)
'''.format(col=line_n, x=line_n)

        return code_diag_write + code_diag_read + code_background_read + code_diag_clear

    def code_gen(self):
        code_all_clear = \
            lambda x: '''
  //清除所有，all set 1
  ldar1, 0	(000 110 0 x)
  ldar2, 0	(000 110 0 x)
  ldc, 511	(000 110 0 x)
lp1x{a}	inc	(000 110 0 x) //对所有单元格写1
  ldc, 511	(000 110 0 x) 
lp2x{a} addr1   (000 110 1 x)
  inc     (000 010 1 x)
  addr2   (000 010 1 x)
  inc     (000 000 1 x)
  inc     (000 111 1 x)
  incar1	(000 110 0 x)
  incar2	(000 110 0 x)
  loop, lp2x{a}	(000 110 0 x)
    incar1	(000 110 0 x)
  loop, lp1x{a}	(000 110 0 x)
'''.format(a=x)
        code_all_read = \
            lambda x: '''
  //读取所有，all set 1
  ldar1, 0	(000 110 0 x)
  ldar2, 0	(000 110 0 x)
  ldc, 511	(000 110 0 x)
lp1r{a}	inc	(000 110 0 x) //对所有单元格写1
  ldc, 511	(000 110 0 x) 
lp2r{a} addr1   (000 111 1 x)
  inc     (000 011 1 x)
  addr2   (000 011 1 x)
  inc     (000 001 1 H)
  inc     (000 111 1 x)
  incar1	(000 110 0 x)
  incar2	(000 110 0 x)
  loop, lp2r{a}	(000 110 0 x)
    incar1	(000 110 0 x)
  loop, lp1r{a}	(000 110 0 x)
'''.format(a=x)
        self.f.write(self.file_header)
        self.f.write(self.code_other)
        for diag_group in range(52):
            self.f.write(self.start_index(diag_group + 13))
            self.f.write(code_all_clear(diag_group))
            for diag_num in range(10 * diag_group, 512 if 10 * diag_group + 10 > 512 else 10 * diag_group + 10):
                diag_code = self.diagonal_line(diag_num)
                self.f.write(diag_code)
            self.f.write(self.halt)
        test_64 = self.start_index(65) + code_all_clear(65) + code_all_read(65) + self.halt
        self.f.write(test_64)
        test_error = self.start_index(66) + code_all_clear(66) + self.w0 + self.r1 + self.w1 + self.r0 + self.halt
        self.f.write(test_error)
        test_fun_loop = self.start_index(67) + self.code_fun_loop + self.halt
        self.f.write(test_fun_loop)
        self.f.write(self.file_end)

    def __del__(self):
        print("Deconstruct Sphere Class Instance")
        self.f.close()


if __name__ == '__main__':
    mdc_gen_inst = MdcGenerator()
    mdc_gen_inst.code_gen()
