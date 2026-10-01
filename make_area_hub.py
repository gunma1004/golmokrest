import os

# 전체 지역 데이터 구조 (시·구·군별 대표 링크 매핑용)
all_regions = {
    "서울 특별시 (25개 자치구)": [
        ("종로구", "seoul", "jongno"), ("중구", "seoul", "jung"), ("용산구", "seoul", "yongsan"), 
        ("성동구", "seoul", "seongdong"), ("광진구", "seoul", "gwangjin"), ("동대문구", "seoul", "dongdaemun"), 
        ("중랑구", "seoul", "jungnang"), ("성북구", "seoul", "seongbuk"), ("강북구", "seoul", "gangbuk"), 
        ("도봉구", "seoul", "dobong"), ("노원구", "seoul", "nowon"), ("은평구", "seoul", "eunpyeong"), 
        ("서대문구", "seoul", "seodaemun"), ("마포구", "seoul", "mapo"), ("양천구", "seoul", "yangcheon"), 
        ("강서구", "seoul", "gangseo"), ("구로구", "seoul", "guro"), ("금천구", "seoul", "geumcheon"), 
        ("영등포구", "seoul", "yeongdeungpo"), ("동작구", "seoul", "dongjak"), ("관악구", "seoul", "gwanak"), 
        ("서초구", "seoul", "seocho"), ("강남구", "seoul", "gangnam"), ("송파구", "seoul", "songpa"), 
        ("강동구", "seoul", "gangdong")  # 한글 '강동구' 오타를 영문 'gangdong'으로 수정 완료
    ],
    "경기도 (시·군·구 분구 포함)": [
        ("수원시 장안구", "gyeonggi", "suwon-jangan"), ("수원시 권선구", "gyeonggi", "suwon-gwonseon"), 
        ("수원시 팔달구", "gyeonggi", "suwon-paldal"), ("수원시 영통구", "gyeonggi", "suwon-yeongtong"),
        ("성남시 수정구", "gyeonggi", "seongnam-sujeong"), ("성남시 중원구", "gyeonggi", "seongnam-jungwon"), 
        ("성남시 분당구", "gyeonggi", "seongnam-bundang"),
        ("의정부시", "gyeonggi", "uijeongbu"), 
        ("안양시 만안구", "gyeonggi", "anyang-manan"), ("안양시 동안구", "gyeonggi", "anyang-dongan"),
        ("부천시 원미구", "gyeonggi", "bucheon-wonmi"), ("부천시 소사구", "gyeonggi", "bucheon-sosa"), 
        ("부천시 오정구", "gyeonggi", "bucheon-ojeong"),
        ("광명시", "gyeonggi", "gwangmyeong"), ("평택시", "gyeonggi", "pyeongtaek"), ("동두천시", "gyeonggi", "dongducheon"),
        ("안산시 상록구", "gyeonggi", "ansan-sangrok"), ("안산시 단원구", "gyeonggi", "ansan-danwon"),
        ("고양시 덕양구", "gyeonggi", "goyang-deogyang"), ("고양시 일산동구", "gyeonggi", "goyang-ilsandong"), 
        ("고양시 일산서구", "gyeonggi", "goyang-ilsanseo"),
        ("과천시", "gyeonggi", "gwacheon"), ("구리시", "gyeonggi", "guri"), ("남양주시", "gyeonggi", "namyangju"),
        ("오산시", "gyeonggi", "osan"), ("시흥시", "gyeonggi", "siheung"), ("군포시", "gyeonggi", "gunpo"),
        ("의왕시", "gyeonggi", "uiwang"), ("하남시", "gyeonggi", "hanam"),
        ("용인시 처인구", "gyeonggi", "yongin-cheoin"), ("용인시 기흥구", "gyeonggi", "yongin-giheung"), 
        ("용인시 수지구", "gyeonggi", "yongin-suji"),
        ("파주시", "gyeonggi", "paju"), ("이천시", "gyeonggi", "icheon"), ("안성시", "gyeonggi", "anseong"),
        ("김포시", "gyeonggi", "gimpo"), ("화성시", "gyeonggi", "hwaseong"), ("광주시", "gyeonggi", "gwangju"),
        ("양주시", "gyeonggi", "yangju"), ("포천시", "gyeonggi", "pocheon"), ("여주시", "gyeonggi", "yeoju"),
        ("연천군", "gyeonggi", "yeoncheon"), ("가평군", "gyeonggi", "gapyeong"), ("양평군", "gyeonggi", "yangpyeong")
    ],
    "인천광역시 (자치구·군)": [
        ("제물포구", "incheon", "jemulpo"), ("영종구", "incheon", "yeongjong"), ("미추홀구", "incheon", "michuhol"),
        ("연수구", "incheon", "yeonsu"), ("남동구", "incheon", "namdong"), ("부평구", "incheon", "bupyeong"),
        ("계양구", "incheon", "gyeyang"), ("서해구", "incheon", "seohae"), ("검단구", "incheon", "geomdan"),
        ("강화군", "incheon", "ganghwa"), ("옹진군", "incheon", "ongjin")
    ]
}

