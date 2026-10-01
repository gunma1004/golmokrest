import os
import re
import itertools

# --- 🌟 100가지 고유 타이틀 & 메타 디스크립션 순환 패턴 풀 ---
SEO_VARIATIONS = [
    ("{GU_NAME} {DONG_NAME} 출장 건식 마사지 & 힐링 케어 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 및 프리미엄 홈케어 전문. 검증된 관리사의 100% 후불제 안심 케어."),
    ("{GU_NAME} {DONG_NAME} 출장 스웨디시 & 프리미엄 테라피 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 전문 플랫폼. 선입금 전혀 없는 현장 결제로 편안하게 즐기는 테라피."),
    ("{GU_NAME} {DONG_NAME} 출장 아로마 마사지 1:1 맞춤 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 추천 코스. 지친 하루의 피로를 풀어주는 1:1 맞춤형 방문 힐링."),
    ("{GU_NAME} {DONG_NAME} 출장 정통 타이 마사지 정찰제 | 골목리스트", "{GU_NAME} {DONG_NAME} 출장 마사지 스웨디시 & 아로마 전문. 정찰제 요금으로 부담 없이 이용하세요."),
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

# 지역 데이터 (예시)
regions_data = {
    "seoul": {
        "jongno": {"name": "종로구", "dongs": ["청운동", "효자동", "사직동", "삼청동", "안국동", "종로1가"]},
        "jung": {"name": "중구", "dongs": ["무교동", "을지로", "명동", "충무로", "회현동"]}
    }
}

shops = [
    {"name": "🔥 한국미인홈케어", "desc": "서울·경기·인천 전지역 신속 방문! 정성 가득한 테라피 & 릴렉싱 프로그램", "phone": "0507-1280-3303", "price": "100,000원부터~"},
    {"name": "✨ 오늘밤테라피", "desc": "품격 있는 힐링을 선사하는 최고급 오일 프라이빗 방문 테라피 서비스", "phone": "0507-1280-3223", "price": "60,000원부터~"},
    {"name": "💎 주주테라피", "desc": "재방문율 1위! 칼도착 25분 보장, 철저한 위생 관리와 럭셔리 케어", "phone": "0507-1280-3193", "price": "60,000원부터~"}
]

# 🌟 네이버 SEO 유사문서 회피용 고유 본문/FAQ 생성기
def get_unique_content(region_name):
    char_sum = sum(ord(c) for c in region_name)
    
    bodies = [
        f"{region_name} 권역을 중심으로 빠르고 안전하게 이용할 수 있는 프리미엄 테라피 안내입니다. 바쁜 일상과 업무 스트레스로 뭉친 근육을 전문 테라피스트의 섬세한 손길로 풀어보세요. 선입금 요구가 없는 100% 현장 결제 시스템으로 내상 없이 쾌적한 힐링을 보장합니다.",
        f"조용하고 프라이빗한 휴식이 필요한 분들을 위해 {region_name} 전 지역 30분 내 방문 시스템을 갖췄습니다. 철저한 위생 관리와 검증된 관리사들의 체계적인 코스를 통해 {region_name} 거주 고객님들의 지친 심신을 완벽하게 리프레시 해드립니다.",
        f"대표 상권이자 주거 밀집 지역인 {region_name} 맞춤형 힐링 바디케어 서비스입니다. 멀리 샵까지 직접 이동할 필요 없이, 머무시는 자택이나 오피스텔, 숙박업소 등 어디서든 전화를 통해 간편하게 예약하고 품격 있는 케어를 경험하실 수 있습니다."
    ]
    
    faqs = [
        [
            {"q": f"{region_name} 지역은 몇 분 안에 도착하나요?", "a": f"교통 상황에 따라 다를 수 있으나, {region_name} 내 주요 지역은 배차 완료 후 평균 30분 이내에 신속하게 방문하는 것을 원칙으로 하고 있습니다."},
            {"q": "결제는 언제 어떻게 하나요?", "a": "최근 빈번한 예약금 사기를 방지하기 위해 관리사가 도착한 후 직접 결제(현금, 계좌이체 등)하는 100% 후불제로만 운영됩니다."}
        ],
        [
            {"q": f"{region_name} 주변 모텔이나 호텔에서도 이용 가능한가요?", "a": f"네, {region_name} 인근의 자택은 물론 오피스텔, 호텔, 모텔 등 고객님이 머무시는 모든 프라이빗한 공간에서 자유롭게 이용하실 수 있습니다."},
            {"q": "원하는 관리사 스타일을 요청할 수 있나요?", "a": "예약 상담 시 선호하시는 압의 세기(강한 타이, 부드러운 스웨디시 등)를 말씀해 주시면 가장 적합한 테라피스트를 매칭해 드립니다."}
        ]
    ]
    
    selected_body = bodies[char_sum % len(bodies)]
    selected_faq = faqs[char_sum % len(faqs)]
    
    faq_html = f"""
    <div style="background:#fff; border:1px solid #e3e8ee; border-radius:12px; padding:20px; margin-bottom:25px; box-shadow:0 2px 8px rgba(0,0,0,0.02);">
        <h3 style="font-size:16px; margin-bottom:15px; color:#c62828; font-weight:800;">💡 {region_name} 자주 묻는 질문</h3>
        <div style="margin-bottom:12px; padding:12px; background:#f8f9fa; border-radius:8px;">
            <p style="font-weight:700; color:#1d2a27; font-size:14px; margin-bottom:4px;">Q. {selected_faq[0]['q']}</p>
            <p style="font-size:13px; color:#46525f; line-height:1.4;">A. {selected_faq[0]['a']}</p>
        </div>
        <div style="padding:12px; background:#f8f9fa; border-radius:8px;">
            <p style="font-weight:700; color:#1d2a27; font-size:14px; margin-bottom:4px;">Q. {selected_faq[1]['q']}</p>
            <p style="font-size:13px; color:#46525f; line-height:1.4;">A. {selected_faq[1]['a']}</p>
        </div>
    </div>
    """
    
    return selected_body, faq_html

def generate_shop_cards(gu_name, region_name):
    cards_html = ""
    for s in shops:
        cards_html += f"""
        <a class="kt-shop" href="tel:{s['phone']}" rel="nofollow" style="text-decoration:none; display:block; margin-bottom:12px; background:#fff; border:1px solid #e3e8ee; border-radius:12px; padding:16px; box-shadow:0 2px 8px rgba(0,0,0,0.03);">
            <h4 style="font-size:16px; font-weight:bold; color:#1d2a27; margin:0 0 6px 0;">{s['name']} ({gu_name} {region_name} 맞춤 안내)</h4>
            <p style="font-size:13px; color:#46525f; margin:0 0 10px 0; line-height:1.4;">{s['desc']}</p>
            <div style="display:flex; justify-content:space-between; align-items:center; font-size:13px; border-top:1px solid #f1f3f5; padding-top:8px;">
                <span style="color:#c62828; font-weight:bold;">요금: {s['price']}</span>
                <span style="background:#c62828; color:#fff; padding:6px 12px; border-radius:6px; font-weight:bold; font-size:12px;">📞 전화 연결</span>
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

        gu_title = f"{gu_name} 출장 스웨디시 & 프리미엄 테라피 | 골목리스트"
        gu_desc = f"{gu_name} 전지역 구·동 출장 마사지 케어 및 프리미엄 홈타이 전문 안내. 검증된 관리사의 100% 후불제 안심 케어."

        # 🌟 구 단위 고유 텍스트 & FAQ 렌더링
        gu_body_text, gu_faq_html = get_unique_content(gu_name)

        # 👇 아래 f-string 안의 CSS는 반드시 {{ }} 를 사용합니다.
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
* {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Pretendard', sans-serif; -webkit-text-size-adjust: 100%; }}
body {{ background-color: #f4f6f8; color: #1d2a27; line-height: 1.5; padding-bottom: 90px; overflow-x: hidden; }}
.kt-wrap {{ width: 100%; max-width: 1180px; margin: 0 auto; padding: 0 15px; }}
.kt-utilbar {{ background: #1d2a27; color: #fff; font-size: 12px; padding: 6px 0; }}
.kt-utilbar .kt-wrap {{ display: flex; justify-content: flex-end; gap: 12px; }}
.kt-utilbar a {{ color: #fff; text-decoration: none; }}
.kt-logorow {{ background: #fff; padding: 12px 0; border-bottom: 1px solid #e3e8ee; }}
.kt-logorow .kt-wrap {{ display: flex; justify-content: space-between; align-items: center; }}
.kt-logo {{ font-size: 20px; font-weight: 800; color: #c62828; text-decoration: none; }}
.kt-menubar {{ background: #2c3e50; color: #fff; overflow-x: auto; white-space: nowrap; }}
.kt-menubar .kt-wrap {{ display: flex; gap: 15px; padding: 10px 15px; }}
.kt-menubar a {{ color: #fff; text-decoration: none; font-weight: 600; font-size: 14px; flex-shrink: 0; }}
.kt-wrap-body {{ width: 100%; max-width: 800px; margin: 15px auto; padding: 0 12px; }}
.kt-crumb {{ font-size: 12px; color: #666; margin-bottom: 12px; word-break: break-all; }}
.kt-crumb a {{ color: #666; text-decoration: none; }}
.kt-hero {{ background: #fff; border: 1px solid #e3e8ee; border-radius: 12px; padding: 18px; margin-bottom: 15px; }}
.kt-hero h1 {{ font-size: 18px; font-weight: 800; margin-top: 4px; color: #1d2a27; word-break: keep-all; }}
.kt-seo-content {{ margin-top: 15px; padding-top: 15px; border-top: 1px solid #f1f3f5; }}
.kt-sectitle {{ font-size: 16px; font-weight: 800; margin: 20px 0 10px 0; border-bottom: 2px solid #c62828; padding-bottom: 5px; }}
.kt-infobox {{ background: #fff; border: 1px solid #e3e8ee; border-radius: 12px; padding: 15px; font-size: 13px; color: #46525f; line-height: 1.6; word-break: keep-all; }}
.region-section {{ background: #fff; border: 1px solid #e3e8ee; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.02); }}
.region-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 8px; }}
.region-grid a:hover {{ background: #c62828; color: #fff; border-color: #c62828; }}
.oc-wrap {{ position: fixed; left: 0; right: 0; bottom: 0; z-index: 70; background: #fff; border-top: 1px solid #e3e8ee; box-shadow: 0 -4px 12px rgba(0,0,0,0.08); }}
.oc-note {{ margin: 0; padding: 6px 10px; text-align: center; font-size: 11px; background: #c62828; color: #ffe082; font-weight: 600; word-break: keep-all; }}
.oc-bar-in {{ display: flex; align-items: center; justify-content: space-between; max-width: 800px; margin: 0 auto; padding: 8px 12px; gap: 10px; }}
.oc-bar-name {{ font-weight: 800; font-size: 12px; color: #1d2a27; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
.oc-btn {{ background: #c62828; color: #fff; padding: 6px 12px; border-radius: 6px; text-decoration: none; font-weight: 700; font-size: 12px; flex-shrink: 0; }}
.unique-desc {{ font-size: 14px; color: #46525f; line-height: 1.6; margin-bottom: 20px; word-break: keep-all; text-align: justify; }}
</style>
</head>
<body>
<div class="kt-utilbar"><div class="kt-wrap">
    <a href="/area/">지역 정보</a>
    <a href="/partner/">제휴 문의</a>
</div></div>

<div class="kt-logorow"><div class="kt-wrap">
    <a class="kt-logo" href="https://golmokrest.netlify.app/">골목리스트</a>
    <div><a href="/partner/" style="background:#c62828; color:#fff; padding:6px 10px; border-radius:6px; text-decoration:none; font-size:12px; font-weight:700;">제휴 문의</a></div>
</div></div>

<div class="kt-menubar"><div class="kt-wrap">
    <a href="/area/">지역 찾기</a>
    <a href="/visit/">출장 홈케어</a>
    <a href="/story/">매거진</a>
    <a href="/partner/">입점 문의</a>
</div></div>

<div class="kt-wrap-body">
    <nav class="kt-crumb"><a href="https://golmokrest.netlify.app/">홈</a> › <a href="/area/">지역 전체보기</a> › <b>{gu_name}</b></nav>
    
    <div class="kt-hero">
        <div style="font-size: 12px; color: #c62828; font-weight: 700;">{gu_name} 지역 안내</div>
        <h1>{gu_name} 홈바디·출장마사지 동별 안내</h1>
        
        <!-- 🌟 SEO 치트키: 구 단위 고유 텍스트 및 FAQ 삽입 -->
        <div class="kt-seo-content">
            <p class="unique-desc">{gu_body_text}</p>
            {gu_faq_html}
        </div>
    </div>
    
    <div class="region-section">
        <h3 style="font-size:15px; margin-bottom:12px; font-weight:700;">📍 {gu_name} 하위 동 선택하기</h3>
        <div class="region-grid">
            {dongs_html}
        </div>
    </div>

    <h2 class="kt-sectitle"><span>{gu_name} 추천 제휴 샵</span></h2>
    <div>
        {gu_shop_cards_html}
    </div>
</div>

<div class="oc-wrap">
  <p class="oc-note">상단 <b>공식 제휴 샵</b>의 개별 번호를 통해 안전하게 이용하세요.</p>
  <div class="oc-bar-in">
    <div class="oc-bar-name">{gu_name} 제휴 안내</div>
    <a class="oc-btn" href="/partner/">제휴·입점 문의</a>
  </div>
</div>
</body>
</html>
"""

        with open(gu_file_path, "w", encoding="utf-8") as f:
            f.write(gu_html_content)
        total_gu_count += 1

        # 2. 각 동별 상세 페이지 생성
        for dong_name in dongs:
            dong_dir = os.path.join("area", city, gu_code, dong_name)
            os.makedirs(dong_dir, exist_ok=True)
            
            file_path = os.path.join(dong_dir, "index.html")
            shop_cards_html = generate_shop_cards(gu_name, dong_name)
            
            title_tpl, desc_tpl = next(seo_cycle)
            page_title = title_tpl.format(GU_NAME=gu_name, DONG_NAME=dong_name)
            page_desc = desc_tpl.format(GU_NAME=gu_name, DONG_NAME=dong_name)

            page_title = re.sub(r'(마사지\s*)+마사지', '마사지', page_title)
            page_desc = re.sub(r'(마사지\s*)+마사지', '마사지', page_desc)

            # 🌟 동 단위 고유 텍스트 및 FAQ 생성
            dong_body_text, dong_faq_html = get_unique_content(dong_name)

            content = template_content.replace("{PAGE_TITLE}", page_title)
            content = content.replace("{PAGE_DESC}", page_desc)
            content = content.replace("{GU_NAME}", gu_name)
            content = content.replace("{DONG_NAME}", dong_name)
            content = content.replace("{CITY}", city)
            content = content.replace("{GU_CODE}", gu_code)
            content = content.replace("{SHOP_CARDS}", shop_cards_html)
            
            # 🌟 template.html에 적용될 텍스트 치환
            content = content.replace("{UNIQUE_INTRO}", f"<p style='font-size:13px; color:#46525f; line-height:1.6; margin-bottom:20px; word-break:keep-all; text-align:justify;'>{dong_body_text}</p>")
            content = content.replace("{UNIQUE_FAQ}", dong_faq_html)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
                
            total_dong_count += 1

print(f"총 {total_gu_count}개의 구(Gu) 페이지 및 {total_dong_count}개의 동 페이지 생성 완료!")