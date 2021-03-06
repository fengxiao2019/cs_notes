Python 是如何执行垃圾回收的
**memory management**
![]()
Arena -\> pool -\> blocks
Arena 的大小： 256k 直接通过系统调用mmap进行内存映射
```c
#define ARENA_SIZE              (256 << 10)     /* 256KB */
```
pool的大小：4kb
```c
#define POOL_SIZE               SYSTEM_PAGE_SIZE        /* must be 2^N */
```
block的大小：大小不等8～512字节，block的大小必需是8的整数倍
可选的范围有：
Arena由pool构成，pool由block构成，每一个pool中block的大小相等

Arena使用的数据结构是双向链表
pool使用的也是双向链表
block是单向链表

pool分成三种类型：
usedpools
fullpools
为什么python选用4k作为sy**system\_page\_size**
usedpools 为一个数组


```c
/*
 * The system's VMM page size can be obtained on most unices with a
 * getpagesize() call or deduced from various header files. To make
 * things simpler, we assume that it is 4K, which is OK for most systems.
 * It is probably better if this is the native page size, but it doesn't
 * have to be.  In theory, if SYSTEM_PAGE_SIZE is larger than the native page
 * size, then `POOL_ADDR(p)->arenaindex' could rarely cause a segmentation
 * violation fault.  4K is apparently OK for all the platforms that python
 * currently targets.
 */
#define SYSTEM_PAGE_SIZE        (4 * 1024)
#define SYSTEM_PAGE_SIZE_MASK   (SYSTEM_PAGE_SIZE - 1) 
```

usedpools 类型：固定大小的数组
**创建对象流程**
object.c file
---- 
```c
# object.c file
_PyObject_New {
	PyObject *op = (PyObject *) PyObject_MALLOC(_PyObject_SIZE(tp));
    ...
}

# obmalloc.c
void *
PyObject_Malloc(size_t size)
{
    /* see PyMem_RawMalloc() */
    if (size > (size_t)PY_SSIZE_T_MAX)
        return NULL;
    return _PyObject.malloc(_PyObject.ctx, size);
}


```
 
```c
# pymem.h
typedef struct {
    /* user context passed as the first argument to the 4 functions */
    void *ctx;

    /* allocate a memory block */
    void* (*malloc) (void *ctx, size_t size);

    /* allocate a memory block initialized by zeros */
    void* (*calloc) (void *ctx, size_t nelem, size_t elsize);

    /* allocate or resize a memory block */
    void* (*realloc) (void *ctx, void *ptr, size_t new_size);

    /* release a memory block */
    void (*free) (void *ctx, void *ptr);
} PyMemAllocatorEx;

#  define PYMALLOC_ALLOC {NULL, _PyObject_Malloc, _PyObject_Calloc, _PyObject_Realloc, _PyObject_Free}
# 所以，_PyObject.malloc 实际对应的是_PyObject_Malloc函数
static PyMemAllocatorEx _PyObject = PYOBJ_ALLOC;

# 此函数调用了pymalloc_alloc 如果pymalloc_alloc成功，就返回，否则调用pyMem_RawMalloc函数。
pymalloc_alloc 负责处理小内存块的处理。小内存块的定义：
#define SMALL_REQUEST_THRESHOLD 512
申请的内存大于512个字节，返回null
假设申请的内存大小为nbytes 
nbytes按8字节或者16字节对齐（指针大小为4字节的，按8字节对齐；指针大小为8字节的，按照16字节对齐）
对齐后的nbytes 假设为size。
usedpool 的设计是这样的：
固定大小的数组（64个元素）
每个元素为一个pool 指针。pool的大小为4kb（系统页的大小）
每个pool中的block的大小是一致的，不会出现两个不同大小的block在同一个pool中。
所以如何在usedpool中找到具有size大小的pool呢？

内存池 usedpool

static void *
_PyObject_Malloc(void *ctx, size_t nbytes)
{
    void* ptr = pymalloc_alloc(ctx, nbytes);
    if (LIKELY(ptr != NULL)) {
        return ptr;
    }

    ptr = PyMem_RawMalloc(nbytes);
    if (ptr != NULL) {
        raw_allocated_blocks++;
    }
    return ptr;
}





```


