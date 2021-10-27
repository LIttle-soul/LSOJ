---
title: STL标准模板库
author: Little-Soul
tags: [C/C++, ACM]
categories: [ACM]
# index_img: /image/page_image/git1.jpg
banner_img: /image/background/background11.jpg
date: 2020-01-31
hide: false
---

```c++
vector, 变长数组，倍增的思想
    size()  返回元素个数
    empty()  返回是否为空
    clear()  清空
    front()/back()
    push_back()/pop_back()
    begin()/end()
    []
    支持比较运算，按字典序

pair<int, int>
    first, 第一个元素
    second, 第二个元素
    支持比较运算，以first为第一关键字，以second为第二关键字（字典序）

string，字符串
    size()/length()  返回字符串长度
    empty()
    clear()
    substr(起始下标，(子串长度))  返回子串
    c_str()  返回字符串所在字符数组的起始地址

queue, 队列
    size()
    empty()
    push()  向队尾插入一个元素
    front()  返回队头元素
    back()  返回队尾元素
    pop()  弹出队头元素

priority_queue, 优先队列，默认是大根堆
    push()  插入一个元素
    top()  返回堆顶元素
    pop()  弹出堆顶元素
    定义成小根堆的方式：priority_queue<int, vector<int>, greater<int>> q;

stack, 栈
    size()
    empty()
    push()  向栈顶插入一个元素
    top()  返回栈顶元素
    pop()  弹出栈顶元素

deque, 双端队列
    size()
    empty()
    clear()
    front()/back()
    push_back()/pop_back()
    push_front()/pop_front()
    begin()/end()
    []

set, map, multiset, multimap, 基于平衡二叉树（红黑树），动态维护有序序列
    size()
    empty()
    clear()
    begin()/end()
    ++, -- 返回前驱和后继，时间复杂度 O(logn)

    set/multiset
        insert()  插入一个数
        find()  查找一个数
        count()  返回某一个数的个数
        erase()
            (1) 输入是一个数x，删除所有x   O(k + logn)
            (2) 输入一个迭代器，删除这个迭代器
        lower_bound()/upper_bound()
            lower_bound(x)  返回大于等于x的最小的数的迭代器
            upper_bound(x)  返回大于x的最小的数的迭代器
    map/multimap
        insert()  插入的数是一个pair
        erase()  输入的参数是pair或者迭代器
        find()
        []  注意multimap不支持此操作。 时间复杂度是 O(logn)
        lower_bound()/upper_bound()

unordered_set, unordered_map, unordered_multiset, unordered_multimap, 哈希表
    和上面类似，增删改查的时间复杂度是 O(1)
    不支持 lower_bound()/upper_bound()， 迭代器的++，--

bitset, 圧位
    bitset<10000> s;
    ~, &, |, ^
    >>, <<
    ==, !=
    []

    count()  返回有多少个1

    any()  判断是否至少有一个1
    none()  判断是否全为0

    set()  把所有位置成1
    set(k, v)  将第k位变成v
    reset()  把所有位变成0
    flip()  等价于~
    flip(k) 把第k位取反
```

## 1. map

> map 中所有元素的 key 的值必须是唯一的，multimap 则允许有重复的 Key 值。

- 构建

```
map<string, long long> m;
```

- 向 map 中插入元素

```c++
m[key]=value;
//[key]操作是map很有特色的操作,如果在map中存在键值为key的元素对, 则返回该元素对的值域部分,否则将会创建一个键值为key的元素对,值域为默认值。所以可以用该操作向map中插入元素对或修改已经存在的元素对的值域部分。
m.insert(male_pair(key,value));
//也可以直接调用insert方法插入元素对,insert操作会返回一个pair,当map中没有与key相匹配的键值时,其first是指向插入元素对的迭代器,其second为true;若map中已经存在与key相等的键值时,其first是指向该元素对的迭代器,second为false。
```

- 查找元素

```c++
int i=m[key];
//要注意的是,当与该键值相匹配的元素对不存在时,会创建键值为key（当另一个元素是整形时，m[key]=0）的元素对。
map<string, int>::iterator it=m.find(key);
//如果map中存在与key相匹配的键值时,find操作将返回指向该元素对的迭代器,否则,返回的迭代器等于map的end()
```

- 删除元素

```c++
//erase的参数可以是key或者迭代器
m.erase(key);
//删除与指定key键值相匹配的元素对,并返回被删除的元素的个数。
m.erase(it);
//删除由迭代器it所指定的元素对,并返回指向下一个元素对的迭代器。
```

- map 的 upper_bound/lower_bound
  > iterator lower_bound( const key_type &key ): 返回一个迭代器，指向键值>= key 的第一个元素。  
  > iterator upper_bound( const key_type &key ):返回一个迭代器，指向键值> key 的第一个元素。
