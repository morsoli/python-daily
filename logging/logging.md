### Logging 组件
* logging 日志记录系统由四种交互类型的对象组成。 每个想要记录的模块或应用程序都使用 Logger 实例将信息添加到日志中。 
    - 调用 logger 会创建一个 LogRecord ，它会将信息保存在内存中，直到它被处理为止。 
    ```python
    Logger.getLogger() # 默认root
    Logger.setLevel()
    Logger.addHandler() and Logger.removeHandler() 
    Logger.addFilter() and Logger.removeFilter()
    Logger.debug(), Logger.info(), Logger.warning(), Logger.error(), and Logger.critical()
    ```
    - Filter 提供了更细粒度的功能，用于确定要输出的日志记录。
    - Logger 可能有一些 `Handler` 对象被配置用来接收和处理日志记录。
    ```python
    StreamHandler instances send messages to streams (file-like objects).
    FileHandler instances send messages to disk files.
    TimedRotatingFileHandler instances send messages to disk files, rotating the log file at certain timed intervals.
    SocketHandler instances send messages to TCP/IP sockets. Since 3.4, Unix domain sockets are also supported.
    DatagramHandler instances send messages to UDP sockets. Since 3.4, Unix domain sockets are also supported.
    SMTPHandler instances send messages to a designated email address.

    setLevel() 
    setFormatter() 
    addFilter() and removeFilter()
    ```
    - Handler 使用 Formatter 将日志记录转换为输出消息。
    ```python
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ```
### Configuring Logging
1. Creating loggers, handlers, and formatters explicitly using Python code that calls the configuration methods listed above.

2. Creating a logging config file and reading it using the fileConfig() function.

3. Creating a dictionary of configuration information and passing it to the dictConfig() function.