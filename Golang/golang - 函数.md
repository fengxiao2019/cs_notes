golang - 函数
## 函数值
函数是一等公民 
可以声明 可以赋值 可以作为函数返回值 可以被调用

只声明的函数不能被调用（the zero value of function is nil）
例如 
```go
var f func(int) int
// panic: call of nil funciton
```

函数值可以与nil 比较
例如
```go
var f func(int) int
if f!= nil {
	f(3)
}
```

函数值与函数值之间不能比较，也不能作为map的key
函数作为其它函数的参数（也就是callback）

## 匿名函数