- 其他简单操作

```c++
m.size();       //返回元素个数
m.empty();      //判断是否为空
m.clear();      //清空所有元素
m.begin();      //返回首迭代器
m.end();        //返回尾迭代器
```

# 2. C++ queue

> **_`#include<queue>`_**  
> 头文件 queue 里包含了循环队列 queue 和优先队列 priority_queue

- #### 循环队列 queue

```c++
queue<int> q;
```

- front()：返回 queue 中第一个元素的引用。如果 queue 是常量，就返回一个常引用；如果 queue 为空，返回值是未定义的。
- back()：返回 queue 中最后一个元素的引用。如果 queue 是常量，就返回一个常引用；如果 queue 为空，返回值是未定义的。
- push(const T& obj)：在 queue 的尾部添加一个元素的副本。这是通过调用底层容器的成员函数 push_back() 来完成的。
- push(T&& obj)：以移动的方式在 queue 的尾部添加元素。这是通过调用底层容器的具有右值引用参数的成员函数 push_back()来完成的。
- pop()：删除 queue 中的第一个元素。
- size()：返回 queue 中元素的个数。
- empty()：如果 queue 中没有元素的话，返回 true。
- emplace()：用传给 emplace() 的参数调用 T 的构造函数，在 queue 的尾部生成对象。
- swap(queue<T> &other_q)：将当前 queue 中的元素和参数 queue 中的元素交换。它们需要包含相同类型的元素。也可以调用全局函数模板 swap() 来完成同样的操作。
- #### 优先队列 priority_queue

```c++
priority_queue<int> q;//大根堆（堆顶值最大）
priority_queue<int,vector<int>,greater<int> > q;//小根堆（堆顶值最小）
```

> 注意 priority_queue 中储存的元素类型必须定义“小于号”（注意这里虽然是<小于号，但实际上是大于号），较大的元素会被放在堆顶。内置的 int、string 等类型已经定义过“小于号”，若使用结构体则必须重载运算符。  
> 由于 priority_queue 是按照从大到小排序所以重载运算符时也要反过来。

###### 1. 大根堆

**重载“<”运算符**

> 下面的 poi 结构体保存了二维平面上的编号和坐标，比较大小时，先比较横坐标，再比较纵坐标，并考虑了精度误差。

```c++
struct poi{
    int id;
    double x,y;
};
const double eps = 1e-8;
bool operator<(const poi &a,const poi &b){
    return a.x+eps<b.x||a.x<b.x+eps&&a.y<b.y;
}
```

###### 2. 小根堆

> 下面代码重载运算符之后定义了一个小根堆（堆顶元素值最小，其实就是从小到大排序）

```c++
struct node{
	int value ;
	friend bool operator < (node a , node b)
	{
		return a.value > b.value;
	}
};
priority_queue<node> q;

//------------------------------------------------

struct node{
	int value ;
	 bool operator < (const node &a) const
	{
		return value > a.value;
	}
};
priority_queue<node> q;

// 成员函数

q.top();        //访问堆顶元素
q.empty();      //检查是否为空
q.size();       //返回容纳的元素数
q.push();       //插入元素，并排序
q.pop();        //删除栈顶元素
```

###### 2. 懒惰删除法

> 如果是手写的堆是支持删除任意一个元素，而 STL 却不支持这种操作所以我们可以用懒惰删除法  
> 懒惰删除法又称延迟删除法，是一种应对策略。当遇到删除操作时，仅在优先队列之外做一些特殊的记录，用于辨别是否堆中的元素被删除。当从堆顶取出元素时判断是否已经被删除，若是，我们重新取一个最值。换言之，元素的“删除”推迟到堆顶执行。  
> 比如“堆优化的 Dijkstra 算法”中当某个元素首次被取出时就达到了最短路，当我们再次取出这个元素时我们不会重新进行扩展，而是使用一个 bool 数组判断“是否进行过扩展”，其本质还是懒惰删除法的应用。

- #### 双端队列 deque
  头文件 deque

```c++
#include<deque>
```

> 双端队列 deque 支持队列两端高效地插入或删除元素的连续性存储空间。与 vector 相比，deque 在头部增删元素只需要 O ( 1 ) O(1)O(1)，并且 deque 像数组一样支持下标随机访问。

|     []     |      随机访问 O(1)       |
| :--------: | :----------------------: |
| begin/end  | deque 的头/尾迭代器 O(1) |
| front/back |    队头/队尾元素 O(1)    |
| push_front |     从队头入队 O(1)      |
| push_back  |     从队尾入队 O(1)      |
| pop_front  |     从队头出队 O(1)      |
|  pop_back  |     从队尾出队 O(1)      |
|   clear    |      清空队列 O(n)       |
