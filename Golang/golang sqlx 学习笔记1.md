golang sqlx 学习笔记1
sqlx是Go的软件包，它在出色的 database/sql软件包的基础上提供了一组扩展。
安装命令
```bash
go get github.com/jmoiron/sqlx
```
- sqlx.DB-与sql.DB类似，表示数据库
- sqlx.Tx-与sql.Tx类似，表示事务
- sqlx.Stmt-与sql.Stmt类似，表示已准备好的语句
- sqlx.NamedStmt-支持命名参数的预准备语句的表示形式
- sqlx.Rows-与sql.Rows类似，从Queryx返回的游标
- sqlx.Row-与sql.Row类似，从QueryRowx返回的结果

要使用这个package，不仅需要import这个package本身，还需要import你要使用的数据库的对应的驱动程序。
例如我们要使用mysql数据库，就需要这么做：
```go
import (
	"database/sql"
    
	_ "github.com/go-sql-driver/mysql"
    "github.com/jmoiron/sqlx"
)
```
 请注意，我们是匿名加载驱动程序，将其包限定符别名命名为_，因此我们的代码看不到其导出的名称。

**连接到数据库**
```go
db, err := sql.Open("mysql",
		"user:password@tcp(127.0.0.1:3306)/hello")
if err != nil {
		log.Fatal(err)
	}
defer db.Close()
```
