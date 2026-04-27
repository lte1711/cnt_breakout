---
tags:
  - cnt
  - ko
  - implementation-report
  - exit
  - status/validated
  - type/documentation
  - status/active
  - type/analysis
  - type/validation
  - status/completed
---

# CNT Target Exit Price Fix Report 20260425 KO

## 요약

목표가 도달 청산 주문에서 `target_price` 대신 현재가가 `SELL LIMIT` 주문 가격으로 전달되던 문제를 수정했다.

## 설계 요약

청산 지정가 선택 책임을 `src/engine.py` 내부 함수 `_select_exit_limit_price()`로 분리했다.

- `TARGET`: `exit_signal.target_price` 사용
- `PARTIAL`: `exit_signal.target_price` 사용
- `TIME_EXIT`: 기존 정책대로 현재가 사용
- `TARGET` 또는 `PARTIAL`인데 `target_price`가 없으면 `ValueError`로 실패 처리

이 변경은 기존 거래소 대기 주문을 취소하거나 재제출하지 않는다. 런타임 상태 변경 없이 다음 엔진 실행의 주문 생성 로직만 수정한다.

## 변경 파일

- `src/engine.py`
- `tests/test_engine_exit_price.py`

## 검증 결과

다음 검증을 완료했다.

- `python -m py_compile src\engine.py tests\test_engine_exit_price.py`
- `python -m pytest tests\test_engine_exit_price.py tests\test_exit_manager.py`
- `python -m pytest`

전체 테스트 결과:

- `62 passed`

## 회귀 테스트

추가된 테스트는 다음 동작을 검증한다.

- 목표가 도달 시 `SELL LIMIT` 기준 가격이 현재가가 아니라 `ExitSignal.target_price`인지 확인
- 부분 청산 목표가도 `ExitSignal.target_price`를 사용하는지 확인
- 시간 기반 청산은 현재가 정책을 유지하는지 확인
- 목표가 청산인데 `target_price`가 없으면 조용히 현재가로 대체하지 않는지 확인

## 기록

관련 원인 분석 문서: [[CNT TARGET EXIT PRICE MISMATCH REPORT 20260425 KO]]

관련 거래 상태 문서: [[CNT TRADING STATUS REPORT 20260425 1948 KO]]
