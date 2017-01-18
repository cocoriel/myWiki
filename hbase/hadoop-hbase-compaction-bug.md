
### HBASE-7465

1. 참고사이트
	- [developer blog](http://gbif.blogspot.kr/2012/07/optimizing-writes-in-hbase.html)
	- [hbase 설정 최적화](http://engineering.vcnc.co.kr/2013/04/hbase-configuration/) 
	- [About HBase flushes and compactions](http://hadoop-hbase.blogspot.kr/2014/07/about-hbase-flushes-and-compactions.html)
	- [HBASE-7465](https://issues.apache.org/jira/browse/HBASE-7465)
2. HBase compaction 버그
	- 최초 발생 시에는 반응속도가 조금씩 느려지기 시작함
	- 반응 속도가 느려지는 것은 네임노드 web UI에서 last contact가 늦어지는 것으로 확인이 되었고, 실제 HBase 배치나 조회 작업 또한 반응속도가 떨어지기 시작함
	- 네임노드의 block수 모니터링 수치를 비교한 결과 bug가 발현된 시점부터 block수가 평소보다 훨씬 빠른 속도로 증가한 것을 확인함
	- 


> Written with [StackEdit](https://stackedit.io/).