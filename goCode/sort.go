package main

import (
    "fmt"
    "sync"
)
var wg sync.WaitGroup
// func main() {
//     // 列举出1-120000之间的素数  除了1和它自身外，不能被其他自然数整除的数叫做质数 倍数也不是
//     start := time.Now().Unix()
//     for i:=2;i<200000;i++{
//         var flag=true
//         for n:=2;n<i;n++{
//             if i%n==0{
//                 flag=false
//                 break
//             }
//         }
//         if flag{
//             // fmt.Println(i,"是素数")
//         }
//     }
//     end := time.Now().Unix()
//     fmt.Println(end-start)
// }

// 利用协程的多核并发执行任务，看下时间效率 启动4个协程
// func main() {
//     start := time.Now().Unix()
//     for i := 1; i <= 4; i++ { //启动了4个协程!
//         wg.Add(1) //如果有多个协程 就设置多个 wg.Add()
//         go B(i)
//     }
//     wg.Wait()
//     end := time.Now().Unix()
//     fmt.Println("是质数")
//     fmt.Println(111,end-start)
// }

func B(num int){
    // 4*30000==120000 循环这么多的数，然后分4个协程统计质数!
    for i:=(num-1)*50000+1;i<num*50000;i++{
        if i>1{
            var flag=true
            for n:=2;n<i;n++{
                if i%n==0{
                    flag=false
                    break
                }
            }
            if flag{
            // fmt.Println(i,"是素数")
            }
        }
    }
    wg.Done()
}

// channle管道
func main() {
    ch := make(chan int,10)
    for i:=0;i<10;i++{
        ch <- i
    }
    // close(ch)
    // 如果是使用 for range 上一个循环就得关闭管道ch
    // for v := range ch{
    //     fmt.Println(v)
    // }
    // 如果是通过 for循环迭代，不会出现死锁 range方法就会出现死锁
    for j:=0;j<10;j++{
        fmt.Println(<-ch)
    }
    li := [9]int{54, 26, 93, 55, 77, 31, 44, 55, 20}
    buddle_sort(li)
    select_sort(li)
    insert_sort(li)
    shell_sort(li)
    quick_sort(li, 0, len(li)-1)
}

func buddle_sort(alist [9]int){
    // 冒泡排序
    n:=len(alist)
    for j:=0;j<n-1;j++{
        flag:=false
        for i:=0;i<n-j-1;i++{
            if alist[i]>alist[i+1]{
                alist[i],alist[i+1]=alist[i+1],alist[i]
                flag=true
            }
        }
        if flag == false{
            break
        }
    }
    fmt.Println("【冒泡排序】:",alist)
}

func select_sort(alist [9]int){
    // 选择排序
    n:=len(alist)
    for i:=0;i<n-1;i++{
        minIndex:=i
        for j:=1+i;j<n;j++{
            if alist[j]<alist[minIndex]{
                minIndex=j
            }
        }
        if minIndex != i{
            alist[minIndex],alist[i] = alist[i],alist[minIndex]
        }
    }
    fmt.Println("【选择排序】:",alist)
}
func insert_sort(alist [9]int){
    n:=len(alist)
    for i:=1;i<n;i++{
        // 这里注意，是朝反向递减数字的!
        for j:=i;j>0;j--{
            if alist[j]<alist[j-1]{
                alist[j],alist[j-1] = alist[j-1],alist[j]
            }else{
                break
            }
        }
    }
    fmt.Println("【插入排序】:",alist)
}

func shell_sort(alist [9]int){
    n:=len(alist)
    gap:=n/2 //间隙 浮点数
    for gap>=1{
        for i:=gap;i<n;i++{
            for i-gap>=0{
                if alist[i]<alist[i-gap]{
                    alist[i],alist[i-gap]=alist[i-gap],alist[i]
                    i=i-gap
                }else{
                    break
                }
            }
        }
        gap=gap/2
    }
    fmt.Println("【希尔排序】:",alist)
}

func quick_sort(alist [9]int,start int,end int){
    if start>=end{
        return
    }
    left:=start //左边起始值
    right := end
    base_value := alist[left] //# 设定的基准值 列表的起始值
    for left<right{
        for left<right && alist[right]>=base_value{
            right-=1
        }  
        alist[left]=alist[right]   
        for left<right && alist[left]<base_value{
            left+=1
        }
        alist[right]=alist[left]
    }
    alist[left]=base_value

    quick_sort(alist,start,left-1)
    quick_sort(alist,left+1,end)
    fmt.Println("【快速排序】:",alist)
}
