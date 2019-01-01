package main

import "fmt"

func boolToInt(b bool) int {
	if b {
		return 1
	} else {
		return 0
	}
}

func main() {
	var u, v, w, x, y z int

	w = w + 16
	y = y + 2
	y = y * y
	y = (19) * y
	y = y * 11
	z = z + 1
	z = z * w
	z = z + 17
	y = y + z
	w = w + u
	z = w
	z = z * w
	z = w + z
	z = w * z
	z = z * 14
	z = z * w
	y = y + z
	u = 0
	w = 0
	v = 1
	x = 1
L3:
	//z = v * x
	z = boolToInt(v * x == y)
	w = z + w
	w = w + 1
	x = x + 1
	z = boolToInt(x > y)
	//w = w + z
	//w = 2
	if x <= y {
		goto L3
	}

	z = v * x
	z = boolToInt(z == y)
	w = z + w
	w = w + 1
	x = x + 1
	z = boolToInt(x > y)
	w = w + z
	w = 2
}
