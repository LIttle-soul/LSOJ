---
title: The C++ Standard Template Library(STL)
author: Little_Soul
date: 2020-09-18
tags: ["C++", "STL"]
categories: ["C++", "STL"]
# index_img: /image/page_image/git1.jpg
banner_img: /image/background/background11.jpg
hide: false
---

> The Standard Template Library (STL) is a set of C++ template classes to provide common programming data structures and functions such as lists, stacks, arrays, etc. It is a library of container classes, algorithms, and iterators. It is a generalized library and so, its components are parameterized. A working knowledge of template classes is a prerequisite for working with STL.
>
> 标准模板库（STL）是一组 C ++模板类，用于提供常见的编程数据结构和功能，例如列表，堆栈，数组等。它是容器类，算法和迭代器的库。 它是一个通用库，因此其组件已参数化。 模板类的工作知识是使用 STL 的先决条件。

# 一. <span id="Algorithms">Algorithms</span>

> The header algorithm defines a collection of functions especially designed to be used on ranges of elements.They act on containers and provide means for various operations for the contents of the containers.
>
> 翻头算法定义了一组专门设计用于元素范围的函数集合，它们作用于容器并为容器的内容提供各种操作手段。

## 1. <span id="">Algorithm</span>

- ### <span id="Sorting">Sorting</span>

  Sorting is one of the most basic functions applied to data. It means arranging the data in a particular fashion, which can be increasing or decreasing. There is a builtin function in C++ STL by the name of sort().  
   This function internally uses IntroSort. In more details it is implemented using hybrid of QuickSort, HeapSort and InsertionSort.By default, it uses QuickSort but if QuickSort is doing unfair partitioning and taking more than N\*logN time, it switches to HeapSort and when the array size becomes really small, it switches to InsertionSort.

  排序是应用于数据的最基本功能之一。这意味着以特定的方式排列数据，可以增加或减少。C ++ STL 中有一个内置函数，名称为 sort（）。  
   此函数在内部使用 IntroSort。更详细地讲，它是使用 QuickSort，HeapSort 和 InsertionSort 的混合实现的。默认情况下，它使用 QuickSort，但是如果 QuickSort 进行不公平的分区并且花费的时间超过 N \* logN，它将切换到 HeapSort，并且当数组大小变得非常小时，它切换到 InsertionSort。

