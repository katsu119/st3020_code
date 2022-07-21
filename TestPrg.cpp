//TMS4256测试程序

#include "StdAfx.h"
#include "testdef.h"
#include "data.h"
#include "math.h"

#define INDEX_VOH 4
void PASCAL TMS4256()
{
	//48 47 46 45 44
	//R  C  W  D  Q
	
    //连接性测试
#if 1
	SET_DPS(1,0,V,30,MA);
	PMU_CONDITIONS(FIMV,-0.1,MA,2,V);
	//if(!PMU_MEASURE("1-9,35-36,44-46",5,"CON_",V,-0.1,-1.9))
	if(!PMU_MEASURE("1-9,44-48",5,"CON_",V,-0.1,-1.9))
		BIN(1);
#endif

	//功能测试   vcc最大最小
	SET_DPS(1,4.5,V,70,MA);
	SET_INPUT_LEVEL(2.4, 0.8);
	SET_OUTPUT_LEVEL(2.4, 0.4);
	//		SET_PERIOD(60);
	//		SET_TIMING(20,30,30);
	SET_PERIOD(60);
	SET_TIMING(10,40,30);
	//			ADDR  D  R
	//FORMAT(NRZ0, "1-9,45,48");
	//FORMAT(RO, "46,47");
	FORMAT(NRZ0, "1-9,44-48");

#if 1
	if(!RUN_PATTERN("ALL_W1R1",65,1,2,0))
		BIN(2); 
	if(!RUN_PATTERN("ALL_W0R0",66,1,2,0))
		BIN(2); 
	if(!RUN_PATTERN("FUN_LOOP",67,1,2,0))
		BIN(2); 
#endif

#if 0
	for(int i = 0; i < 52; ++i)
	{
		char tmp[50];
		sprintf(tmp, "FUN_4V5__%d", i);
		if(!RUN_PATTERN(tmp,i+13,1,2,0))
		//(CString csItem ,int start_idx,int get_fail,int apgen，int time_range)
			BIN(2);
	}
#endif
	// SET_DPS(1,5.5,V,70,MA);
	// Delay(100);
	// if(!RUN_PATTERN("FUN_5V5",0,1,2,0))
	// 	BIN(2);
	// DPS_OFF(DPS1);

	Delay(200);
/*
	 //功能测试   vcc最大最小
		SET_DPS(1,4.5,V,70,MA);
		SET_INPUT_LEVEL(2.4, 0.8);
		SET_OUTPUT_LEVEL(2.4, 0.4);
//		SET_PERIOD(60);
//		SET_TIMING(20,30,30);
		SET_PERIOD(2000);
		SET_TIMING(400,500,1220);
		FORMAT(NRZ0, "1-9,35,44-46");
		if(!RUN_PATTERN("FUN_4V5",0,1,2,0))
			BIN(2);
		

		SET_DPS(1,5.5,V,70,MA);
		Delay(100);
		if(!RUN_PATTERN("FUN_5V5",0,1,2,0))
			BIN(2);

	DPS_OFF(DPS1);
	Delay(100);
*/
	//VOH测试
	SET_DPS(1,4.5,V,70,MA);
	SET_INPUT_LEVEL(4.5,0);
	SET_PERIOD(2000);
	SET_TIMING(400,500,1220);
	FORMAT(NRZ0, "1-9,35,44-46");
	RUN_PATTERN(1,1,0,0);
	PMU_CONDITIONS(FIMV,-5,MA,5,V);
	if(!PMU_MEASURE("36",10,"VOH4V5_",V,No_UpLimit,2.4))
		BIN(3);
	//	
	//
	//
 	//VOL测试
 	SET_DPS(1,4.5,V,70,MA);
	SET_INPUT_LEVEL(2.4, 0.8);
	RUN_PATTERN(2,1,0,0);
	PMU_CONDITIONS(FIMV,8,MA,0.6,V);
	if(!PMU_MEASURE("36",5,"VOL4V5_",V,0.4,No_LoLimit))
 		BIN(4);	
	//		
	//
	
	
	//Ii测试
	SET_DPS(1,5,V,70,MA);
	SET_INPUT_LEVEL(5, 0);
	RUN_PATTERN(3,1,0,0);
	PMU_CONDITIONS(FVMI,0,V,0.01,MA);
	if(!PMU_MEASURE("1-9,35,44-46",5,"Ii0V_",UA,10,-10))
		BIN(5);	
		

	RUN_PATTERN(4,1,0,0);
	PMU_CONDITIONS(FVMI,6.5,V,10,UA);
	if(!PMU_MEASURE("1-9,35,44-46",5,"Ii6V5_",UA,10,-10))    //
		BIN(5);		
	
	//	
	////Io测试

	SET_DPS(1,5,V,70,MA);
	RUN_PATTERN(5,1,0,0);
	PMU_CONDITIONS(FVMI,5.5,V,15,UA);
	if(!PMU_MEASURE("36",5,"Io6V5_",UA,10,-10))
		BIN(6);
	
	PMU_CONDITIONS(FVMI,0,V,20,UA);
	if(!PMU_MEASURE("36",5,"Io0V_",UA,10,-10))  //
		BIN(6);	

	//IDD1
	SET_DPS(1,5.5,V,70,MA);
	SET_PERIOD(55);
	SET_TIMING(20,30,30);
	RUN_PATTERN(6,1,0,0);
	if(!DPS_MEASURE(DPS1,R200MA,10,"IDD1W_",MA,65,No_LoLimit))    
		BIN(7);	
	RUN_PATTERN(7,1,0,0);
	if(!DPS_MEASURE(DPS1,R200MA,10,"IDD1R_",MA,65,No_LoLimit))    
		BIN(7);	
	
	
	//IDD2
	SET_DPS(1,5.5,V,70,MA);
	RUN_PATTERN(8,1,0,0);
	if(!DPS_MEASURE(DPS1,R20MA,10,"IDD2Wr_",MA,4.5,No_LoLimit))   
		BIN(8);	
	RUN_PATTERN(9,1,0,0);
	if(!DPS_MEASURE(DPS1,R20MA,10,"IDD2Re_",MA,4.5,No_LoLimit))   
		BIN(8);
	
	//IDD3
	SET_DPS(1,5.5,V,70,MA);
	SET_PERIOD(110);
	SET_TIMING(30,70,70);
	RUN_PATTERN(10,1,0,0);
	if(!DPS_MEASURE(1,R200MA,5,"IDD3_",MA,53,No_LoLimit))    //
		BIN(9);
	
	//IDD4
	SET_DPS(1,5.5,V,70,MA);
	SET_PERIOD(60);
	SET_TIMING(20,30,30);
	RUN_PATTERN(11,1,0,0);
	if(!DPS_MEASURE(1,R200MA,5,"IDD4_Re",MA,45,No_LoLimit))    //
		BIN(10);
	RUN_PATTERN(12,1,0,0);
	if(!DPS_MEASURE(1,R200MA,5,"IDD4_Wr",MA,45,No_LoLimit))    //
		BIN(10);
}

#if 0
 //Read H
 inc (000 111 1 x) //Init State
 addr1 (000 011 1 x) //Row Addr
 addr2 (000 001 1 x) //Col Addr
 inc (000 001 1 H) //Test Q For H
 inc (000 011 1 x)
 inc (000 111 1 x)
 inc (000 111 1 x)
 //Read L
 inc (000 111 1 x) //Init State
 addr1 (000 011 1 x) //Row Addr
 addr2 (000 001 1 x) //Col Addr
 inc (000 001 1 L) //Test Q For L
 inc (000 011 1 x)
 inc (000 111 1 x)
 inc (000 111 1 x)
 //Write 1
 inc (000 110 1 x)
 addr1 (000 010 1 x)
 addr2 (000 000 1 x)
 inc (000 000 1 x)
 inc (000 011 1 x)
 inc (000 111 1 x)
 inc (000 111 1 x)
 //Write 0
 inc (000 110 1 x)
 addr1 (000 010 0 x)
 addr2 (000 000 0 x)
 inc (000 000 0 x)
 inc (000 011 0 x)
 inc (000 111 1 x)
 inc (000 111 1 x)
#endif