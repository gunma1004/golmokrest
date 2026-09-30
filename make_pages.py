import os
import re
import itertools

# --- 🌟 100가지 고유 타이틀 & 메타 디스크립션 순환 패턴 풀 ---
# 규칙 1: 타이틀 내 '마사지' 키워드 중복 배제 및 다채로운 테라피 종목 분산
# 규칙 2: 메타 디스크립션에 {GU_NAME} {DONG_NAME} 바로 뒤에 '출장 마사지'가 자연스럽게 연결
SEO_VARIATIONS = [
    ("{GU_NAME} {DONG_NAME} 출장 건식 마사지 & 힐링 케어 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 및 프리미엄 홈케어 전문. 검증된 관리사의 100% 후불제 안심 케어."),
    ("{GU_NAME} {DONG_NAME} 출장 스웨디시 & 프리미엄 테라피 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 전문 플랫폼. 선입금 전혀 없는 현장 결제로 편안하게 즐기는 테라피."),
    ("{GU_NAME} {DONG_NAME} 출장 아로마 마사지 1:1 맞춤 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 추천 코스. 지친 하루의 피로를 풀어주는 1:1 맞춤형 방문 힐링."),
    ("{GU_NAME} {DONG_NAME} 출장 정통 타이 마사지 정찰제 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 스웨디시 & 아로마 전문. 정찰제 요금으로 부담 없이 이용하세요."),
    ("{GU_NAME} {DONG_NAME} 출장 감성 스웨디시 테라피 케어 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 신속 방문 케어. 전문 자격을 갖춘 한국인 관리사의 명품 바디테라피."),
    ("{GU_NAME} {DONG_NAME} 출장 딥티슈 테라피 & 안심 서비스 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 100% 후불 보장제. 내 집에서 편안하게 누리는 감성 스웨디시 힐링."),
    ("{GU_NAME} {DONG_NAME} 출장 힐링 바디케어 코스 예약 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 예약 안내. 건식, 아로마, 타이 등 다채로운 코스를 합리적으로."),
    ("{GU_NAME} {DONG_NAME} 출장 릴렉싱 마사지 안심 후불제 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 프라이빗 케어. 고객 만족도 높은 검증된 제휴 샵 맞춤 매칭."),
    ("{GU_NAME} {DONG_NAME} 출장 스포츠 마사지 피로해소 코스 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 안심 방문 서비스. 늦은 심야 시간에도 할증 걱정 없는 정찰제 힐링."),
    ("{GU_NAME} {DONG_NAME} 출장 프리미엄 홈타이 테라피 안내 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 힐링 테라피 안내. 뭉친 근육을 부드럽게 이완하는 프리미엄 프로그램."),
    ("{GU_NAME} {DONG_NAME} 출장 로미로미 테라피 전문 안내 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 최고급 아로마 오일 케어. 편안한 공간에서 누리는 VIP 전신 관리."),
    ("{GU_NAME} {DONG_NAME} 출장 림프 순환 테라피 안심 케어 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 홈타이 & 스웨디시 추천. 안전하고 투명한 100% 현장 결제 방식."),
    ("{GU_NAME} {DONG_NAME} 출장 아로마 오일 테라피 코스 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 맞춤 바디 솔루션. 하루의 스트레스를 날려주는 정성스러운 손길."),
    ("{GU_NAME} {DONG_NAME} 출장 풋&바디 마사지 맞춤 코스 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 빠른 배차 안내. 전화 한 통으로 신속하게 찾아가는 방문 테라피."),
    ("{GU_NAME} {DONG_NAME} 출장 나이트 안심 케어 테라피 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 전문 힐러들의 밀착 케어. 위생과 퀄리티를 최우선으로 생각합니다."),
    ("{GU_NAME} {DONG_NAME} 출장 전신 스트레칭 마사지 코스 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 정통 힐링 바디 테라피. 품격 있는 관리로 몸과 마음에 활력을 충전."),
    ("{GU_NAME} {DONG_NAME} 출장 센슈얼 스웨디시 테라피 케어 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 실시간 예약 시스템. 선입금 사기 걱정 없는 완벽한 안심 후불제."),
    ("{GU_NAME} {DONG_NAME} 출장 딥 릴렉스 마사지 안내 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 딥티슈 & 림프 순환 케어. 묵은 피로를 말끔하게 날려드립니다."),
    ("{GU_NAME} {DONG_NAME} 출장 바디 밸런스 테라피 맞춤 케어 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 VIP 스웨디시 안내. 섬세하고 부드러운 테크닉으로 극상의 힐링 선사."),
    ("{GU_NAME} {DONG_NAME} 출장 시그니처 힐링 테라피 예약 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 홈케어 서비스. 내가 원하는 시간과 장소에서 누리는 고품격 휴식."),
    ("{GU_NAME} {DONG_NAME} 출장 클래식 타이 마사지 안내 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 정찰제 가격 안내. 추가 비용 일체 없이 투명하게 진행되는 바디케어."),
    ("{GU_NAME} {DONG_NAME} 출장 소프트 스웨디시 힐링 케어 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 맞춤형 안심 케어. 프라이빗한 개인 공간에서 경험하는 최고의 휴식."),
    ("{GU_NAME} {DONG_NAME} 출장 에너제틱 스포츠 테라피 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 전신 피로해소 코스. 전문적인 테크닉으로 개운한 일상을 선사합니다."),
    ("{GU_NAME} {DONG_NAME} 출장 올인원 전신 마사지 예약 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 스웨디시 테라피 추천. 은은한 향기와 함께 즐기는 감성 바디케어."),
    ("{GU_NAME} {DONG_NAME} 출장 내추럴 아로마 테라피 코스 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 1:1 예약 안내. 친절하고 숙련된 관리사가 꼼꼼하게 케어해 드립니다."),
    ("{GU_NAME} {DONG_NAME} 출장 토탈 릴렉싱 마사지 케어 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 안전 후불 결제. 예약금 요구 없는 투명하고 정직한 테라피 플랫폼."),
    ("{GU_NAME} {DONG_NAME} 출장 럭셔리 스웨디시 테라피 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 힐링 코스 모음. 나에게 딱 맞는 맞춤형 프로그램으로 힐링하세요."),
    ("{GU_NAME} {DONG_NAME} 출장 데일리 피로해소 마사지 케어 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 홈타이 전문. 경직된 몸을 시원하게 풀어주는 정통 스트레칭 케어."),
    ("{GU_NAME} {DONG_NAME} 출장 젠틀 딥티슈 테라피 맞춤 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 프리미엄 서비스. 번거로운 이동 없이 집에서 편안하게 받는 바디케어."),
    ("{GU_NAME} {DONG_NAME} 출장 감성 아로마 마사지 예약 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 전문점 안내. 청결하고 안전한 관리로 쾌적한 힐링을 보장합니다."),
    ("{GU_NAME} {DONG_NAME} 출장 힐링 마인드 테라피 코스 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 바디 릴렉싱 케어. 일상에 지친 현대인을 위한 맞춤 힐링 솔루션."),
    ("{GU_NAME} {DONG_NAME} 출장 정통 건식 릴렉스 케어 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 추천 제휴 샵 안내. 후기와 만족도가 증명하는 고품격 테라피."),
    ("{GU_NAME} {DONG_NAME} 출장 프리미엄 바디 밸런스 케어 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 심야 안심 방문. 늦은 시간에도 언제든 부담 없이 연락해 보세요."),
    ("{GU_NAME} {DONG_NAME} 출장 캄 테라피 & 마사지 코스 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 감성 아로마 코스. 천연 에센셜 오일로 피부와 마음을 촉촉하게."),
    ("{GU_NAME} {DONG_NAME} 출장 스페셜 홈타이 마사지 안내 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 스피드 방문 예약. 전화 상담 후 가장 빠르게 도착하는 홈케어."),
    ("{GU_NAME} {DONG_NAME} 출장 오일 바디 테라피 케어 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 힐링의 새로운 기준. 편안함과 전문성을 모두 갖춘 프리미엄 서비스."),
    ("{GU_NAME} {DONG_NAME} 출장 전신 딥 릴렉싱 마사지 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 현장 카드/현금 후불제. 믿고 이용할 수 있는 투명한 케어 시스템."),
    ("{GU_NAME} {DONG_NAME} 출장 포커스 힐링 테라피 예약 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 림프 순환 테라피. 가벼워진 몸으로 일상에 활력을 더해드립니다."),
    ("{GU_NAME} {DONG_NAME} 출장 릴렉스 스웨디시 테라피 케어 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 1인 맞춤 케어. 고객님의 컨디션에 맞춘 맞춤형 압과 테크닉 적용."),
    ("{GU_NAME} {DONG_NAME} 출장 퍼펙트 바디케어 코스 안내 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 쾌적한 홈테라피. 편안한 침대나 소파에서 안심하고 케어 받으세요."),
    ("{GU_NAME} {DONG_NAME} 출장 수딩 아로마 마사지 안내 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 명품 스웨디시 코스. 따뜻한 온기로 온몸을 녹여주는 감성 바디케어."),
    ("{GU_NAME} {DONG_NAME} 출장 비탈리티 스포츠 테라피 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 실속형 정찰제 안내. 거품 없는 착한 가격으로 만나는 고품격 테라피."),
    ("{GU_NAME} {DONG_NAME} 출장 심야 힐링 마사지 코스 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 바디 밸런스 교정 케어. 균형 잡힌 바디 라인을 위한 힐링 프로그램."),
    ("{GU_NAME} {DONG_NAME} 출장 오가닉 오일 테라피 케어 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 믿을 수 있는 플랫폼. 검증된 한국인 테라피스트의 정성스러운 관리."),
    ("{GU_NAME} {DONG_NAME} 출장 마일드 스웨디시 마사지 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 타이 & 아로마 복합 코스. 뭉친 근육 이완과 심신 안정을 동시에."),
    ("{GU_NAME} {DONG_NAME} 출장 컴포트 홈타이 테라피 안내 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 프리미엄 방문 서비스. 나만을 위한 가장 안락한 힐링 스튜디오."),
    ("{GU_NAME} {DONG_NAME} 출장 힐링 바디 리셋 마사지 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 빠른 도착 보장. 전지역 네트워크망으로 빠르게 방문합니다."),
    ("{GU_NAME} {DONG_NAME} 출장 엑스퍼트 테라피 케어 안내 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 릴렉싱 테라피 예약. 피로에 지친 당신을 위한 완벽한 휴식 시간."),
    ("{GU_NAME} {DONG_NAME} 출장 프리미엄 딥티슈 테라피 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 감동 서비스. 작은 부분까지 세심하게 배려하는 고품격 힐링 케어."),
    ("{GU_NAME} {DONG_NAME} 출장 감성 릴렉싱 마사지 예약 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 100% 현장 정산. 사기 걱정 없는 가장 신뢰할 수 있는 테라피 안내."),
    ("{GU_NAME} {DONG_NAME} 출장 밸런스드 아로마 테라피 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 토탈 바디 솔루션. 하루 한 시간의 여유로 건강한 활력을 충전하세요."),
    ("{GU_NAME} {DONG_NAME} 출장 디럭스 스웨디시 마사지 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 감성 스웨디시 안내. 깃털처럼 부드러운 터치로 전신 긴장 해소."),
    ("{GU_NAME} {DONG_NAME} 출장 리프레시 타이 테라피 케어 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 전문 출장 방문. 원하는 시간대에 맞춰 방문하는 맞춤 테라피."),
    ("{GU_NAME} {DONG_NAME} 출장 프로페셔널 바디 마사지 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 힐링 네트워크. 지역 최고 수준의 테라피스트들이 찾아갑니다."),
    ("{GU_NAME} {DONG_NAME} 출장 시그니처 아로마 테라피 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 순수 힐링 프로그램. 조용하고 차분한 분위기에서 즐기는 휴식."),
    ("{GU_NAME} {DONG_NAME} 출장 프라이빗 힐링 케어 예약 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 스트레스 완화 코스. 뇌와 몸의 긴장을 풀어주는 명품 케어."),
    ("{GU_NAME} {DONG_NAME} 출장 소프트 릴렉스 마사지 코스 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 간편 예약 안내. 복잡한 절차 없이 터치 몇 번으로 손쉬운 예약."),
    ("{GU_NAME} {DONG_NAME} 출장 하이엔드 테라피 서비스 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 바디 리셋 프로그램. 찌뿌둥한 하루를 활기차게 바꿔주는 손길."),
    ("{GU_NAME} {DONG_NAME} 출장 바디 리바이탈 마사지 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 안심 홈케어. 철저한 위생 관리로 늘 쾌적함을 선물합니다."),
    ("{GU_NAME} {DONG_NAME} 출장 슬로우 힐링 아로마 케어 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 스웨디시 & 타이 안내. 취향에 따라 자유롭게 선택하는 힐링 코스."),
    ("{GU_NAME} {DONG_NAME} 출장 올데이 안심 마사지 예약 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 VIP 고객 맞춤 케어. 오직 한 사람만을 위한 스페셜 테라피."),
    ("{GU_NAME} {DONG_NAME} 출장 럭스 스웨디시 테라피 케어 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 합리적인 가격 정책. 투명한 정찰제로 편안하게 경험하세요."),
    ("{GU_NAME} {DONG_NAME} 출장 모빌리티 스트레칭 코스 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 피로 회복의 명가. 숙련된 테크닉으로 묵은 결림을 말끔히 해결."),
    ("{GU_NAME} {DONG_NAME} 출장 에센셜 오일 마사지 예약 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 친절 방문 서비스. 밝은 미소와 정성으로 편안함을 드립니다."),
    ("{GU_NAME} {DONG_NAME} 출장 이지 케어 홈타이 안내 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 딥티슈 테라피. 속근육까지 시원하게 풀어주는 집중 케어."),
    ("{GU_NAME} {DONG_NAME} 출장 풀바디 릴렉싱 테라피 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 감성 힐링 스웨디시. 감각을 깨우는 프리미엄 전신 바디케어."),
    ("{GU_NAME} {DONG_NAME} 출장 딥 릴리프 마사지 코스 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 즉시 출발 서비스. 기다리는 지루함 없이 신속하게 방문합니다."),
    ("{GU_NAME} {DONG_NAME} 출장 힐링 아우라 스웨디시 케어 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 정직한 홈케어. 예약부터 방문까지 투명하게 안심하고 이용하세요."),
    ("{GU_NAME} {DONG_NAME} 출장 밸런싱 바디 테라피 예약 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 수면 개선 힐링 코스. 깊은 숙면을 유도하는 릴렉싱 아로마 케어."),
    ("{GU_NAME} {DONG_NAME} 출장 마인드풀 테라피 서비스 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 활력 충전 바디테라피. 무거운 어깨와 허리를 가볍게 케어합니다."),
    ("{GU_NAME} {DONG_NAME} 출장 퓨어 아로마 마사지 코스 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 후불제 전문 플랫폼. 안전과 신뢰를 가장 중요하게 여깁니다."),
    ("{GU_NAME} {DONG_NAME} 출장 스트롱 스포츠 마사지 안내 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 프리미엄 홈타이 예약. 집에서도 수준 높은 타이 관리를 누려보세요."),
    ("{GU_NAME} {DONG_NAME} 출장 나이트 릴렉스 테라피 케어 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 맞춤 아로마 블렌딩. 피부 보습과 릴렉스를 함께 선사합니다."),
    ("{GU_NAME} {DONG_NAME} 출장 VIP 시그니처 마사지 안내 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 신속 매칭 시스템. 계신 곳에서 가장 가까운 베스트 샵 안내."),
    ("{GU_NAME} {DONG_NAME} 출장 에스테틱 바디 테라피 케어 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 명품 바디 솔루션. 하루하루 지친 당신을 위한 프라이빗 힐링."),
    ("{GU_NAME} {DONG_NAME} 출장 프레시 타이 마사지 안내 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 스웨디시 정찰제 코스. 군더더기 없는 깔끔하고 품격 있는 케어."),
    ("{GU_NAME} {DONG_NAME} 출장 릴렉싱 오일 테라피 코스 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 전문 힐링 안내. 언제나 최상의 만족을 제공하는 방문 테라피."),
    ("{GU_NAME} {DONG_NAME} 출장 젠틀 케어 마사지 서비스 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 야간 힐링 서비스. 밤낮 가리지 않고 고객님의 피로를 덜어드립니다."),
    ("{GU_NAME} {DONG_NAME} 출장 컴팩트 힐링 테라피 예약 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 투명한 후불 안내. 선입금 요구가 전혀 없는 정직한 시스템."),
    ("{GU_NAME} {DONG_NAME} 출장 로열 스웨디시 마사지 코스 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 릴렉싱 케어의 정석. 몸의 균형을 되찾아주는 특별한 테라피."),
    ("{GU_NAME} {DONG_NAME} 출장 딥 바디 스트레칭 케어 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 웰니스 방문 프로그램. 일상의 질을 높여주는 건강한 바디케어."),
    ("{GU_NAME} {DONG_NAME} 출장 센서티브 아로마 마사지 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 스피드 힐링 예약. 계신 곳으로 바로 찾아가는 감동 서비스."),
    ("{GU_NAME} {DONG_NAME} 출장 홈 웰니스 테라피 안내 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 감성 테라피 코스. 섬세한 케어로 하루의 스트레스를 씻어내세요."),
    ("{GU_NAME} {DONG_NAME} 출장 릴렉세이션 마사지 코스 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 전신 풀케어 안내. 발끝부터 머리까지 가벼워지는 놀라운 경험."),
    ("{GU_NAME} {DONG_NAME} 출장 프리미엄 에센스 테라피 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 홈 웰니스 1:1 방문. 쾌적한 나만의 쉼터에서 즐기는 테라피."),
    ("{GU_NAME} {DONG_NAME} 출장 클래식 바디케어 마사지 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 안심 예약 플랫폼. 정직하고 검증된 관리사들만 함께합니다."),
    ("{GU_NAME} {DONG_NAME} 출장 스무스 스웨디시 테라피 케어 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 프리미엄 감성 스웨디시. 하루를 완벽하게 보상받는 힐링 시간."),
    ("{GU_NAME} {DONG_NAME} 출장 힐링 포레스트 마사지 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 속근육 릴렉스 케어. 굳어있던 관절과 근육을 유연하게 풀어드립니다."),
    ("{GU_NAME} {DONG_NAME} 출장 인텐시브 딥티슈 테라피 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 정통 아로마 테라피. 고급 천연 오일로 피부에 활력을 부여합니다."),
    ("{GU_NAME} {DONG_NAME} 출장 캄 앤 릴렉스 마사지 안내 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 100% 현장 결제 시스템. 처음부터 끝까지 안심할 수 있는 케어."),
    ("{GU_NAME} {DONG_NAME} 출장 오리엔탈 홈타이 테라피 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 감동 힐링 파트너. 매일매일 상쾌한 아침을 맞이할 수 있도록 돕습니다."),
    ("{GU_NAME} {DONG_NAME} 출장 럭셔리 바디 마사지 코스 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 힐링 라이프 안내. 내 손안에서 시작되는 가장 편안한 휴식."),
    ("{GU_NAME} {DONG_NAME} 출장 내추럴 릴렉스 테라피 케어 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 고품격 방문 케어. 호텔 부럽지 않은 프리미엄 테라피를 집에서."),
    ("{GU_NAME} {DONG_NAME} 출장 퀵 안심 방문 마사지 안내 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 맞춤 압 조절 테라피. 나에게 꼭 맞는 최적의 힐링을 선사합니다."),
    ("{GU_NAME} {DONG_NAME} 출장 프리미엄 코스 테라피 안내 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 스웨디시 & 홈타이 코스. 만족도 1위 제휴 샵에서 확인하세요."),
    ("{GU_NAME} {DONG_NAME} 출장 리얼 힐링 마사지 프로그램 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 안전 케어 솔루션. 고객님의 소중한 프라이버시를 철저히 지킵니다."),
    ("{GU_NAME} {DONG_NAME} 출장 스페셜 바디 밸런스 코스 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 힐링 리포트. 매일매일 더 가볍고 활기찬 몸을 만들어 드립니다."),
    ("{GU_NAME} {DONG_NAME} 출장 어반 릴렉싱 스웨디시 케어 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 투명 정찰 방문제. 숨은 추가금 없이 정직하게 운영됩니다."),
    ("{GU_NAME} {DONG_NAME} 출장 힐링 모먼트 테라피 코스 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 감성 전신 케어. 은은한 향과 따뜻한 손길로 전하는 감동의 휴식."),
    ("{GU_NAME} {DONG_NAME} 출장 퍼펙트 전신 마사지 안내 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 프리미엄 힐링 서비스. 100% 후불제로 부담 없이 예약해 보세요.")
]

