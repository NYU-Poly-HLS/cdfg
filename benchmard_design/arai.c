/* Program for DCT-II, N=8, based on 
   Arai's fast DCT algorithm
   Pennebraker & Mitchell, "JPEG"
   p. 52.

   Author:   Miodrag Potkonjak
   January 1995.

    DIF = .5 * Arai * sec(pi*u/16)  u=1..7
    DIF = Arai                      u = 0
    simulated and changed (lmg)
*/

//#define  num8 fix<8,6>
#define  num8 (short)

//#define  num12 fix<12,10>
#define  num12 (short)

#define  m1  num12 (7071)    
#define  m2  num12 (3826)   
#define  m3  num12 (5411)    
#define  m4  num12 (13060)    


short y10, y11, y12, y13, y14, y15, y16, y17;

void arai(short x10, short x11, short x12, short x13,
          short x14, short x15, short x16, short x17)         
{
  short b0, b1, b2, b3, b4, b5, b6;
  short c0, c1, c3;
  short d2, d3, d4, d5, d6, d7, d8;
  short e2, e3, e4, e5, e6, e7, e8;
  short f4, f5, f6, f7;
    
  b0 = x10 + x17;
  b1 = x11 + x16;
  b2 = x13 - x14;
  b3 = x11 - x16;
  b4 = x12 + x15;
  b5 = x13 + x14;
  b6 = x12 - x15;
  d8 = x10 - x17;

  c0 = b0 + b5;
  c1 = b1 - b4;
  d2 = -(b2 + b6);
  c3 = b1 + b4;
  d5 = b0 - b5;
  d6 = b3 + d8;
  d7 = b3 + b6;

  d3 = c1 + d5;
  d4 = d2 + d6;

  e2 = num8 (m3 * d2);
  e3 = num8 (m1 * d7);
  e4 = num8 (m4 * d6);
  e5 = d5;
  e6 = num8 (m1 * d3);
  e7 = num8 (m2 * d4);
  e8 = d8;
  
  f4 = e3 + e8;
  f5 = e8 - e3;
  f6 = -(e2 + e7);
  f7 = e4 - e7;
  
  y10 = c0 + c3;
  y14 = c0 - c3;

  y12 = e5 + e6;
  y16 = e5 - e6;

  y11 = f4 + f7;
  y13 = f5 - f6;
  y15 = f5 + f6;
  y17 = f4 - f7;
}

