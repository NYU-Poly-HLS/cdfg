/* Program for DCT-II, N=8, based on 
   Lee's fast algorithm, Rao & Yip, page 350

   Author:   Miodrag Potkonjak
   January 1994.

   simulated and corrected (Sandeep Singh)
*/

#define  num8 (short)
#define  num12 (short)

#define  C1  num12(5098)
#define  C2  num12(5412)
#define  C3  num12(6013)
#define  C4  num12(7071)
#define  C5  num12(8999)
#define  C6  num12(13065)
#define  C7  num12(25629)
#define  quarter  num12(25)

short y10, y11, y12, y13, y14, y15, y16, y17;

void lee(short x10, short x11, short x12, short x13,
         short x14, short x15, short x16, short x17)
{

    short x20, x21, x22, x23, x24, x25, x26, x27,
          x30, x31, x32, x33, x34, x35, x36, x37,
          x40, x41, x42, x43, x44, x45, x46, x47,
          x50, x51, x52, x53, x54, x55, x56, x57,
          x60, x61, x62, x63, x64, x65, x66, x67,
          x70, x71, x72, x73, x74, x75, x76, x77,
          x80, x81, x82, x83, x84, x85, x86, x87,
          x90, x91, x92, x93, x94, x95, x96, x97; 

    
    x20 = x10 + x17;
    x21 = x11 + x16;
    x22 = x13 + x14;
    x23 = x12 + x15;
    x24 = x10 - x17;
    x25 = x11 - x16;
    x26 = x13 - x14;
    x27 = x12 - x15;

    x30 = x20; 
    x31 = x21; 
    x32 = x22; 
    x33 = x23;
    x34 = num8 (C1 * x24);
    x35 = num8 (C3 * x25);
    x36 = num8 (C7 * x26);
    x37 = num8 (C5 * x27);
 
    x40 = x30 + x32;
    x41 = x31 + x33; 
    x42 = x30 - x32;
    x43 = x31 - x33;
    x44 = x34 + x36; 
    x45 = x35 + x37; 
    x46 = x34 - x36; 
    x47 = x35 - x37; 
    
    x50 = x40;
    x51 = x41;
    x52 = num8 (C2 * x42);
    x53 = num8 (C6 * x43);
    x54 = x44;
    x55 = x45;
    x56 = num8 (C2 * x46);
    x57 = num8 (C6 * x47);

    x60 = x50 + x51;
    x61 = x50 - x51;
    x62 = x52 + x53;
    x63 = x52 - x53;
    x64 = x54 + x55;
    x65 = x54 - x55;
    x66 = x56 + x57;
    x67 = x56 - x57;

    x70 = x60;
    x71 = num8 (C4 * x61);
    x72 = x62;
    x73 = num8 (C4 * x63);
    x74 = x64;
    x75 = num8 (C4 * x65);
    x76 = x66;
    x77 = num8 (C4 * x67);

    x80 = x70;
    x81 = x71;
    x82 = x72 + x73;
    x83 = x73;
    x84 = x74;
    x85 = x75;
    x86 = x76 + x77;
    x87 = x77;

    x90 = x80;
    x91 = x81;
    x92 = x82;
    x93 = x83;
    x94 = x84 + x86;
    x95 = x85 + x87;
    x96 = x85 + x86;
    x97 = x87;
    
    y10 = num8 (quarter * x90);
    y11 = num8 (quarter * x94);
    y12 = num8 (quarter * x92);
    y13 = num8 (quarter * x96);
    y14 = num8 (quarter * x91);
    y15 = num8 (quarter * x95);
    y16 = num8 (quarter * x93);
    y17 = num8 (quarter * x97);
}
