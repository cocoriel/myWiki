
### Hadoop-HBase-xceivers
1. [Cloudera Blog](http://blog.cloudera.com/blog/2012/03/hbase-hadoop-xceivers/)
2. **dfs.datanode.max.xcievers**
	- data connection을 위해 사용할 수 있는 서버측 thread & socket 개수
	- 해당 설정은 hadoop client에 직접적인 영향을 미칠 수 있음
3. 문제점
	- region server & datanode에서 아래와 같은 메세지 확인할 수 있음
```sh
#regionserver
2008-11-11 19:55:52,451 INFO org.apache.hadoop.dfs.DFSClient: Exception in createBlockOutputStream java.io.IOException: Could not read from stream
2008-11-11 19:55:52,451 INFO org.apache.hadoop.dfs.DFSClient: Abandoning block blk_-5467014108758633036_595771
2008-11-11 19:55:58,455 WARN org.apache.hadoop.dfs.DFSClient: DataStreamer Exception: java.io.IOException: Unable to create new block.
2008-11-11 19:55:58,455 WARN org.apache.hadoop.dfs.DFSClient: Error Recovery for block blk_-5467014108758633036_595771 bad datanode[0]
2008-11-11 19:55:58,482 FATAL org.apache.hadoop.hbase.regionserver.Flusher: Replay of hlog required. Forcing server shutdown
```
```sh
#datanode
ERROR org.apache.hadoop.dfs.DataNode: DatanodeRegistration(10.10.10.53:50010,storageID=DS-1570581820-10.10.10.53-50010-1224117842339,infoPort=50075, ipcPort=50020):DataXceiver: java.io.IOException: xceiverCount 258 exceeds the limit of concurrent xcievers 256  
```
```sh
<property>    
	<name>dfs.datanode.max.xcievers</name>
    <value>4096</value><!-- 기본 설정값 256인데 hbase 사용하는 경우 높이길 권장함 -->
</property>
```

4.  

> Written with [StackEdit](https://stackedit.io/).