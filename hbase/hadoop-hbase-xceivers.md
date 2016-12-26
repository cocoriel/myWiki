
### Hadoop-HBase-xceivers
 

 1. [Cloudera Blog 원문](http://blog.cloudera.com/blog/2012/03/hbase-hadoop-xceivers/)
 2. **dfs.datanode.max.xcievers**
	- data connection을 위해 사용할 수 있는 서버측 thread & socket 개수
	- 해당 설정은 hadoop client에 직접적인 영향을 미칠 수 있음
 3. 문제점
	- region server & datanode에서 아래와 같은 메세지 확인할 수 있음
	- 아래와 같은 메제지가 나는 경우는 region server가 shutdown 될수 있음
	- 따라서 xceiver를 정확히 산출하는 공식은 없으나, 아래의 예시와 같이 xceivers의 개수를 늘려주는 것을 권장함.
	- 설정을 변경한 이후는 datanode 재기동
	- **이 설정은 무턱대고 64K 등으로 설정하면 절대 안됨!!!!**
		- 이유 1. 
			- thread 생성되면 thread의 stack이 필요하므로, 그에 따라 필요한 메모리를 사용하게 됨. 
			- 결국, **4096 xceivers를 설정해두면 대략 4GB의 메모리를 사용하게 된다는 말**
			- 예를 들어 설정값이 4096이라고 하면, 4096개의 dataxceiver thread를 모두 사용하는 경우 memstore나 block cachef를 위해 사용할 수 있는 메모리가 줄어들게 된다는 말이다. 이런 경우 재수가 없으면(?) region server 가 OOM으로 죽을 수도 있음...
		- 이유2. 
			- active된 thread가 많으면 CPU 사용이 그만큼 높아지게 됨.
			- 그리고 **thread 수가 많을 수록 context switching이 많이 일어나게 되므로** 이 또한 서버의 리소스를 잡아먹는 원인이 될 수 있다!!! 
	```sh
	#regionserver
	2008-11-11 19:55:52,451 INFO org.apache.hadoop.dfs.DFSClient: Exception in createBlockOutputStream java.io.IOException: Could not read from stream
	2008-11-11 19:55:52,451 INFO org.apache.hadoop.dfs.DFSClient: Abandoning block blk_-5467014108758633036_595771
	2008-11-11 19:55:58,455 WARN org.apache.hadoop.dfs.DFSClient: DataStreamer Exception: java.io.IOException: Unable to create new block.
	2008-11-11 19:55:58,455 WARN org.apache.hadoop.dfs.DFSClient: Error Recovery for block blk_-5467014108758633036_595771 bad datanode[0]
	2008-11-11 19:55:58,482 FATAL org.apache.hadoop.hbase.regionserver.Flusher: Replay of hlog required. Forcing server shutdown
	#datanode
	ERROR org.apache.hadoop.dfs.DataNode: DatanodeRegistration(10.10.10.53:50010,storageID=DS-1570581820-10.10.10.53-50010-1224117842339,infoPort=50075, ipcPort=50020):DataXceiver: java.io.IOException: xceiverCount 258 exceeds the limit of concurrent xcievers 256  
	# property 설정
			<property>    
			<name>dfs.datanode.max.xcievers</name>
		    <value>4096</value><!-- 기본 설정값 256인데 hbase 사용하는 경우 높이길 권장함 -->
		    </property>
	```
 4. Hadoop File System Details
    + HBase가 파일을 열 때 다음의  메소드를 호출하게 됨
> public DFSInputStream open(String src) throws IOException 
> public FSDataOutputStream create(Path f) throws IOException

	+ 리턴으로 파일의 read와 write에 사용될 server-side의 socket과 thread를 돌려줌
	+ 리턴된 socket과 thread는 namenode 및 datanode 사이에 어느 datanode의 block에 데이터를 저장하는지 등의 상호작용을 위해 사용됨.
	+ 반면 server 쪽에서는 DataXceiverServer class를 DataNode가 wrapping하고 있기 때문에 설정된 한계치를 넘는 경우 exception을 발생하게 된다.
	```sh
	# DataNode가 시작되면 다음과 같은 thread group 생성
	this.threadGroup = new ThreadGroup(“dataXceiverServer”);
  this.dataXceiverServer = new Daemon(threadGroup,
      new DataXceiverServer(ss, conf, this));
  this.threadGroup.setDaemon(true); // auto destroy when empty 
  # datanode는 다음과 같이 thread count를 체크하는 class를 가지고 있음
    /** Number of concurrent xceivers per node. */
  int getXceiverCount() {
    return threadGroup == null ? 0 : threadGroup.activeCount();
  }
	```
	+ 
	+ 

5.client측 영향
6.Hadoop deep dive
7.Back to HBase
8.What does that all mean?
9.Final advie & TL;DR



> Written with [StackEdit](https://stackedit.io/).