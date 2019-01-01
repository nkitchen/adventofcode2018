#include <stdio.h>

int main() {
    int u = 0, v = 0, w = 0, x = 0, target = 0, z = 0;

    L00: w = w + 16;
    // w == 16
    goto labels[w + 1];

    L01: v = 1;              // [0 1 1 0 10551275 10550400]
    do {
       L02: x = 1;            // [0 1 2 1 10551275 10550400]

       L03:
       do {
          if (v * x == target) {
             // Add v to u for each time v * x == target
             // Add v to u for each time v * x == 10551275
             u += v;
          }

          L08: x = x + 1;    // [0 1 8 2/3 10551275 0]
          L09: z = (x > target);  // [0 1 9 2/3 10551275 0]
       } while (x <= target);

       L12: v = v + 1;
    } while (v <= target);
    
    L16: w = w * w;
    goto labels[w + 1];

    L17: target = target + 2;      // target == 2
    L18: target = target * target;   // target == 4
    L19: target = w * target;    // target == 76
    L20: target = target * 11;     // target == 836
    L21: z = z + 1;      // z == 1
    L22: z = z * w;    // z == 22
    L23: z = z + 17;     // z == 39
    L24: target = target + z;   // target == 875
    L25: w = w + u;     // w == 26
    goto labels[w + 1];

    L26: w = 0;
    goto L01;

    L27: z = w;           // z == 27
    L28: z = z * w;    // z == 756
    L29: z = w + z;    // z == 785
    L30: z = w * z;    // z == 23550
    L31: z = z * 14;     // z == 329700
    L32: z = z * w;    // z == 10550400
    L33: target = target + z;   // target == 10551275
    L34: u = 0;
    L35: w = 0;              // [0 0 0 0 10551275 10550400]
    goto L01;

    void *labels = {
        &&L00,
        &&L01,
        &&L02,
        &&L03,
        &&L04,
        &&L05,
        &&L06,
        &&L07,
        &&L08,
        &&L09,
        &&L10,
        &&L11,
        &&L12,
        &&L13,
        &&L14,
        &&L15,
        &&L16,
        &&L17,
        &&L18,
        &&L19,
        &&L20,
        &&L21,
        &&L22,
        &&L23,
        &&L24,
        &&L25,
        &&L26,
        &&L27,
        &&L28,
        &&L29,
        &&L30,
        &&L31,
        &&L32,
        &&L33,
        &&L34,
        &&L35,
    };

#if 0
L00:
    w = w + 16;
L17:
	target = target + 2;
	target = target * target;
	target = (19) * target;
	target = target * 11;
	z = z + 1;
	z = z * w;
	z = z + 17;
	target = target + z;
L25:
	w = w + u;
L27:
	z = w;
	z = z * w;
	z = w + z;
	z = w * z;
	z = z * 14;
	z = z * w;
	target = target + z;
	u = 0;
	w = 0;
L01:
	v = 1;
	x = 1;
L03:
	//z = v * x;
	z = (v * x == target);
	w = z + w;
L06:
	w = w + 1;
L08:
	x = x + 1;
	z = (x > target);
L10:
	//w = w + z;
L11:
	//w = 2;
	if x <= target {
		goto L03;
	}

	z = v * x;
	z = (z == target);
	w = z + w;
	w = w + 1;
	x = x + 1;
	z = (x > target);
	w = w + z;
	w = 2;
#endif
}
