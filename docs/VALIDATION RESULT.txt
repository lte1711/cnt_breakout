검증 완료 항목:

1. 신규 진입 차단
- action=NO_ENTRY_SIGNAL 확인
- reason=market_not_trend_up 확인

2. 신규 BUY 진입
- action=BUY_FILLED 확인
- open_trade 생성 확인

3. 보유 상태 유지
- action=HOLD_OPEN_TRADE 확인
- reason=target_and_stop_not_triggered 확인

4. 보호 손절 청산
- action=STOP_MARKET_FILLED 확인
- open_trade 해제 확인

5. 목표가 청산
- action=SELL_FILLED 확인
- reason=target_exit_limit_filled 확인
- open_trade 해제 확인

6. 운영본 복귀 확인
- 테스트 우회 제거 후 action=NO_ENTRY_SIGNAL 확인