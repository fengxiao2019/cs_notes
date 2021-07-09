SQL注入攻击包括通过客户端的输入数据插入或 "注入 "一个SQL查询到应用程序中。一个成功的SQL注入攻击可以从数据库中读取敏感数据，修改数据库数据（插入/更新/删除），在数据库上执行管理操作（如关闭DBMS），恢复DBMS文件系统中存在的特定文件的内容，在某些情况下还可以向操作系统发出命令。
当软件开发人员创建包括用户输入的动态数据库查询时，就会出现SQL注入缺陷。要避免SQL注入的缺陷很简单。开发人员需要：
a）停止编写动态查询；和/或
b）防止包含恶意SQL的用户输入影响执行查询的逻辑。

主要的防御措施：

选项1：变量绑定。
选项2：使用存储过程
选项3：允许列表输入验证
选项4：zhuanyi。
其他防御措施：

-强制执行最低权限
-执行允许列表输入验证作为辅助防御措施

下面（Java）的例子是不安全的，它允许攻击者在查询中注入代码，由数据库执行。未验证的 "customerName "参数被简单地添加到查询中，允许攻击者注入他们想要的任何SQL代码。不幸的是，这种访问数据库的方法太常见了。
```java
String query = "SELECT account_balance FROM user_data WHERE user_name = "
             + request.getParameter("customerName");
try {
    Statement statement = connection.createStatement( ... );
    ResultSet results = statement.executeQuery( query );
}
...
```
## 预防措施
### 参数化（变量绑定）
使用带有变量绑定的准备好的语句（又称参数化查询）是所有开发人员应该首先被教导如何编写数据库查询的方式。它们写起来很简单，而且比动态查询更容易理解。参数化查询迫使开发人员首先定义所有的SQL代码，然后再把每个参数传递给查询。这种编码方式允许数据库区分代码和数据，而不管用户输入了什么。
预备语句确保攻击者不能改变查询的意图，即使SQL命令是由攻击者插入的。在下面的安全例子中，如果攻击者输入tom'或'1'='1的userID，参数化的查询就不会有漏洞，而是寻找一个与整个字符串tom'或'1'='1字面相符的用户名。
```cs
String query = "SELECT account_balance FROM user_data WHERE user_name = ?";
try {
  OleDbCommand command = new OleDbCommand(query, connection);
  command.Parameters.Add(new OleDbParameter("customerName", CustomerName Name.Text));
  OleDbDataReader reader = command.ExecuteReader();
  // …
} catch (OleDbException se) {
  // error handling
}
```
### 存储过程
存储过程并不总是对SQL注入安全的。然而，某些标准的存储过程编程结构在安全实施时具有与使用参数化查询相同的效果，这是大多数存储过程语言的规范。

它们要求开发者只是建立带有参数的SQL语句，而这些参数是自动参数化的，除非开发者做了一些基本不符合规范的事情。预备语句和存储过程的区别在于，存储过程的SQL代码被定义并存储在数据库本身，然后从应用程序中调用。这两种技术在防止SQL注入方面具有相同的效力。
### 输入验证
SQL查询的各个部分都不是使用绑定变量的合法位置，例如表或列的名称，以及排序指标（ASC或DESC）。在这种情况下，输入验证或重新设计查询是最合适的防御措施。对于表或列的名称，理想的情况是这些值来自代码，而不是来自用户参数。
但是如果用户参数值被用于针对不同的表名和列名，那么参数值应该被映射到合法/预期的表名或列名，以确保未经验证的用户输入不会在查询中出现。请注意，这是设计不良的症状，如果时间允许，应该考虑进行全面重写。

### 对输入的数据进行全部转义
这种技术只应作为最后的手段，当上述方法都不可行时才使用。输入验证可能是一个更好的选择，因为这种方法与其他防御措施相比是脆弱的，我们不能保证在所有情况下都能防止所有的SQL注入。

这种技术是在把用户输入的信息放到查询中之前，对其进行转义。它的实现是非常针对数据库的。通常只建议在实施输入验证不符合成本效益的情况下，对遗留的代码进行改造。从头开始建立的应用程序，或需要低风险容忍度的应用程序，应该使用参数化查询、存储过程或某种为你建立查询的对象关系映射器（ORM）来建立或重写。
这种技术是这样工作的。每个DBMS都支持一个或多个特定于某些类型的查询的字符转义方案。如果你使用你所使用的数据库的适当转义方案转义所有用户提供的输入，DBMS将不会把输入与开发者编写的SQL代码混淆，从而避免任何可能的SQL注入漏洞。

## Django ORM 和 SQL 注入
SQL注入是一种攻击类型，恶意用户能够在数据库中执行任意的SQL代码。这可能会导致记录被删除或数据泄露。

Django的查询集可以防止SQL注入，因为它们的查询是使用查询参数化构建的。一个查询的SQL代码是与查询的参数分开定义的。由于参数可能是用户提供的，因此是不安全的，它们会被底层数据库驱动转义。

Django还为开发者提供了编写原始查询或执行自定义SQL的能力。这些功能应该少用，你应该总是小心翼翼地正确转义任何用户可以控制的参数。此外，在使用extra()和RawSQL时，你应该谨慎行事。
[https://code.djangoproject.com/ticket/17741][1]
Is there another way to get valid sql, without executing the query?
There isn't, because Django never actually interpolates the parameters: it sends the query and the parameters separately to the database adapter, which performs the appropriate operations.

[1]:	https://code.djangoproject.com/ticket/17741