seo_cycle = itertools.cycle(SEO_VARIATIONS)

regions_data = {
    "seoul": {
        "jongno": {"name": "종로구", "dongs": ["청운동", "효자동", "사직동", "삼청동", "안국동", "종로1가", "종로2가", "종로3가", "인사동", "창신동", "숭인동", "평창동", "무악동"]},
        "jung": {"name": "중구", "dongs": ["무교동", "을지로", "명동", "충무로", "회현동", "소공동", "장충동", "신당동", "황학동", "중림동"]},
        "yongsan": {"name": "용산구", "dongs": ["후암동", "용산동", "갈월동", "남영동", "원효로", "효창동", "용문동", "이촌동", "이태원동", "한남동", "보광동", "청파동", "한강로"]},
        "seongdong": {"name": "성동구", "dongs": ["왕십리동", "마장동", "사근동", "행당동", "응봉동", "금호동", "성수동", "송정동", "용답동", "옥수동"]},
        "gwangjin": {"name": "광진구", "dongs": ["화양동", "중곡동", "능동", "구의동", "광장동", "자양동", "군자동"]},
        "dongdaemun": {"name": "동대문구", "dongs": ["신설동", "용두동", "제기동", "전농동", "답십리동", "장안동", "회기동", "휘경동", "이문동"]},
        "jungnang": {"name": "중랑구", "dongs": ["면목동", "상봉동", "중화동", "묵동", "망우동", "신내동"]},
        "seongbuk": {"name": "성북구", "dongs": ["성북동", "삼선동", "동선동", "보문동", "안암동", "정릉동", "길음동", "종암동", "하월곡동", "장위동", "석관동"]},
        "gangbuk": {"name": "강북구", "dongs": ["미아동", "번동", "수유동", "우이동"]},
        "dobong": {"name": "도봉구", "dongs": ["창동", "도봉동", "방학동", "쌍문동"]},
        "nowon": {"name": "노원구", "dongs": ["월계동", "공릉동", "하계동", "상계동", "중계동"]},
        "eunpyeong": {"name": "은평구", "dongs": ["불광동", "갈현동", "구산동", "대조동", "응암동", "역촌동", "신사동", "증산동", "수색동", "진관동"]},
        "seodaemun": {"name": "서대문구", "dongs": ["충정로", "북아현동", "신촌동", "창천동", "연희동", "홍제동", "홍은동", "남가좌동", "북가좌동"]},
        "mapo": {"name": "마포구", "dongs": ["아현동", "공덕동", "도화동", "용강동", "대흥동", "염리동", "신수동", "창전동", "상수동", "서교동", "동교동", "합정동", "망원동", "연남동", "성산동", "상암동"]},
        "yangcheon": {"name": "양천구", "dongs": ["목동", "신월동", "신정동"]},
        "gangseo": {"name": "강서구", "dongs": ["화곡동", "등촌동", "염창동", "가양동", "마곡동", "내발산동", "외발산동", "공항동", "방화동"]},
        "guro": {"name": "구로구", "dongs": ["신도림동", "구로동", "가리봉동", "개봉동", "오류동", "수궁동", "항동"]},
        "geumcheon": {"name": "금천구", "dongs": ["가산동", "독산동", "시흥동"]},
        "yeongdeungpo": {"name": "영등포구", "dongs": ["영등포동", "여의도동", "당산동", "도림동", "문래동", "양평동", "신길동", "대림동"]},
        "dongjak": {"name": "동작구", "dongs": ["노량진동", "상도동", "흑석동", "사당동", "대방동", "신대방동"]},
        "gwanak": {"name": "관악구", "dongs": ["봉천동", "신림동", "남현동"]},
        "seocho": {"name": "서초구", "dongs": ["서초동", "잠원동", "반포동", "방배동", "양재동", "우면동", "내곡동"]},
        "gangnam": {"name": "강남구", "dongs": ["역삼동", "개포동", "청담동", "삼성동", "대치동", "신사동", "논현동", "압구정동", "일원동", "수서동", "도곡동"]},
        "songpa": {"name": "송파구", "dongs": ["잠실동", "신천동", "풍납동", "거여동", "마천동", "방이동", "오금동", "석촌동", "삼전동", "가락동", "문정동", "송파동"]},
        "gangdong": {"name": "강동구", "dongs": ["강일동", "상일동", "명일동", "고덕동", "암사동", "천호동", "성내동", "둔촌동", "길동"]}
    },
    "gyeonggi": {
        "suwon-jangan": {"name": "수원시 장안구", "dongs": ["파장동", "정자동", "율전동", "천천동", "조원동", "송죽동", "연무동"]},
        "suwon-gwonseon": {"name": "수원시 권선구", "dongs": ["세류동", "평동", "서둔동", "구운동", "탑동", "금곡동", "호매실동", "곡반정동", "권선동", "고색동"]},
        "suwon-paldal": {"name": "수원시 팔달구", "dongs": ["매교동", "매산동", "고등동", "화서동", "인계동", "우만동", "지동"]},
        "suwon-yeongtong": {"name": "수원시 영통구", "dongs": ["영통동", "원천동", "이의동", "하동", "매탄동", "망포동", "신동"]},
        "seongnam-sujeong": {"name": "성남시 수정구", "dongs": ["신흥동", "태평동", "단대동", "산성동", "양지동", "복정동", "시흥동", "창곡동", "고등동"]},
        "seongnam-jungwon": {"name": "성남시 중원구", "dongs": ["성남동", "중앙동", "금광동", "은행동", "하대원동", "도촌동"]},
        "seongnam-bundang": {"name": "성남시 분당구", "dongs": ["분당동", "수내동", "정자동", "서현동", "이매동", "야탑동", "금곡동", "구미동", "판교동", "삼평동", "백현동", "운중동"]},
        "uijeongbu": {"name": "의정부시", "dongs": ["의정부동", "호원동", "장암동", "신곡동", "용현동", "가능동", "녹양동", "민락동"]},
        "anyang-manan": {"name": "안양시 만안구", "dongs": ["안양동", "석수동", "박달동"]},
        "anyang-dongan": {"name": "안양시 동안구", "dongs": ["비산동", "관양동", "평촌동", "호계동", "부림동"]},
        "bucheon-wonmi": {"name": "부천시 원미구", "dongs": ["원미동", "심곡동", "춘의동", "도당동", "중동", "상동", "약대동"]},
        "bucheon-sosa": {"name": "부천시 소사구", "dongs": ["소사본동", "범박동", "역곡동", "옥길동", "괴안동"]},
        "bucheon-ojeong": {"name": "부천시 오정구", "dongs": ["오정동", "여월동", "작동", "고강동", "삼정동", "내동"]},
        "gwangmyeong": {"name": "광명시", "dongs": ["광명동", "철산동", "하안동", "소하동", "일직동"]},
        "pyeongtaek": {"name": "평택시", "dongs": ["비전동", "동삭동", "세교동", "지산동", "서정동", "팽성읍", "안중읍", "포승읍"]},
        "dongducheon": {"name": "동두천시", "dongs": ["생연동", "보산동", "동두천동", "송내동", "지행동"]},
        "ansan-sangrok": {"name": "안산시 상록구", "dongs": ["사동", "일동", "이동", "본오동", "부곡동", "월피동", "성포동"]},
        "ansan-danwon": {"name": "안산시 단원구", "dongs": ["와동", "고잔동", "초지동", "원곡동", "신길동", "선부동", "대부동"]},
        "goyang-deogyang": {"name": "고양시 덕양구", "dongs": ["주교동", "성사동", "원흥동", "삼송동", "화정동", "행신동"]},
        "goyang-ilsandong": {"name": "고양시 일산동구", "dongs": ["식사동", "중산동", "정발산동", "마두동", "백석동", "풍동", "장항동"]},
        "goyang-ilsanseo": {"name": "고양시 일산서구", "dongs": ["일산동", "탄현동", "주엽동", "대화동", "가좌동", "덕이동"]},
        "gwacheon": {"name": "과천시", "dongs": ["중앙동", "갈현동", "문원동", "과천동", "별양동", "부림동"]},
        "guri": {"name": "구리시", "dongs": ["인창동", "교문동", "수택동", "갈매동"]},
        "namyangju": {"name": "남양주시", "dongs": ["와부읍", "진접읍", "화도읍", "오남읍", "퇴계원읍", "호평동", "평내동", "다산동"]},
        "osan": {"name": "오산시", "dongs": ["중앙동", "세마동", "초평동", "남촌동", "대원동"]},
        "siheung": {"name": "시흥시", "dongs": ["대야동", "신천동", "은행동", "목감동", "정왕동", "배곧동"]},
        "gunpo": {"name": "군포시", "dongs": ["산본동", "금정동", "당동", "당정동", "부곡동"]},
        "uiwang": {"name": "의왕시", "dongs": ["고천동", "부곡동", "오전동", "내손동", "청계동"]},
        "hanam": {"name": "하남시", "dongs": ["신장동", "덕풍동", "감일동", "위례동", "미사동"]},
        "yongin-cheoin": {"name": "용인시 처인구", "dongs": ["포곡읍", "모현읍", "역삼동", "유림동", "중앙동", "양지면"]},
        "yongin-giheung": {"name": "용인시 기흥구", "dongs": ["신갈동", "구갈동", "상갈동", "보라동", "마북동", "동백동", "보정동"]},
        "yongin-suji": {"name": "용인시 수지구", "dongs": ["풍덕천동", "죽전동", "동천동", "신봉동", "성복동", "상현동"]},
        "paju": {"name": "파주시", "dongs": ["문산읍", "조리읍", "법원읍", "교하동", "운정동", "금촌동"]},
        "icheon": {"name": "이천시", "dongs": ["창전동", "중리동", "증포동", "관고동", "부발읍"]},
        "anseong": {"name": "안성시", "dongs": ["공도읍", "죽산면", "삼죽면", "일죽면", "미양면", "대덕면"]},
        "gimpo": {"name": "김포시", "dongs": ["통진읍", "고촌읍", "양촌읍", "사우동", "풍무동", "장기동", "구래동", "운양동"]},
        "hwaseong": {"name": "화성시", "dongs": ["봉담읍", "우정읍", "향남읍", "남양읍", "동탄동", "병점동"]},
        "gwangju": {"name": "광주시", "dongs": ["오포읍", "초월읍", "곤지암읍", "경안동", "송정동"]},
        "yangju": {"name": "양주시", "dongs": ["회천동", "양주동", "백석읍", "고읍동", "옥정동"]},
        "pocheon": {"name": "포천시", "dongs": ["소흘읍", "군내면", "가산면", "신북면", "포천동"]},
        "yeoju": {"name": "여주시", "dongs": ["가남읍", "여흥동", "중앙동", "오학동"]},
        "yeoncheon": {"name": "연천군", "dongs": ["연천읍", "전곡읍", "군남면"]},
        "gapyeong": {"name": "가평군", "dongs": ["가평읍", "설악면", "청평면", "상면"]},
        "yangpyeong": {"name": "양평군", "dongs": ["양평읍", "강상면", "양서면", "옥천면", "용문면"]}
    },
    "incheon": {
        "jemulpo": {"name": "제물포구", "dongs": ["내동", "경동", "용동", "전동", "북성동", "송학동", "관동", "중앙동"]},
        "yeongjong": {"name": "영종구", "dongs": ["운서동", "중산동", "운남동", "운북동"]},
        "michuhol": {"name": "미추홀구", "dongs": ["숭의동", "용현동", "학익동", "도화동", "주안동", "관교동", "문학동"]},
        "yeonsu": {"name": "연수구", "dongs": ["옥련동", "선학동", "연수동", "청학동", "동춘동", "송도동"]},
        "namdong": {"name": "남동구", "dongs": ["구월동", "간석동", "만수동", "장수동", "서창동", "논현동"]},
        "bupyeong": {"name": "부평구", "dongs": ["부평동", "산곡동", "청천동", "십정동", "부개동", "삼산동"]},
        "gyeyang": {"name": "계양구", "dongs": ["효성동", "작전동", "서운동", "임학동", "동양동", "병방동"]},
        "seohae": {"name": "서해구", "dongs": ["북성동", "신흥동", "선화동"]},
        "geomdan": {"name": "검단구", "dongs": ["마전동", "당하동", "원당동", "불로동", "왕길동"]},
        "ganghwa": {"name": "강화군", "dongs": ["강화읍", "선원면", "불은면", "길상면", "화도면", "내가면"]},
        "ongjin": {"name": "옹진군", "dongs": ["북도면", "연평면", "백령면", "대청면", "덕적면", "영흥면"]}
    }
}

