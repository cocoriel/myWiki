
### Top 10 Performance Tuning Tips for Amazon Athena

1. 사이트
	- [Top 10 Performance Tuning Tips for Amazon Athena](https://aws.amazon.com/ko/blogs/big-data/top-10-performance-tuning-tips-for-amazon-athena/)
2. 내용
	- Athena는 SQL 쿼리를 Presto를 통해 실행하므로, 몇몇 tip들은 presto를 사용한다면 공통적으로 적용해 볼 수 있음
	1. partition data : 
		- athena는 hive partitioning을 지원함. 쿼리 시 where절에 partition 포함시킴
		- partition을 너무 과도하게 하면 partition metadata를 처리하는데 overhead가 있으니, partition을 과도하게 나누지 말것
		- 그리고 partition별로 데이터량이 비슷해야 하고, skew가 심하게 되어있으면 partition의 이점이 없음
	2. 압축(compress) 하거나, 파일 나누기(split files)
	3. 파일 크기 최적화
		- 128MB 보다 파일 사이즈가 작으면 성능이 많이 떨어짐
	4. columnar data store 
		- parquet/ORC 등..
	5. order by
		- order by 가 일어나면 presto는 모든 데이터를 single worker에 모아두고 sort를 진행함
		- 따라서 order by가 필요한 경우 limit를 주는 것이 좋음 
	6. joins
		- join하는 경우 Big(left table) * Small(right table) 이 좋음
		- join 시 presto는 right table을 각 worker 노드에 분배한다는 left table을 streaming하여 join 하기 때문
	7. group by 
		- group by 할때 cardinality가 높은 순서대로 group by를 하는 것이 좋음
	8. like
		- string 데이터의 경우 like 문을 쓰는것보다 regexp_like를 쓰는 것이 훨씬 성능이 좋음
	9. approximate function
		- count(distinct column)을 사용하는 경우에 정확한 count가 필요하지 않다면 approx_distinct를 쓰는 것이 훨씬 성능이 좋음
	10. 필요한 column만 포함
		


> Written with [StackEdit](https://stackedit.io/).