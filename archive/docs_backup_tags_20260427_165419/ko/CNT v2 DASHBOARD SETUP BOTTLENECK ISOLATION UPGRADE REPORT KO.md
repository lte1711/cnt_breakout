---
title: CNT v2 DASHBOARD SETUP BOTTLENECK ISOLATION UPGRADE REPORT KO
status: completed
updated: 2026-04-24
---

# CNT v2 대시보드 Setup 병목 분리 업그레이드 보고서

## 목적

운영 대시보드에서 `breakout_v3`의 현재 shadow 단계가 단순 개선이 아니라 `setup bottleneck isolation` 단계임을 바로 읽을 수 있게 만든다.

## 대시보드 변경

전용 `V3 Setup Bottleneck` 카드를 추가하여 다음을 바로 보여주도록 했다.
- setup pass 희소성
- allowed trace 수
- setup_pass 이지만 blocked 된 trace 수
- 현재 shadow snapshot 기준의 주요 setup 측 실패

## 의도한 해석

- 공식 gate는 계속 최종 권위로 유지
- auxiliary recovery는 설명 계층으로 유지
- setup bottleneck 카드는 왜 `breakout_v3`가 여전히 shadow-only인지 설명

## Obsidian Links

- [[CNT DATA DASHBOARD KO]]
