# golang-关于Strings
String类型的内部细节
```go
type stringStruct struct {
	str unsafe.Pointer
	len int
}
```
关于String类型你需要了解的一些基本知识
1. 不可变的字节序列（immutable）
就是说你不能这么操作
```go
s := "hello, world"
s[0] = "j" // 编译错误
```
2. len 函数返回的是字节的数量，而不是字符的数量，这个是有区别的，因为golang中字符串默认是utf-8编码的，utf-8编码字符占用的字节数从1-4不等。
```go
import (
	"fmt"
	"unicode/utf8"
)
s := "hello, 世界"
// len(s)获取s包含的字节数量
// utf8.RuneCountInString 获取s包含的字符的数量
// 也可以用strings.Count(s, "")获取s包含的字符的数量
fmt.Printf("%d, %d \n", len(s), utf8.RuneCountInString(s))
// 如果想要获取每一个字符，可以通过utf8.DecodeRuneInString获取
for i := 0; i < len(s); {
		r, size := utf8.DecodeRuneInString(s[i:])
		fmt.Printf("%d\t%c\n", i, r)
		i += size
	}

```

3. 字符串连接可以通过操作符“+”实现，获取子字符串可以通过索引片获取，新的字符串和原来的字符串有没有什么关系？在内存上是如何分配的？这就涉及到文章一开始提到的string类型的内部结构。
	- 字符串拼接之后，存储字符串的地址是否会发生变化？会发生变化，相当于新开辟了一块内存
	-  [] 获取的子字符串的指针（elements）和原字符串的指针（elements）指向同一块地址空间，子字符串的指针（elements）等于原字符串的指针（elements）+偏移量
分析src/runtime/string.go 代码中concatstrings实现，可以看出“+”会申请buf，拷贝原来的string到buf，最后返回新实例。每次的“+”操作，都会涉及新申请buf，然后是对应的copy。||如果反复使用+，就不可避免有大量的申请内存操作，对于大量的拼接，性能就会受到影响了。||
```go
import (
	"fmt"
	"reflect"
	"unsafe"
)

a := "hello"
b := ", world"
c := a+b
m := a[:5]
d : = a[1:]
// 可以通过反射获取对应的存储字符串的指针
func stringptr(s string) uintptr {
	// Data为指针类型
	return ((*reflect.StringHeader)(unsafe.Pointer(&s))).Data
}
// stringptr(a) == stringptr(m)
// stringptr(a) + 1 == stringptr(d)
// stringptr(c) != stringptr(a) 
```
4. 转义字符
字符串有两种表示方法，第一种是双引号""表示，这种表示方法下，可以使用转义字符，第二种``表示**raw strings**，这种表示方法下，无法使用转义字符。
```go
a := "hello,/n World"
// 输出
//hello,
// World 
b := `hello, /n World`
// 输出
// hello, /n World
```
5. 关于strings，bytes, runes, characters
要充分了解字符串，不仅要掌握它的工作原理，还要知晓bytes、characters、runes之间的区别，unicode和utf8的区别，string 和 string literal的区别。
- string 和 bytes
string 本质上是只读的字节序列，可以包含任意字节，string 和 bytes可以互相转换。
character通常由一个或者多个字节表示，但是字符本身是模棱两可的，在ascii编码格式下，一个字符就是一个字节，但是其它编码格式下，一个字符就不是一个字节了，所以在unicode中引入了一个新的概念，称为“code point”，因为这个叫法比较拗口，在golang语言中引入了一个新的概念rune，所以rune对应的就是unicode中的“code point”，但是unicode只是一种编码标准，具体的编码方式由很多中，比较常见如：utf-8、utf-16、utf-32等，每一种编码方式中“code point”占用的bit数量也是不同的，比如在utf-16中每一个“code point”占用16个bit，utf-32占用32个bits，但是utf-8中“code point”占用bit数量是根据要表达的字符来确定的，例如英文字母用8个bit就足够表示。golang中rune实际就是int32的别名，所以每一个rune占用32个bits。所以，rune在golang中被定义为一种类型，就像byte 这种类型实际上是unit8，rune也是一种代表unicode “code point”的类型，占用32个bits。runes 可以和string类型进行转换。
```go
// rune is an alias for int32 and is equivalent to int32 in all ways. It is
// used, by convention, to distinguish character values from integer values.
type rune = int32
```
6. utf-8
一种编码方式，使用1-4个字节来表示rune。但是，
 1个字节仅能表示ASCII 字符集