shops = [
    {"name": "🔥 한국미인홈케어", "desc": "서울·경기·인천 전지역 신속 방문! 정성 가득한 테라피 & 릴렉싱 프로그램", "phone": "0507-1280-3303", "price": "100,000원부터~"},
    {"name": "✨ 오늘밤테라피", "desc": "품격 있는 힐링을 선사하는 최고급 오일 프라이빗 방문 테라피 서비스", "phone": "0507-1280-3223", "price": "60,000원부터~"},
    {"name": "💎 주주테라피", "desc": "재방문율 1위! 칼도착 25분 보장, 철저한 위생 관리와 럭셔리 케어", "phone": "0507-1280-3193", "price": "60,000원부터~"},
    {"name": "🌟 퀸즈홈테라피", "desc": "전문 힐러들의 맞춤형 VIP 피로회복 특화 프로그램 진행 중", "phone": "0507-1280-3334", "price": "60,000원부터~"},
    {"name": "👑 골든테라피", "desc": "선입금 없는 100% 후불제! 수도권 전지역 평균 25분 내 실시간 도착", "phone": "0507-1280-3360", "price": "110,000원부터~"}
]

def generate_shop_cards(gu_name, region_name):
    cards_html = ""
    for s in shops:
        cards_html += f"""
        <a class="kt-shop" href="tel:{s['phone']}" rel="nofollow" style="text-decoration:none; display:block; margin-bottom:12px;">
            <div style="background:#fff; border:1px solid #e3e8ee; border-radius:12px; padding:16px; box-shadow:0 2px 8px rgba(0,0,0,0.03);">
                <h4 style="font-size:16px; font-weight:bold; color:#1d2a27; margin:0 0 6px 0;">{s['name']} ({gu_name} {region_name} 맞춤 안내)</h4>
                <p style="font-size:13px; color:#46525f; margin:0 0 10px 0; line-height:1.4;">{s['desc']}</p>
                <div style="display:flex; justify-content:space-between; align-items:center; font-size:13px; border-top:1px solid #f1f3f5; padding-top:8px;">
                    <span style="color:#c62828; font-weight:bold;">요금: {s['price']}</span>
                    <span style="background:#c62828; color:#fff; padding:6px 12px; border-radius:6px; font-weight:bold; font-size:12px;">📞 전화 연결</span>
                </div>
            </div>
        </a>
        """
    return cards_html

