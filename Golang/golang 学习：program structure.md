# golang 学习：program structure
1. go 命名 字母、下划线、数字，必须以字母或下划线开头，区分大小写
2. 25个关键字
> 关键字
> > break  default  func interface select
> > case defer go map struct
> > chan else goto package switch
> > const   fallthrough    if    range    type 
> >  continue     for     import     return       var
> 预定义的名字
> 预定义的名字并不是保留字，可以是在声明中使用，但是要注意别搞混淆了
> > constants
> > > true      false        iota      nil
> > Types 
> > > int      int8      int32     int64
> > > uint     unit8      uint16      unit32      unit64      uintptr
> > > float32    float64     float128      complex64  
> > > bool      byte    **rune**      string       error
> > Functions
> > > make       len       **cap**       new       append      copy     **close**    delete      **complex**        real        **imag**

3. 当声明过程发生在函数内时，这份声明只能在函数内起作用。如果 声明是在函数外发生的，这份声明在整个package范围内起作用。
4. 首字母大写的命名表示export，可以被其它的package访问到。
5. 命名时驼峰命名规则
6. 声明的类型：var   const     type   func
7. package 声明的作用是定义这个.go文件所属的package
## 变量相关
格式如下
```go
var name type = expression
```
type 或者 “= expression” 可以省略（不能两个一起省略）
如果type省略了，系统会根据expression判断出name的类型
如果”=expression”省略了，系统会根据type初始化name的值
可以一次声明多个变量
一次给多个变量赋值
like this:
```go
var i, j, k int
var b, f, s = true, 2.3, "four"
```

package 级别的变量初始化在main函数开始前进行。
可以通过调用函数给一组变量赋值，like this:
```go
var f, err = os.Open(name)
```

### Short Variable Declarations
格式： `name := expression`

什么时候用var?
- 当局部变量需要明确指定类型的时候
- 当局部变量需要先声明，不进行初始化
eg 
```go
var boiling float64 = 100
var names []string
var err error
var p Point
```

注意： **:= ** 是声明， ** = ** 是赋值
short variable declaration 必须最少声明一个新的变量
像下面这种用法就会导致编译失败
```go
f, err := os.Open(infile)
f, err := os.Create(outfile) // 编译error: no new variables
```

### 指针
指针的用法和c中指针的用法基本一致，但是有一点需要注意：
> it is perfectly safe for a function to return the address of a local variable.
在c中，返回局部变量的指针会变成悬挂指针，导致程序异常
在go中，不用担心这个问题
