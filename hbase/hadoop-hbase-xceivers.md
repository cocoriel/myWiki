
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
			- 예를 들어 설정값이 4096이라고 하면, 4096개의 dataxceiver thread를 모두 사용하는 경우 memstore나 block cache를 위해 사용할 수 있는 메모리가 줄어들게 된다는 말이다. 이런 경우 재수가 없으면(?) region server 가 OOM으로 죽을 수도 있음...
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
	+ block을 읽거나 쓸때, client에서 DataXceiver instance의 thread group에 해당 thread를 등록한다. 이를 통해 server-side에서는 read&write에 사용되는 active thread를 추적가능하다. 따라서 이 thread들의 개수가 maximum값을 초과하게 되면 exception을 던지게 됨
>  if (curXceiverCount > dataXceiverServer.maxXceiverCount) {
>     throw new IOException(“xceiverCount ” + curXceiverCount + ” exceeds the limit of concurrent xcievers “  + dataXceiverServer.maxXceiverCount);   }

 5. Implications for Clients
	- Client는 어떤 방식으로 server-side의 read&write thread와 연관이 있는가?
> LOG.debug(“Number of active connections is: ” + datanode.getXceiverCount()); …
> LOG.debug(datanode.dnRegistration + “:Number of active connections is: ” + datanode.getXceiverCount());
	
	- 간단히 확인하기 위해 single datanode mode에서 datanode & regionserver log를 확인해 보면 된다.
	- Region server의 storefile metric을 확인해보면, HBase가 적어도 어느 정도의 파일을 handle하고 있는지 확인할 수 있다. 물론 여기에 추가로 write-ahead log도 있다. 
