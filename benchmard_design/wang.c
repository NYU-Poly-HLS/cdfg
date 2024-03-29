/* Program for DCT-II, N=8, based on 
   Z. Wang: "Fast Algorithms for discrete W transform and for the
   discrete Fourier Transform", IEEE Transactions on Acoustic, Speech,
   and Signal porcessing, Vol. 32, No. 8, pp.803-816, 1994.

   Also in Rao & Yip  pp. 370-380 

   Author:   Miodrag Potkonjak
   January 1994.

   simulated and corrected (lmg)
*/

/*#define  num8 fix<8,8> */
#define  num8 (short)
/*#define  num12 fix<12,11>*/
#define  num12 (short)

#define  C1I4  num12(3535)
#define  S1I4  num12(3535)
#define  C1I8  num12(4619)
#define  S1I8  num12(1913)
#define  C1I4B num12(4999)
#define  S1I4B num12(4999)
#define  V1  num12(7071)
#define  C1I16  num12(9807)
#define  S1I16  num12(1950)
#define  C5I16  num12(5555)
#define  S5I16  num12(8314)





void WANG (short x11, short x12, short x13, short x14, short x15,
           short x16, short x17, short x18,
           
           short *y1, short *y2, short *y3, short *y4, short *y5,
           short *y6, short *y7, short *y8 )

{
short x21, x22, x23, x24, x25, x26, x27, x28,
  x31, x32, x33, x34,
  x81, x82, x83, x84,
  x91, x92, x93, x94;

 x21 = x11 + x18;
 x22 = x12 + x17;
 x23 = x13 + x16;
 x24 = x14 + x15;
 x25 = x14 - x15;
 x26 = x13 - x16;
 x27 = x12 - x17;
 x28 = x11 - x18;

 x31 = x21 + x24;
 x32 = x22 + x23;
 x33 = x22 - x23;
 x34 = x21 - x24;

  *y1 = num8 ((x31 + x32) * C1I4);
  *y5 = num8 ((x31 - x32) * C1I4);
  *y7 = num8 ( num8 (x34 * S1I8) - num8 (x33 * C1I8));
  *y3 = num8 ( num8 (x34 * C1I8) + num8 (x33 * S1I8));

  x81 = num8 (x28 * V1);
  x82 = num8 (x25 * V1);
  x83 = num8 ((x27 + x26) * C1I4B);
  x84 = num8 ((x27 - x26) * C1I4B);

  x91 = num8 ((x81 + x83) * V1);
  x92 = num8 ((x82 + x84) * V1);
  x93 = num8 ((x81 - x83) * V1);
  x94 = num8 ((x82 - x84) * V1);

  *y2 = num8 (x91 * C1I16) + num8 (x92 * S1I16);
  *y8 = num8 (x91 * S1I16) - num8 (x92 * C1I16);
  *y6 = num8 (x93 * C5I16) + num8 (x94 * S5I16);
  *y4 = num8 (x93 * S5I16) - num8 (x94 * C5I16);
}
