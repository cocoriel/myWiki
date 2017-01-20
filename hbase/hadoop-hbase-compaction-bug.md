
### HBASE-7465

 1. 참고사이트
	- [developer blog](http://gbif.blogspot.kr/2012/07/optimizing-writes-in-hbase.html)
	- [hbase 설정 최적화](http://engineering.vcnc.co.kr/2013/04/hbase-configuration/) 
	- [About HBase flushes and compactions](http://hadoop-hbase.blogspot.kr/2014/07/about-hbase-flushes-and-compactions.html)
	- [HBASE-7465](https://issues.apache.org/jira/browse/HBASE-7465)

 2. HBase compaction 버그(0.94.16)
	- 최초 발생 시에는 반응속도가 조금씩 느려지기 시작함
	- 반응 속도가 느려지는 것은 네임노드 web UI에서 last contact가 늦어지는 것으로 확인이 되었고, 실제 HBase 배치나 조회 작업 또한 반응속도가 떨어지기 시작함
	- 네임노드의 block수 모니터링 수치를 비교한 결과 bug가 발현된 시점부터 block수가 평소보다 훨씬 빠른 속도로 증가한 것을 확인함
	- hbase log에서 flush 횟수 및 compaction 횟수를 찾아보면 flush 횟수는 비슷한 수준이지만, compaction 횟수가 100배 이상 증가함. 
	- compaction 로그에서 다음과 같이 아주 작은 사이즈의 HFile 하나에 대해서만 compaction이 반복되고 있는 것을 확인
		> INFO org.apache.hadoop.hbase.regionserver.Store: Starting compaction of 1 file(s) in cf of 
		> usertable,,1484111814408.1e6212fd6e09d1f85a795d58c5d8120b. into
		> tmpdir=hdfs://hostname:8020/hbase/usertable/1e6212fd6e09d1f85a795d58c5d8120b/.tmp,seqid=3871,
		> totalSize=552.0
	
	-  해당 HFile은 TTL 만료로 인해서 store file에 대해 데이터가 하나도 남지 않음으로 인해 생긴 것으로 파악됨
	- 결국 TTL이 경과하면서 생긴 빈 HFile에 대해 compaction을 무한 반복하고 있음을 확인.

 3. 버그로 인해 생긴 현상들
	- total block수 증가 : 네임노드 모니터링을 통해 file & directory / blocks / total을 살펴본 결과, file & directory수에는 별 변화가 없지만 block의 수가 증가. 이로 인해 네임노드의 heap이 모자라서 namenode 다운됨. 
	- pending deletion blocks :  네임노드 jmx를 통해서 pendingDeletionBlocks을 확인할 수 있는데, 네임노드가 invalide block을 계산하여 데이터노드를 통해 이를 삭제하는 속도보다 삭제해야 할 파일 수의 증가가 훨씬 빨라서 pendingDeletionBlock의 수가 지속적으로 증가함
	- HDFS 재기동 지연 : 버그 패치 이후에 HDFS/HBase를 재기동 하는데 있어서 HDFS 기동 시 safe mode를 빠져나왔음에도 불구하고 데이터노드의 반응이 느려 HBase를 기동했을 시 HBase meta등의 파일을 제대로 읽어들이지 못함

 4. 기타
	 - 네임노드의 stateChange 로그를 통해 정상적인 block에 비해 비정상적인 block이 8배 정도 많이 생긴 것을 확인함
	 - pendingDeletionBlocks의 수가 많은 경우 HDFS의 재기동 시 정상 기동 시간이 많이 걸리므로 HDFS를 재기동 하기 전에 반드시 해당 요소를 모니터링 해보아야 함!!

> Written with [StackEdit](https://stackedit.io/).