# template.html 읽기
with open("template.html", "r", encoding="utf-8") as f:
    template_content = f.read()

total_dong_count = 0
total_gu_count = 0

for city, gu_dict in regions_data.items():
    for gu_code, gu_info in gu_dict.items():
        gu_name = gu_info["name"]
        dongs = gu_info["dongs"]
        
        # 1. 구(Gu) 허브 페이지 생성
        gu_dir = os.path.join("area", city, gu_code)
        os.makedirs(gu_dir, exist_ok=True)
        gu_file_path = os.path.join(gu_dir, "index.html")
        
        dongs_html = ""
        for dong in dongs:
            dongs_html += f'<a href="/area/{city}/{gu_code}/{dong}/" style="background:#f8f9fa; border:1px solid #e3e8ee; padding:12px 15px; border-radius:8px; text-align:center; color:#333; text-decoration:none; font-weight:600; font-size:14px; transition:all 0.2s;">{dong}</a>\n'

        gu_shop_cards_html = generate_shop_cards(gu_name, "전지역")

        # 구 단위 타이틀 & 디스크립션 정돈 (키워드 연속 중복 배제)
        gu_title = f"{gu_name} 출장 스웨디시 & 프리미엄 테라피 | 골목리스트"
        gu_desc = f"{gu_name} 전지역 구·동 출장 마사지 케어 및 프리미엄 홈타이 전문 안내. 검증된 관리사의 100% 후불제 안심 케어."

        gu_html_content = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<meta name="naver-site-verification" content="e077c41bc3896bcecf18407976496548bea3a79c" />
