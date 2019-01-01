#include <stdio.h>

int main() {
    int u = 0, v = 0, w = 0, x = 0, y = 0, z = 0;

    L00: w = w + 16;
    // w == 16
    goto labels[w + 1];

    L01: v = 1;              // [0 1 1 0 10551275 10550400]
    L02: x = 1;            // [0 1 2 1 10551275 10550400]

    L03: z = v * x;   // [0 1 3 1/2 10551275 1]
    L04: z = z == y;  // [0 1 4 1/2 10551275 0]
    L05: w = z + w;     // [0 1 5 1/2 10551275 0]
    // w += (v * x == y);
    goto labels[w + 1];

    L06: w = w + 1;        // [0 1 7 1/2 10551275 0]
    goto L08;

    L07: u = v + u;
    // Add v to u for each time v * x == y
    // Add v to u for each time v * x == 10551275
    L08: x = x + 1;    // [0 1 8 2/3 10551275 0]
    L09: z = x > y;  // [0 1 9 2/3 10551275 0]
    L10: w = w + z;     // [0 1 10 2/3 10551275 0]
    goto labels[w + 1];

    L11: w = 2;              // [0 1 2 2/3 10551275 0]
    goto L03;

    L12: v = v + 1;
    L13: z = v > y;
    L14: w = z + w;
    goto labels[w + 1];

    L15: w = 1;
    goto labels[w + 1];

    L16: w = w * w;
    goto labels[w + 1];

    L17: y = y + 2;      // y == 2
    L18: y = y * y;   // y == 4
    L19: y = w * y;    // y == 76
    L20: y = y * 11;     // y == 836
    L21: z = z + 1;      // z == 1
    L22: z = z * w;    // z == 22
    L23: z = z + 17;     // z == 39
    L24: y = y + z;   // y == 875
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
    L33: y = y + z;   // y == 10551275
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
	y = y + 2;
	y = y * y;
	y = (19) * y;
	y = y * 11;
	z = z + 1;
	z = z * w;
	z = z + 17;
	y = y + z;
L25:
	w = w + u;
L27:
	z = w;
	z = z * w;
	z = w + z;
	z = w * z;
	z = z * 14;
	z = z * w;
	y = y + z;
	u = 0;
	w = 0;
L01:
	v = 1;
	x = 1;
L03:
	//z = v * x;
	z = (v * x == y);
	w = z + w;
L06:
	w = w + 1;
L08:
	x = x + 1;
	z = (x > y);
L10:
	//w = w + z;
L11:
	//w = 2;
	if x <= y {
		goto L03;
	}

	z = v * x;
	z = (z == y);
	w = z + w;
	w = w + 1;
	x = x + 1;
	z = (x > y);
	w = w + z;
	w = 2;
#endif
}