# area 폴더 생성
os.makedirs("area", exist_ok=True)

# 메타 태그 값 정의
hub_page_title = "수도권 홈바디·출장마사지 지역 전체보기 (서울·경기·인천) | 골목리스트"
hub_page_desc = "서울, 경기, 인천 출장 마사지 전 지역 시·구·동 홈케어 및 딥 아로마 스웨디시 제휴 업체 통합 안내. 24시간 실시간 예약 상담."

# HTML 내용 구성
html_content = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<meta name="naver-site-verification" content="e077c41bc3896bcecf18407976496548bea3a79c" />

<!-- 검색엔진 최적화(SEO) 타이틀 & 디스크립션 -->
<title>{hub_page_title}</title>
<meta name="description" content="{hub_page_desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://golmokrest.netlify.app/area/">

<!-- SNS 공유 메타 태그 -->
<meta property="og:site_name" content="골목리스트">
<meta property="og:locale" content="ko_KR">
<meta property="og:type" content="website">
<meta property="og:title" content="{hub_page_title}">
<meta property="og:description" content="{hub_page_desc}">
<meta property="og:url" content="https://golmokrest.netlify.app/area/">

<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard-dynamic-subset.min.css" />
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Pretendard', sans-serif; -webkit-text-size-adjust: 100%; }}
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
.content-wrap {{ max-width: 1180px; margin: 30px auto; padding: 0 15px; }}
h1 {{ font-size: 24px; font-weight: 800; margin-bottom: 25px; color: #1d2a27; border-left: 5px solid #c62828; padding-left: 12px; }}
.region-section {{ background: #fff; border: 1px solid #e3e8ee; border-radius: 12px; padding: 25px; margin-bottom: 25px; box-shadow: 0 2px 8px rgba(0,0,0,0.02); }}
.region-section h2 {{ font-size: 18px; font-weight: 700; color: #2c3e50; margin-bottom: 15px; border-bottom: 2px solid #f1f3f5; padding-bottom: 8px; }}
.region-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 10px; }}
.region-grid a {{ background: #f8f9fa; border: 1px solid #e3e8ee; padding: 12px 15px; border-radius: 8px; text-align: center; color: #333; text-decoration: none; font-weight: 600; font-size: 14px; transition: all 0.2s; }}
.region-grid a:hover {{ background: #c62828; color: #fff; border-color: #c62828; }}
.kt-foot {{ background: #1d2a27; color: #adb5bd; padding: 30px 0; font-size: 13px; margin-top: 50px; text-align: center; }}
</style>
</head>
<body>
<div class="kt-utilbar"><div class="kt-wrap">
    <a href="/">홈으로</a>
    <a href="/partner/">제휴 문의</a>
</div></div>

<div class="kt-logorow"><div class="kt-wrap">
    <a class="kt-logo" href="/">골목리스트</a>
    <div><a href="/partner/" style="background:#c62828; color:#fff; padding:8px 14px; border-radius:6px; text-decoration:none; font-size:13px; font-weight:700;">제휴 문의</a></div>
</div></div>

<div class="kt-menubar"><div class="kt-wrap">
    <a href="/area/">지역 찾기</a>
    <a href="/visit/">출장 홈케어</a>
    <a href="/story/">골목 매거진</a>
    <a href="/partner/">입점 문의</a>
</div></div>

<div class="content-wrap">
    <nav style="font-size: 13px; color: #666; margin-bottom: 15px;"><a href="/" style="color:#666; text-decoration:none;">홈</a> › <b>지역 전체보기</b></nav>
    <h1>수도권 홈바디·출장마사지 지역 전체보기</h1>
"""

for category, regions in all_regions.items():
    html_content += f"""
    <div class="region-section">
        <h2>{category}</h2>
        <div class="region-grid">
    """
    for name, city, code in regions:
        html_content += f'<a href="/area/{city}/{code}/">{name}</a>\n'
    
    html_content += """
        </div>
    </div>
    """

html_content += """
</div>

<footer class="kt-foot">
    <p>&copy; 2026 골목리스트 All Rights Reserved.</p>
</footer>
</body>
</html>
"""

with open("area/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("지역 전체보기 페이지 (area/index.html) 생성 완료!")