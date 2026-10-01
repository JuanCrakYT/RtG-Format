RtG-CLI — 도움말
=================

RtG-CLI는 RtG-Format 생태계의 명령줄 인터페이스입니다.
애드온 검색 및 실행, 언어 쿼리, 규칙 및 버전 보기를 가능하게 합니다.

사용법
-------

  rtg [옵션] <명령어> [인수]

  첫 번째 인수는 실행할 명령어 또는 애드온을 식별합니다.

  예시:
    rtg image
    rtg preview
    rtg help image


시스템 명령어
--------------

  -h, --help        이 일반 도움말 표시
  -v, --version     RtG-CLI 버전 표시
  -l, --lang        RtG-CLI에서 사용 가능한 언어 나열
  -r, --rules       RtG-CLI 규칙 표시
  -c, --commands    RtG-CLI 내부 명령어 나열
  -a, --addons      사용자에게 보이는 문서가 있는 애드온 나열
  -u, --usage       일반 사용법 정보 표시 (신규)
  -u-<언어>         특정 언어 사용법 표시 (예: -u-es, -u-en) (신규)
  --usage-<언어>     특정 언어 사용법 표시 (예: --usage-es, --usage-en) (신규)
  -language <언어>    시작 텍스트 (void) 언어 설정

명령어: help
---------------

  rtg help                    # 일반 도움말 (이 화면)
  rtg help <명령어>           # 특정 명령어/애드온 도움말
  rtg help <명령어> -<언어>     # 특정 언어 도움말 (예: -es, -en)
  rtg help <명령어> -lang       # 해당 명령어의 사용 가능한 언어
  rtg help -u                  # 일반 도움말 (신규)
  rtg help -u-<언어>           # 특정 언어 도움말 (예: -u-es) (신규)
  rtg help --usage             # 일반 도움말 (신규)
  rtg help --usage-<언어>       # 특정 언어 도움말 (예: --usage-es) (신규)
  rtg help usage               # 일반 도움말 (대체 구문, 신규)

  예시:
    rtg help image
    rtg help image -en
    rtg help image -lang
    rtg help -u
    rtg help -u-en
    rtg help --usage-es


명령어: version
------------------

  rtg -v
  rtg --version

  버전 및 모든 사용 가능한 언어의 버전 내용 표시.


명령어: rules
----------------

  rtg -r
  rtg --rules
  rtg -r -<언어>   # 특정 언어 규칙 (예: rtg -r -en)

  기본적으로 'rules'에서 정의된 첫 번째 언어 (스페인어) 사용.


명령어: lang
---------------

  rtg -l
  rtg --lang

  모든 사용 가능한 언어를 카테고리별로 나열:
  Version, Rules, Help, Void, 및 애드온별.


명령어: commands
---------------------

  rtg -c
  rtg --commands

  RtG-CLI 내부 명령어만 나열.
  애드온 명령어는 포함하지 않음.


명령어: addons
----------------

  rtg -a
  rtg --addons

  사용자에게 보이는 문서/도움말이 있는 애드온 나열.
  문서 없는 등록된 애드온은 여기에 표시되지 않음.


명령어: usage
-----------------

  rtg -u
  rtg --usage
  rtg -u-<언어>         # 특정 언어 사용법 (예: -u-es, -u-en) (신규)
  --usage-<언어>         특정 언어 사용법 표시 (예: --usage-es, --usage-en) (신규)

  요청된 언어로 일반 사용법 정보 (void) 표시.
  언어는 assets.json의 'void-language'에 존재해야 함.


명령어: language
--------------------

  rtg -language <언어>

  시작 텍스트 (void) 언어 선택.
  해당 언어는 assets.json의 'void-language'에 존재해야 함.

  예시:
    rtg -language en


사용 가능한 애드온
---------------------

  image      | RtG Image        - 이미지 변환기
  preview    | RtG Preview      - RtG-Format 빌드 3D 뷰어
  test-addon | RtG Test Addon   - CLI 검증용 테스트 애드온


언어
-------

언어는 단일 하이픈으로 표시: -es, -en, -pt 등.
언어는 내부 명령어 이름을 변경하지 않음.

  rtg help image -es    # 스페인어 도움말
  rtg help image -en    # 영어 도움말
  rtg -r -en            # 영어 규칙

  애드온 언어 보기:
    rtg help image -lang

  -lang의 의미는 위치에 따라 다름:
    rtg --lang          # RtG-CLI 언어 (애드온 전)
    rtg image -lang     # 애드온 언어 (애드온 후)


애드온 인수
--------------

애드온 식별 후, 인수는 접두사로 분류:

  하이픈 없음       -> 애드온        (예: convert, file.png)
  --옵션           -> 애드온        (예: --width 128)
  -옵션            -> RtG-CLI      (예: -lang, -en)

예시:
  rtg image convert file.png     # convert, file.png -> 애드온
  rtg image --width 128          # --width 128 -> 애드온
  rtg image -lang                # -lang -> RtG-CLI (애드온 언어)
  rtg image -en                  # -en -> RtG-CLI (언어 선택기)


공백이 있는 인수
-------------------

공백이 포함된 인수는 따옴표로 묶어야 함:

  rtg image "my image.png" "output.json"

RtG-CLI는 인수 순서를 보존하고 그대로 애드온에 전달.


추가 정보
--------------

  rtg help <명령어>      # 애드온 상세 도움말
  rtg help <명령어> -lang  # 해당 애드온 언어
  rtg --addons           # 모든 문서화된 애드온 보기
  rtg --commands         # 내부 명령어 보기