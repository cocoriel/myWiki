
### Wallaroo

1. 사이트
	- [Wallaroo 소개](http://engineering.sendence.com/2017/03/hello-wallaroo/)
2. Wallaroo
	1. 무엇
		- event-by-event distributed data processing application을 위해 만들어진 framework
		- high-throughput과 low-latency를 handling 하기 위해 design 됨
		- big data 영역에서는 streaming data의 영역에 들어가는 tool(Storm/Heron/Samza)이라 보면 됨
	2. 목적
		- streaming data를 처리하는데 있어서 per-worker throughput을 향상
		- dramatically low-latencies
		- 보다 간단한 형식의 state management
		- operation을 보다 쉽게
	3. POC - Market Spread
		- 실험결과 단일 머신(AWS m4 level, 16cores)에서 stream/sec 당 1.5 million messaged 처리 
		- letency는 50%는 66 microseconds/99.9%는 0.5ms 안에 처리함 

> Written with [StackEdit](https://stackedit.io/).