#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
카카오 로컬 API 테스트 스크립트
"""

import os
import requests
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

def test_kakao_local_api():
    """카카오 로컬 API 테스트"""
    
    # API 키 확인
    api_key = os.getenv('KAKAO_REST_API_KEY')
    if not api_key:
        print("❌ KAKAO_REST_API_KEY 환경변수가 설정되지 않았습니다.")
        print("📝 env.example 파일을 참고하여 .env 파일을 생성하세요.")
        return False
    
    print(f"✅ API 키 확인됨: {api_key[:10]}...")
    
    # 테스트 주소
    test_addresses = [
        "서울특별시 성북구 안암로 145 고려대학교",
        "서울특별시 관악구 관악로 1 서울대학교",
        "서울특별시 서대문구 신촌로 134 연세대학교"
    ]
    
    api_url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {
        'Authorization': f'KakaoAK {api_key}'
    }
    
    print(f"\n🗺️  카카오 로컬 API 테스트 시작...")
    print("=" * 60)
    
    for i, address in enumerate(test_addresses, 1):
        print(f"\n{i}. 주소: {address}")
        
        try:
            params = {'query': address}
            response = requests.get(api_url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data['documents']:
                    result = data['documents'][0]
                    print(f"   ✅ 성공!")
                    print(f"   📍 좌표: ({result['y']}, {result['x']})")
                    print(f"   🏠 정확한 주소: {result['address_name']}")
                else:
                    print(f"   ❌ 주소를 찾을 수 없습니다.")
            else:
                print(f"   ❌ API 호출 실패: {response.status_code}")
                print(f"   📄 응답: {response.text}")
                
        except Exception as e:
            print(f"   ❌ 오류 발생: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ 테스트 완료!")
    return True

if __name__ == "__main__":
    test_kakao_local_api() 