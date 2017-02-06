### HBase scan시 responseTooSlow 문제

1. 참고사이트
	- [stackoverflow1 - gc문제](http://stackoverflow.com/questions/25599434/hbase-have-no-response-to-client-for-minutes)
	- [stackoverflow2 - scanner timeout](http://stackoverflow.com/questions/41787738/regionserver-hregionserver-scanner-15209-lease-expired-on-region-webpage)
	- [responseTooSlow](http://grokbase.com/t/hbase/user/155x6mtejr/response-too-slow-in-regionserver-logs)
	- [hbase slow query log](http://hbase.apache.org/book.html#ops.monitoring)

2. 현상
	- 배치 실행시에 scan을 통해 작업을 하는데 이 작업속도가 현저히 느려짐
	- hbase region 로그를 살펴보니 scan 호출 시에 **responseTooSlow** 로그가 많이 발견됨
	- query 실행이 느린 경우 발견되는 로그
	- query 실행이 느린 case는 여러가지가 있으나, gc 시간이 길어서 그런것이 아닐까 의심됨..
	- hbase의 gc 로그를 살펴보니까(클러스터 설정 때문에 gc 실행 시간이 없으나...) **concurrent mode failure** 도 가끔 발생하고, 또한 **CMS-concurrent-sweep** 시간이 길때는 10초 이상 걸리기도 함..
	- 배치 도는 시간동안 gc를 모니터링 해 보아야 할 듯함.. 


> Written with [StackEdit](https://stackedit.io/).