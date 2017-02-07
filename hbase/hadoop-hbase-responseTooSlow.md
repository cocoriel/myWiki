### HBase scan시 responseTooSlow 문제

1. 참고사이트
	- [stackoverflow1 - gc문제](http://stackoverflow.com/questions/25599434/hbase-have-no-response-to-client-for-minutes)
	- [stackoverflow2 - scanner timeout](http://stackoverflow.com/questions/41787738/regionserver-hregionserver-scanner-15209-lease-expired-on-region-webpage)
	- [responseTooSlow](http://grokbase.com/t/hbase/user/155x6mtejr/response-too-slow-in-regionserver-logs)
	- [hbase slow query log](http://hbase.apache.org/book.html#ops.monitoring)
	- [비슷한 현상](http://git.net/ml/java-hadoop-hbase-user/2010-11/msg00142.html)
	- [region server going down due to gc pauses](https://community.hortonworks.com/articles/73953/region-server-going-down-due-to-gc-pauses.html)
	- [Java GC](http://www.reins.altervista.org/java/gc1.4.2_faq.html)

2. 현상
	- 배치 실행시에 scan을 통해 작업을 하는데 이 작업속도가 현저히 느려짐
	- hbase region 로그를 살펴보니 scan 호출 시에 **responseTooSlow** 로그가 많이 발견됨
	- query 실행이 느린 경우 발견되는 로그
	- query 실행이 느린 case는 여러가지가 있으나, gc 시간이 길어서 그런것이 아닐까 의심됨..
	- hbase의 gc 로그를 살펴보니까(클러스터 설정 때문에 gc 실행 시간이 없으나...) **concurrent mode failure** 도 가끔 발생하고, 또한 **CMS-concurrent-sweep** 시간이 길때는 10초 이상 걸리기도 함..
	- 배치 도는 시간동안 gc를 모니터링 해 보아야 할 듯함.. 

3. 모니터링
	- GC 로그 보니까 Permgen 영영에 대한 concurrent mode failure 가 생가보다 자주 일어나는데, 이 영역이 좀 모자라서 그러는거 아닌가 싶음...
	- concurrent mode failure 일어나면 대략 10초 내외로 걸림..
		- 그런데 생각해보면 10초면 zookeeper timeout이 나거나 하는 정도의 GC 시간은 아닌것 같은데..
	- 그리고 minor GC가 아주 자주 일어남
		- hbase니까 flush 된 부분에 대해 GC가 일어나는 것 같은데 이제 너무 잦은건가...
		- minor GC에 대한거는 flush 때문인지 원래 GC가 나야하는 부분에 대해 나는건지 구분이 안가서 판단이 힘드네..
		- jstat 상(3초에 한번)으로 보면 minor GC는 3초동안 4번 정도는 일어나는 것 같음..



> Written with [StackEdit](https://stackedit.io/).