<title>{gu_title}</title>
<meta name="description" content="{gu_desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://golmokrest.netlify.app/area/{city}/{gu_code}/">

<meta property="og:site_name" content="골목리스트">
<meta property="og:locale" content="ko_KR">
<meta property="og:type" content="website">
<meta property="og:title" content="{gu_title}">
<meta property="og:description" content="{gu_desc}">
<meta property="og:url" content="https://golmokrest.netlify.app/area/{city}/{gu_code}/">

<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard-dynamic-subset.min.css" />
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Pretendard', sans-serif; }}
body {{ background-color: #f4f6f8; color: #1d2a27; line-height: 1.5; }}
.kt-wrap {{ max-width: 1180px; margin: 0 auto; padding: 0 15px; }}
.kt-utilbar {{ background: #1d2a27; color: #fff; font-size: 13px; padding: 8px 0; }}
.kt-utilbar .kt-wrap {{ display: flex; justify-content: flex-end; gap: 15px; }}
.kt-utilbar a {{ color: #fff; text-decoration: none; }}
.kt-logorow {{ background: #fff; padding: 20px 0; border-bottom: 1px solid #e3e8ee; }}
.kt-logorow .kt-wrap {{ display: flex; justify-content: space-between; align-items: center; }}
.kt-logo {{ font-size: 24px; font-weight: 800; color: #c62828; text-decoration: none; }}
.kt-menubar {{ background: #2c3e50; color: #fff; }}
.kt-menubar .kt-wrap {{ display: flex; gap: 20px; padding: 12px 15px; }}
.kt-menubar a {{ color: #fff; text-decoration: none; font-weight: 600; font-size: 15px; }}
.content-wrap {{ max-width: 800px; margin: 20px auto; padding: 0 15px; }}
h1 {{ font-size: 22px; font-weight: 800; margin-bottom: 15px; color: #1d2a27; border-left: 5px solid #c62828; padding-left: 12px; }}
.region-section {{ background: #fff; border: 1px solid #e3e8ee; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.02); }}
.region-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 8px; }}
.region-grid a:hover {{ background: #c62828; color: #fff; border-color: #c62828; }}
.kt-sectitle {{ font-size: 18px; font-weight: 800; margin: 25px 0 12px 0; border-bottom: 2px solid #c62828; padding-bottom: 6px; }}
.kt-foot {{ background: #1d2a27; color: #adb5bd; padding: 30px 0; font-size: 13px; margin-top: 50px; text-align: center; }}
</style>
</head>
<body>
<div class="kt-utilbar"><div class="kt-wrap">
    <a href="/area/">지역 전체보기</a>
    <a href="/partner/">제휴 문의</a>
</div></div>

<div class="kt-logorow"><div class="kt-wrap">
    <a class="kt-logo" href="/">골목리스트</a>
    <div><a href="/partner/" style="background:#c62828; color:#fff; padding:8px 14px; border-radius:6px; text-decoration:none; font-size:13px; font-weight:700;">제휴 문의</a></div>
</div></div>

<div class="kt-menubar"><div class="kt-wrap">
    <a href="/area/">지역 찾기</a>
    <a href="/partner/">입점 문의</a>
</div></div>

<div class="content-wrap">
    <nav style="font-size: 13px; color: #666; margin-bottom: 15px;"><a href="/" style="color:#666; text-decoration:none;">홈</a> › <a href="/area/" style="color:#666; text-decoration:none;">지역 전체보기</a> › <b>{gu_name}</b></nav>
    <h1>{gu_name} 홈바디·출장마사지 동별 안내</h1>
    
    <div class="region-section">
        <h3 style="font-size:15px; margin-bottom:12px; font-weight:700;">📍 {gu_name} 하위 동 선택하기</h3>
        <div class="region-grid">
            {dongs_html}
        </div>
    </div>

    <h2 class="kt-sectitle"><span>{gu_name} 공식 제휴 샵</span></h2>
    <div>
        {gu_shop_cards_html}
    </div>
</div>

<footer class="kt-foot">
    <p>&copy; 2026 골목리스트 All Rights Reserved.</p>
</footer>
</body>
</html>
"""

        with open(gu_file_path, "w", encoding="utf-8") as f:
            f.write(gu_html_content)
        total_gu_count += 1

        # 2. 각 동별 상세 페이지 생성 (100개 패턴 순환 적용)
        for dong_name in dongs:
            dong_dir = os.path.join("area", city, gu_code, dong_name)
            os.makedirs(dong_dir, exist_ok=True)
            
            file_path = os.path.join(dong_dir, "index.html")
            shop_cards_html = generate_shop_cards(gu_name, dong_name)
            
            # 100가지 패턴 중 다음 타이틀/디스크립션 세트 순환 선택
            title_tpl, desc_tpl = next(seo_cycle)
            page_title = title_tpl.format(GU_NAME=gu_name, DONG_NAME=dong_name)
            page_desc = desc_tpl.format(GU_NAME=gu_name, DONG_NAME=dong_name)

            # 안전장치: 혹시라도 연속해서 나오는 '마사지'를 정규식으로 1개로 압축
            page_title = re.sub(r'(마사지\s*)+마사지', '마사지', page_title)
            page_desc = re.sub(r'(마사지\s*)+마사지', '마사지', page_desc)

            content = template_content.replace("{PAGE_TITLE}", page_title)
            content = content.replace("{PAGE_DESC}", page_desc)
            content = content.replace("{GU_NAME}", gu_name)
            content = content.replace("{DONG_NAME}", dong_name)
            content = content.replace("{CITY}", city)
            content = content.replace("{GU_CODE}", gu_code)
            content = content.replace("{SHOP_CARDS}", shop_cards_html)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
                
            total_dong_count += 1

print(f"총 {total_gu_count}개의 구(Gu) 페이지 및 {total_dong_count}개의 동 페이지 생성 완료!")