> 2012-03-05 13:01:35,309 DEBUG
> org.apache.hadoop.hdfs.server.datanode.DataNode: Number of active
> connections is: 1 2012-03-05 13:01:35,315 DEBUG
> org.apache.hadoop.hdfs.server.datanode.DataNode:
> DatanodeRegistration(127.0.0.1:50010,
> storageID=DS-1423642448-10.0.0.64-50010-1321352233772, infoPort=50075,
> ipcPort=50020):Number of active connections is: 2 12/03/05 13:01:35
> INFO regionserver.MemStoreFlusher: globalMemStoreLimit=396.7m,
> globalMemStoreLimitLowMark=347.1m, maxHeap=991.7m 12/03/05 13:01:39
> INFO http.HttpServer: Port returned by
> webServer.getConnectors()[0].getLocalPort() before open() is -1.
> Opening the listener on 60030 2012-03-05 13:01:40,003 DEBUG
> org.apache.hadoop.hdfs.server.datanode.DataNode: Number of active
> connections is: 1 12/03/05 13:01:40 INFO regionserver.HRegionServer:
> Received request to open region: -ROOT-,,0.70236052 2012-03-05
> 13:01:40,882 DEBUG org.apache.hadoop.hdfs.server.datanode.DataNode:
> Number of active connections is: 3 2012-03-05 13:01:40,884 DEBUG
> org.apache.hadoop.hdfs.server.datanode.DataNode:
> DatanodeRegistration(127.0.0.1:50010,
> storageID=DS-1423642448-10.0.0.64-50010-1321352233772, infoPort=50075,
> ipcPort=50020):Number of active connections is: 4 2012-03-05
> 13:01:40,888 DEBUG org.apache.hadoop.hdfs.server.datanode.DataNode:
> Number of active connections is: 3 … 12/03/05 13:01:40 INFO
> regionserver.HRegion: Onlined -ROOT-,,0.70236052; next
> sequenceid=63083 2012-03-05 13:01:40,982 DEBUG
> org.apache.hadoop.hdfs.server.datanode.DataNode: Number of active
> connections is: 3 2012-03-05 13:01:40,983 DEBUG
> org.apache.hadoop.hdfs.server.datanode.DataNode:
> DatanodeRegistration(127.0.0.1:50010,
> storageID=DS-1423642448-10.0.0.64-50010-1321352233772, infoPort=50075,
> ipcPort=50020):Number of active connections is: 4 … 12/03/05 13:01:41
> INFO regionserver.HRegionServer: Received request to open region:
> .META.,,1.1028785192 2012-03-05 13:01:41,026 DEBUG
> org.apache.hadoop.hdfs.server.datanode.DataNode: Number of active
> connections is: 3 2012-03-05 13:01:41,027 DEBUG
> org.apache.hadoop.hdfs.server.datanode.DataNode:
> DatanodeRegistration(127.0.0.1:50010,
> storageID=DS-1423642448-10.0.0.64-50010-1321352233772, infoPort=50075,
> ipcPort=50020):Number of active connections is: 4 … 12/03/05 13:01:41
> INFO regionserver.HRegion: Onlined .META.,,1.1028785192; next
> sequenceid=63082 2012-03-05 13:01:41,109 DEBUG
> org.apache.hadoop.hdfs.server.datanode.DataNode: Number of active
> connections is: 3 2012-03-05 13:01:41,114 DEBUG
> org.apache.hadoop.hdfs.server.datanode.DataNode: Number of active
> connections is: 4 2012-03-05 13:01:41,117 DEBUG
> org.apache.hadoop.hdfs.server.datanode.DataNode: Number of active
> connections is: 5 12/03/05 13:01:41 INFO regionserver.HRegionServer:
> Received request to open 16 region(s) 12/03/05 13:01:41 INFO
> regionserver.HRegionServer: Received request to open region:
> usertable,,1330944810191.62a312d67981c86c42b6bc02e6ec7e3f. 12/03/05
> 13:01:41 INFO regionserver.HRegionServer: Received request to open
> region:
> usertable,user1120311784,1330944810191.90d287473fe223f0ddc137020efda25d.
> …
> 2012-03-05 13:01:41,246 DEBUG
> org.apache.hadoop.hdfs.server.datanode.DataNode: Number of active
> connections is: 6 2012-03-05 13:01:41,248 DEBUG
> org.apache.hadoop.hdfs.server.datanode.DataNode: Number of active
> connections is: 7 … 2012-03-05 13:01:41,257 DEBUG
> org.apache.hadoop.hdfs.server.datanode.DataNode:
> DatanodeRegistration(127.0.0.1:50010,
> storageID=DS-1423642448-10.0.0.64-50010-1321352233772, infoPort=50075,
> ipcPort=50020):Number of active connections is: 10 2012-03-05
> 13:01:41,257 DEBUG org.apache.hadoop.hdfs.server.datanode.DataNode:
> DatanodeRegistration(127.0.0.1:50010,
> storageID=DS-1423642448-10.0.0.64-50010-1321352233772, infoPort=50075,
> ipcPort=50020):Number of active connections is: 9 … 12/03/05 13:01:41
> INFO regionserver.HRegion: Onlined
> usertable,user1120311784,1330944810191.90d287473fe223f0ddc137020efda25d.;
> next sequenceid=62917 12/03/05 13:01:41 INFO regionserver.HRegion:
> Onlined usertable,,1330944810191.62a312d67981c86c42b6bc02e6ec7e3f.;
> next sequenceid=62916 … 12/03/05 13:01:41 INFO regionserver.HRegion:
> Onlined
> usertable,user1361265841,1330944811370.80663fcf291e3ce00080599964f406ba.;
> next sequenceid=62919 2012-03-05 13:01:41,474 DEBUG
> org.apache.hadoop.hdfs.server.datanode.DataNode: Number of active
> connections is: 6 2012-03-05 13:01:41,491 DEBUG
> org.apache.hadoop.hdfs.server.datanode.DataNode: Number of active
> connections is: 7 2012-03-05 13:01:41,495 DEBUG
> org.apache.hadoop.hdfs.server.datanode.DataNode:
> DatanodeRegistration(127.0.0.1:50010,
> storageID=DS-1423642448-10.0.0.64-50010-1321352233772, infoPort=50075,
> ipcPort=50020):Number of active connections is: 8 2012-03-05
> 13:01:41,508 DEBUG org.apache.hadoop.hdfs.server.datanode.DataNode:
> Number of active connections is: 7 … 12/03/05 13:01:41 INFO
> regionserver.HRegion: Onlined
> usertable,user1964968041,1330944848231.dd89596e9129e1caa7e07f8a491c9734.;
> next sequenceid=62920 2012-03-05 13:01:41,618 DEBUG
> org.apache.hadoop.hdfs.server.datanode.DataNode: Number of active
> connections is: 6 2012-03-05 13:01:41,621 DEBUG
> org.apache.hadoop.hdfs.server.datanode.DataNode:
> DatanodeRegistration(127.0.0.1:50010,
> storageID=DS-1423642448-10.0.0.64-50010-1321352233772, infoPort=50075,
> ipcPort=50020):Number of active connections is: 7 … 2012-03-05
> 13:01:41,829 DEBUG org.apache.hadoop.hdfs.server.datanode.DataNode:
> DatanodeRegistration(127.0.0.1:50010,
> storageID=DS-1423642448-10.0.0.64-50010-1321352233772, infoPort=50075,
> ipcPort=50020):Number of active connections is: 7 12/03/05 13:01:41
> INFO regionserver.HRegion: Onlined
> usertable,user515290649,1330944849739.d23924dc9e9d5891f332c337977af83d.;
> next sequenceid=62926 2012-03-05 13:01:41,832 DEBUG
> org.apache.hadoop.hdfs.server.datanode.DataNode: Number of active
> connections is: 6 2012-03-05 13:01:41,838 DEBUG
> org.apache.hadoop.hdfs.server.datanode.DataNode:
> DatanodeRegistration(127.0.0.1:50010,
> storageID=DS-1423642448-10.0.0.64-50010-1321352233772, infoPort=50075,
> ipcPort=50020):Number of active connections is: 7 12/03/05 13:01:41
> INFO regionserver.HRegion: Onlined
> usertable,user757669512,1330944850808.cd0d6f16d8ae9cf0c9277f5d6c6c6b9f.;
> next sequenceid=62929 … 2012-03-05 14:01:39,711 DEBUG
> org.apache.hadoop.hdfs.server.datanode.DataNode: Number of active
> connections is: 4 2012-03-05 22:48:41,945 DEBUG
> org.apache.hadoop.hdfs.server.datanode.DataNode:
> DatanodeRegistration(127.0.0.1:50010,
> storageID=DS-1423642448-10.0.0.64-50010-1321352233772, infoPort=50075,
> ipcPort=50020):Number of active connections is: 4 12/03/05 22:48:41
> INFO regionserver.HRegion: Onlined
> usertable,user757669512,1330944850808.cd0d6f16d8ae9cf0c9277f5d6c6c6b9f.;
> next sequenceid=62929 2012-03-05 22:48:41,963 DEBUG
> org.apache.hadoop.hdfs.server.datanode.DataNode:
> DatanodeRegistration(127.0.0.1:50010,
> storageID=DS-1423642448-10.0.0.64-50010-1321352233772, infoPort=50075,
> ipcPort=50020):Number of active connections is: 4

	- 위의 datanode 로그에서 확인할 수 있듯이 active connection의 숫자는 22(storefile의 개수)를 넘지 않는다.

 6. Hadoop Deep Dive
	- DFSInputStream은 DFSClient.BlockReader라는 클래스를 instance로 가지고 있다. 이 클래스는 datanode로의 connection을 열고, stream이 block을 읽는다. block을 읽고 난 이후에는 connection이 close되게 됨.
	- DFSOutputStream은 DataStreamer라는 helper 클래스를 가지고 있고, 이를 통해 server로의 connection을 tracking하게 된다. 
	- block을 읽은 때나 쓸때 모두 그에 해당하는 thread 와 socket이 필요하고, client가 수행하고 있는 작업에 따라서 connection의 수가 바뀌는 것을 관찰할 수 있다. 
	- 리전에서 connection의 수가 22까지 올라가지 않는 것은, region이 열려있는 동안에는 HFile의 info block만 읽으면 되기 때문이다.  결국 이로 인해 server-side의 resource를 재빨리 사용하고 반환할 수 있다. 
	- datanod의 JStack dump를 통해 더욱 자세한 정보를 알 수 있다. 
