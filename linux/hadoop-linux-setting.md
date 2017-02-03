###  리눅스 캐시

1. 참고사이트
	- [리눅스 캐시](https://brunch.co.kr/@alden/25)
	- [리눅스 메모리 관리](http://www.myservlab.com/155)

2. 문제
	- 하둡 클러스터 전체 서버에서 다음과 같은 메시지 반복적으로 발생함
		> kernel : java: page allocation failure. order:2, mode:0x20
		
	- redhat 페이지에서는 문제 해결을 다음과 같이 제시(https://access.redhat.com/solutions/90883)
	- workaound 방안 중에서 vm.zone_reclaim_mode는 변경 불가(하둡 사용시 권고사항이어서 0으로 설정)
		

> Written with [StackEdit](https://stackedit.io/).