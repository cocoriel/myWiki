
### HBase Client Timeout

1. 사이트
	- [HBase Client Timeout](http://hadoop-hbase.blogspot.kr/2012/09/hbase-client-timeouts.html)
	- [Long Running HBase Clients](http://hadoop-hbase.blogspot.kr/2011/12/long-running-hbase-clients.html)
	- [zookeeper session expired](https://community.hortonworks.com/questions/11779/hbase-master-shutting-down-with-zookeeper-delete-f.html)
2. 내용
	1. 현상
		- thrift서버에서 HBase scan시 scan 응답이 느리자 zookeeper와의 세션이 만료
		- 세션이 만료되었지만 client에서는 계속해서 retry(default 설정이 10인듯)하고, 이걸 zookeeper 각각(recoverableZookeeper)에 수행함 : .META.와 -ROOT- 테이블을 계속 호출함
		- 그런데 이 retry를 각 scan을 호출한 thread별로 반복
		- retry를 할때마다 중간 sleeping 하는 시간이 늘어남
		- 따라서 retry가 끝날때까지 엄청 오랜 시간이 걸림...
		- HBase 로그에도 client가 이미 expired된 scan을 호출한다는 로그가 발생함..
	2. 해결방법(아마도..)
		- GC 확인 후 메모리 증설 또는 클러스터 증설을 통한 부하 줄이기..
		- 위의 블로그 내용 살펴보면, 결국은 client에서 HBase와 zookeeper의 timeout 상황이 겹치면서 작업 실패 메세지를 빠른 시간안에 받을 수 없다는 내용. 
		- 이를 위해서 HBase의 patch 적용해야 할 수도(현재 버전에 적용된건지 살펴보기!!)
			- [HBASE-5682](https://issues.apache.org/jira/browse/HBASE-5682)
			- [HBASE-4805](https://issues.apache.org/jira/browse/HBASE-4805)
			- [HBASE-6326](https://issues.apache.org/jira/browse/HBASE-6326)
			- [HBASE-6323](https://issues.apache.org/jira/browse/HBASE-6326)
	3. 기타
		![zookeeper session expired](https://community.hortonworks.com/storage/attachments/1585-zk-state-dia.jpg)

> Written with [StackEdit](https://stackedit.io/).