> sort(startaddress, endaddress)
>
> startaddress: the address of the first element of the array  
> endaddress: the address of the next contiguous location of the last element of the array.  
> So actually sort() sorts in the range of [startaddress,endaddress)
>
> startaddress：数组第一个元素的地址。  
> endaddress：数组最后一个元素的下一个连续位置的地址。  
> 所以 sort（）实际上在[startaddress，endaddress）范围内排序  
> 注: 可用 cmp 定义 sort 的排序方式（sort(startaddress,endaddress,cmp)）

```c++
//cmp用法
bool cmp(int a,int b){
    return a>b;
}//实现从大到小的排序
```

```c++
#include <iostream>
#include <algorithm>

using namespace std;

void show(int a[])
{
	for(int i = 0; i < 10; ++i)
		cout << a[i] << " ";
}

int main()
{
	int a[10]= {1, 5, 8, 9, 6, 7, 3, 4, 2, 0};
	cout << "\n The array before sorting is : ";
	show(a);

	sort(a, a+10);

	cout << "\n\n The array after sorting is : ";
	show(a);

	return 0;

}


<!--The array before sorting is : 1 5 8 9 6 7 3 4 2 0-->
<!--The array after sorting is : 0 1 2 3 4 5 6 7 8 9-->

```

[返回目录](#Menu)

- ### <span id="Searching">Searching</span>

      Binary search is a widely used searching algorithm that requires the array to be sorted before search is applied. The main idea behind this algorithm is to keep dividing the array in half (divide and conquer) until the element is found, or all the elements are exhausted.
      It works by comparing the middle item of the array with our target, if it matches, it returns true otherwise if the middle term is greater than the target, the search is performed in the left sub-array.
      If the middle term is less than target, the search is performed in the right sub-array.

      二进制搜索是一种广泛使用的搜索算法，该算法要求在应用搜索之前对数组进行排序。 该算法背后的主要思想是将数组继续分成两半（分而治之），直到找到元素或所有元素用尽为止。
      它通过将数组的中间项与目标进行比较来工作，如果匹配，则返回true；否则，如果中间项大于目标，则在左侧子数组中执行搜索。
      如果中间项小于目标，则在右边的子数组中执行搜索。

  > binary_search(startaddress, endaddress, valuetofind)
  >
  > startaddress: the address of the first element of the array.  
  > endaddress: the address of the last element of the array.  
  > valuetofind: the target value which we have to search for.
  >
  > startaddress：数组第一个元素的地址。  
  > endaddress：数组最后一个元素的地址。  
  > valuetofind：要搜索的目标值。

```c++
// CPP program to implement
// Binary Search in
// Standard Template Library (STL)
#include <algorithm>
#include <iostream>

using namespace std;

void show(int a[], int arraysize)
{
	for (int i = 0; i < arraysize; ++i)
		cout << a[i] << " ";
}

int main()
{
	int a[] = { 1, 5, 8, 9, 6, 7, 3, 4, 2, 0 };
	int asize = sizeof(a) / sizeof(a[0]);
	cout << "\n The array is : ";
	show(a, asize);

	cout << "\n\nLet's say we want to search for 2 in the array";
	cout << "\n So, we first sort the array";
	sort(a, a + asize);
	cout << "\n\n The array after sorting is : ";
	show(a, asize);
	cout << "\n\nNow, we do the binary search";
	if (binary_search(a, a + 10, 2))
		cout << "\nElement found in the array";
	else
		cout << "\nElement not found in the array";

	cout << "\n\nNow, say we want to search for 10";
	if (binary_search(a, a + 10, 10))
		cout << "\nElement found in the array";
	else
		cout << "\nElement not found in the array";

	return 0;
}



<!--The array is : 1 5 8 9 0 6 7 3 4 2 0-->

<!--Let's say we want to search for 2 in the array-->
<!-- So, we first sort the array-->

<!--The array after sorting is : 0 1 2 3 4 5 6 7 8 9-->

<!--Now, we do the binary search-->
<!--Element found in the array-->

<!--Now, say we want to search for 10-->
<!--Element not found in the array-->

```

[返回目录](#Menu)

- ### <span id="Important_STL_Algorithms">Important STL Algorithms</span>

      For all those who aspire to excel in competitive programming, only having a knowledge about containers of STL is of less use till one is not aware what all STL has to offer.
      STL has an ocean of algorithms, for all < algorithm > library functions : Refer here.
      Some of the most used algorithms on vectors and most useful one’s in Competitive Programming are mentioned as follows :

      对于那些渴望在竞争性编程方面出类拔萃的人来说，只有了解STL的容器是没有多大用处的，直到你不知道STL提供了什么。
      STL有大量的算法，对于所有的<algorithm>库函数：请参阅这里。
      关于向量的一些最常用的算法和竞争编程中最有用的算法如下：

  > <center>Non-Manipulating Algorithms</center>
  >  
  > 1. sort(first_iterator, last_iterator)  
  > To sort the given vector.  
  > `排序给定的向量。`
  > 2. reverse(first_iterator, last_iterator)  
  > To reverse a vector.`反转向量。`
  > 3. *max_element (first_iterator, last_iterator)  
  > To find the maximum element of a vector.  
  > `查找向量的最大元素。`
  > 4. *min_element (first_iterator, last_iterator)  
  > To find the minimum element of a vector.  
  > `查找向量的最小元素。`
  > 5. accumulate(first_iterator, last_iterator, initial value of sum)  
  > Does the summation of vector elements.  
  > `对向量元素求和。`
  > 6. count(first_iterator, last_iterator,x)  
  > To count the occurrences of x in vector.  
  > `计算向量中x的出现。`
  > 7. find(first_iterator, last_iterator, x)  
  > Points to last address of vector ((name_of_vector).end()) if element is not present in vector.  
  > `如果向量中不存在元素，则指向向量（（name_of_vector）.end（））的最后地址。`
  > 8. binary_search(first_iterator, last_iterator, x)  
  > Tests whether x exists in sorted vector or not.  
  > `测试x是否存在于排序的向量中。`
  > 9. lower_bound(first_iterator, last_iterator, x)  
  > returns an iterator pointing to the first element in the range [first,last) which has a value not less than ‘x’.  
  > `返回一个迭代器，该迭代器指向[first，last）范围内第一个元素，该元素的值不少于“ x”。`
  > 10. upper_bound(first_iterator, last_iterator, x)  
  > returns an iterator pointing to the first element in the range [first,last) which has a value greater than ‘x’.  
  > `返回一个迭代器，该迭代器指向[first，last）范围内第一个元素的值大于“ x”。`
  > 11. arr.erase(position to be deleted)  
  > This erases selected element in vector and shifts and resizes the vector elements accordingly.  
  > `删除矢量中的选定元素，并相应地移动和调整矢量元素的大小。`
  > 12. arr.erase(unique(arr.begin(),arr.end()),arr.end())  
  > This erases the duplicate occurrences in sorted vector in a single line.  
  > `擦除单行中排序向量中的重复项。`
  > 13. next_permutation(first_iterator, last_iterator)  
  > This modified the vector to its next permutation.  
  > `这将向量修改为其下一个排列。`
  > 14. prev_permutation(first_iterator, last_iterator)  
  > This modified the vector to its previous permutation.  
  > `这将向量修改为其先前的排列。`
  > 15. distance(first_iterator,desired_position)  
  > It returns the distance of desired position from the first iterator.This function is very useful while finding the index.  
  > `返回到第一个迭代器的期望位置的距离。此函数在查找索引时非常有用。`

```c++
/*-----------------------------------------------------------------*/
// A C++ program to demonstrate working of sort(),
// reverse()
#include <algorithm>
#include <iostream>
#include <vector>
#include <numeric> //For accumulate operation
using namespace std;

int main()
{
	// Initializing vector with array values
	int arr[] = {10, 20, 5, 23 ,42 , 15};
	int n = sizeof(arr)/sizeof(arr[0]);
	vector<int> vect(arr, arr+n);

	cout << "Vector is: ";
	for (int i=0; i<n; i++)
		cout << vect[i] << " ";

	// Sorting the Vector in Ascending order
	sort(vect.begin(), vect.end());

	cout << "\nVector after sorting is: ";
	for (int i=0; i<n; i++)
	cout << vect[i] << " ";

	// Reversing the Vector
	reverse(vect.begin(), vect.end());

	cout << "\nVector after reversing is: ";
	for (int i=0; i<6; i++)
		cout << vect[i] << " ";

	cout << "\nMaximum element of vector is: ";
	cout << *max_element(vect.begin(), vect.end());

	cout << "\nMinimum element of vector is: ";
	cout << *min_element(vect.begin(), vect.end());

	// Starting the summation from 0
	cout << "\nThe summation of vector elements is: ";
	cout << accumulate(vect.begin(), vect.end(), 0);

	return 0;
}

<!--Vector before sorting is: 10 20 5 23 42 15 -->
<!--Vector after sorting is: 5 10 15 20 23 42 -->
<!--Vector before reversing is: 5 10 15 20 23 42 -->
<!--Vector after reversing is: 42 23 20 15 10 5 -->
<!--Maximum element of vector is: 42-->
<!--Minimum element of vector is: 5-->
<!--The summation of vector elements is: 115-->



/*------------------------------------------------*/

// C++ program to demonstrate working of count()
// and find()
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main()
{
	// Initializing vector with array values
	int arr[] = {10, 20, 5, 23 ,42, 20, 15};
	int n = sizeof(arr)/sizeof(arr[0]);
	vector<int> vect(arr, arr+n);

	cout << "Occurrences of 20 in vector : ";

	// Counts the occurrences of 20 from 1st to
	// last element
	cout << count(vect.begin(), vect.end(), 20);

	// find() returns iterator to last address if
	// element not present
	find(vect.begin(), vect.end(),5) != vect.end()?
						cout << "\nElement found":
					cout << "\nElement not found";

	return 0;
}


<!--Occurrences of 20 in vector: 2-->
<!--Element found-->


/*-----------------------------------------------------*/

// C++ program to demonstrate working of lower_bound()
// and upper_bound().
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main()
{
	// Initializing vector with array values
	int arr[] = {5, 10, 15, 20, 20, 23, 42, 45};
	int n = sizeof(arr)/sizeof(arr[0]);
	vector<int> vect(arr, arr+n);

	// Sort the array to make sure that lower_bound()
	// and upper_bound() work.
	sort(vect.begin(), vect.end());

	// Returns the first occurrence of 20
	auto q = lower_bound(vect.begin(), vect.end(), 20);

	// Returns the last occurrence of 20
	auto p = upper_bound(vect.begin(), vect.end(), 20);

	cout << "The lower bound is at position: ";
	cout << q-vect.begin() << endl;

	cout << "The upper bound is at position: ";
	cout << p-vect.begin() << endl;

	return 0;
}


<!--The lower bound is at position: 3-->
<!--The upper bound is at position: 5-->


/*----------------------------------------------------*/
// C++ program to demonstrate working of erase()
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main()
{
	// Initializing vector with array values
	int arr[] = {5, 10, 15, 20, 20, 23, 42, 45};
	int n = sizeof(arr)/sizeof(arr[0]);
	vector<int> vect(arr, arr+n);

	cout << "Vector is :";
	for (int i=0; i<6; i++)
		cout << vect[i]<<" ";

	// Delete second element of vector
	vect.erase(vect.begin()+1);

	cout << "\nVector after erasing the element: ";
	for (int i=0; i<5; i++)
		cout << vect[i] << " ";

	// sorting to enable use of unique()
	sort(vect.begin(), vect.end());

	cout << "\nVector before removing duplicate "
			" occurrences: ";
	for (int i=0; i<5; i++)
		cout << vect[i] << " ";

	// Deletes the duplicate occurrences
	vect.erase(unique(vect.begin(),vect.end()),vect.end());

	cout << "\nVector after deleting duplicates: ";
	for (int i=0; i< vect.size(); i++)
		cout << vect[i] << " ";

	return 0;
}



<!--Vector is :5 10 15 20 20 23 -->
<!--Vector after erasing the element: 5 15 20 20 23 -->
<!--Vector before removing duplicate  occurrences: 5 15 20 20 23 -->
<!--Vector after deleting duplicates: 5 15 20 23 42 45 -->


/*------------------------------------------------------*/
// C++ program to demonstrate working of next_permutation()
// and prev_permutation()
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main()
{
	// Initializing vector with array values
	int arr[] = {5, 10, 15, 20, 20, 23, 42, 45};
	int n = sizeof(arr)/sizeof(arr[0]);
	vector<int> vect(arr, arr+n);

	cout << "Given Vector is:\n";
	for (int i=0; i<n; i++)
		cout << vect[i] << " ";

	// modifies vector to its next permutation order
	next_permutation(vect.begin(), vect.end());
	cout << "\nVector after performing next permutation:\n";
	for (int i=0; i<n; i++)
		cout << vect[i] << " ";

	prev_permutation(vect.begin(), vect.end());
	cout << "\nVector after performing prev permutation:\n";
	for (int i=0; i<n; i++)
		cout << vect[i] << " ";

	return 0;
}



<!--Given Vector is:-->
<!--5 10 15 20 20 23 42 45 -->
<!--Vector after performing next permutation:-->
<!--5 10 15 20 20 23 45 42 -->
<!--Vector after performing prev permutation:-->
<!--5 10 15 20 20 23 42 45 -->


/*-------------------------------------------------*/

// C++ program to demonstrate working of distance()
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main()
{
	// Initializing vector with array values
	int arr[] = {5, 10, 15, 20, 20, 23, 42, 45};
	int n = sizeof(arr)/sizeof(arr[0]);
	vector<int> vect(arr, arr+n);

	// Return distance of first to maximum element
	cout << "Distance between first to max element: ";
	cout << distance(vect.begin(),
					max_element(vect.begin(), vect.end()));
	return 0;
}


<!--Distance between first to max element: 7-->
```

[返回目录](#Menu)

- ### <span id="Useful_Array_algorithms">Useful Array algorithms</span>

      From C++ 11 onwards, some new and interesting algorithms are added in STL of C++. These algorithms operate on an array and are useful in saving time during coding and hence useful in competitive programming as well.

      从C ++ 11开始，在C ++的STL中添加了一些有趣的新算法。 这些算法在数组上运行，可用于节省编码时间，因此也可用于竞争性编程。

  > 1. all_of()  
  >    This function operates on whole range of array elements and can save time to run a loop to check each elements one by one. It checks for a given property on every element and returns true when each element in range satisfies specified property, else returns false.  
  >    `此函数可在整个数组元素范围内运行，并且可以节省时间运行循环以逐个检查每个元素。 它检查每个元素上的给定属性，并在范围内的每个元素满足指定属性时返回true，否则返回false。`
  > 2. any_of()  
  >    This function checks for a given range if there’s even one element satisfying a given property mentioned in function. Returns true if at least one element satisfies the property else returns false.  
  >    `如果甚至没有一个元素满足函数中提到的给定属性，则此函数会检查给定范围。 如果至少一个元素满足属性，则返回true，否则返回false。`
  > 3. none_of()  
  >    This function returns true if none of elements satisfies the given condition else returns false.  
  >    `如果没有元素满足给定条件，则此函数返回true，否则返回false。`
  > 4. copy_n()  
  >    copy_n() copies one array elements to new array. This type of copy creates a deep copy of array. This function takes 3 arguments, source array name, size of array and the target array name.  
  >    `copy_n（）将一个数组元素复制到新数组。 这种类型的副本会创建数组的深层副本。 此函数接受3个参数，即源数组名称，数组大小和目标数组名称。`
  >
  > - iota()  
  >   This function is used to assign continuous values to array. This function accepts 3 arguments, the array name, size, and the starting number.  
  >   `此函数用于为数组分配连续值。 该函数接受3个参数，即数组名称，大小和起始编号。`

```c++
// C++ code to demonstrate working of all_of()
#include<iostream>
#include<algorithm> // for all_of()
using namespace std;
int main()
{
	// Initializing array
	int ar[6] = {1, 2, 3, 4, 5, -6};

	// Checking if all elements are positive
	all_of(ar, ar+6, [](int x) { return x>0; })?
		cout << "All are positive elements" :
		cout << "All are not positive elements";

	return 0;

}

<!--All are not positive elements-->

/*----------------------------------------*/

// C++ code to demonstrate working of any_of()
#include<iostream>
#include<algorithm> // for any_of()
using namespace std;
int main()
{
	// Initializing array
	int ar[6] = {1, 2, 3, 4, 5, -6};

	// Checking if any element is negative
	any_of(ar, ar+6, [](int x){ return x<0; })?
		cout << "There exists a negative element" :
		cout << "All are positive elements";

	return 0;

}


<!--There exists a negative element-->

/*---------------------------------------*/

// C++ code to demonstrate working of none_of()
#include<iostream>
#include<algorithm> // for none_of()
using namespace std;
int main()
{
	// Initializing array
	int ar[6] = {1, 2, 3, 4, 5, 6};

	// Checking if no element is negative
	none_of(ar, ar+6, [](int x){ return x<0; })?
		cout << "No negative elements" :
		cout << "There are negative elements";

	return 0;
}


<!--No negative elements-->

/*--------------------------------------------*/

// C++ code to demonstrate working of copy_n()
#include<iostream>
#include<algorithm> // for copy_n()
using namespace std;
int main()
{
	// Initializing array
	int ar[6] = {1, 2, 3, 4, 5, 6};

	// Declaring second array
	int ar1[6];

	// Using copy_n() to copy contents
	copy_n(ar, 6, ar1);

	// Displaying the copied array
	cout << "The new array after copying is : ";
	for (int i=0; i<6 ; i++)
	cout << ar1[i] << " ";

	return 0;

}


<!--The new array after copying is : 1 2 3 4 5 6-->

/*-----------------------------------------*/

// C++ code to demonstrate working of iota()
#include<iostream>
#include<numeric> // for iota()
using namespace std;
int main()
{
	// Initializing array with 0 values
	int ar[6] = {0};

	// Using iota() to assign values
	iota(ar, ar+6, 20);

	// Displaying the new array
	cout << "The new array after assigning values is : ";
	for (int i=0; i<6 ; i++)
	cout << ar[i] << " ";

	return 0;

}


<!--The new array after assigning values is : 20 21 22 23 24 25-->
```

[返回目录](#Menu)

- ### <span id="Partition_Operations">Partition Operations</span>

      C++ has a class in its STL algorithms library which allows us easy partition algorithms using certain inbuilt functions. Partition refers to act of dividing elements of containers depending upon a given condition.

      C ++在其STL算法库中有一个类，该类允许我们使用某些内置函数轻松进行分区算法。分区是指根据给定条件划分容器元素的动作。

  > Partition operations :
  >
  > 1. partition(beg, end, condition)  
  >    This function is used to partition the elements on basis of condition mentioned in its arguments.  
  >    `此函数用于根据参数中提到的条件对元素进行分区。`
  > 2. is_partitioned(beg, end, condition)  
  >    This function returns boolean true if container is partitioned else returns false.  
  >    `如果容器已分区，则此函数返回true，否则返回false。`
  > 3. stable_partition(beg, end, condition)  
  >    This function is used to partition the elements on basis of condition mentioned in its arguments in such a way that the relative order of the elements is preserved.  
  >    `该函数用于根据参数中提到的条件对元素进行分区，以保留元素的相对顺序。`
  > 4. partition_point(beg, end, condition)  
  >    This function returns an iterator pointing to the partition point of container i.e. the first element in the partitioned range [beg,end) for which condition is not true. The container should already be partitioned for this function to work.  
  >    `此函数返回一个迭代器，该迭代器指向容器的分区点，即条件不成立的分区范围[beg，end）中的第一个元素。容器应该已经分区了，此功能才能起作用。`
  > 5. partition_copy(beg, end, beg1, beg2, condition)  
  >    This function copies the partitioned elements in the differenet containers mentioned in its arguments. It takes 5 arguments. Beginning and ending position of container, beginning position of new container where elements have to be copied (elements returning true for condition), beginning position of new container where other elements have to be copied (elements returning false for condition) and the condition. Resizing new containers is necessary for this function.  
  >    `此函数将其分区中的分区元素复制到其参数中提到的differnet容器中。它需要5个参数。容器的开始和结束位置，必须复制元素的新容器的开始位置（元素返回条件为true），必须复制其他元素的新容器的开始位置（元素返回条件为false）和条件。调整新容器的大小对于此功能是必需的。`

```c++
// C++ code to demonstrate the working of
// partition() and is_partitioned()
#include<iostream>
#include<algorithm> // for partition algorithm
#include<vector> // for vector
using namespace std;
int main()
{
	// Initializing vector
	vector<int> vect = { 2, 1, 5, 6, 8, 7 };

	// Checking if vector is partitioned
	// using is_partitioned()
	is_partitioned(vect.begin(), vect.end(), [](int x)
	{
		return x%2==0;

	})?

	cout << "Vector is partitioned":
	cout << "Vector is not partitioned";
	cout << endl;

	// partitioning vector using partition()
	partition(vect.begin(), vect.end(), [](int x)
	{
		return x%2==0;

	});

	// Checking if vector is partitioned
	// using is_partitioned()
	is_partitioned(vect.begin(), vect.end(), [](int x)
	{
		return x%2==0;

	})?

	cout << "Now, vector is partitioned after partition operation":
	cout << "Vector is still not partitioned after partition operation";
	cout << endl;

	// Displaying partitioned Vector
	cout << "The partitioned vector is : ";
	for (int &x : vect) cout << x << " ";

	return 0;

}


<!--Vector is not partitioned-->
<!--Now, vector is partitioned after partition operation-->
<!--The partitioned vector is : 2 8 6 5 1 7 -->


/*---------------------------------------------------*/

// C++ code to demonstrate the working of
// stable_partition() and partition_point()
#include<iostream>
#include<algorithm> // for partition algorithm
#include<vector> // for vector
using namespace std;
int main()
{
	// Initializing vector
	vector<int> vect = { 2, 1, 5, 6, 8, 7 };

	// partitioning vector using stable_partition()
	// in sorted order
	stable_partition(vect.begin(), vect.end(), [](int x)
	{
		return x%2 == 0;
	});

	// Displaying partitioned Vector
	cout << "The partitioned vector is : ";
	for (int &x : vect) cout << x << " ";
	cout << endl;

	// Declaring iterator
	vector<int>::iterator it1;

	// using partition_point() to get ending position of partition
	auto it = partition_point(vect.begin(), vect.end(), [](int x)
	{
		return x%2==0;
	});

	// Displaying partitioned Vector
	cout << "The vector elements returning true for condition are : ";
	for ( it1= vect.begin(); it1!=it; it1++)
	cout << *it1 << " ";
	cout << endl;

	return 0;

}


<!--The partitioned vector is : 2 6 8 1 5 7 -->
<!--The vector elements returning true for condition are : 2 6 8 -->

/*--------------------------------------------------*/


// C++ code to demonstrate the working of
// partition_copy()
#include<iostream>
#include<algorithm> // for partition algorithm
#include<vector> // for vector
using namespace std;
int main()
{
	// Initializing vector
	vector<int> vect = { 2, 1, 5, 6, 8, 7 };

	// Declaring vector1
	vector<int> vect1;

	// Declaring vector1
	vector<int> vect2;

	// Resizing vectors to suitable size using count_if() and resize()
	int n = count_if (vect.begin(), vect.end(), [](int x)
	{
		return x%2==0;

	} );
	vect1.resize(n);
	vect2.resize(vect.size()-n);

	// Using partition_copy() to copy partitions
	partition_copy(vect.begin(), vect.end(), vect1.begin(),
									vect2.begin(), [](int x)
	{
		return x%2==0;
	});


	// Displaying partitioned Vector
	cout << "The elements that return true for condition are : ";
	for (int &x : vect1)
			cout << x << " ";
	cout << endl;

	// Displaying partitioned Vector
	cout << "The elements that return false for condition are : ";
	for (int &x : vect2)
			cout << x << " ";
	cout << endl;

	return 0;
}


<!--The elements that return true for condition are : 2 6 8 -->
<!--The elements that return false for condition are : 1 5 7 -->

```

[返回目录](#Menu)

## 2. <span id="Numeric">Numeric</span>

- ### <span id="valarray_class">valarray class</span>
  C++98 introduced a special container called valarray to hold and provide mathematical operations on arrays efficiently.
  - It supports element-wise mathematical operations and various forms of generalized subscript operators, slicing and indirect access.
  - As compare to vectors, valarrays are efficient in certain mathematical operations than vectors also.
    C ++ 98 引入了一个名为 valarray 的特殊容器，可以有效地保存并提供对数组的数学运算。
  - 它支持按元素进行数学运算以及各种形式的广义下标运算符，切片和间接访问。
  - 与向量相比，valarray 在某些数学运算中比向量更有效。

> Public member functions in valarray class :
>
> 1. apply()  
>    This function applies the manipulation given in its arguments to all the valarray elements at once and returns a new valarray with manipulated values.  
>    `此函数立即将其参数中给出的操作应用于所有valarray元素，并返回具有操作值的新valarray。`
> 2. sum()  
>    This function returns the summation of all the elements of valarrays at once.  
>    `此函数一次返回valarrays所有元素的总和。`
> 3. min()  
>    This function returns the smallest element of valarray.  
>    `此函数返回valarray的最小元素。`
> 4. max()  
>    This function returns the largest element of valarray.  
>    `此函数返回valarray的最大元素。`
> 5. shift()  
>    This function returns the new valarray after shifting elements by the number mentioned in its argument. If the number is positive, left-shift is applied, if number is negative, right-shift is applied.  
>    `该函数在将元素移位其参数中提到的数字后返回新的valarray。 如果数字为正，则应用左移；如果数字为负，则应用右移。`
> 6. cshift()  
>    This function returns the new valarray after circularly shifting(rotating) elements by the number mentioned in its argument. If the number is positive, left-circular shift is applied, if number is negative, right-circular shift is applied.  
>    `该函数将元素循环移位（旋转）其参数中提到的数字后，将返回新的valarray。 如果数字为正，则应用左圆周移位；如果数字为负，则应用右圆周移位。`
> 7. swap()  
>    This function swaps one valarray with other.  
>    `此函数将一个valarray与另一个交换。`

```c++
// C++ code to demonstrate the working of
// apply() and sum()
#include<iostream>
#include<valarray> // for valarray functions
using namespace std;
int main()
{
	// Initializing valarray
	valarray<int> varr = { 10, 2, 20, 1, 30 };

	// Declaring new valarray
	valarray<int> varr1 ;

	// Using apply() to increment all elements by 5
	varr1 = varr.apply([](int x){return x=x+5;});

	// Displaying new elements value
	cout << "The new valarray with manipulated values is : ";
	for (int &x: varr1) cout << x << " ";
	cout << endl;

	// Displaying sum of both old and new valarray
	cout << "The sum of old valarray is : ";
	cout << varr.sum() << endl;
	cout << "The sum of new valarray is : ";
	cout << varr1.sum() << endl;

	return 0;

}



<!--The new valarray with manipulated values is : 15 7 25 6 35 -->
<!--The sum of old valarray is : 63-->
<!--The sum of new valarray is : 88-->


/*----------------------------------------------------*/

// C++ code to demonstrate the working of
// max() and min()
#include<iostream>
#include<valarray> // for valarray functions
using namespace std;
int main()
{
	// Initializing valarray
	valarray<int> varr = { 10, 2, 20, 1, 30 };

	// Displaying largest element of valarray
	cout << "The largest element of valarray is : ";
	cout << varr.max() << endl;

	// Displaying smallest element of valarray
	cout << "The smallest element of valarray is : ";
	cout << varr.min() << endl;

	return 0;

}



<!--The largest element of valarray is : 30-->
<!--The smallest element of valarray is : 1-->


/*-------------------------------------------------*/

// C++ code to demonstrate the working of
// shift() and cshift()
#include<iostream>
#include<valarray> // for valarray functions
using namespace std;
int main()
{
	// Initializing valarray
	valarray<int> varr = { 10, 2, 20, 1, 30 };

	// Declaring new valarray
	valarray<int> varr1;

	// using shift() to shift elements to left
	// shifts valarray by 2 position
	varr1 = varr.shift(2);

	// Displaying elements of valarray after shifting
	cout << "The new valarray after shifting is : ";
	for ( int&x : varr1) cout << x << " ";
	cout << endl;

	// using cshift() to circulary shift elements to right
	// rotates valarray by 3 position
	varr1 = varr.cshift(-3);

	// Displaying elements of valarray after circular shifting
	cout << "The new valarray after circular shifting is : ";
	for ( int&x : varr1) cout << x << " ";
	cout << endl;

	return 0;

}



<!--The new valarray after shifting is : 20 1 30 0 0 -->
<!--The new valarray after circular shifting is : 20 1 30 10 2 -->


/*--------------------------------------------------------*/

// C++ code to demonstrate the working of
// swap()
#include<iostream>
#include<valarray> // for valarray functions
using namespace std;
int main()
{
// Initializing 1st valarray
	valarray<int> varr1 = {1, 2, 3, 4};

	// Initializing 2nd valarray
	valarray<int> varr2 = {2, 4, 6, 8};

	// Displaying valarrays before swapping
	cout << "The contents of 1st valarray "
			"before swapping are : ";
	for (int &x : varr1)
		cout << x << " ";
	cout << endl;
	cout << "The contents of 2nd valarray "
			"before swapping are : ";
	for (int &x : varr2)
		cout << x << " ";
	cout << endl;

	// Use of swap() to swap the valarrays
	varr1.swap(varr2);

	// Displaying valarrays after swapping
	cout << "The contents of 1st valarray "
			"after swapping are : ";
	for (int &x : varr1)
		cout << x << " ";
	cout << endl;

	cout << "The contents of 2nd valarray "
			"after swapping are : ";
	for (int &x : varr2)
		cout << x << " ";
	cout << endl;

	return 0;

}



<!--The contents of 1st valarray before swapping are : 1 2 3 4 -->
<!--The contents of 2nd valarray before swapping are : 2 4 6 8 -->
<!--The contents of 1st valarray after swapping are : 2 4 6 8 -->
<!--The contents of 2nd valarray after swapping are : 1 2 3 4 -->
```

[返回目录](#Menu)

# 二. <span id="Containers">Containers</span>

> Containers or container classes store objects and data. There are in total seven standard “first-class” container classes and three container adaptor classes and only seven header files that provide access to these containers or container adaptors.  
> 容器或容器类存储对象和数据。总共有七个标准的“一流”容器类和三个容器适配器类，并且只有七个头文件可提供对这些容器或容器适配器的访问。

## 1. <span id="Sequence_Containers">Sequence Containers</span> [^sequence_containers]

- ### <span id="vector">vector</span>
  Vectors are same as dynamic arrays with the ability to resize itself automatically when an element is inserted or deleted, with their storage being handled automatically by the container. Vector elements are placed in contiguous storage so that they can be accessed and traversed using iterators. In vectors, data is inserted at the end. Inserting at the end takes differential time, as sometimes there may be a need of extending the array. Removing the last element takes only constant time because no resizing happens. Inserting and erasing at the beginning or in the middle is linear in time.
  向量与动态数组一样，当插入或删除元素时，向量可以自动调整自身大小，容器会自动处理向量的存储。向量元素被放置在连续的存储器中，这样就可以使用迭代器访问和遍历它们。在向量中，数据是在末尾插入的。在末尾插入需要不同的时间，因为有时可能需要扩展数组。移除最后一个元素只需要固定的时间，因为没有调整大小。开始或中间的插入和删除在时间上是线性的。
- ###### All Vector Function
  |            -            |              -               |              -              |            -            |
  | :---------------------: | :--------------------------: | :-------------------------: | :---------------------: |
  |  [vector::begin()](#)   |      [vector::end()](#)      |    [vector::rbegin()](#)    |   [vector::rend()](#)   |
  |  [vector::cbegin()](#)  |     [vector::cend()](#)      |    [vector::crend()](#)     | [vector::crbegin()](#)  |
  |  [vector::assign()](#)  |      [vector::at()](#)       |     [vector::back()](#)     | [vector::capacity()](#) |
  |  [vector::clear()](#)   |   [vector::push_back()](#)   |   [vector::pop_back()](#)   |  [vector::empty()](#)   |
  |  [vector::erase()](#)   |     [vector::size()](#)      |     [vector::swap()](#)     | [vector::reserve()](#)  |
  |  [vector::resize()](#)  | [vector::shrink_to_fit()](#) |   [vector::operator=](#)    | [vector::operator[]](#) |
  |  [vector::front()](#)   |     [vector::data()](#)      | [vector::emplace_back()](#) | [vector::emplace()](#)  |
  | [vector::max_size()](#) |    [vector::insert()](#)     |

> Certain functions associated with the vector are:  
> `与向量相关的某些函数有：`
>
> - Iterators
>
> 1. begin()  
>    Returns an iterator pointing to the first element in the vector  
>    `返回指向向量中第一个元素的迭代器`
> 2. end()  
>    Returns an iterator pointing to the theoretical element that follows the last element in the vector  
>    `返回指向向量中最后一个元素后面的理论元素的迭代器`
> 3. rbegin()  
>    Returns a reverse iterator pointing to the last element in the vector (reverse beginning). It moves from last to first element  
>    `返回指向向量中最后一个元素的反向迭代器（反向开始）。它从最后一个元素移动到第一个元素`
> 4. rend()  
>    Returns a reverse iterator pointing to the theoretical element preceding the first element in the vector (considered as reverse end)  
>    `返回指向向量中第一个元素前面的理论元素的反向迭代器（视为反向结束）`
> 5. cbegin()  
>    Returns a constant iterator pointing to the first element in the vector.  
>    `返回指向向量中第一个元素的常量迭代器。`
> 6. cend()  
>    Returns a constant iterator pointing to the theoretical element that follows the last element in the vector.  
>    `返回一个常量迭代器，该迭代器指向向量中最后一个元素后面的理论元素。`
> 7. crbegin()  
>    Returns a constant reverse iterator pointing to the last element in the vector (reverse beginning). It moves from last to first element
>    `返回指向向量中最后一个元素的常量反向迭代器（反向开始）。它从最后一个元素移动到第一个元素`
> 8. crend()  
>    Returns a constant reverse iterator pointing to the theoretical element preceding the first element in the vector (considered as reverse end)  
>    `返回一个常量反向迭代器，该迭代器指向向量中第一个元素之前的理论元素（视为反向结束）`
>
> - Capacity
>
> 1. size()  
>    Returns the number of elements in the vector.  
>    `返回矢量中的元素数。`
> 2. max_size()  
>    Returns the maximum number of elements that the vector can hold.  
>    `返回向量可以容纳的最大元素数。`
> 3. capacity()  
>    Returns the size of the storage space currently allocated to the vector expressed as number of elements.  
>    `返回当前分配给向量的存储空间大小，用元素数表示。`
> 4. resize(n)  
>    Resizes the container so that it contains ‘n’ elements.  
>    `调整容器大小，使其包含“n”个元素。`
> 5. empty()  
>    Returns whether the container is empty.  
>    `返回容器是否为空。`
> 6. shrink_to_fit()  
>    Reduces the capacity of the container to fit its size and destroys all elements beyond the capacity.  
>    `减少容器的容量以适合其大小，并销毁超出容量的所有元素。`
> 7. reserve()  
>    Requests that the vector capacity be at least enough to contain n elements.  
>    `要求向量容量至少足以包含n个元素。`
>
> - Element access:
>
> 1. reference operator [g]  
>    Returns a reference to the element at position ‘g’ in the vector  
>    `返回对向量中位置“g”处元素的引用`
> 2. at(g)  
>    Returns a reference to the element at position ‘g’ in the vector  
>    `返回对向量中位置“g”处元素的引用`
> 3. front()  
>    Returns a reference to the first element in the vector  
>    `返回对向量中第一个元素的引用`
> 4. back()  
>    Returns a reference to the last element in the vector  
>    `返回对向量中最后一个元素的引用`
> 5. data()  
>    Returns a direct pointer to the memory array used internally by the vector to store its owned elements.  
>    `返回指向向量内部用于存储其所属元素的内存数组的直接指针。`
>
> - Modifiers:
>
> 1. assign()  
>    It assigns new value to the vector elements by replacing old ones  
>    `它通过替换旧元素来为向量元素赋值`
> 2. push_back()  
>    It push the elements into a vector from the back  
>    `它将元素从后面推到一个向量中`
> 3. pop_back()  
>    It is used to pop or remove elements from a vector from the back.  
>    `它用于从后面弹出或删除向量中的元素。`
> 4. insert()  
>    It inserts new elements before the element at the specified position  
>    `它在元素之前的指定位置插入新元素`
> 5. erase()  
>    It is used to remove elements from a container from the specified position or range.  
>    `它用于从容器的指定位置或范围移除元素。`
> 6. swap()  
>    It is used to swap the contents of one vector with another vector of same type. Sizes may differ.  
>    `它用于将一个向量的内容与另一个相同类型的向量交换。尺寸可能不同。`
> 7. clear()  
>    It is used to remove all the elements of the vector container  
>    `它用于移除向量容器的所有元素`
> 8. emplace()  
>    It extends the container by inserting new element at position  
>    `它通过在位置插入新元素来扩展容器`
> 9. emplace_back()  
>    It is used to insert a new element into the vector container, the new element is added to the end of the vector  
>    `它用于在向量容器中插入新元素，新元素被添加到向量的末尾`

```c++

// C++ program to illustrate the
// iterators in vector
#include <iostream>
#include <vector>

using namespace std;

int main()
{
	vector<int> g1;

	for (int i = 1; i <= 5; i++)
		g1.push_back(i);

	cout << "Output of begin and end: ";
	for (auto i = g1.begin(); i != g1.end(); ++i)
		cout << *i << " ";

	cout << "\nOutput of cbegin and cend: ";
	for (auto i = g1.cbegin(); i != g1.cend(); ++i)
		cout << *i << " ";

	cout << "\nOutput of rbegin and rend: ";
	for (auto ir = g1.rbegin(); ir != g1.rend(); ++ir)
		cout << *ir << " ";

	cout << "\nOutput of crbegin and crend : ";
	for (auto ir = g1.crbegin(); ir != g1.crend(); ++ir)
		cout << *ir << " ";

	return 0;
}


<!--Output of begin and end: 1 2 3 4 5 -->
<!--Output of cbegin and cend: 1 2 3 4 5 -->
<!--Output of rbegin and rend: 5 4 3 2 1 -->
<!--Output of crbegin and crend : 5 4 3 2 1-->

/*----------------------------------------------------------*/

// C++ program to illustrate the
// capacity function in vector
#include <iostream>
#include <vector>

using namespace std;

int main()
{
	vector<int> g1;

	for (int i = 1; i <= 5; i++)
		g1.push_back(i);

	cout << "Size : " << g1.size();
	cout << "\nCapacity : " << g1.capacity();
	cout << "\nMax_Size : " << g1.max_size();

	// resizes the vector size to 4
	g1.resize(4);

	// prints the vector size after resize()
	cout << "\nSize : " << g1.size();

	// checks if the vector is empty or not
	if (g1.empty() == false)
		cout << "\nVector is not empty";
	else
		cout << "\nVector is empty";

	// Shrinks the vector
	g1.shrink_to_fit();
	cout << "\nVector elements are: ";
	for (auto it = g1.begin(); it != g1.end(); it++)
		cout << *it << " ";

	return 0;
}


<!--Size : 5-->
<!--Capacity : 8-->
<!--Max_Size : 4611686018427387903-->
<!--Size : 4-->
<!--Vector is not empty-->
<!--Vector elements are: 1 2 3 4-->

/*---------------------------------------------------------*/

// C++ program to illustrate the
// element accesser in vector
#include <bits/stdc++.h>
using namespace std;

int main()
{
	vector<int> g1;

	for (int i = 1; i <= 10; i++)
		g1.push_back(i * 10);

	cout << "\nReference operator [g] : g1[2] = " << g1[2];

	cout << "\nat : g1.at(4) = " << g1.at(4);

	cout << "\nfront() : g1.front() = " << g1.front();

	cout << "\nback() : g1.back() = " << g1.back();

	// pointer to the first element
	int* pos = g1.data();

	cout << "\nThe first element is " << *pos;
	return 0;
}


<!--Reference operator [g] : g1[2] = 30-->
<!--at : g1.at(4) = 50-->
<!--front() : g1.front() = 10-->
<!--back() : g1.back() = 100-->
<!--The first element is 10-->


/*------------------------------------------------------------*/

// C++ program to illustrate the
// Modifiers in vector
#include <bits/stdc++.h>
#include <vector>
using namespace std;

int main()
{
	// Assign vector
	vector<int> v;

	// fill the array with 10 five times
	v.assign(5, 10);

	cout << "The vector elements are: ";
	for (int i = 0; i < v.size(); i++)
		cout << v[i] << " ";

	// inserts 15 to the last position
	v.push_back(15);
	int n = v.size();
	cout << "\nThe last element is: " << v[n - 1];

	// removes last element
	v.pop_back();

	// prints the vector
	cout << "\nThe vector elements are: ";
	for (int i = 0; i < v.size(); i++)
		cout << v[i] << " ";

	// inserts 5 at the beginning
	v.insert(v.begin(), 5);

	cout << "\nThe first element is: " << v[0];

	// removes the first element
	v.erase(v.begin());

	cout << "\nThe first element is: " << v[0];

	// inserts at the beginning
	v.emplace(v.begin(), 5);
	cout << "\nThe first element is: " << v[0];

	// Inserts 20 at the end
	v.emplace_back(20);
	n = v.size();
	cout << "\nThe last element is: " << v[n - 1];

	// erases the vector
	v.clear();
	cout << "\nVector size after erase(): " << v.size();

	// two vector to perform swap
	vector<int> v1, v2;
	v1.push_back(1);
	v1.push_back(2);
	v2.push_back(3);
	v2.push_back(4);

	cout << "\n\nVector 1: ";
	for (int i = 0; i < v1.size(); i++)
		cout << v1[i] << " ";

	cout << "\nVector 2: ";
	for (int i = 0; i < v2.size(); i++)
		cout << v2[i] << " ";

	// Swaps v1 and v2
	v1.swap(v2);

	cout << "\nAfter Swap \nVector 1: ";
	for (int i = 0; i < v1.size(); i++)
		cout << v1[i] << " ";

	cout << "\nVector 2: ";
	for (int i = 0; i < v2.size(); i++)
		cout << v2[i] << " ";
}


<!--The vector elements are: 10 10 10 10 10 -->
<!--The last element is: 15-->
<!--The vector elements are: 10 10 10 10 10 -->
<!--The first element is: 5-->
<!--The first element is: 10-->
<!--The first element is: 5-->
<!--The last element is: 20-->
<!--Vector size after erase(): 0-->

<!--Vector 1: 1 2 -->
<!--Vector 2: 3 4 -->
<!--After Swap -->
<!--Vector 1: 3 4 -->
<!--Vector 2: 1 2-->
```

[返回目录](#Menu)

- ### <span id="list">list</span>
  Lists are sequence containers that allow non-contiguous memory allocation. As compared to vector, list has slow traversal, but once a position has been found, insertion and deletion are quick. Normally, when we say a List, we talk about doubly linked list. For implementing a singly linked list, we use forward list.
  列表是允许非连续内存分配的序列容器。和 vector 相比，list 遍历速度较慢，但一旦找到位置，插入和删除都很快。通常，当我们说一个列表时，我们谈论的是双链表。为了实现一个单链表，我们使用 forward list。

> Functions used with List:
>
> 1. front()  
>    Returns the value of the first element in the list.  
>    `返回列表中第一个元素的值。`
> 2. back()  
>    Returns the value of the last element in the list .  
>    `返回列表中最后一个元素的值。`
> 3. push_front(g)  
>    Adds a new element ‘g’ at the beginning of the list .  
>    `在列表的开头添加新元素“g”。`
> 4. push_back(g)  
>    Adds a new element ‘g’ at the end of the list.  
>    `在列表末尾添加新元素“g”。`
> 5. pop_front()  
>    Removes the first element of the list, and reduces size of the list by 1.  
>    `删除列表的第一个元素，并将列表大小减小1。`
> 6. pop_back()  
>    Removes the last element of the list, and reduces size of the list by 1.  
>    `删除列表的最后一个元素，并将列表大小减小1。`
> 7. list::begin() and list::end() in C++ STL  
>    begin() function returns an iterator pointing to the first element of the list.  
>    `函数begin()返回指向列表第一个元素的迭代器。`  
>    end() function returns an iterator pointing to the theoretical last element which follows the last element.  
>    `函数end()返回一个迭代器，该迭代器指向最后一个元素后面的理论上的最后一个元素。`
> 8. list rbegin() and rend() function in C++ STL  
>    rbegin() returns a reverse iterator which points to the last element of the list. rend() returns a reverse iterator which points to the position before the beginning of the list.  
>    `rbegin（）返回指向列表最后一个元素的反向迭代器。rend（）返回一个反向迭代器，它指向列表开头之前的位置。`
> 9. list cbegin() and cend() function in C++ STL  
>    cbegin() returns a constant random access iterator which points to the beginning of the list. cend() returns a constant random access iterator which points to the end of the list.  
>    `cbegin（）返回指向列表开头的常量随机访问迭代器。cend（）返回指向列表末尾的常量随机访问迭代器。`
> 10. list crbegin() and crend() function in C++ STL  
>     crbegin() returns a constant reverse iterator which points to the last element of the list i.e reversed beginning of container. crend() returns a constant reverse iterator which points to the theoretical element preceding the first element in the list i.e. the reverse end of the list.  
>     `crbegin（）返回一个常量反向迭代器，它指向列表的最后一个元素，即容器的反向开头。crend（）返回一个常量反向迭代器，该迭代器指向列表中第一个元素之前的理论元素，即列表的反向结尾。`
> 11. empty()  
>     Returns whether the list is empty(1) or not(0).  
>     `返回列表是否为空（1）或非空（0）。`
> 12. insert()  
>     Inserts new elements in the list before the element at a specified position.  
>     `在列表中元素之前的指定位置插入新元素。`
> 13. erase()  
>     Removes a single element or a range of elements from the list.  
>     `从列表中删除单个元素或一系列元素。`
> 14. assign()  
>     Assigns new elements to list by replacing current elements and resizes the list.  
>     `通过替换当前元素将新元素指定给列表，并调整列表大小。`
> 15. remove()  
>     Removes all the elements from the list, which are equal to given element.  
>     `从列表中删除与给定元素相等的所有元素。`
> 16. list::remove_if() in C++ STL  
>     Used to remove all the values from the list that correspond true to the predicate or condition given as parameter to the function.  
>     `用于从列表中删除与作为函数参数给定的谓词或条件相对应的所有值。`
> 17. reverse()  
>     Reverses the list.  
>     `反转列表。`
> 18. size()  
>     Returns the number of elements in the list.  
>     `返回列表中的元素数。`
> 19. list resize() function in C++ STL  
>     Used to resize a list container.  
>     `用于调整列表容器的大小。`
> 20. sort()  
>     Sorts the list in increasing order.  
>     `按递增顺序对列表排序。`
> 21. list max_size() function in C++ STL  
>     Returns the maximum number of elements a list container can hold.  
>     `返回列表容器可以容纳的最大元素数。`
> 22. list unique() in C++ STL  
>     Removes all duplicate consecutive elements from the list.  
>     `从列表中删除所有重复的连续元素。`
> 23. list::emplace_front() and list::emplace_back() in C++ STL  
>     emplace_front() function is used to insert a new element into the list container, the new element is added to the beginning of the list. emplace_back() function is used to insert a new element into the list container, the new element is added to the end of the list.  
>     `emplace_front（）函数用于在列表容器中插入新元素，将新元素添加到列表的开头。emplace_back（）函数用于在列表容器中插入新元素，将新元素添加到列表的末尾。`
> 24. list::clear() in C++ STL  
>     clear() function is used to remove all the elements of the list container, thus making it size 0.  
>     `clear（）函数用于删除列表容器的所有元素，从而使其大小为0。`
> 25. list::operator= in C++ STL  
>     This operator is used to assign new contents to the container by replacing the existing contents.  
>     `此运算符用于通过替换现有内容将新内容分配给容器。`
> 26. list::swap() in C++ STL  
>     This function is used to swap the contents of one list with another list of same type and size.  
>     `此函数用于将一个列表的内容与另一个类型和大小相同的列表交换。`
> 27. list splice() function in C++ STL  
>     Used to transfer elements from one list to another.  
>     `用于将元素从一个列表转移到另一个列表。`
> 28. list merge() function in C++ STL  
>     Merges two sorted lists into one.  
>     `将两个已排序的列表合并为一个。`
> 29. list emplace() function in C++ STL  
>     Extends list by inserting new element at a given position.  
>     `通过在给定位置插入新元素来扩展列表。`

```c++
#include <iostream>
#include <list>
#include <iterator>
using namespace std;

//function for printing the elements in a list
void showlist(list <int> g)
{
	list <int> :: iterator it;
	for(it = g.begin(); it != g.end(); ++it)
		cout << '\t' << *it;
	cout << '\n';
}

int main()
{

	list <int> gqlist1, gqlist2;


	for (int i = 0; i < 10; ++i)
	{
		gqlist1.push_back(i * 2);
		gqlist2.push_front(i * 3);
	}
	cout << "\nList 1 (gqlist1) is : ";
	showlist(gqlist1);

	cout << "\nList 2 (gqlist2) is : ";
	showlist(gqlist2);

	cout << "\ngqlist1.front() : " << gqlist1.front();
	cout << "\ngqlist1.back() : " << gqlist1.back();

	cout << "\ngqlist1.pop_front() : ";
	gqlist1.pop_front();
	showlist(gqlist1);

	cout << "\ngqlist2.pop_back() : ";
	gqlist2.pop_back();
	showlist(gqlist2);

	cout << "\ngqlist1.reverse() : ";
	gqlist1.reverse();
	showlist(gqlist1);

	cout << "\ngqlist2.sort(): ";
	gqlist2.sort();
	showlist(gqlist2);

	return 0;

}

<!--List 1 (gqlist1) is :     0    2    4    6    -->
<!--8    10    12    14    16    18-->

<!--List 2 (gqlist2) is :     27    24    21    18    -->
<!--15    12    9    6    3    0-->

<!--gqlist1.front() : 0-->
<!--gqlist1.back() : 18-->
<!--gqlist1.pop_front() :     2    4    6    8    -->
<!--10    12    14    16    18-->

<!--gqlist2.pop_back() :     27    24    21    18    -->
<!--15    12    9    6    3-->

<!--gqlist1.reverse() :     18    16    14    12    -->
<!--10    8    6    4    2-->

<!--gqlist2.sort():     3    6    9    12    -->
<!--15    18    21    24    27-->

```

[返回目录](#Menu)

- ### <span id="deque">deque</span>

      Double ended queues are sequence containers with the feature of expansion and contraction on both the ends.
      They are similar to vectors, but are more efficient in case of insertion and deletion of elements. Unlike vectors, contiguous storage allocation may not be guaranteed.
      Double Ended Queues are basically an implementation of the data structure double ended queue. A queue data structure allows insertion only at the end and deletion from the front. This is like a queue in real life, wherein people are removed from the front and added at the back. Double ended queues are a special case of queues where insertion and deletion operations are possible at both the ends.
      The functions for deque are same as vector, with an addition of push and pop operations for both front and back.

      双端队列是序列容器，两端具有扩张和收缩的特性。
      它们类似于向量，但在插入和删除元素时效率更高。与向量不同，连续存储分配可能无法保证。
      双端队列基本上是数据结构双头队列的一种实现。队列数据结构只允许在末尾插入，从前面删除。这就像现实生活中的一个队列，人们从前面被移走，在后面添加。双端队列是队列的一种特殊情况，在这种情况下，两端都可以执行插入和删除操作。
      deque的函数与vector相同，在前面和后面都添加了push和pop操作。

  > 1. deque insert() function in C++ STL:  
  >    Inserts an element. And returns an iterator that points to the first of the newly inserted elements.  
  >    `插入元素。并返回一个迭代器，该迭代器指向新插入的第一个元素。`
  > 2. deque rbegin() function in C++ STL:  
  >    Returns a reverse iterator which points to the last element of the deque (i.e., its reverse beginning).  
  >    `返回一个反向迭代器，它指向deque的最后一个元素（即，它的反向开始）。`
  > 3. deque rend() function in C++ STL:  
  >    Returns a reverse iterator which points to the position before the beginning of the deque (which is considered its reverse end).  
  >    `返回一个反向迭代器，它指向deque开始之前的位置（被认为是deque的反向结束）。`
  > 4. deque cbegin() in C++ STL:  
  >    Returns a constant iterator pointing to the first element of the container, that is, the iterator cannot be used to modify, only traverse the deque.  
  >    `返回指向容器第一个元素的常量迭代器，即迭代器不能用于修改，只能遍历deque。`
  > 5. deque max_size() function in C++ STL:  
  >    Returns the maximum number of elements that a deque container can hold.  
  >    `返回deque容器可以容纳的最大元素数。`
  > 6. deque assign() function in C++ STL:  
  >    Assign values to the same or different deque container.  
  >    `为相同或不同的deque容器指定值。`
  > 7. deque resize() function in C++ STL:  
  >    Function which changes the size of the deque.  
  >    `改变deque大小的函数。`
  > 8. deque::push_front() in C++ STL:  
  >    This function is used to push elements into a deque from the front.  
  >    `此函数用于将元素从前面推入deque。`
  > 9. deque::push_back() in C++ STL:  
  >    This function is used to push elements into a deque from the back.  
  >    `此函数用于从后面将元素推入deque。`
  > 10. deque::pop_front() and deque::pop_back() in C++ STL:  
  >     pop_front() function is used to pop or remove elements from a deque from the front. pop_back() function is used to pop or remove elements from a deque from the back.  
  >     `函数用于从前面弹出或删除deque中的元素。函数用于从后面弹出或删除deque中的元素。`
  > 11. deque::front() and deque::back() in C++ STL:  
  >     front() function is used to reference the first element of the deque container. back() function is used to reference the last element of the deque container.  
  >     `函数用于引用deque容器的第一个元素。函数用于引用deque容器的最后一个元素。`
  > 12. deque::clear() and deque::erase() in C++ STL:  
  >     clear() function is used to remove all the elements of the deque container, thus making its size 0. erase() function is used to remove elements from a container from the specified position or range.  
  >     `clear（）函数用于删除deque容器的所有元素，从而使其大小为0。函数的作用是：从容器的指定位置或范围中删除元素。`
  > 13. deque::empty() and deque::size() in C++ STL:  
  >     empty() function is used to check if the deque container is empty or not. size() function is used to return the size of the deque container or the number of elements in the deque container.  
  >     `如果函数deque（）为空，则使用该函数检查容器是否为空。函数用于返回deque容器的大小或deque容器中元素的数量。`
  > 14. deque::operator= and deque::operator[] in C++ STL:  
  >     operator= operator is used to assign new contents to the container by replacing the existing contents. operator[] operator is used to reference the element present at position given inside the operator.  
  >     `operator=运算符用于通过替换现有内容将新内容分配给容器。运算符[]运算符用于引用位于运算符内部给定位置的元素。`
  > 15. deque::at() and deque::swap() in C++ STL:  
  >     at() function is used reference the element present at the position given as the parameter to the function. swap() function is used to swap the contents of one deque with another deque of same type and size.  
  >     `at（）函数用于引用作为函数参数给定位置的元素。swap（）函数用于将一个deque的内容与另一个相同类型和大小的deque交换。`
  > 16. deque::begin() and deque::end() in C++ STL:  
  >     begin() function is used to return an iterator pointing to the first element of the deque container. end() function is used to return an iterator pointing to the last element of the deque container.  
  >     `函数用于返回指向deque容器的第一个元素的迭代器。函数用于返回指向deque容器的最后一个元素的迭代器。`
  > 17. deque::emplace_front() and deque::emplace_back() in C++ STL:  
  >     emplace_front() function is used to insert a new element into the deque container. The new element is added to the beginning of the deque. emplace_back() function is used to insert a new element into the deque container. The new element is added to the end of the deque.  
  >     `emplace_front（）函数用于在deque容器中插入新元素。新元素被添加到deque的开头。emplace_back（）函数用于在deque容器中插入新元素。新元素被添加到deque的末尾。`

```c++
#include <iostream>
#include <deque>

using namespace std;

void showdq(deque <int> g)
{
	deque <int> :: iterator it;
	for (it = g.begin(); it != g.end(); ++it)
		cout << '\t' << *it;
	cout << '\n';
}

int main()
{
	deque <int> gquiz;
	gquiz.push_back(10);
	gquiz.push_front(20);
	gquiz.push_back(30);
	gquiz.push_front(15);
	cout << "The deque gquiz is : ";
	showdq(gquiz);

	cout << "\ngquiz.size() : " << gquiz.size();
	cout << "\ngquiz.max_size() : " << gquiz.max_size();

	cout << "\ngquiz.at(2) : " << gquiz.at(2);
	cout << "\ngquiz.front() : " << gquiz.front();
	cout << "\ngquiz.back() : " << gquiz.back();

	cout << "\ngquiz.pop_front() : ";
	gquiz.pop_front();
	showdq(gquiz);

	cout << "\ngquiz.pop_back() : ";
	gquiz.pop_back();
	showdq(gquiz);

	return 0;
}

<!--The deque gquiz is :     15    20    10    30-->

<!--gquiz.size() : 4-->
<!--gquiz.max_size() : 4611686018427387903-->
<!--gquiz.at(2) : 10-->
<!--gquiz.front() : 15-->
<!--gquiz.back() : 30-->
<!--gquiz.pop_front() :     20    10    30-->

<!--gquiz.pop_back() :     20    10-->

```

[返回目录](#Menu)

- ### <span id="arrays">arrays</span>

      The introduction of array class from C++11 has offered a better alternative for C-style arrays. The advantages of array class over C-style array are :

      - Array classes knows its own size, whereas C-style arrays lack this property. So when passing to functions, we don’t need to pass size of Array as a separate parameter.
      - With C-style array there is more risk of array being decayed into a pointer. Array classes don’t decay into pointers
      - Array classes are generally more efficient, light-weight and reliable than C-style arrays.

      从C++ 11引入数组类为C风格数组提供了更好的选择。array class相对于C-style array的优势在于：

      - 数组类知道它自己的大小，而C风格的数组缺少这个属性。所以当传递给函数时，我们不需要将数组的大小作为单独的参数传递。
      - 使用C样式的数组，数组衰减为指针的风险更大。数组类不会衰减为指针
      - 数组类通常比C样式数组更高效、更轻、更可靠。

  > Operations on array :
  >
  > 1. at() :  
  >    This function is used to access the elements of array.  
  >    `此函数用于访问数组的元素。`
  > 2. get() :  
  >    This function is also used to access the elements of array. This function is not the member of array class but overloaded function from class tuple.  
  >    `此函数还用于访问数组的元素。此函数不是数组类的成员，而是类元组的重载函数。`
  > 3. operator[] :  
  >    This is similar to C-style arrays. This method is also used to access array elements.  
  >    `这类似于C样式数组。此方法也用于访问数组元素。`
  > 4. front() :  
  >    This returns the first element of array.  
  >    `返回数组的第一个元素。`
  > 5. back() :  
  >    This returns the last element of array.  
  >    `返回数组的最后一个元素。`
  > 6. size() :  
  >    It returns the number of elements in array. This is a property that C-style arrays lack.  
  >    `返回数组中的元素数。这是C样式数组缺少的属性。`
  > 7. max_size() :  
  >    It returns the maximum number of elements array can hold i.e, the size with which array is declared. The size() and max_size() return the same value.  
  >    `返回数组可以容纳的最大元素数，即声明数组的大小。size（）和max_size（）返回相同的值。`
  > 8. swap() :  
  >    The swap() swaps all elements of one array with other.  
  >    `swap（）将一个数组的所有元素与另一个数组交换。`
  > 9. empty() :  
  >    This function returns true when the array size is zero else returns false.  
  >    `当数组大小为零时，此函数返回true，否则返回false。`
  > 10. fill() :  
  >     This function is used to fill the entire array with a particular value.  
  >     `此函数用于用特定值填充整个数组。`

```c++
// C++ code to demonstrate working of array,
// to() and get()
#include<iostream>
#include<array> // for array, at()
#include<tuple> // for get()
using namespace std;
int main()
{
	// Initializing the array elements
	array<int,6> ar = {1, 2, 3, 4, 5, 6};

	// Printing array elements using at()
	cout << "The array elements are (using at()) : ";
	for ( int i=0; i<6; i++)
	cout << ar.at(i) << " ";
	cout << endl;

	// Printing array elements using get()
	cout << "The array elements are (using get()) : ";
	cout << get<0>(ar) << " " << get<1>(ar) << " ";
	cout << get<2>(ar) << " " << get<3>(ar) << " ";
	cout << get<4>(ar) << " " << get<5>(ar) << " ";
	cout << endl;

	// Printing array elements using operator[]
	cout << "The array elements are (using operator[]) : ";
	for ( int i=0; i<6; i++)
	cout << ar[i] << " ";
	cout << endl;

	return 0;

}


<!--The array elemets are (using at()) : 1 2 3 4 5 6 -->
<!--The array elemets are (using get()) : 1 2 3 4 5 6 -->
<!--The array elements are (using operator[]) : 1 2 3 4 5 6 -->

/*--------------------------------------------------------------------*/

// C++ code to demonstrate working of
// front() and back()
#include<iostream>
#include<array> // for front() and back()
using namespace std;
int main()
{
	// Initializing the array elements
	array<int,6> ar = {1, 2, 3, 4, 5, 6};

	// Printing first element of array
	cout << "First element of array is : ";
	cout << ar.front() << endl;

	// Printing last element of array
	cout << "Last element of array is : ";
	cout << ar.back() << endl;

	return 0;

}


<!--First element of array is : 1-->
<!--Last element of array is : 6-->


/*--------------------------------------------------------------*/

// C++ code to demonstrate working of
// size() and max_size()
#include<iostream>
#include<array> // for size() and max_size()
using namespace std;
int main()
{
	// Initializing the array elements
	array<int,6> ar = {1, 2, 3, 4, 5, 6};

	// Printing number of array elements
	cout << "The number of array elements is : ";
	cout << ar.size() << endl;

	// Printing maximum elements array can hold
	cout << "Maximum elements array can hold is : ";
	cout << ar.max_size() << endl;

	return 0;

}


<!--The number of array elements is : 6-->
<!--Maximum elements array can hold is : 6-->


/*--------------------------------------------------------*/

// C++ code to demonstrate working of swap()
#include<iostream>
#include<array> // for swap() and array
using namespace std;
int main()
{

	// Initializing 1st array
	array<int,6> ar = {1, 2, 3, 4, 5, 6};

	// Initializing 2nd array
	array<int,6> ar1 = {7, 8, 9, 10, 11, 12};

	// Printing 1st and 2nd array before swapping
	cout << "The first array elements before swapping are : ";
	for (int i=0; i<6; i++)
	cout << ar[i] << " ";
	cout << endl;
	cout << "The second array elements before swapping are : ";
	for (int i=0; i<6; i++)
	cout << ar1[i] << " ";
	cout << endl;

	// Swapping ar1 values with ar
	ar.swap(ar1);

	// Printing 1st and 2nd array after swapping
	cout << "The first array elements after swapping are : ";
	for (int i=0; i<6; i++)
	cout << ar[i] << " ";
	cout << endl;
	cout << "The second array elements after swapping are : ";
	for (int i=0; i<6; i++)
	cout << ar1[i] << " ";
	cout << endl;

	return 0;

}


<!--The first array elements before swapping are : 1 2 3 4 5 6 -->
<!--The second array elements before swapping are : 7 8 9 10 11 12 -->
<!--The first array elements after swapping are : 7 8 9 10 11 12 -->
<!--The second array elements after swapping are : 1 2 3 4 5 6 -->

/*-------------------------------------------------------*/

// C++ code to demonstrate working of empty()
// and fill()
#include<iostream>
#include<array> // for fill() and empty()
using namespace std;
int main()
{

	// Declaring 1st array
	array<int,6> ar;

	// Declaring 2nd array
	array<int,0> ar1;

	// Checking size of array if it is empty
	ar1.empty()? cout << "Array empty":
		cout << "Array not empty";
	cout << endl;

	// Filling array with 0
	ar.fill(0);

	// Displaying array after filling
	cout << "Array after filling operation is : ";
	for ( int i=0; i<6; i++)
		cout << ar[i] << " ";

	return 0;

}

<!--Array empty-->
<!--Array after filling operation is : 0 0 0 0 0 0 -->

```

[返回目录](#Menu)

- ### <span id="forward_list">forward_list (Introduced in C++11)</span>

      Forward list in STL implements singly linked list. Introduced from C\++11, forward list are useful than other containers in insertion, removal and moving operations (like sort) and allows time constant insertion and removal of elements.
      It differs from list by the fact that forward list keeps track of location of only next element while list keeps track to both next and previous elements, thus increasing the storage space required to store each element. The drawback of forward list is that it cannot be iterated backwards and its individual elements cannot be accessed directly.
      Forward List is preferred over list when only forward traversal is required (same as singly linked list is preferred over doubly linked list) as we can save space. Some example cases are, chaining in hashing, adjacency list representation of graph, etc.

      STL中的转发列表实现了单链表。从C++ 11中介绍，转发列表在插入、删除和移动操作（如排序）中比其他容器有用，并允许元素的时间常数插入和移除。
      它与list的不同之处在于forward list只跟踪下一个元素的位置，而list则同时跟踪下一个和前一个元素，从而增加了存储每个元素所需的存储空间。forward list的缺点是它不能向后迭代，并且不能直接访问它的各个元素。
      当只需要向前遍历时，转发列表比列表优先（与单链表优先于双链表相同），这样可以节省空间。例如，散列中的链接、图的邻接表表示等。

  > Operations on Forward List :
  >
  > 1. assign() :  
  >    This function is used to assign values to forward list, its another variant is used to assign repeated elements.  
  >    `此函数用于为转发列表赋值，它的另一个变量用于分配重复的元素。`
  > 2. push_front() :  
  >    This function is used to insert the element at the first position on forward list. The value from this function is copied to the space before first element in the container. The size of forward list increases by 1.  
  >    `此函数用于在前向列表的第一个位置插入元素。此函数中的值将复制到容器中第一个元素之前的空间中。转发列表的大小增加1。`
  > 3. emplace_front() :  
  >    This function is similar to the previous function but in this no copying operation occurs, the element is created directly at the memory before the first element of the forward list.  
  >    `此函数与上一个函数类似，但在这个函数中不会发生复制操作，元素直接在转发列表的第一个元素之前的内存中创建。`
  > 4. pop_front() :  
  >    This function is used to delete the first element of list.  
  >    `此函数用于删除列表的第一个元素。`
  > 5. insert_after():  
  >    This function gives us a choice to insert elements at any position in forward list. The arguments in this function are copied at the desired position.  
  >    `此函数使我们可以选择在转发列表的任何位置插入元素。此函数中的参数被复制到所需的位置。`
  > 6. emplace_after():  
  >    This function also does the same operation as above function but the elements are directly made without any copy operation.  
  >    `此函数也执行与上述函数相同的操作，但元素是直接生成的，没有任何复制操作。`
  > 7. erase_after():  
  >    This function is used to erase elements from a particular position in the forward list.  
  >    `此函数用于从转发列表中的特定位置删除元素。`
  > 8. remove() :  
  >    This function removes the particular element from the forward list mentioned in its argument.  
  >    `此函数从其参数中提到的转发列表中删除特定元素。`
  > 9. remove_if() :  
  >    This function removes according to the condition in its argument.  
  >    `此函数根据参数中的条件删除。`
  > 10. splice_after() :  
  >     This function transfers elements from one forward list to other.  
  >     `此函数用于将元素从一个转发列表传输到另一个转发列表。`
  >
  > Some more methods of forward_list:
  >
  > 1. front():  
  >    This function is used to reference the first element of the forward list container.  
  >    `此函数用于引用转发列表容器的第一个元素。`
  > 2. begin():  
  >    begin() function is used to return an iterator pointing to the first element of the forward list container.  
  >    `begin（）函数用于返回指向转发列表容器的第一个元素的迭代器。`
  > 3. end():  
  >    end() function is used to return an iterator pointing to the last element of the list container.  
  >    `end（）函数用于返回指向列表容器的最后一个元素的迭代器。`
  > 4. cbegin():  
  >    Returns a constant iterator pointing to the first element of the forward_list.  
  >    `返回指向前向列表的第一个元素的常量迭代器。`
  > 5. cend():  
  >    Returns a constant iterator pointing to the past-the-last element of the forward_list.  
  >    `返回指向前向列表最后一个元素的常量迭代器。`
  > 6. before_begin():  
  >    Returns a iterator which points to the position before the first element of the forward_list.  
  >    `返回一个迭代器，该迭代器指向转发列表的第一个元素之前的位置。`
  > 7. cbefore_begin():  
  >    Returns a constant random access iterator which points to the position before the first element of the forward_list.  
  >    `返回一个常量随机访问迭代器，该迭代器指向转发列表第一个元素之前的位置。`
  > 8. max_size():  
  >    Returns the maximum number of elements can be held by forward_list.  
  >    `返回转发列表可以容纳的最大元素数。`
  > 9. resize():  
  >    Changes the size of forward_list.  
  >    `更改转发列表的大小。`

```c++
// C++ code to demonstrate forward list
// and assign()
#include<iostream>
#include<forward_list>
using namespace std;

int main()
{
	// Declaring forward list
	forward_list<int> flist1;

	// Declaring another forward list
	forward_list<int> flist2;

	// Assigning values using assign()
	flist1.assign({1, 2, 3});

	// Assigning repeating values using assign()
	// 5 elements with value 10
	flist2.assign(5, 10);

	// Displaying forward lists
	cout << "The elements of first forward list are : ";
	for (int&a : flist1)
		cout << a << " ";
	cout << endl;

	cout << "The elements of second forward list are : ";
	for (int&b : flist2)
		cout << b << " ";
	cout << endl;

	return 0;
}


<!--The elements of first forward list are : 1 2 3 -->
<!--The elements of second forward list are : 10 10 10 10 10 -->

/*-----------------------------------------------------------*/

// C++ code to demonstrate working of
// push_front(), emplace_front() and pop_front()
#include<iostream>
#include<forward_list>
using namespace std;

int main()
{
	// Initializing forward list
	forward_list<int> flist = {10, 20, 30, 40, 50};

	// Inserting value using push_front()
	// Inserts 60 at front
	flist.push_front(60);

	// Displaying the forward list
	cout << "The forward list after push_front operation : ";
	for (int&c : flist)
		cout << c << " ";
	cout << endl;

	// Inserting value using emplace_front()
	// Inserts 70 at front
	flist.emplace_front(70);

	// Displaying the forward list
	cout << "The forward list after emplace_front operation : ";
	for (int&c : flist)
	cout << c << " ";
	cout << endl;

	// Deleting first value using pop_front()
	// Pops 70
	flist.pop_front();

	// Displaying the forward list
	cout << "The forward list after pop_front operation : ";
	for (int&c : flist)
		cout << c << " ";
	cout << endl;

	return 0;
}


<!--The forward list after push_front operation : 60 10 20 30 40 50 -->
<!--The forward list after emplace_front operation : 70 60 10 20 30 40 50 -->
<!--The forward list after pop_front operation : 60 10 20 30 40 50-->

/*------------------------------------------------------------*/

// C++ code to demonstrate working of
// insert_after(), emplace_after() and erase_after()
#include<iostream>
#include<forward_list>
using namespace std;

int main()
{
	// Initializing forward list
	forward_list<int> flist = {10, 20, 30} ;

	// Declaring a forward list iterator
	forward_list<int>::iterator ptr;

	// Inserting value using insert_after()
	// starts insertion from second position
	ptr = flist.insert_after(flist.begin(), {1, 2, 3});

	// Displaying the forward list
	cout << "The forward list after insert_after operation : ";
	for (int&c : flist)
		cout << c << " ";
	cout << endl;

	// Inserting value using emplace_after()
	// inserts 2 after ptr
	ptr = flist.emplace_after(ptr,2);

	// Displaying the forward list
	cout << "The forward list after emplace_after operation : ";
	for (int&c : flist)
		cout << c << " ";
	cout << endl;

	// Deleting value using erase.after Deleted 2
	// after ptr
	ptr = flist.erase_after(ptr);

	// Displaying the forward list
	cout << "The forward list after erase_after operation : ";
	for (int&c : flist)
		cout << c << " ";
	cout << endl;

	return 0;
}


<!--The forward list after insert_after operation : 10 1 2 3 20 30 -->
<!--The forward list after emplace_after operation : 10 1 2 3 2 20 30 -->
<!--The forward list after erase_after operation : 10 1 2 3 2 30 -->

/*------------------------------------------------------*/

// C++ code to demonstrate working of remove() and
// remove_if()
#include<iostream>
#include<forward_list>
using namespace std;

int main()
{
	// Initializing forward list
	forward_list<int> flist = {10, 20, 30, 25, 40, 40};

	// Removing element using remove()
	// Removes all occurrences of 40
	flist.remove(40);

	// Displaying the forward list
	cout << "The forward list after remove operation : ";
	for (int&c : flist)
		cout << c << " ";
	cout << endl;

	// Removing according to condition. Removes
	// elements greater than 20. Removes 25 and 30
	flist.remove_if([](int x){ return x>20;});

	// Displaying the forward list
	cout << "The forward list after remove_if operation : ";
	for (int&c : flist)
	cout << c << " ";
	cout << endl;

	return 0;

}


<!--The forward list after remove operation : 10 20 30 25 -->
<!--The forward list after remove_if operation : 10 20 -->

/*-------------------------------------------------------------------*/

// C++ code to demonstrate working of
// splice_after()
#include<iostream>
#include<forward_list> // for splice_after()
using namespace std;

int main()
{
	// Initializing forward list
	forward_list<int> flist1 = {10, 20, 30};

	// Initializing second list
	forward_list<int> flist2 = {40, 50, 60};

	// Shifting elements from first to second
	// forward list after 1st position
	flist2.splice_after(flist2.begin(),flist1);

	// Displaying the forward list
	cout << "The forward list after splice_after operation : ";
	for (int&c : flist2)
	cout << c << " ";
	cout << endl;

	return 0;
}


<!--The forward list after splice_after operation : 40 10 20 30 50 60 -->
```

[返回目录](#Menu)

## 2. <span id="Container_Adaptors">Container Adaptors</span> [^container_adaptors]

- ### <span id="queue">queue</span>

      Queues are a type of container adaptors which operate in a first in first out (FIFO) type of arrangement. Elements are inserted at the back (end) and are deleted from the front.

      队列是一种容器适配器，它以先进先出（FIFO）的方式进行操作。元素将在后面（末端）插入，并从前面删除。

  > The functions supported by queue are :
  >
  > 1. empty():  
  >    Returns whether the queue is empty.  
  >    `返回队列是否为空。`
  > 2. size():  
  >    Returns the size of the queue.  
  >    `返回队列的大小。`
  > 3. queue::swap() in C++ STL:  
  >    Exchange the contents of two queues but the queues must be of same type, although sizes may differ.  
  >    `交换两个队列的内容，但队列必须是相同类型的，尽管大小可能不同。`
  > 4. queue::emplace() in C++ STL:  
  >    Insert a new element into the queue container, the new element is added to the end of the queue.  
  >    `将新元素插入队列容器中，将新元素添加到队列的末尾。`
  > 5. queue::front() and queue::back() in C++ STL:  
  >    front() function returns a reference to the first element of the queue. back() function returns a reference to the last element of the queue.  
  >    `front()函数的作用是：返回对队列第一个元素的引用。back()函数的作用是：返回对队列最后一个元素的引用。`
  > 6. push(g) and pop():  
  >    push() function adds the element ‘g’ at the end of the queue. pop() function deletes the first element of the queue.  
  >    `push（）函数在队列末尾添加元素“g”。pop()函数的作用是：删除队列的第一个元素。`

```c++
// CPP code to illustrate
// Queue in Standard Template Library (STL)
#include <iostream>
#include <queue>

using namespace std;

void showq(queue <int> gq)
{
	queue <int> g = gq;
	while (!g.empty())
	{
		cout << '\t' << g.front();
		g.pop();
	}
	cout << '\n';
}

int main()
{
	queue <int> gquiz;
	gquiz.push(10);
	gquiz.push(20);
	gquiz.push(30);

	cout << "The queue gquiz is : ";
	showq(gquiz);

	cout << "\ngquiz.size() : " << gquiz.size();
	cout << "\ngquiz.front() : " << gquiz.front();
	cout << "\ngquiz.back() : " << gquiz.back();

	cout << "\ngquiz.pop() : ";
	gquiz.pop();
	showq(gquiz);

	return 0;
}


<!--The queue gquiz is :     10    20    30-->

<!--gquiz.size() : 3-->
<!--gquiz.front() : 10-->
<!--gquiz.back() : 30-->
<!--gquiz.pop() :     20    30-->
```

[返回目录](#Menu)

- ### <span id="priority_queue">priority_queue</span>

      Priority queues are a type of container adapters, specifically designed such that the first element of the queue is the greatest of all elements in the queue and elements are in non increasing order(hence we can see that each element of the queue has a priority{fixed order}).

      优先级队列是一种容器适配器，专门设计为队列的第一个元素是队列中所有元素中最大的元素，元素的顺序不是递增的（因此我们可以看到队列的每个元素都有一个优先级{fixed order}）。

  > Methods of priority queue are:
  >
  > 1. priority_queue::empty() in C++ STL:  
  >    empty() function returns whether the queue is empty.  
  >    `empty()函数的作用是：返回队列是否为空。`
  > 2. priority_queue::size() in C++ STL:  
  >    size() function returns the size of the queue.  
  >    `size()函数的作用是：返回队列的大小。`
  > 3. priority_queue::top() in C++ STL:  
  >    Returns a reference to the top most element of the queue.  
  >    `返回对队列最顶层元素的引用。`
  > 4. priority_queue::push() in C++ STL:  
  >    push(g) function adds the element ‘g’ at the end of the queue.  
  >    `push（g）函数在队列末尾添加元素“g”。`
  > 5. priority_queue::pop() in C++ STL:  
  >    pop() function deletes the first element of the queue.  
  >    `pop()函数的作用是：删除队列的第一个元素。`
  > 6. priority_queue::swap() in C++ STL:  
  >    This function is used to swap the contents of one priority queue with another priority queue of same type and size.  
  >    `此函数用于将一个优先级队列的内容与另一个类型和大小相同的优先级队列的内容交换。`
  > 7. priority_queue::emplace() in C++ STL:  
  >    This function is used to insert a new element into the priority queue container, the new element is added to the top of the priority queue.  
  >    `此函数用于将新元素插入优先级队列容器中，将新元素添加到优先级队列的顶部。`
  > 8. priority_queue value_type in C++ STL:  
  >    Represents the type of object stored as an element in a priority_queue. It acts as a synonym for the template parameter.  
  >    `表示存储为优先级队列中元素的对象类型。它充当模板参数的同义词。`

```c++
// Note that by default C++ creates a max-heap
// for priority queue
#include <iostream>
#include <queue>

using namespace std;

void showpq(priority_queue <int> gq)
{
	priority_queue <int> g = gq;
	while (!g.empty())
	{
		cout << '\t' << g.top();
		g.pop();
	}
	cout << '\n';
}

int main ()
{
	priority_queue <int> gquiz;
	gquiz.push(10);
	gquiz.push(30);
	gquiz.push(20);
	gquiz.push(5);
	gquiz.push(1);

	cout << "The priority queue gquiz is : ";
	showpq(gquiz);

	cout << "\ngquiz.size() : " << gquiz.size();
	cout << "\ngquiz.top() : " << gquiz.top();


	cout << "\ngquiz.pop() : ";
	gquiz.pop();
	showpq(gquiz);

	return 0;
}


<!--The priority queue gquiz is :     30    20    10    5    1-->

<!--gquiz.size() : 5-->
<!--gquiz.top() : 30-->
<!--gquiz.pop() :     20    10    5    1-->

/*-------------------------------------------------------------------*/

// C++ program to demonstrate min heap
#include <iostream>
#include <queue>

using namespace std;

void showpq(priority_queue <int, vector<int>, greater<int>> gq)
{
	priority_queue <int, vector<int>, greater<int>> g = gq;
	while (!g.empty())
	{
		cout << '\t' << g.top();
		g.pop();
	}
	cout << '\n';
}

int main ()
{
	priority_queue <int, vector<int>, greater<int>> gquiz;
	gquiz.push(10);
	gquiz.push(30);
	gquiz.push(20);
	gquiz.push(5);
	gquiz.push(1);

	cout << "The priority queue gquiz is : ";
	showpq(gquiz);

	cout << "\ngquiz.size() : " << gquiz.size();
	cout << "\ngquiz.top() : " << gquiz.top();


	cout << "\ngquiz.pop() : ";
	gquiz.pop();
	showpq(gquiz);

	return 0;
}


<!--The priority queue gquiz is :     1    5    10    20    30-->

<!--gquiz.size() : 5-->
<!--gquiz.top() : 1-->
<!--gquiz.pop() :     5    10    20    30-->
```

[返回目录](#Menu)

- ### <span id="stack">stack</span>

      Stacks are a type of container adaptors with LIFO(Last In First Out) type of working, where a new element is added at one end and (top) an element is removed from that end only.

      堆栈是一种具有后进先出（后进先出）工作方式的容器适配器，在这种情况下，在一端添加新元素，而只从该端移除元素。

  > The functions associated with stack are:
  >
  > 1. empty():  
  >    Returns whether the stack is empty – Time Complexity : O(1)  
  >    `返回堆栈是否为空-时间复杂度：O（1）`
  > 2. size():  
  >    Returns the size of the stack – Time Complexity : O(1)  
  >    `返回堆栈的大小-时间复杂性：O（1）`
  > 3. top():  
  >    Returns a reference to the top most element of the stack – Time Complexity : O(1)  
  >    `返回对堆栈最顶层元素的引用-时间复杂性：O（1）`
  > 4. push(g):  
  >    Adds the element ‘g’ at the top of the stack – Time Complexity : O(1)  
  >    `在堆栈顶部添加元素“g”–时间复杂性：O（1）`
  > 5. pop():  
  >    Deletes the top most element of the stack – Time Complexity : O(1)  
  >    `删除堆栈最上面的元素-时间复杂性：O（1）`

```c++
// CPP program to demonstrate working of STL stack
#include <bits/stdc++.h>
using namespace std;

void showstack(stack <int> s)
{
	while (!s.empty())
	{
		cout << '\t' << s.top();
		s.pop();
	}
	cout << '\n';
}

int main ()
{
	stack <int> s;
	s.push(10);
	s.push(30);
	s.push(20);
	s.push(5);
	s.push(1);

	cout << "The stack is : ";
	showstack(s);

	cout << "\ns.size() : " << s.size();
	cout << "\ns.top() : " << s.top();


	cout << "\ns.pop() : ";
	s.pop();
	showstack(s);

	return 0;
}


<!--The stack is :     1    5    20    30    10-->

<!--s.size() : 5-->
<!--s.top() : 1-->
<!--s.pop() :     5    20    30    10-->
```

[返回目录](#Menu)

## 3. <span id="Associative_Containers">Associative Containers</span> [^associative_containers]

- ### <span id="set">set</span>
      Sets are a type of associative containers in which each element has to be unique, because the value of the element identifies it. The value of the element cannot be modified once it is added to the set, though it is possible to remove and add the modified value of that element.
  > Some basic functions associated with Set:
  >
  > 1. begin() – Returns an iterator to the first element in the set.
  > 2. end() – Returns an iterator to the theoretical element that follows last element in the set.
  > 3. size() – Returns the number of elements in the set.
  > 4. max_size() – Returns the maximum number of elements that the set can hold.
  > 5. empty() – Returns whether the set is empty.
  >
  > Methods of set:
  >
  > 1. begin() – Returns an iterator to the first element in the set.
  > 2. end() – Returns an iterator to the theoretical element that follows last element in the set.
  > 3. rbegin()– Returns a reverse iterator pointing to the last element in the container.
  > 4. rend()– Returns a reverse iterator pointing to the theoretical element right before the first element in the set container.
  > 5. crbegin()– Returns a constant iterator pointing to the last element in the container.
  > 6. crend() – Returns a constant iterator pointing to the position just before the first element in the container.
  > 7. cbegin()– Returns a constant iterator pointing to the first element in the container.
  > 8. cend() – Returns a constant iterator pointing to the position past the last element in the container.
  > 9. size() – Returns the number of elements in the set.
  > 10. max_size() – Returns the maximum number of elements that the set can hold.
  > 11. empty() – Returns whether the set is empty.
  > 12. insert(const g) – Adds a new element ‘g’ to the set.
  > 13. iterator insert (iterator position, const g) – Adds a new element ‘g’ at the position pointed by iterator.
  > 14. erase(iterator position) – Removes the element at the position pointed by the iterator.
  > 15. erase(const g)– Removes the value ‘g’ from the set.
  > 16. clear() – Removes all the elements from the set.
  > 17. key_comp() / value_comp() – Returns the object that determines how the elements in the set are ordered (‘<‘ by default).
  > 18. find(const g) – Returns an iterator to the element ‘g’ in the set if found, else returns the iterator to end.
  > 19. count(const g) – Returns 1 or 0 based on the element ‘g’ is present in the set or not.
  > 20. lower_bound(const g) – Returns an iterator to the first element that is equivalent to ‘g’ or definitely will not go before the element ‘g’ in the set.
  > 21. upper_bound(const g) – Returns an iterator to the first element that is equivalent to ‘g’ or definitely will go after the element ‘g’ in the set.
  > 22. equal_range()– The function returns an iterator of pairs. (key_comp). The pair refers to the range that includes all the elements in the container which have a key equivalent to k.
  > 23. emplace()– This function is used to insert a new element into the set container, only if the element to be inserted is unique and does not already exists in the set.
  > 24. emplace_hint()– Returns an iterator pointing to the position where the insertion is done. If the element passed in the parameter already exists, then it returns an iterator pointing to the position where the existing element is.
  > 25. swap()– This function is used to exchange the contents of two sets but the sets must be of same type, although sizes may differ.
  > 26. operator= – The ‘=’ is an operator in C++ STL which copies (or moves) a set to another set and set::operator= is the corresponding operator function.
  > 27. get_allocator()– Returns the copy of the allocator object associated with the set.

```
#include <iostream>
#include <set>
#include <iterator>

using namespace std;

int main()
{
	// empty set container
	set <int, greater <int> > s1;

	// insert elements in random order
	s1.insert(40);
	s1.insert(30);
	s1.insert(60);
	s1.insert(20);
	s1.insert(50);
	s1.insert(50); // only one 50 will be added to the set
	s1.insert(10);

	// printing set s1
	set <int, greater <int> > :: iterator itr;
	cout << "\nThe set s1 is : ";
	for (itr = s1.begin(); itr != s1.end(); ++itr)
	{
		cout << '\t' << *itr;
	}
	cout << endl;

	// assigning the elements from s1 to s2
	set <int> s2(s1.begin(), s1.end());

	// print all elements of the set s2
	cout << "\nThe set s2 after assign from s1 is : ";
	for (itr = s2.begin(); itr != s2.end(); ++itr)
	{
		cout << '\t' << *itr;
	}
	cout << endl;

	// remove all elements up to 30 in s2
	cout << "\ns2 after removal of elements less than 30 : ";
	s2.erase(s2.begin(), s2.find(30));
	for (itr = s2.begin(); itr != s2.end(); ++itr)
	{
		cout << '\t' << *itr;
	}

	// remove element with value 50 in s2
	int num;
	num = s2.erase (50);
	cout << "\ns2.erase(50) : ";
	cout << num << " removed \t" ;
	for (itr = s2.begin(); itr != s2.end(); ++itr)
	{
		cout << '\t' << *itr;
	}

	cout << endl;

	//lower bound and upper bound for set s1
	cout << "s1.lower_bound(40) : "
		<< *s1.lower_bound(40) << endl;
	cout << "s1.upper_bound(40) : "
		<< *s1.upper_bound(40) << endl;

	//lower bound and upper bound for set s2
	cout << "s2.lower_bound(40) : "
		<< *s2.lower_bound(40) << endl;
	cout << "s2.upper_bound(40) : "
		<< *s2.upper_bound(40) << endl;

	return 0;

}


<!--The set s1 is :      60    50    40    30    20    10-->

<!--The set s2 after assign from s1 is : 10      20    30    40    50    60-->

<!--s2 after removal of elements less than 30 : 30    40    50    60-->
<!--s2.erase(50) : 1 removed     30    40    60-->
<!--s1.lower_bound(40) : 40-->
<!--s1.upper_bound(40) : 30-->
<!--s2.lower_bound(40) : 40-->
<!--s2.upper_bound(40) : 60-->

```

[返回目录](#Menu)

- ### <span id="multiset">multiset</span>
      Multisets are a type of associative containers similar to set, with an exception that multiple elements can have same values.
  > Some Basic Functions associated with multiset:
  >
  > 1. begin() – Returns an iterator to the first element in the multiset
  > 2. end() – Returns an iterator to the theoretical element that follows last element in the multiset
  > 3. size() – Returns the number of elements in the multiset
  > 4. max_size() – Returns the maximum number of elements that the multiset can hold
  > 5. empty() – Returns whether the multiset is empty
  >
  > List of functions of Multiset:
  >
  > 1. begin() – Returns an iterator to the first element in the multiset.
  > 2. end() – Returns an iterator to the theoretical element that follows last element in the multiset.
  > 3. size() – Returns the number of elements in the multiset.
  > 4. max_size()– Returns the maximum number of elements that the multiset can hold.
  > 5. empty() – Returns whether the multiset is empty.
  > 6. pair insert(const g) – Adds a new element ‘g’ to the multiset.
  > 7. iterator insert (iterator position,const g) – Adds a new element ‘g’ at the position pointed by iterator.
  > 8. erase(iterator position)– Removes the element at the position pointed by the iterator.
  > 9. erase(const g)– Removes the value ‘g’ from the multiset.
  > 10. clear()– Removes all the elements from the multiset.
  > 11. key_comp() / value_comp()– Returns the object that determines how the elements in the multiset are ordered (‘<' by default).
  > 12. find(const g)– Returns an iterator to the element ‘g’ in the multiset if found, else returns the iterator to end.
  > 13. count(const g)– Returns the number of matches to element ‘g’ in the multiset.
  > 14. lower_bound(const g)– Returns an iterator to the first element that is equivalent to ‘g’ or definitely will not go before the element ‘g’ in the multiset.
  > 15. upper_bound(const g)– Returns an iterator to the first element that is equivalent to ‘g’ or definitely will go after the element ‘g’ in the multiset.
  > 16. multiset::swap()– This function is used to exchange the contents of two multisets but the sets must be of same type, although sizes may differ.
  > 17. multiset::operator=– This operator is used to assign new contents to the container by replacing the existing contents.
  > 18. multiset::emplace()– This function is used to insert a new element into the multiset container.
  > 19. multiset equal_range()– Returns an iterator of pairs. The pair refers to the range that includes all the elements in the container which have a key equivalent to k.
  > 20. multiset::emplace_hint() – Inserts a new element in the multiset.
  > 21. multiset::rbegin()– Returns a reverse iterator pointing to the last element in the multiset container.
  > 22. multiset::rend()– Returns a reverse iterator pointing to the theoretical element right before the first element in the multiset container.
  > 23. multiset::cbegin()– Returns a constant iterator pointing to the first element in the container.
  > 24. multiset::cend()– Returns a constant iterator pointing to the position past the last element in the container.
  > 25. multiset::crbegin()– Returns a constant reverse iterator pointing to the last element in the container.
  > 26. multiset::crend()– Returns a constant reverse iterator pointing to the position just before the first element in the container.
  > 27. multiset::get_allocator()– Returns a copy of the allocator object associated with the multiset.

```c++
#include <iostream>
#include <set>
#include <iterator>

using namespace std;

int main()
{
	// empty multiset container
	multiset <int, greater <int> > gquiz1;

	// insert elements in random order
	gquiz1.insert(40);
	gquiz1.insert(30);
	gquiz1.insert(60);
	gquiz1.insert(20);
	gquiz1.insert(50);
	gquiz1.insert(50); // 50 will be added again to the multiset unlike set
	gquiz1.insert(10);

	// printing multiset gquiz1
	multiset <int, greater <int> > :: iterator itr;
	cout << "\nThe multiset gquiz1 is : ";
	for (itr = gquiz1.begin(); itr != gquiz1.end(); ++itr)
	{
		cout << '\t' << *itr;
	}
	cout << endl;

	// assigning the elements from gquiz1 to gquiz2
	multiset <int> gquiz2(gquiz1.begin(), gquiz1.end());

	// print all elements of the multiset gquiz2
	cout << "\nThe multiset gquiz2 after assign from gquiz1 is : ";
	for (itr = gquiz2.begin(); itr != gquiz2.end(); ++itr)
	{
		cout << '\t' << *itr;
	}
	cout << endl;

	// remove all elements up to element with value 30 in gquiz2
	cout << "\ngquiz2 after removal of elements less than 30 : ";
	gquiz2.erase(gquiz2.begin(), gquiz2.find(30));
	for (itr = gquiz2.begin(); itr != gquiz2.end(); ++itr)
	{
		cout << '\t' << *itr;
	}

	// remove all elements with value 50 in gquiz2
	int num;
	num = gquiz2.erase(50);
	cout << "\ngquiz2.erase(50) : ";
	cout << num << " removed \t" ;
	for (itr = gquiz2.begin(); itr != gquiz2.end(); ++itr)
	{
		cout << '\t' << *itr;
	}

	cout << endl;

	//lower bound and upper bound for multiset gquiz1
	cout << "gquiz1.lower_bound(40) : "
		<< *gquiz1.lower_bound(40) << endl;
	cout << "gquiz1.upper_bound(40) : "
		<< *gquiz1.upper_bound(40) << endl;

	//lower bound and upper bound for multiset gquiz2
	cout << "gquiz2.lower_bound(40) : "
		<< *gquiz2.lower_bound(40) << endl;
	cout << "gquiz2.upper_bound(40) : "
		<< *gquiz2.upper_bound(40) << endl;

		return 0;

}


<!--The multiset gquiz1 is :  60     50    50    40    30    20    10-->

<!--The multiset gquiz2 after assign from gquiz1 is :  10     20    30    40    50    50    60-->

<!--gquiz2 after removal of elements less than 30 :  30    40    50    50    60-->
<!--gquiz2.erase(50) : 2 removed         30    40    60-->
<!--gquiz1.lower_bound(40) : 40-->
<!--gquiz1.upper_bound(40) : 30-->
<!--gquiz2.lower_bound(40) : 40-->
<!--gquiz2.upper_bound(40) : 60-->
```

[返回目录](#Menu)

- ### <span id="map">map</span>
  Maps are associative containers that store elements in a mapped fashion. Each element has a key value and a mapped value. No two mapped values can have same key values.

> Some basic functions associated with Map:
>
> 1. begin() – Returns an iterator to the first element in the map
> 2. end() – Returns an iterator to the theoretical element that follows last element in the map
> 3. size() – Returns the number of elements in the map
> 4. max_size() – Returns the maximum number of elements that the map can hold
> 5. empty() – Returns whether the map is empty
> 6. pair insert(keyvalue, mapvalue) – Adds a new element to the map
> 7. erase(iterator position) – Removes the element at the position pointed by the iterator
> 8. erase(const g)– Removes the key value ‘g’ from the map
> 9. clear() – Removes all the elements from the map
>
> List of all functions of Map:
>
> 1. map insert() in C++ STL– Insert elements with a particular key in the map container. .
> 2. map count() function in C++ STL– Returns the number of matches to element with key value ‘g’ in the map.
> 3. map equal_range() in C++ STL– Returns an iterator of pairs. The pair refers to the bounds of a range that includes all the elements in the container which have a key equivalent to k.
> 4. map erase() function in C++ STL– Used to erase element from the container.
> 5. map rend() function in C++ STL– Returns a reverse iterator pointing to the theoretical element right before the first key-value pair in the map(which is considered its reverse end).
> 6. map rbegin() function in C++ STL– Returns a reverse iterator which points to the last element of the map.
> 7. map find() function in C++ STL– Returns an iterator to the element with key value ‘g’ in the map if found, else returns the iterator to end.
> 8. map crbegin() and crend() function in C++ STL– crbegin() returns a constant reverse iterator referring to the last element in the map container. crend() returns a constant reverse iterator pointing to the theoretical element before the first element in the map.
> 9. map cbegin() and cend() function in C++ STL– cbegin() returns a constant iterator referring to the first element in the map container. cend() returns a constant iterator pointing to the theoretical element that follows last element in the multimap.
> 10. map emplace() in C++ STL– Inserts the key and its element in the map container.
> 11. map max_size() in C++ STL– Returns the maximum number of elements a map container can hold.
> 12. map upper_bound() function in C++ STL– Returns an iterator to the first element that is equivalent to mapped value with key value ‘g’ or definitely will go after the element with key value ‘g’ in the map
> 13. map operator= in C++ STL– Assigns contents of a container to a different container, replacing its current content.
> 14. map lower_bound() function in C++ STL– Returns an iterator to the first element that is equivalent to mapped value with key value ‘g’ or definitely will not go before the element with key value ‘g’ in the map.
> 15. map emplace_hint() function in C++ STL– Inserts the key and its element in the map container with a given hint.
> 16. map value_comp() in C++ STL– Returns the object that determines how the elements in the map are ordered (‘<' by default).
> 17. map key_comp() function in C++ STL– Returns the object that determines how the elements in the map are ordered (‘<' by default).
> 18. map::size() in C++ STL– Returns the number of elements in the map.
> 19. map::empty() in C++ STL– Returns whether the map is empty.
> 20. map::begin() and end() in C++ STL– begin() returns an iterator to the first element in the map. end() returns an iterator to the theoretical element that follows last element in the map
> 21. map::operator[] in C++ STL– This operator is used to reference the element present at position given inside the operator.
> 22. map::clear() in C++ STL– Removes all the elements from the map.
> 23. map::at() and map::swap() in C++ STL– at() function is used to return the reference to the element associated with the key k. swap() function is used to exchange the contents of two maps but the maps must be of same type, although sizes may differ.

```c++
#include <iostream>
#include <iterator>
#include <map>

using namespace std;

int main()
{

	// empty map container
	map<int, int> gquiz1;

	// insert elements in random order
	gquiz1.insert(pair<int, int>(1, 40));
	gquiz1.insert(pair<int, int>(2, 30));
	gquiz1.insert(pair<int, int>(3, 60));
	gquiz1.insert(pair<int, int>(4, 20));
	gquiz1.insert(pair<int, int>(5, 50));
	gquiz1.insert(pair<int, int>(6, 50));
	gquiz1.insert(pair<int, int>(7, 10));

	// printing map gquiz1
	map<int, int>::iterator itr;
	cout << "\nThe map gquiz1 is : \n";
	cout << "\tKEY\tELEMENT\n";
	for (itr = gquiz1.begin(); itr != gquiz1.end(); ++itr) {
		cout << '\t' << itr->first
			<< '\t' << itr->second << '\n';
	}
	cout << endl;

	// assigning the elements from gquiz1 to gquiz2
	map<int, int> gquiz2(gquiz1.begin(), gquiz1.end());

	// print all elements of the map gquiz2
	cout << "\nThe map gquiz2 after"
		<< " assign from gquiz1 is : \n";
	cout << "\tKEY\tELEMENT\n";
	for (itr = gquiz2.begin(); itr != gquiz2.end(); ++itr) {
		cout << '\t' << itr->first
			<< '\t' << itr->second << '\n';
	}
	cout << endl;

	// remove all elements up to
	// element with key=3 in gquiz2
	cout << "\ngquiz2 after removal of"
			" elements less than key=3 : \n";
	cout << "\tKEY\tELEMENT\n";
	gquiz2.erase(gquiz2.begin(), gquiz2.find(3));
	for (itr = gquiz2.begin(); itr != gquiz2.end(); ++itr) {
		cout << '\t' << itr->first
			<< '\t' << itr->second << '\n';
	}

	// remove all elements with key = 4
	int num;
	num = gquiz2.erase(4);
	cout << "\ngquiz2.erase(4) : ";
	cout << num << " removed \n";
	cout << "\tKEY\tELEMENT\n";
	for (itr = gquiz2.begin(); itr != gquiz2.end(); ++itr) {
		cout << '\t' << itr->first
			<< '\t' << itr->second << '\n';
	}

	cout << endl;

	// lower bound and upper bound for map gquiz1 key = 5
	cout << "gquiz1.lower_bound(5) : "
		<< "\tKEY = ";
	cout << gquiz1.lower_bound(5)->first << '\t';
	cout << "\tELEMENT = "
		<< gquiz1.lower_bound(5)->second << endl;
	cout << "gquiz1.upper_bound(5) : "
		<< "\tKEY = ";
	cout << gquiz1.upper_bound(5)->first << '\t';
	cout << "\tELEMENT = "
		<< gquiz1.upper_bound(5)->second << endl;

	return 0;
}


<!--The map gquiz1 is : -->
<!--    KEY    ELEMENT-->
<!--    1    40-->
<!--    2    30-->
<!--    3    60-->
<!--    4    20-->
<!--    5    50-->
<!--    6    50-->
<!--    7    10-->


<!--The map gquiz2 after assign from gquiz1 is : -->
<!--    KEY    ELEMENT-->
<!--    1    40-->
<!--    2    30-->
<!--    3    60-->
<!--    4    20-->
<!--    5    50-->
<!--    6    50-->
<!--    7    10-->


<!--gquiz2 after removal of elements less than key=3 : -->
<!--    KEY    ELEMENT-->
<!--    3    60-->
<!--    4    20-->
<!--    5    50-->
<!--    6    50-->
<!--    7    10-->

<!--gquiz2.erase(4) : 1 removed -->
<!--    KEY    ELEMENT-->
<!--    3    60-->
<!--    5    50-->
<!--    6    50-->
<!--    7    10-->

<!--gquiz1.lower_bound(5) :     KEY = 5        ELEMENT = 50-->
<!--gquiz1.upper_bound(5) :     KEY = 6        ELEMENT = 50-->
```

[返回目录](#Menu)

- ### <span id="multimap">multimap</span>
      Multimap is similar to map with an addition that multiple elements can have same keys. Also, it is NOT required that the key value and mapped value pair has to be unique in this case.
  > Some Basic Functions associated with multimap:
  >
  > 1. begin() – Returns an iterator to the first element in the multimap
  > 1. end() – Returns an iterator to the theoretical element that follows last element in the multimap
  > 1. size() – Returns the number of elements in the multimap
  > 1. max_size() – Returns the maximum number of elements that the multimap can hold
  > 1. empty() – Returns whether the multimap is empty
  > 1. pair<int,int> insert(keyvalue,multimapvalue) – Adds a new element to the multimap
  >
  > List of Functions of Multimap:
  >
  > 1. multimap::operator= in C++ STL– It is used to assign new contents to the container by replacing the existing contents.
  > 1. multimap::crbegin() and multimap::crend() in C++ STL– crbegin() returns a constant reverse iterator referring to the last element in the multimap container. crend() returns a constant reverse iterator pointing to the theoretical element before the first element in the multimap.
  > 1. multimap::emplace_hint() in C++ STL– Inserts the key and its element in the multimap container with a given hint.
  > 1. multimap clear() function in C++ STL– Removes all the elements from the multimap.
  > 1. multimap empty() function in C++ STL– Returns whether the multimap is empty.
  > 1. multimap maxsize() in C++ STL– Returns the maximum number of elements a multimap container can hold.
  > 1. multimap value_comp() function in C++ STL– Returns the object that determines how the elements in the multimap are ordered (‘<‘ by default)
  > 1. multimap rend in C++ STL– Returns a reverse iterator pointing to the theoretical element preceding to the first element of the multimap container.
  > 1. multimap::cbegin() and multimap::cend() in C++ STL– cbegin() returns a constant iterator referring to the first element in the multimap container. cend() returns a constant iterator pointing to the theoretical element that follows last element in the multimap.
  > 1. multimap::swap() in C++ STL– Swap the contents of one multimap with another multimap of same type and size.
  > 1. multimap rbegin in C++ STL– Returns an iterator pointing to the last element of the container.
  > 1. multimap size() function in C++ STL– Returns the number of elements in the multimap container.
  > 1. multimap::emplace() in C++ STL– Inserts the key and its element in the multimap container.
  > 1. multimap::begin() and multimap::end() in C++ STL– begin() returns an iterator referring to the first element in the multimap container. end() returns an iterator to the theoretical element that follows last element in the multimap.
  > 1. multimap upper_bound() function in C++ STL– Returns an iterator to the first element that is equivalent to multimapped value with key value ‘g’ or definitely will go after the element with key value ‘g’ in the multimap.
  > 1. multimap::count() in C++ STL– Returns the number of matches to element with key value ‘g’ in the multimap.
  > 1. multimap::erase() in C++ STL– Removes the key value from the multimap.
  > 1. multimap::find() in C++ STL– Returns an iterator to the element with key value ‘g’ in the multimap if found, else returns the iterator to end.
  > 1. multimap equal_range() in C++ STL– Returns an iterator of pairs. The pair refers to the bounds of a range that includes all the elements in the container which have a key equivalent to k.
  > 1. multimap insert() in C++ STL– Used to insert elements in the multimap container.
  > 1. multimap lower_bound() function in C++ STL– Returns an iterator to the first element that is equivalent to multimapped value with key value ‘g’ or definitely will not go before the element with key value ‘g’ in the multimap.
  > 1. multimap key_comp() in C++ STL– Returns the object that determines how the elements in the multimap are ordered (‘<‘ by default).

```c++
#include <iostream>
#include <map>
#include <iterator>

using namespace std;

int main()
{
	multimap <int, int> gquiz1;	 // empty multimap container

	// insert elements in random order
	gquiz1.insert(pair <int, int> (1, 40));
	gquiz1.insert(pair <int, int> (2, 30));
	gquiz1.insert(pair <int, int> (3, 60));
	gquiz1.insert(pair <int, int> (4, 20));
	gquiz1.insert(pair <int, int> (5, 50));
	gquiz1.insert(pair <int, int> (6, 50));
	gquiz1.insert(pair <int, int> (6, 10));

	// printing multimap gquiz1
	multimap <int, int> :: iterator itr;
	cout << "\nThe multimap gquiz1 is : \n";
	cout << "\tKEY\tELEMENT\n";
	for (itr = gquiz1.begin(); itr != gquiz1.end(); ++itr)
	{
		cout << '\t' << itr->first
			<< '\t' << itr->second << '\n';
	}
	cout << endl;

	// assigning the elements from gquiz1 to gquiz2
	multimap <int, int> gquiz2(gquiz1.begin(),gquiz1.end());

	// print all elements of the multimap gquiz2
	cout << "\nThe multimap gquiz2 after assign from gquiz1 is : \n";
	cout << "\tKEY\tELEMENT\n";
	for (itr = gquiz2.begin(); itr != gquiz2.end(); ++itr)
	{
		cout << '\t' << itr->first
			<< '\t' << itr->second << '\n';
	}
	cout << endl;

	// remove all elements up to element with value 30 in gquiz2
	cout << "\ngquiz2 after removal of elements less than key=3 : \n";
	cout << "\tKEY\tELEMENT\n";
	gquiz2.erase(gquiz2.begin(), gquiz2.find(3));
	for (itr = gquiz2.begin(); itr != gquiz2.end(); ++itr)
	{
		cout << '\t' << itr->first
			<< '\t' << itr->second << '\n';
	}

	// remove all elements with key = 4
	int num;
	num = gquiz2.erase(4);
	cout << "\ngquiz2.erase(4) : ";
	cout << num << " removed \n" ;
	cout << "\tKEY\tELEMENT\n";
	for (itr = gquiz2.begin(); itr != gquiz2.end(); ++itr)
	{
		cout << '\t' << itr->first
			<< '\t' << itr->second << '\n';
	}

	cout << endl;

	//lower bound and upper bound for multimap gquiz1 key = 5
	cout << "gquiz1.lower_bound(5) : " << "\tKEY = ";
	cout << gquiz1.lower_bound(5)->first << '\t';
	cout << "\tELEMENT = " << gquiz1.lower_bound(5)->second << endl;
	cout << "gquiz1.upper_bound(5) : " << "\tKEY = ";
	cout << gquiz1.upper_bound(5)->first << '\t';
	cout << "\tELEMENT = " << gquiz1.upper_bound(5)->second << endl;

	return 0;

}


<!--The multimap gquiz1 is : -->
<!--    KEY    ELEMENT-->
<!--    1    40-->
<!--    2    30-->
<!--    3    60-->
<!--    4    20-->
<!--    5    50-->
<!--    6    50-->
<!--    6    10-->


<!--The multimap gquiz2 after assign from gquiz1 is : -->
<!--    KEY    ELEMENT-->
<!--    1    40-->
<!--    2    30-->
<!--    3    60-->
<!--    4    20-->
<!--    5    50-->
<!--    6    50-->
<!--    6    10-->


<!--gquiz2 after removal of elements less than key=3 : -->
<!--    KEY    ELEMENT-->
<!--    3    60-->
<!--    4    20-->
<!--    5    50-->
<!--    6    50-->
<!--    6    10-->

<!--gquiz2.erase(4) : 1 removed -->
<!--    KEY    ELEMENT-->
<!--    3    60-->
<!--    5    50-->
<!--    6    50-->
<!--    6    10-->

<!--gquiz1.lower_bound(5) :     KEY = 5        ELEMENT = 50-->
<!--gquiz1.upper_bound(5) :     KEY = 6        ELEMENT = 50-->

```

[返回目录](#Menu)

## 4. <span id="Unordered_Associative_Containers">Unordered Associative Containers</span> [^unordered_associative_containers]

- ### <span id="unordered_set">unordered_set (Introduced in C++11)</span>

  An unordered_set is implemented using a hash table where keys are hashed into indices of a hash table so that the insertion is always randomized. All operations on the unordered_set takes constant time O(1) on an average which can go up to linear time O(n) in worst case which depends on the internally used hash function, but practically they perform very well and generally provide a constant time lookup operation.  
   The unordered_set can contain key of any type – predefined or user-defined data structure but when we define key of type user define the type, we need to specify our comparison function according to which keys will be compared.

  Sets vs Unordered Sets  
   Set is an ordered sequence of unique keys whereas unordered_set is a set in which key can be stored in any order, so unordered. Set is implemented as a balanced tree structure that is why it is possible to maintain order between the elements (by specific tree traversal). The time complexity of set operations is O(log n) while for unordered_set, it is O(1).

  Methods on Unordered Sets:  
   For unordered_set many functions are defined among which most users are the size and empty for capacity, find for searching a key, insert and erase for modification.  
   The Unordered_set allows only unique keys, for duplicate keys unordered_multiset should be used.

  Example of declaration, find, insert and iteration in unordered_set is given below :

```c++
// C++ program to demonstrate various function of unordered_set
#include <bits/stdc++.h>
using namespace std;

int main()
{
	// declaring set for storing string data-type
	unordered_set <string> stringSet ;

	// inserting various string, same string will be stored
	// once in set

	stringSet.insert("code") ;
	stringSet.insert("in") ;
	stringSet.insert("c++") ;
	stringSet.insert("is") ;
	stringSet.insert("fast") ;

	string key = "slow" ;

	// find returns end iterator if key is not found,
	// else it returns iterator to that key

	if (stringSet.find(key) == stringSet.end())
		cout << key << " not found" << endl << endl ;
	else
		cout << "Found " << key << endl << endl ;

	key = "c++";
	if (stringSet.find(key) == stringSet.end())
		cout << key << " not found\n" ;
	else
		cout << "Found " << key << endl ;

	// now iterating over whole set and printing its
	// content
	cout << "\nAll elements : ";
	unordered_set<string> :: iterator itr;
	for (itr = stringSet.begin(); itr != stringSet.end(); itr++)
		cout << (*itr) << endl;
}


<!--slow not found-->

<!--Found c++-->

<!--All elements : -->
<!--is-->
<!--fast-->
<!--c++-->
<!--in-->
<!--code-->
```

find, insert and erase take constant amount of time on average. The find() function returns an iterator to end() if key is not there in set, otherwise an iterator to the key position is returned. The iterator works as a pointer to the key values so that we can get the key by dereferencing them using \* operator.

A practical problem based on unordered_set – Given a set of integers, find all the duplicates among them.

    Input  : arr[] = {1, 5, 2, 1, 4, 3, 1, 7, 2, 8, 9, 5}
    Output : Duplicate item are : 5 2 1

Below is C++ solution using unordered_set.

```c++
// C++ program to find duplicate from an array using
// unordered_set
#include <bits/stdc++.h>
using namespace std;

// Print duplicates in arr[0..n-1] using unordered_set
void printDuplicates(int arr[], int n)
{
	// declaring unordered sets for checking and storing
	// duplicates
	unordered_set<int> intSet;
	unordered_set<int> duplicate;

	// looping through array elements
	for (int i = 0; i < n; i++)
	{
		// if element is not there then insert that
		if (intSet.find(arr[i]) == intSet.end())
			intSet.insert(arr[i]);

		// if element is already there then insert into
		// duplicate set
		else
			duplicate.insert(arr[i]);
	}

	// printing the result
	cout << "Duplicate item are : ";
	unordered_set<int> :: iterator itr;

	// iterator itr loops from begin() till end()
	for (itr = duplicate.begin(); itr != duplicate.end(); itr++)
		cout << *itr << " ";
}

// Driver code
int main()
{
	int arr[] = {1, 5, 2, 1, 4, 3, 1, 7, 2, 8, 9, 5};
	int n = sizeof(arr) / sizeof(int);

	printDuplicates(arr, n);
	return 0;
}


<!--Duplicate item are : 5 1 2 -->
```

> Methods of unordered_set:
>
> 1. insert()– Insert a new {element} in the unordered_set container.
> 1. begin()– Return an iterator pointing to the first element in the unordered_set container.
> 1. end()– Returns an iterator pointing to the past-the-end-element.
> 1. count()– Count occurrences of a particular element in an unordered_set container.
> 1. find()– Search for an element in the container.
> 1. clear()– Removes all of the elements from an unordered_set and empties it.
> 1. cbegin()– Return a const_iterator pointing to the first element in the unordered_set container.
> 1. cend()– Return a const_iterator pointing to past-the-end element in the unordered_set container or in one of it’s bucket.
> 1. bucket_size()– Returns the total number of elements present in a specific bucket in an unordered_set container.
> 1. erase()– Remove either a single element of a range of elements ranging from start(inclusive) to end(exclusive).
> 1. size()– Return the number of elements in the unordered_set container.
> 1. swap()– Exchange values of two unordered_set containers.
> 1. emplace()– Insert an element in an unordered_set container.
> 1. max_size()– Returns maximum number of elements that an unordered_set container can hold.
> 1. empty()– Check if an unordered_set container is empty or not.
> 1. equal_range– Returns range that includes all elements equal to given value.
> 1. operator= – Copies (or moves) an unordered_set to another unordered_set and unordered_set::operator= is the corresponding operator function.
> 1. hash_function() – This hash function is a unary function which takes asingle argument only and returns a unique value of type size_t based on it.
> 1. reserve()– Used to request capacity change of unordered_set.
> 1. bucket()– Returns the bucket number of a specific element.
> 1. bucket_count() – Returns the total number of buckets present in an unordered_set container.
> 1. load_factor()– Returns the current load factor in the unordered_set container.
> 1. rehash()– Set the number of buckets in the container of unordered_set to given size or more.
> 1. max_load_factor()– Returns(Or sets) the current maximum load factor of the unordered set container.
> 1. emplace_hint()– Inserts a new element in the unordered_set only if the value to be inserted is unique, with a given hint.
> 1. \== operator – The ‘\==’ is an operator in C++ STL performs equality comparison operation between two unordered sets and unordered_set::operato\== is the corresponding operator function for the same.
> 1. key_eq()– Returns a boolean value according to the comparison. It returns the key equivalence comparison predicate used by the unordered_set.
> 1. operator!=– The != is a relational operator in C++ STL which compares the equality and inequality between unordered_set containers.
> 1. max_bucket_count() – Find the maximum number of buckets that unordered_set can have.

[返回目录](#Menu)

- ### <span id="unordered_multiset">unordered_multiset (Introduced in C++11)</span>
  We have discussed about unordered_set in our previous post the problem with unordered_set is that, it is not possible to store duplicate entries in that data structure. For example if we have some value v already in unordered_set, inserting v again will have no effect.  
   To handle this duplication unordered_mulitset should be used, it can store duplicate elements also. Internally when an existing value is inserted, the data structure increases its count which is associated with each value. As count of each value is stored in unordered_multiset, it takes more space than unordered_set (if all values are distinct).  
   The internal implementation of unordered_multiset is same as that of unordered_set and also uses hash table for searching, just the count value is associated with each value in former one. Due to hashing of elements it has no particular order of storing the elements so all element can come in any order but duplicate element comes together. All operation on unordered_multiset takes constant time on average but can go upto linear in worst case.  
   Unordered_multiset supports many function which are demonstrated in below code :

```c++
// C++ program to demonstrate various function
// of unordered_multiset
#include <bits/stdc++.h>
using namespace std;

// making typedef for short declaration
typedef unordered_multiset<int>::iterator umit;

// Utility function to print unordered_multiset
void printUset(unordered_multiset<int> ums)
{
	// begin() returns iterator to first element of set
	umit it = ums.begin();
	for (; it != ums.end(); it++)
		cout << *it << " ";
	cout << endl;
}

// Driver program to check all function
int main()
{
	// empty initialization
	unordered_multiset<int> ums1;

	// Initialization by intializer list
	unordered_multiset<int> ums2 ({1, 3, 1, 7, 2, 3,
								4, 1, 6});

	// Initialization by assignment
	ums1 = {2, 7, 2, 5, 0, 3, 7, 5};

	// empty() function return true if set is empty
	// otherwise false
	if (ums1.empty())
		cout << "unordered multiset 1 is empty\n";
	else
		cout << "unordered multiset 1 is not empty\n";

	// size() function returns total number of elements
	// in data structure
	cout << "The size of unordered multiset 2 is : "
		<< ums2.size() << endl;

	printUset(ums1);

	ums1.insert(7);

	printUset(ums1);

	int val = 3;

	// find function returns iterator to first position
	// of val, if exist otherwise it returns iterator
	// to end
	if (ums1.find(val) != ums1.end())
		cout << "unordered multiset 1 contains "
			<< val << endl;
	else
		cout << "unordered multiset 1 does not contains "
			<< val << endl;

	// count function returns total number of occurrence in set
	val = 5;
	int cnt = ums1.count(val);
	cout << val << " appears " << cnt
		<< " times in unordered multiset 1 \n";

	val = 9;

	// if count return >0 value then element exist otherwise not
	if (ums1.count(val))
		cout << "unordered multiset 1 contains "
			<< val << endl;
	else
		cout << "unordered multiset 1 does not contains "
			<< val << endl;

	val = 1;

	// equal_range returns a pair, where first is iterator
	// to first position of val and second it iterator to
	// last position to val
	pair<umit, umit> erange_it = ums2.equal_range(val);
	if (erange_it.first != erange_it.second)
		cout << val << " appeared atleast once in "
						"unoredered_multiset \n";


	printUset(ums2);

	// erase function deletes all instances of val
	ums2.erase(val);

	printUset(ums2);

	// clear function deletes all entries from set
	ums1.clear();
	ums2.clear();

	if (ums1.empty())
		cout << "unordered multiset 1 is empty\n";
	else
		cout << "unordered multiset 1 is not empty\n";
}


<!--unordered multiset 1 is not empty-->
<!--The size of unordered multiset 2 is : 9-->
<!--3 0 5 5 7 7 2 2 -->
<!--3 0 5 5 7 7 7 2 2 -->
<!--unordered multiset 1 contains 3-->
<!--5 appears 2 times in unordered multiset 1 -->
<!--unordered multiset 1 does not contains 9-->
<!--1 appeared atleast once in unoredered_multiset -->
<!--6 4 2 7 3 3 1 1 1 -->
<!--6 4 2 7 3 3 -->
<!--unordered multiset 1 is empty-->
```

As we can see most of the operation work similar to that of unordered_set but some things to note are:
equal_range(val) function returns a pair of type where first iterator points to first position of val and second points to last position of val in data structure.  
erase(val) function deletes all its instances from the data structure for example if some value v has occurred t times in unordered_multiset and when erase is called, v is deleted completely which is not a expected behavior many times.

We can delete only one copy of some value by using find function and iterator version of erase, as find function returns iterator to first position of found value we can pass this iterator to erase instead of actual value to delete only one copy, the code for doing this is shown below :

```c++
// C++ program to delete one copy from unordered set
#include <bits/stdc++.h>
using namespace std;

// making typedef for short declaration
typedef unordered_multiset<int>::iterator umit;

// Utility function to print unordered_multiset
void printUset(unordered_multiset<int> ums)
{
	// begin() returns iterator to first element of
	// set
	umit it = ums.begin();
	for (; it != ums.end(); it++)
		cout << *it << " ";
	cout << endl;
}

// function to delete one copy of val from set
void erase_one_entry(unordered_multiset<int>& ums,
					int val)
{
	// find returns iterator to first position
	umit it = ums.find(val);

	// if element is there then erasing that
	if (it != ums.end())
	ums.erase(it);
}

// Driver program to check above function
int main()
{
	// initializing multiset by initializer list
	unordered_multiset<int> ums ({1, 3, 1, 7, 2, 3,
								4, 1, 6});

	int val = 1;
	printUset(ums);
	erase_one_entry(ums, val);
	printUset(ums);
}



<!--6 4 2 7 3 3 1 1 1 -->
<!--6 4 2 7 3 3 1 1 -->
```

> Methods of unordered_multiset:
>
> 1. insert()– Inserts new elements in the unordered_multiset. Thus increases the container size.
> 1. begin()– Returns an iterator pointing to the first element in the container or to the first element in one of its bucket.
> 1. end()– Returns an iterator pointing to the position immediately after the last element in the container or to the position immediately after the last element in one of its bucket.
> 1. empty()– It returns true if the unordered_multiset container is empty. Otherwise, it returns false.
> 1. find()– Returns an iterator which points to the position which has the element val.
> 1. cbegin()– Returns a constant iterator pointing to the first element in the container or to the first element in one of its bucket.
> 1. cend()– Returns a constant iterator pointing to the position immediately after the last element in the container or to the position immediately after the last element in one of its bucket.
> 1. equal_range()– Returns the range in which all the elements are equal to a given value.
> 1. emplace()– Inserts a new element in the unordered_multiset container.
> 1. clear()– Clears the contents of the unordered_multiset container.
> 1. count()– Returns the count of elements in the unordered_multiset container which is equal to a given value.
> 1. size()– The size() method of unordered_multiset is used to count the number of elements of unordered_set it is called with.
> 1. max_size– The max_size() of unordered_multiset takes the maximum number of elements that the unordered_multiset container is able to hold.
> 1. swap()– Swaps the contents of two unordered_multiset containers.
> 1. erase() – Used to remove either a single element or, all elements with a definite value or, a range of elements ranging from start(inclusive) to end(exclusive).
> 1. bucket()– Returns the bucket number in which a given element is. Bucket size varies from 0 to bucket_count-1.
> 1. bucket_size()– Returns the number of elements in the bucket which has the element val.
> 1. reserve()– The reverse() function of unordered_multiset sets the number of buckets in the container (bucket_count) to the most appropriate to contain at least n elements.
> 1. max_bucket_count()– Returns the maximum number of buckets that the unordered multiset container can have.
> 1. load_factor()– Returns the current load factor in the unordered_multiset container.
> 1. max_load_factor()– Returns the maximum load factor of the unordered_multiset container.
> 1. bucket_count()– Returns the total number of buckets in the unordered_multiset container.
> 1. hash_function()– This hash function is a unary function which takes a single argument only and returns a unique value of type size_t based on it.
> 1. rehash()– Sets the number of buckets in the container to N or more.
> 1. key_eq()– Returns a boolean value according to the comparison.
> 1. emplace_hint()– Inserts a new element in the unordered_multiset container.
> 1. get_allocator– This function gets the stored allocator object and returns the allocator object which is used to construct the container.
> 1. operator =– The ‘=’ is an operator in C++ STL which copies (or moves) an unordered_multiset to another unordered_multiset and unordered_multiset::operator= is the corresponding operator function.

[返回目录](#Menu)

- ### <span id="unordered_map">unordered_map (Introduced in C++11)</span>

      unordered_map is an associated container that stores elements formed by combination of key value and a mapped value. The key value is used to uniquely identify the element and mapped value is the content associated with the key. Both key and value can be of any type predefined or user-defined.
      Internally unordered_map is implemented using Hash Table, the key provided to map are hashed into indices of hash table that is why performance of data structure depends on hash function a lot but on an average the cost of search, insert and delete from hash table is O(1).
      ```c++
      // C++ program to demonstrate functionality of unordered_map
      #include <iostream>
      #include <unordered_map>
      using namespace std;

      int main()
      {
      	// Declaring umap to be of <string, int> type
      	// key will be of string type and mapped value will
      	// be of double type
      	unordered_map<string, int> umap;

      	// inserting values by using [] operator
      	umap["GeeksforGeeks"] = 10;
      	umap["Practice"] = 20;
          umap["Contribute"] = 30;

      	// Traversing an unordered map
      	for (auto x : umap)
      	cout << x.first << " " << x.second << endl;

      }

      <!--Contribute 30-->
      <!--GeeksforGeeks 10-->
      <!--Practice 20-->
      ```
      **unordered_map vs unordered_set :**
      In unordered_set, we have only key, no value, these are mainly used to see presence/absence in a set. For example, consider the problem of counting frequencies of individual words. We can’t use unordered_set (or set) as we can’t store counts.

      **unordered_map vs map :**
      map (like set) is an ordered sequence of unique keys whereas in unordered_map key can be stored in any order, so unordered.
      Map is implemented as balanced tree structure that is why it is possible to maintain an order between the elements (by specific tree traversal). Time complexity of map operations is O(Log n) while for unordered_map, it is O(1) on average.

      **Methods on unordered_map**
      A lot of function are available which work on unordered_map. most useful of them are – operator =, operator [], empty and size for capacity, begin and end for iterator, find and count for lookup, insert and erase for modification.
      The C++11 library also provides function to see internally used bucket count, bucket size and also used hash function and various hash policies but they are less useful in real application.
      We can iterate over all elements of unordered_map using Iterator. Initialization, indexing and iteration is shown in below sample code :
      ```c++
      // C++ program to demonstrate functionality of unordered_map
      #include <iostream>
      #include <unordered_map>
      using namespace std;

      int main()
      {
      	// Declaring umap to be of <string, double> type
      	// key will be of string type and mapped value will
      	// be of double type
      	unordered_map<string, double> umap;

      	// inserting values by using [] operator
      	umap["PI"] = 3.14;
      	umap["root2"] = 1.414;
      	umap["root3"] = 1.732;
      	umap["log10"] = 2.302;
      	umap["loge"] = 1.0;

      	// inserting value by insert function
      	umap.insert(make_pair("e", 2.718));

      	string key = "PI";

      	// If key not found in map iterator to end is returned
      	if (umap.find(key) == umap.end())
      		cout << key << " not found\n\n";

      	// If key found then iterator to that key is returned
      	else
      		cout << "Found " << key << "\n\n";

      	key = "lambda";
      	if (umap.find(key) == umap.end())
      		cout << key << " not found\n";
      	else
      		cout << "Found " << key << endl;

      	// iterating over all value of umap
      	unordered_map<string, double>:: iterator itr;
      	cout << "\nAll Elements : \n";
      	for (itr = umap.begin(); itr != umap.end(); itr++)
      	{
      		// itr works as a pointer to pair<string, double>
      		// type itr->first stores the key part and
      		// itr->second stroes the value part
      		cout << itr->first << " " << itr->second << endl;
      	}
      }


      <!--    Found PI-->

      <!--lambda not found-->

      <!--All Elements : -->
      <!--loge  1-->
      <!--e  2.718-->
      <!--log10  2.302-->
      <!--root3  1.732-->
      <!--PI  3.14-->
      <!--root2  1.414-->

      ```
      A practical problem based on unordered_map – given a string of words, find frequencies of individual words.

          Input :  str = "geeks for geeks geeks quiz practice qa for";
          Output : Frequencies of individual words are
          (practice, 1)
          (for, 2)
          (qa, 1)
          (quiz, 1)
          (geeks, 3)
      Below is a C++ solution using unordered_map.
      ```c++
      // C++ program to find freq of every word using
      // unordered_map
      #include <bits/stdc++.h>
      using namespace std;

      // Prints frequencies of individual words in str
      void printFrequencies(const string &str)
      {
      	// declaring map of <string, int> type, each word
          // is mapped to its frequency
          unordered_map<string, int> wordFreq;

      	// breaking input into word using string stream
      	stringstream ss(str); // Used for breaking words
      	string word; // To store individual words
      	while (ss >> word)
      		wordFreq[word]++;

      	// now iterating over word, freq pair and printing
      	// them in <, > format
      	unordered_map<string, int>:: iterator p;
      	for (p = wordFreq.begin(); p != wordFreq.end(); p++)
      		cout << "(" << p->first << ", " << p->second << ")\n";
      }

      // Driver code
      int main()
      {
      	string str = "geeks for geeks geeks quiz "
      				"practice qa for";
      	printFrequencies(str);
      	return 0;
      }



      <!--(qa, 1)-->
      <!--(quiz, 1)-->
      <!--(practice, 1)-->
      <!--(geeks, 3)-->
      <!--(for, 2)-->
      ```

  > Methods of unordered_map :
  >
  > 1. at(): This function in C++ unordered_map returns the reference to the value with the element as key k.
  > 1. begin(): Returns an iterator pointing to the first element in the container in the unordered_map container
  > 1. end(): Returns an iterator pointing to the position past the last element in the container in the > 1. unordered_map container
  > 1. bucket(): Returns the bucket number where the element with the key k is located in the map.
  > 1. bucket_count: bucket_count is used to count the total no. of buckets in the unordered_map. No parameter is required to pass into this function.
  > 1. bucket_size: Returns number of elements in each bucket of the unordered_map.
  > 1. count(): Count the number of elements present in an unordered_map with a given key.
  > 1. equal_range: Return the bounds of a range that includes all the elements in the container with a key that compares equal to k.

[返回目录](#Menu)

- ### <span id="unordered_multimap">unordered_multimap (Introduced in C++11)</span>

  **Allows Duplicates:**  
   We have discussed about unordered_map in our previous post , but there is a limitation, we can not store duplicates in unordered_map, that is if we have a key value pair already in our unordered_multimap and another pair is inserted, then both will be there whereas in case of unordered_map the previous value corresponding to the key is updated by new value that is only would be there. Even can exist in unordered_multimap twice.

  **Internal Representation:**  
   The internal implementation of unordered_multimap is same as that of unordered_map but for duplicate keys another count value is maintained with each key- value pair. As pairs are stored in hash table, there is no particular order among them but pair with same keys come together in data structure whereas pair with same values are not guaranteed to come together.

  **Time Complexity:**  
   All operation on unordered_multimap takes constant amount of time on an average but time can go to linear in worst case depending on internally used hash function but in long run unordered_multimap outperforms multimap (tree based multimap).

Functions:
unorderd_multimap supports many function which are demonstrated in below code :

```c++
// C++ program to demonstrate various function of
// unordered_multimap
#include <bits/stdc++.h>
using namespace std;

//making typedef for short declaration
typedef unordered_multimap<string, int>::iterator umit;

// Utility function to print unordered_multimap
void printUmm(unordered_multimap<string, int> umm)
{
	// begin() returns iterator to first element of map
	umit it = umm.begin();

	for (; it != umm.end(); it++)
		cout << "<" << it->first << ", " << it->second
			<< "> ";

	cout << endl;
}

// Driver program to check all function
int main()
{
	// empty initialization
	unordered_multimap<string, int> umm1;

	// Initialization bu intializer list
	unordered_multimap<string, int> umm2 ({{"apple", 1},
										{"ball", 2},
										{"apple", 10},
										{"cat", 7},
										{"dog", 9},
										{"cat", 6},
										{"apple", 1}});

	// Initialization by assignment operation
	umm1 = umm2;
	printUmm(umm1);

	// empty returns true, if container is empty else it returns
	// false
	if (umm2.empty())
		cout << "unordered multimap 2 is empty\n";
	else
		cout << "unordered multimap 2 is not empty\n";

	// size returns total number of elements in container
	cout << "Size of unordered multimap 1 is " << umm1.size()
		<< endl;

	string key = "apple";

	// find and return any pair, associated with key
	umit it = umm1.find(key);
	if (it != umm1.end())
	{
		cout << "\nkey " << key << " is there in unordered "
			<< " multimap 1\n";
		cout << "\none of the value associated with " << key
			<< " is " << it->second << endl;
	}
	else
		cout << "\nkey " << key << " is not there in unordered"
			<< " multimap 1\n";

	// count returns count of total number of pair associated
	// with key
	int cnt = umm1.count(key);
	cout << "\ntotal values associated with " << key << " are "
		<< cnt << "\n\n";

	printUmm(umm2);

	// one insertion by makeing pair explicitly
	umm2.insert(make_pair("dog", 11));

	// insertion by initializer list
	umm2.insert({{"alpha", 12}, {"beta", 33}});
	cout << "\nAfter insertion of <apple, 12> and <beta, 33>\n";
	printUmm(umm2);

	// erase deletes all pairs corresponding to key
	umm2.erase("apple");
	cout << "\nAfter deletion of apple\n";
	printUmm(umm2);

	// clear deletes all pairs from container
	umm1.clear();
	umm2.clear();

	if (umm2.empty())
		cout << "\nunordered multimap 2 is empty\n";
	else
		cout << "\nunordered multimap 2 is not empty\n";
}



<!--<apple, 1>  <apple, 10>  <apple, 1>  <ball, 2>  <cat, 6>  <cat, 7>  <dog, 9>  -->
<!--unordered multimap 2 is not empty-->
<!--Size of unordered multimap 1 is 7-->

<!--key apple is there in unordered  multimap 1-->

<!--one of the value associated with apple is 1-->

<!--total values associated with apple are 3-->

<!--<apple, 1>  <apple, 10>  <apple, 1>  <ball, 2>  <cat, 6>  <cat, 7>  <dog, 9>  -->

<!--After insertion of <apple, 12> and <beta, 33>-->
<!--<beta, 33>  <alpha, 12>  <apple, 1>  <apple, 10>  <apple, 1>  <ball, 2>-->
<!--<cat, 6>  <cat, 7>  <dog, 11>  <dog, 9>  -->

<!--After deletion of apple-->
<!--<beta, 33>  <alpha, 12>  <ball, 2>  <cat, 6>  <cat, 7>  <dog, 11>  <dog, 9>  -->

<!--unordered multimap 2 is empty-->
```

As we can see in above code most of the operation work similar to unordered_map but some things to note are :  
We can use initializer list for initializing and inserting many pairs at once.  
There is no [] operator for unordered_multimap because values corresponding to a key are not unique, there can be many values associated with a single key so [] operator can not be applied to them.  
Erase function deletes all instances of values associated with supplied key.  
Find function returns an iterator to any instance of key-value pair among all pair associated with that key.

**How to access/delete if a specific value for a key?**  
If we want to check whether a specific is there or not, we need to loop over all pairs of key-value corresponding to k, in similar way we can erase one copy of a specific from data structure. There is no specified order in which all values of a key are stored.

```c++
// C++ program to implement find and erase for specific
// key-value pair for unordered_multimap
#include <bits/stdc++.h>
using namespace std;

// making typedef for short declaration
typedef unordered_multimap<string, int>:: iterator umit;

// function to check whether p is there in map or not
bool find_kv(unordered_multimap<string, int>& umm,
			pair<string, int> p)
{
	// equal_range returns pair of iterator of first and last
	// position associated with key
	pair<umit, umit> it = umm.equal_range(p.first);
	umit it1 = it.first;

	pair<string, int> tmp;

	// looping over all values associated with key
	while (it1 != it.second)
	{
		tmp = *it1;
		if (tmp == p)
			return true;
		it1++;
	}
	return false;
}

// function to delete one copy of pair p from map umm
void erase_kv(unordered_multimap<string, int>& umm,
			pair<string, int> p)
{
	// equal_range returns pair of iterator of first and
	// last position associated with key
	pair<umit, umit> it = umm.equal_range(p.first);
	umit it1 = it.first;
	pair<string, int> tmp;

	// looping over all values associated with key
	while (it1 != it.second)
	{
		tmp = *it1;
		if (tmp == p)
		{
			// iterator version of erase : deletes pair
			// at that position only
			umm.erase(it1);
			break;
		}
		it1++;
	}
}

// Utility function to print unordered_multimap
void printUmm(unordered_multimap<string, int> umm)
{
	// begin() returns iterator to first element of map
	umit it = umm.begin();
	for (; it != umm.end(); it++)
		cout << "<" << it->first << ", " << it->second << "> ";
	cout << endl;
}

// Driver program to check above function
int main()
{
	// initializing multimap by initializer list
	unordered_multimap<string, int> umm ({{"apple", 1},
		{"ball", 2},
		{"apple", 10},
		{"cat", 7},
		{"dog", 9},
		{"cat", 6},
		{"apple", 1}
	});

	cout << "Initial content\n";
	printUmm(umm);
	pair<string, int> kv = make_pair("apple", 1);

	cout << "\nAfter insertion of one more <apple, 1>\n";
	printUmm(umm);

	if (find_kv(umm, kv))
		erase_kv(umm, kv);
	else
		cout << "key-value pair is not there in unordered multimap\n";

	cout << "\nAfter deletion one occurrence of <apple, 1>\n";
	printUmm(umm);
}



<!--Initial content-->
<!--<apple, 1> <apple, 10> <apple, 1> <ball, 2> <cat, 6> <cat, 7> <dog, 9> -->

<!--After insertion of one more <apple, 1>-->
<!--<apple, 1> <apple, 10> <apple, 1> <ball, 2> <cat, 6> <cat, 7> <dog, 9> -->

<!--After deletion one occurrence of <apple, 1>-->
<!--<apple, 10> <apple, 1> <ball, 2> <cat, 6> <cat, 7> <dog, 9> -->
```

> Methods of unordered_multimap:
>
> 1. begin()– Returns an iterator pointing to the first element in the container or to the first element in one of its bucket.
> 1. end()– Returns an iterator pointing to the position after the last element in the container or to the position after the last element in one of its bucket.
> 1. count()– Returns the number of elements in the container whose key is equal to the key passed in the parameter.
> 1. cbegin()– Returns a constant iterator pointing to the first element in the container or to the first element in one of its bucket.
> 1. cend()– Returns a constant iterator pointing to the position after the last element in the container or to the position after the last element in one of its bucket.
> 1. clear() – Clears the contents of the unordered_multimap container.
> 1. size()– Returns the size of the unordered_multimap. It denotes the number of elements in that container.
> 1. swap()– Swaps the contents of two unordered_multimap containers. The sizes can differ of both the containers.
> 1. find()– Returns an iterator which points to one of the elements which has the key k.
> 1. bucket_size()– Returns the number of elements in the bucket n.
> 1. empty()– It returns true if the unordered_multimap container is empty. Otherwise, it returns false.
> 1. equal_range()– Returns the range in which all the element’s key is equal to a key.
> 1. operator=– Copy/Assign/Move elements from different container.
> 1. max_size()– Returns the maximum number of elements that the unordered_multimap container can hold.
> 1. load_factor()– Returns the current load factor in the unordered_multimap container.
> 1. key_eq()– Returns a boolean value according to the comparison.
> 1. emplace()– Inserts a new {key, element} in the unordered_multimap container.
> 1. emplace_hint()– Inserts a new {key:element} in the unordered_multimap container.
> 1. bucket_count()– Returns the total number of buckets in the unordered_multimap container.
> 1. bucket()– Returns the bucket number in which a given key is.
> 1. max_load_factor()– Returns the maximum load factor of the unordered_multimap container.
> 1. rehash()– Sets the number of buckets in the container to N or more.
> 1. reserve()– Sets the number of buckets in the container (bucket_count) to the most appropriate number so that it contains at least n elements.
> 1. hash_function()– This hash function is a unary function which takes a single argument only and returns a unique value of type size_t based on it.
> 1. max_bucket_count()– Returns the maximum number of buckets that the unordered multimap container can have.

[返回目录](#Menu)

# 三. <span id="Functions">Functions</span>

> The STL includes classes that overload the function call operator. Instances of such classes are called function objects or functors. Functors allow the working of the associated function to be customized with the help of parameters to be passed.
>
> STL 包含使函数调用运算符重载的类。这种类的实例称为函数对象或函子。函子允许在要传递的参数的帮助下自定义关联功能的工作。

## 1. <span id="Functors">Functors</span>

> Please note that the title is Functors (Not Functions)!!  
> Consider a function that takes only one argument. However, while calling this function we have a lot more information that we would like to pass to this function, but we cannot as it accepts only one parameter. What can be done?  
> One obvious answer might be global variables. However, good coding practices do not advocate the use of global variables and say they must be used only when there is no other alternative.  
> Functors are objects that can be treated as though they are a function or function pointer. Functors are most commonly used along with STLs in a scenario like following:  
> Below program uses transform() in STL to add 1 to all elements of arr[].
>
> 请注意标题是函子（不是函数）！！  
> 考虑一个只接受一个参数的函数。然而，在调用这个函数时，我们有更多的信息想传递给这个函数，但是我们不能，因为它只接受一个参数。能做什么？  
> 一个显而易见的答案可能是全局变量。然而，良好的编码实践并不提倡使用全局变量，并且说只有在没有其他选择的情况下才必须使用全局变量。  
> 函子是可以当作函数或函数指针对待的对象。函子通常与 STL 一起在以下场景中使用：
> 下面的程序使用 STL 中的 transform（）将 1 添加到 arr[]的所有元素。
>
> ```c++
> // A C++ program uses transform() in STL to add
> // 1 to all elements of arr[]
> #include <bits/stdc++.h>
> using namespace std;
>
> int increment(int x) { return (x+1); }
>
> int main()
> {
> 	int arr[] = {1, 2, 3, 4, 5};
> 	int n = sizeof(arr)/sizeof(arr[0]);
>
> 	// Apply increment to all elements of
> 	// arr[] and store the modified elements
> 	// back in arr[]
> 	transform(arr, arr+n, arr, increment);
>
> 	for (int i=0; i<n; i++)
> 		cout << arr[i] <<" ";
>
> 	return 0;
> }
>
>
> <!--2 3 4 5 6-->
>
> ```
>
> This code snippet adds only one value to the contents of the arr[]. Now suppose, that we want to add 5 to contents of arr[].  
> See what’s happening? As transform requires a unary function(a function taking only one argument) for an array, we cannot pass a number to increment(). And this would, in effect, make us write several different functions to add each number. What a mess. This is where functors come into use.  
> A functor (or function object) is a C++ class that acts like a function. Functors are called using the same old function call syntax. To create a functor, we create a object that overloads the operator().
>
> 这个代码片段只向 arr[]的内容添加一个值。现在假设我们要在 arr[]的内容中添加 5。  
> 看到发生什么了吗？由于 transform 要求数组使用一元函数（一个只接受一个参数的函数），因此不能将数字传递给 increment（）。实际上，这会让我们写几个不同的函数来加上每个数。真是一团糟。这就是函子开始使用的地方。  
> 函子（或函数对象）是一个 C++类，它的作用类似于函数。使用相同的旧函数调用语法调用函数。为了创建函子，我们创建一个重载 operator（）的对象。
>
> ```
> The line,
> MyFunctor(10);
> Is same as
> MyFunctor.operator()(10);
> ```
>
> Let’s delve deeper and understand how this can actually be used in conjunction with STLs.
>
> 让我们更深入地研究并理解如何将其与 stl 结合使用。
>
> ```c++
> // C++ program to demonstrate working of
> // functors.
> #include <bits/stdc++.h>
> using namespace std;
>
> // A Functor
> class increment
> {
> private:
> 	int num;
> public:
> 	increment(int n) : num(n) { }
>
> 	// This operator overloading enables calling
> 	// operator function () on objects of increment
> 	int operator () (int arr_num) const {
> 		return num + arr_num;
> 	}
> };
>
> // Driver code
> int main()
> {
> 	int arr[] = {1, 2, 3, 4, 5};
> 	int n = sizeof(arr)/sizeof(arr[0]);
> 	int to_add = 5;
>
> 	transform(arr, arr+n, arr, increment(to_add));
>
> 	for (int i=0; i<n; i++)
> 		cout << arr[i] << " ";
> }
>
>
> <!--6 7 8 9 10-->
> ```
>
> Thus, here, Increment is a functor, a c++ class that acts as a function.
>
> 因此，在这里，Increment 是一个函子，一个充当函数的 c++类。
>
> ```
> The line,
> transform(arr, arr+n, arr, increment(to_add));
>
> is the same as writing below two lines,
> // Creating object of increment
> increment obj(to_add);
>
> // Calling () on object
> transform(arr, arr+n, arr, obj);
> ```
>
> Thus, an object a is created that overloads the operator(). Hence, functors can be used effectively in conjunction with C++ STLs.
>
> 因此，将创建一个重载 operator（）的对象 a。因此，函数可以有效地结合 C++的 STL 使用。

[返回目录](#Menu)

# 四. <span id="Iterators">Iterators</span>

> As the name suggests, iterators are used for working upon a sequence of values. They are the major feature that allow generality in STL.
>
> 顾名思义，迭代器用于处理一系列值。它们是允许在 STL 中通用的主要功能。

## 1. <span id="Iterator">Iterators</span>

- Iterators are used to point at the memory addresses of STL containers. They are primarily used in sequence of numbers, characters etc. They reduce the complexity and execution time of program.  
  迭代器用于指向 STL 容器的内存地址。它们主要用于数字、字符等序列，降低了程序的复杂度和执行时间。

> Operations of iterators :
>
> 1. begin()  
>    This function is used to return the beginning position of the container.  
>    `此函数用于返回容器的起始位置。`
> 2. end()  
>    This function is used to return the after end position of the container.  
>    `此函数用于返回容器的结束后位置。`
> 3. advance()  
>    This function is used to increment the iterator position till the specified number mentioned in its arguments.  
>    `此函数用于递增迭代器位置，直到其参数中指定的数字为止。`
> 4. next()  
>    This function returns the new iterator that the iterator would point after advancing the positions mentioned in its arguments.  
>    `此函数返回迭代器，迭代器将在推进其参数中提到的位置后指向该迭代器。`
> 5. prev()  
>    This function returns the new iterator that the iterator would point after decrementing the positions mentioned in its arguments.  
>    `此函数返回迭代器，迭代器将在递减其参数中提到的位置后指向该迭代器。`
> 6. inserter()  
>    This function is used to insert the elements at any position in the container. It accepts 2 arguments, the container and iterator to position where the elements have to be inserted.  
>    `此函数用于在容器中的任何位置插入元素。它接受2个参数，容器和迭代器来定位必须插入元素的位置。`

```c++
// C++ code to demonstrate the working of
// iterator, begin() and end()
#include<iostream>
#include<iterator> // for iterators
#include<vector> // for vectors
using namespace std;
int main()
{
	vector<int> ar = { 1, 2, 3, 4, 5 };

	// Declaring iterator to a vector
	vector<int>::iterator ptr;

	// Displaying vector elements using begin() and end()
	cout << "The vector elements are : ";
	for (ptr = ar.begin(); ptr < ar.end(); ptr++)
		cout << *ptr << " ";

	return 0;
}


<!--The vector elements are : 1 2 3 4 5 -->

/*--------------------------------------------------*/

// C++ code to demonstrate the working of
// advance()
#include<iostream>
#include<iterator> // for iterators
#include<vector> // for vectors
using namespace std;
int main()
{
	vector<int> ar = { 1, 2, 3, 4, 5 };

	// Declaring iterator to a vector
	vector<int>::iterator ptr = ar.begin();

	// Using advance() to increment iterator position
	// points to 4
	advance(ptr, 3);

	// Displaying iterator position
	cout << "The position of iterator after advancing is : ";
	cout << *ptr << " ";

	return 0;

}


<!--The position of iterator after advancing is : 4 -->


/*------------------------------------------------------------*/

// C++ code to demonstrate the working of
// next() and prev()
#include<iostream>
#include<iterator> // for iterators
#include<vector> // for vectors
using namespace std;
int main()
{
	vector<int> ar = { 1, 2, 3, 4, 5 };

	// Declaring iterators to a vector
	vector<int>::iterator ptr = ar.begin();
	vector<int>::iterator ftr = ar.end();


	// Using next() to return new iterator
	// points to 4
	auto it = next(ptr, 3);

	// Using prev() to return new iterator
	// points to 3
	auto it1 = prev(ftr, 3);

	// Displaying iterator position
	cout << "The position of new iterator using next() is : ";
	cout << *it << " ";
	cout << endl;

	// Displaying iterator position
	cout << "The position of new iterator using prev() is : ";
	cout << *it1 << " ";
	cout << endl;

	return 0;
}


<!--The position of new iterator using next() is : 4 -->
<!--The position of new iterator using prev()  is : 3 -->

/*---------------------------------------------------------*/

// C++ code to demonstrate the working of
// inserter()
#include<iostream>
#include<iterator> // for iterators
#include<vector> // for vectors
using namespace std;
int main()
{
	vector<int> ar = { 1, 2, 3, 4, 5 };
	vector<int> ar1 = {10, 20, 30};

	// Declaring iterator to a vector
	vector<int>::iterator ptr = ar.begin();

	// Using advance to set position
	advance(ptr, 3);

	// copying 1 vector elements in other using inserter()
	// inserts ar1 after 3rd position in ar
	copy(ar1.begin(), ar1.end(), inserter(ar,ptr));

	// Displaying new vector elements
	cout << "The new vector after inserting elements is : ";
	for (int &x : ar)
		cout << x << " ";

	return 0;
}



<!--The new vector after inserting elements is : 1 2 3 10 20 30 4 5 -->
```

[返回目录](#Menu)

[^sequence_containers]:
    implement data structures which can be accessed in a sequential manner.  
    序列容器：实现可以按顺序访问的数据结构。  
    [返回](#Sequence_Containers)

[^container_adaptors]:
    provide a different interface for sequential containers.  
    容器适配器：为顺序容器提供不同的接口。  
    [返回](#Container_Adaptors)

[^associative_containers]:
    implement sorted data structures that can be quickly searched (O(log n) complexity).  
    关联容器：实现可以快速搜索的排序数据结构（O（log n）复杂度）。  
    [返回](#Associative_Containers)

[^unordered_associative_containers]:
    implement unordered data structures that can be quickly searched.  
    无序关联容器：实现可以快速搜索的无序数据结构.  
    [返回](#Unordered_Associative_Containers)
