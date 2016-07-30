## 最基本的异步 url request 模型

由于最近接触异步比较多， 所以想更深入了解一下。  

总结起来， 异步 request 的大致组成部分是：  
1. 某种 io_event_drive (epoll, select 等)  
2. 一个非阻塞的 sock， 通过 io_event_drive 注册侦听事件和 callback  
3. 通过 coroutine 的 yield 语句返回控制权， 和传递数据+触发进一步操作  
4. 一个 event_loop 时刻侦听 sock 事件， 并通过 callback 触发响应操作  
5. Future 是预期事件和最后结果的桥梁  
 
    5.1 预期 io_event 事件发生, 触发 event_callback, 控制权转移到 Future Object
    5.2 触发 Future 进行 result 解析， 获得数据
    5.3 触发 Future callback, 传送 Future 的 result 数据给 request 事务， 控制权转移到 request  
    5.4 request 处理获得的数据， 再创建新的 Future object, 注册下一个 io 事件， yield， 控制权转移到 io_event_loop  
    5.5 等待， 返回第一步  
