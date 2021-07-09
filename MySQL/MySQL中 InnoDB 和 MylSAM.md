MyISAM和InnoDB是MySQL存储引擎。存储引擎是数据库管理系统的组件，用于操作数据库中的数据。
- MyISAM
> MyISAM是索引顺序访问法（indexed sequence  access method）的缩写。在2009年12月之前，它是MySQL的默认存储引擎。随着MySQL 5.5的发布，MyISAM被InnoDB取代。
> MySQL 5.7 still used MyISAM storage for the system tables in the MySQL schema. 8.0版本，在引入新的数据字典后，MyISAM表已经从系统模式（"mysql "db）中消失。
![][image-1]
所以MyISAM的优势只剩下。
- 与未压缩的InnoDB表相比，表在磁盘上会更小。
- Count(\*)在MyISAM中仍然要快得多。


[image-1]:	https://tva1.sinaimg.cn/large/008i3skNly1gri7v3g2uoj318o0nq0wa.jpg