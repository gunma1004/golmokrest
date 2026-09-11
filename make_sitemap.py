import os

# 사이트 기본 주소
base_url = "https://golmokrest.netlify.app"

# sitemap.xml 상단 헤더
sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{}/</loc>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>
""".strip()

# sitemap 구조를 열고 닫기 위해 리스트로 관리
urls = [f"{base_url}/"]

# area 폴더 안의 모든 하위 index.html 경로 탐색
area_dir = "area"
if os.path.exists(area_dir):
    for root, dirs, files in os.walk(area_dir):
        if "index.html" in files:
            # 윈도우 역슬래시(\)를 슬래시(/)로 변환
            rel_path = os.path.relpath(root, ".").replace("\\", "/")
            url = f"{base_url}/{rel_path}/"
            urls.append(url)

# XML 형식으로 조합
xml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
]

for url in urls:
    xml_lines.append("    <url>")
    xml_lines.append(f"        <loc>{url}</loc>")
    xml_lines.append("        <changefreq>weekly</changefreq>")
    xml_lines.append("        <priority>0.8</priority>")
    xml_lines.append("    </url>")

xml_lines.append('</urlset>')

# sitemap.xml 파일 저장
with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(xml_lines))

print(f"총 {len(urls)}개의 페이지 주소가 포함된 sitemap.xml 생성 완료!")