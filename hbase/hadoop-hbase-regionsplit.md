
###hbase split

1. 참고 사이트
	- [apache-hbase-region-splitting-and-merging](https://ko.hortonworks.com/blog/apache-hbase-region-splitting-and-merging/)
	- [Capacity Planning and Region Sizing](http://archive-primary.cloudera.com/cdh5/cdh/5/hbase-0.98.1-cdh5.1.5/book/ops.capacity.html)

2. split policy
	- 0.94.16의 경우는 default로 constant size region split policy를 따름
	- split 할때 다음과 같은 식에 의해 split size가 결정됨
		- min(R^2*hbase.hregion.memstore.flush.size, hbase.hregion.max.filesize)
		- R은 같은 region server에 존재하는 동일한 테이블의 region 개수
		- FQA의 경우는, hbase.hregion.memstore.flush.size=128M/hbase.hregion.max.filesize=100G로 되어 있음.
		- - region이 자동으로 split이 된다면, 128M/512MB/1152MB/2GB/3.2GB/4.6GB/6.2GB/ 8GB/10.125GB/12.5GB순으로 split이 됨.
		- maxfilesize가 10G라면 region 개수가 9개를 넘으면  항상 10G로 split이 됨.
		- 근데 이상하게 split하믄 6.2G + 알파로 되는 것 같단 말이지..


> Written with [StackEdit](https://stackedit.io/).