> "DataXceiver for client /127.0.0.1:64281 [sending block blk_5532741233443227208_4201]” daemon prio=5 tid=7fb96481d000 nid=0x1178b4000 runnable [1178b3000]    
> java.lang.Thread.State: RUNNABLE    
> ... 
> "DataXceiver for client /127.0.0.1:64172 [receiving block blk_-2005512129579433420_4199  client=DFSClient_hb_rs_10.0.0.29,60020,1330984111693_1330984118810]” daemon prio=5 tid=7fb966109000 nid=0x1169cb000 runnable [1169ca000]   
> java.lang.Thread.State: RUNNABLE    
> …

	- thread 사용
		- DataXceiverServer daemon이 thread 1개 점유하고 있고, 이거는 위 dump의 2개 connection과도 연관이 있음. 결국 해당 daemon이 thread 3개 사용(dataXceiver for Client /172.0.01:64281 & dataXceiver for Client /172.0.01:64172) 
		- 로그에서 thread 개수가 4로 보이는 것은 counter가 곧 소멸될 active thread의 개수를 세기 때문임. 
		- 내부적으로 helper class인 PacketResponder 도 추가적으로 thread 하나를 점유함.
> “PacketResponder 0 for Block blk_-2005512129579433420_4199” daemon
> prio=5 tid=7fb96384d000 nid=0x116ace000 in Object.wait() [116acd000]  
> java.lang.Thread.State: TIMED_WAITING (on object monitor)
>      at java.lang.Object.wait(Native Method)
>      at org.apache.hadoop.hdfs.server.datanode.BlockReceiver\$PacketResponder
>        .lastDataNodeRun(BlockReceiver.java:779)
>      – locked (a org.apache.hadoop.hdfs.server.datanode.BlockReceiver\$PacketResponder)
>      at org.apache.hadoop.hdfs.server.datanode.BlockReceiver\$PacketResponder.run(BlockReceiver.java:870)
>      at java.lang.Thread.run(Thread.java:680)

		- 위의 로그에서 PacketResponder의 경우 상태가 TIME_WAIT이므로 thread counter에서는 위의 thread를 active thread로 취급하지 않음.
		- 또 한가지 생각해 보아야 할건, client와 server 사이에 분리된 connection이나 socket이 필요하지 않다는 것이다.  
		- **hadoop fsck /hbase -openforwrite** : 해당 옵션을 통해 현재 쓰기를 위해 열려 있는 파일을 확인할 수 있다. 이를 **hadoop fsck /hbase -files -blocks** report와 비교해 보면 block에 해당하는 file을 알수 있고, thread 로그와의 비교를 통해서 해당 files에 access하고 있는 thread도 알 수 있다. 

 7. What does that all mean?
	- 그래서 결국 xcievers는 몇개나 필요한걸까? 다음의 계산식은 오직 client로 오직 HBase만 사용하는 것을 가정한 경우고, mapreduce나 flume 등등을 사용한다면 xcievers의 값은 여기서 산출하는 값보다 커야 한다. 
	- 수식 
	$$
	\#ofxcievers=\frac{(#ofActiveWriters*2)+(#ofActiveReaders)}{#ofDataNodes}
	$$
	- 이 수식에서 write operation을 위해서는 2개, read operation을 위해서 1개의 thread가 필요하다고 가정
	-  홍홍
	

> Written with [StackEdit](https://stackedit.io/).