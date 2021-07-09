golang-slice
长度可变
元素的类型必须一致
编程时要注意：
**go fuctions should treat all  zero-length slices the same way, whether nil or not nil.**
slice创建的几种方式
```go
//[]T, T表示数据类型
//eg
var s []int    // 声明一个slice, s == nil， len(m) == 0, 
s = nil        // len(s) == 0, s == nil
s = []int(nil) // len(s) == 0, s == nil
s = []int {}   // len(s) == 0, s != nil
// 利用make可以创建指定元素类型、len和cap的slice，其中cap参数可以省略（省略的话，cap 等于len）。
s = make([]int, 10) // int类型，len为10，cap为10的slice
s = make([]int, 10, 20) // int类型，len为10，cap为20的slice

// 注意区别声明数组的形式
var z [5]string //声明一个数组, 字符串的初始值为""


```

slice 有三个部分组成：
```go
type slice struct {
	array unsafe.Pointer
	len   int
	cap   int
}
```
其中 slice.array是一个指针，这个指针指向一个数组，这个数组我们称为基础数组（underlying array），这个指针具体定义了slice可以访问到的数组的位置。
len 是指slice中元素数量
```go
wordArray := [4]string{"吹哨人", "chuishaoren", "big"}
withCnWord := wordArray[0:1]
enWord := wordArray[1:]
fmt.Printf("len(withCnWord):%d, len(enWord):%d", len(withCnWord), len(enWord)) // len(withCnWord):1, len(enWord):3
```
cap 是指slice的容量，一般是指从slice.array这个指针指向的数组的位置到这个数组的结尾处，例如下面的例子中subPoems 对应数组的开闭区间为[x, y)， x为1， y为4，但是cap的数值其实是len(poems) - x = 13 - 1 = 12。
]()```go
poems := []string{"Stray", "birds", "of", "summer", "come", "to", "my", "window", "to", "sing", "and", "fly", "away"}
subPoems := poems[1:4]
fmt.Printf("len(subPoems): %d, cap(subPoems): %d\n", len(subPoems), cap(subPoems))// len(subPoems): 3, cap(subPoems): 12
```

多个slice可以共享一个基础数组，而且对应数组中的部分可以重叠。

s[i:j] 这个表示创建一个slice。
其中：
- s 表示一个数组或者一个指向数组的指针或者另一个slice。
- `0 <= i <= j <= cap(s) `
- 如果i省略的话，就变成s[:j]实际就是s[0:j]。如果j省略的话，就变成s[i:]实际就是s[i:len(s)]，如果两个都省略，就是s本身。
访问slice时，index超过slice的长度时，会发生什么现象？
slice作为函数参数传递时，是值传递还是引用传递？
两个silce是否利用”==” 比较？为什么？
如何判断一个slice是否为空？

