golang-测试

测试函数的命名格式：
func TestXxx(*testing.T)
其中Xxx不以小写字母开头，函数名称用于标识测试例程。
go test命令可以识别测试函数，自动完成测试。
如何针对测试你的package进行测试？
新建文件，文件名以_test.go结尾，将文件放到package目录下，在文件中编写你的测试函数。
一个比较简单的测试函数如下所示：
```go
func TestAbs(t *testing.T) {
    got := Abs(-1)
    if got != 1 {
        t.Errorf("Abs(-1) = %d; want 1", got)
    }
}
```

Benchmarks
函数格式：
```go
func BenchmarkXxx(*testing.B)
```
