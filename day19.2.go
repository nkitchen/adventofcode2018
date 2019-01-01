package main

import "bufio"
import "fmt"
import "log"
import "os"

func addr(regs []int, a, b, c int) {
	regs[c] = regs[a] + regs[b]
}

func addi(regs []int, a, b, c int) {
	regs[c] = regs[a] + b
}

func mulr(regs []int, a, b, c int) {
	regs[c] = regs[a] * regs[b]
}

func muli(regs []int, a, b, c int) {
	regs[c] = regs[a] * b
}

func banr(regs []int, a, b, c int) {
	regs[c] = regs[a] & regs[b]
}

func bani(regs []int, a, b, c int) {
	regs[c] = regs[a] & b
}

func borr(regs []int, a, b, c int) {
	regs[c] = regs[a] | regs[b]
}

func bori(regs []int, a, b, c int) {
	regs[c] = regs[a] | b
}

func setr(regs []int, a, b, c int) {
	_ = b
	regs[c] = regs[a]
}

func seti(regs []int, a, b, c int) {
	_ = b
	regs[c] = a
}

func boolToInt(b bool) int {
	if b {
		return 1
	} else {
		return 0
	}
}

func gtir(regs []int, a, b, c int) {
	regs[c] = boolToInt(a > regs[b])
}

func gtri(regs []int, a, b, c int) {
	regs[c] = boolToInt(regs[a] > b)
}

func gtrr(regs []int, a, b, c int) {
	regs[c] = boolToInt(regs[a] > regs[b])
}

func eqir(regs []int, a, b, c int) {
	regs[c] = boolToInt(a == regs[b])
}

func eqri(regs []int, a, b, c int) {
	regs[c] = boolToInt(regs[a] == b)
}

func eqrr(regs []int, a, b, c int) {
	regs[c] = boolToInt(regs[a] == regs[b])
}

type instf func(regs []int, a, b, c int)

var byName = map[string]instf {
    "addr": addr,
    "addi": addi,
    "mulr": mulr,
    "muli": muli,
    "banr": banr,
    "bani": bani,
    "borr": borr,
    "bori": bori,
    "setr": setr,
    "seti": seti,
    "gtir": gtir,
    "gtri": gtri,
    "gtrr": gtrr,
    "eqir": eqir,
    "eqri": eqri,
    "eqrr": eqrr,
}

type inst struct {
	op string
	a, b, c int
}

func main() {
	prog := []inst{}
	ipReg := -1
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		line := scanner.Text()
		var reg int
		_, err := fmt.Sscanf(line, "#ip %d", &reg)
		if err == nil {
			if len(prog) > 0 {
				log.Fatal("#ip after instruction")
			}
			if ipReg != -1 {
				log.Fatal("Duplicate #ip:", reg)
			}
			ipReg = reg
			continue
		}

		var op string
		var a, b, c int
		_, err = fmt.Sscanf(line, "%s %d %d %d", &op, &a, &b, &c)
		if err != nil {
			log.Fatal("Unable to parse line:", line)
		}
		prog = append(prog, inst{op, a, b, c})
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	// 9 {gtrr 3 4 5} [0 1 9 167 10551275 0]
	primes := []int{5, 5, 7, 60293}
	factors := map[int]bool{}
    
	for b := 0; b < 16; b++ {
		m := 1
		for i := uint(0); i < 4; i++ {
			if (b >> i) & 1 == 1 {
				m *= primes[i]
			}
		}
		factors[m] = true
	}
	s := 0
	for f := range factors {
		s += f
	}
	fmt.Println(s)
	os.Exit(0)

	regs := []int{s, 10551275, 7, 1, 10551275, 1}
	ip := 8
	for 0 <= ip && ip < len(prog) {
		regs[ipReg] = ip
		inst := prog[ip]
		f := byName[inst.op]
		f(regs, inst.a, inst.b, inst.c)

		fmt.Println(ip, inst, regs)

		ip = regs[ipReg]
		ip++

		if inst.c == 0 && regs[0] != 0 {
			//fmt.Println(ip, inst, regs)
		}
	}

	fmt.Println(regs[0])
}
