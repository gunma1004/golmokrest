import os

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

# 템플릿 파일 읽기
with open("template.html", "r", encoding="utf-8") as f:
    template_content = f.read()

total_dong_count = 0
total_gu_count = 0

for city, gu_dict in regions_data.items():
    for gu_code, gu_info in gu_dict.items():
        gu_name = gu_info["name"]
        dongs = gu_info["dongs"]
        
        # 1. 구(Gu) 허브 페이지 생성 (동 목록 + 제휴샵 카드 포함)
        gu_dir = os.path.join("area", city, gu_code)
        os.makedirs(gu_dir, exist_ok=True)
        gu_file_path = os.path.join(gu_dir, "index.html")
        
        dongs_html = ""
        for dong in dongs:
            dongs_html += f'<a href="/area/{city}/{gu_code}/{dong}/" style="background:#f8f9fa; border:1px solid #e3e8ee; padding:12px 15px; border-radius:8px; text-align:center; color:#333; text-decoration:none; font-weight:600; font-size:14px; transition:all 0.2s;">{dong}</a>\n'

        gu_shop_cards_html = generate_shop_cards(gu_name, "전지역")

        gu_html_content = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<meta name="naver-site-verification" content="e077c41bc3896bcecf18407976496548bea3a79c" />
<title>{gu_name} 스웨디시 홈케어 제휴 정보 | 골목리스트</title>
<meta name="description" content="{gu_name} 지역 동별 스웨디시 및 홈케어 제휴 업체 안내">
<meta property="og:site_name" content="골목리스트">
<meta property="og:locale" content="ko_KR">
<meta property="og:type" content="website">
<meta property="og:title" content="{gu_name} 스웨디시 홈케어 제휴 정보 | 골목리스트">
<meta property="og:description" content="{gu_name} 지역 동별 스웨디시 및 홈케어 제휴 업체 안내">
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
    <h1>{gu_name} 지역 안내 및 동 선택</h1>
    
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

        # 2. 각 동별 상세 페이지 생성
        for dong_name in dongs:
            dong_dir = os.path.join("area", city, gu_code, dong_name)
            os.makedirs(dong_dir, exist_ok=True)
            
            file_path = os.path.join(dong_dir, "index.html")
            shop_cards_html = generate_shop_cards(gu_name, dong_name)
            
            content = template_content.replace("{GU_NAME}", gu_name)
            content = content.replace("{DONG_NAME}", dong_name)
            content = content.replace("{CITY}", city)
            content = content.replace("{GU_CODE}", gu_code)
            content = content.replace("{SHOP_CARDS}", shop_cards_html)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
                
            total_dong_count += 1

print(f"총 {total_gu_count}개의 구(Gu) 페이지(동 목록+제휴샵 포함) 및 {total_dong_count}개의 동 페이지 생성 완료!")