可以使用2～3个字节表示绝大多数的runes。
- 0xxxxxxx     runes 0-127   (ASCII)
- 11xxxxx    10xxxxxx   128-2047 (value \< 128 unused)
- 110xxxx   10xxxxxx    10xxxxxx    2048-65535  (value \< 2048没有使用)
- 1110xxx    10xxxxxx 10xxxxxx  10xxxxxx      65536-0x10ffff (other values unused)
8. range函数和字符串
如何打印字符串中的每个字符？获取字符串中字符的长度？
你可以用range函数或者unicode/utf8 package中提供的函数来打印每个字符
```go
for i := 0; i < len(s); {
	r, size := utf8.DecodeRuneInString(s[i])
	fmt.Printf("%d\t%c\n", i, r)
	i += size
}

//或者用range函数

for i,r := range("Hello, 世界") {
	fmt.Printf("%d\t%q\t%d\n", i, r, r)
}
```

获取字符长度
```go
n := 0
for _, _ = range s {
	n++
}

// 或者
n := 0

for range s {
	n++
}
```
9. 字符串和数值类型之间的转换
直接用string(54) 这种强制转换是无法将数字转换成string类型的（假如你的期望是54=\> “54”），string(54)只能输出54所代表的ascii代表的字符“-”，golang中有专门针对string和数值之间做转换用的packagestrconv，用法如下：
```go
i, err := strconv.Atoi("-42")
s := strconv.Itoa(-42)
```
strconv还提供其它基本类型和string之间转换，每个函数都提供了对应的例子，具体细节可以查阅[https://golang.org/pkg/strconv/#QuoteRune][1]。
10. 字符串和字节数组（`[]` byte）之间的转换
转换的方式很简单
string =\> `[]`byte:
```go
data := []byte("hello, 世界")
```
`[]`byte =\> string:
```go
strData := string(data) //data为[]byte类型的数据
```

string和[]byte 之间的数据转换会涉及到内存的分配吗？
先来看下[]byte的内部结构：
```go
type slice struct {
    data uintptr
    len int       // 当前数据的长度
    cap int       // 容量，表示在重新申请内存前可以存储的字节数量
}
```
string的内部结构如下：
```go
type stringStruct struct {
	str unsafe.Pointer
	len int
}
```

你可能会这样想，在string转换为[]string类型时，只需要将对应的指针指向原来的那块地址，并更新len的长度就ok了，但是实际并不是这样，因为[]byte是可变类型，而string 是不可变类型，这是不可调和的部分。所以，在两种类型转换时，就涉及到了申请内存和数据copy。
而这是在[runtime package中stringtoslicebyte][2] 和 [slicebytetostring][3] 实现的。
但是，golang在runtime的代码中实际提供了这个功能（直接引用而非新申请内存），这样就省去了申请内存和copy的过程，这个函数：[slicebytetostringtmp][4]或者[stringtoslicebytetmp][5]提供了这种功能。你要用这个方式进行转换的话，你得注意下转换之后，不要改变[]byte的数据。另外这个函数还用在“+”操作符的优化上。
你可以自己实现一个
```go
import (
        “unsafe”
)
// ByteSliceToString is used when you really want to convert a slice // of bytes to a string without incurring overhead. It is only safe
// to use if you really know the byte slice is not going to change // in the lifetime of the string
func ByteSliceToString(bs []byte) string {
        // This is copied from runtime. It relies on the string
        // header being a prefix of the slice header!
        return *(*string)(unsafe.Pointer(&bs))
}
```
11. bytes.Buffer
先记录一下问题吧，如何高效的实现字符串的拼接？[网上有人总结了几种方法，并做了相应的性能测试][6]。
我在这里记录下golang中字符串拼接的几种操作，并给出测试结果。
```go
//利用fmt.Sprintf函数
func sprintfString(itemType string, clientID string, id string) string {
	key := fmt.Sprintf("%s:%s:%s", itemType, clientID, id)
	return key
}

//利用strings.Join函数
func joinString(itemType string, clientID string, id string) string {
	key := strings.Join([]string{itemType, clientID, id}, ":")
	return key
}

//利用byte.Buffer
func bufferString(itemType string, clientID string, id string) string {
	l := len(itemType) + len(clientID) + len(id) + 2
	buf := make([]byte, 0, l)
	w := bytes.NewBuffer(buf)
	w.WriteString(itemType)
	w.WriteRune(':')
	w.WriteString(clientID)
	w.WriteRune(':')
	w.WriteString(id)
	key := w.String()
	return key
}

// 比较tricky的做法
func bytesString(itemType string, clientID string, id string) string {
	l := len(itemType) + len(clientID) + len(id) + 2
	buf := make([]byte, l)
	offset := 0
	copy(buf, itemType)
	offset += len(itemType)
	copy(buf[offset:], ":")
	offset += len(":")
	copy(buf[offset:], clientID)
	offset += len(clientID)
	copy(buf[offset:], ":")
	offset += len(":")
	copy(buf[offset:], id)
	key := ByteSliceToString(buf)
	return key
}

// 利用strings.Builder
func buildString(itemType string, clientID string, id string) string {
	w := strings.Builder{}
	w.Grow(len(itemType) + len(clientID) + len(id) + 2)
	w.WriteString(itemType)
	w.WriteRune(':')
	w.WriteString(clientID)
	w.WriteRune(':')
	w.WriteString(id)
	key := w.String()
	return key
}
```
测试结果如下：
BenchmarkAppendString-4         13409830                80.9 ns/op             7 B/op          0 allocs/op
BenchmarkSprintfString-4         3733785               310 ns/op              87 B/op          5 allocs/op
BenchmarkJoinString-4           10735363               101 ns/op              39 B/op          1 allocs/op
BenchmarkBufferString-4          8137467               173 ns/op              71 B/op          2 allocs/op
BenchmarkBytesString-4          13672458               119 ns/op              39 B/op          1 allocs/op
BenchmarkBuildString-4          11920328               111 ns/op              39 B/op          1 allocs/op
从测试结果来看，通过“+”来进行字符串的拼接从时间和内存使用上都更胜一筹（这与从我之前的经验得出的结论背道而驰），而通过byte.buffer实现的字符串拼接方法却不尽如人意。所以，在进行字符串拼接时，请优先使用“+”或者strings.Builder。
具体为什么“+”的速度这么快呢？这就需要去看下源码了。
```go
const tmpStringBufSize = 32

type tmpBuf [tmpStringBufSize]byte
func concatstrings(buf *tmpBuf, a []string) string {
	idx := 0
	l := 0
	count := 0
	for i, x := range a {
		n := len(x)
		if n == 0 {
			continue
		}
     // 大于最大数的时候会变成负数，l的默认类型是int32
		if l+n < l {
			throw("string concatenation too long")
		}
		l += n
		count++
		idx = i
	}
	if count == 0 {
		return ""
	}

	// If there is just one string and either it is not on the stack
	// or our result does not escape the calling frame (buf != nil),
	// then we can return that string directly.
	if count == 1 && (buf != nil || !stringDataOnStack(a[idx])) {
		return a[idx]
	}
	s, b := rawstringtmp(buf, l) // tmpStringBufSize是32， 如果“+”的字符数量大于32个就会存在“allocs/op”（注意看测试结果）
	for _, x := range a {
		copy(b, x) // 将数据copy到s unsafe.Pointer对应的字节数组
		b = b[len(x):] // 子串指向的地址空间和原串的地址空间一致，只是有偏移量
	}
	return s
}

func rawstringtmp(buf *tmpBuf, l int) (s string, b []byte) {
	if buf != nil && l <= len(buf) {
		b = buf[:l]
		s = slicebytetostringtmp(b) //slicebytetostringtmp returns a "string" referring to the actual []byte bytes.
	} else {
		s, b = rawstring(l)
	}
	return
}


```
12. Index的实现细节
判断一个字符串是否是字串 并返回第一个匹配的开始序号？
[Rabin-Karp Algorithm][7]


[1]:	https://golang.org/pkg/strconv/#QuoteRune
[2]:	https://golang.org/pkg/runtime/?m=all#stringtoslicebyte
[3]:	%20https://golang.org/pkg/runtime/?m=all#slicebytetostring
[4]:	https://golang.org/pkg/runtime/?m=all#slicebytetostringtmp
[5]:	https://golang.org/pkg/runtime/?m=all#stringtoslicebytetmp
[6]:	https://syslog.ravelin.com/bytes-buffer-i-thought-you-were-my-friend-4148fd001229
[7]:	http://courses.csail.mit.edu/6.006/spring11/rec/rec06.pdf