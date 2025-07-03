#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
카카오 API 상태 확인 스크립트
"""

import os
import requests
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

def check_kakao_api_status():
    """카카오 API 상태 확인"""
    
    # API 키 확인
    api_key = os.getenv('KAKAO_REST_API_KEY')
    if not api_key:
        print("❌ KAKAO_REST_API_KEY 환경변수가 설정되지 않았습니다.")
        return False
    
    print(f"✅ API 키 확인됨: {api_key[:10]}...")
    
    # 1. 로컬 API 테스트
    print("\n1️⃣ 로컬 API 테스트:")
    print("-" * 40)
    
    local_url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {'Authorization': f'KakaoAK {api_key}'}
    
    try:
        response = requests.get(local_url, headers=headers, params={'query': '서울대학교'}, timeout=10)
        print(f"   상태 코드: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ 로컬 API 정상 작동")
        elif response.status_code == 403:
            print("   ❌ 로컬 API 비활성화 또는 권한 없음")
            print("   📝 해결방법: 카카오 개발자 센터에서 로컬 서비스 활성화 필요")
        else:
            print(f"   ⚠️  예상치 못한 응답: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 오류: {str(e)}")
    
    # 2. 사용자 정보 API 테스트 (기본 권한 확인)
    print("\n2️⃣ 사용자 정보 API 테스트:")
    print("-" * 40)
    
    user_url = "https://kapi.kakao.com/v2/user/me"
    
    try:
        response = requests.get(user_url, headers=headers, timeout=10)
        print(f"   상태 코드: {response.status_code}")
        
        if response.status_code == 401:
            print("   ❌ 인증 실패 - API 키 확인 필요")
        elif response.status_code == 403:
            print("   ❌ 권한 없음 - 동의항목 설정 필요")
        else:
            print(f"   📄 응답: {response.text[:100]}...")
            
    except Exception as e:
        print(f"   ❌ 오류: {str(e)}")
    
    print("\n" + "=" * 50)
    print("💡 권장 해결 방법:")
    print("1. 카카오 개발자 센터에서 새 애플리케이션 생성")
    print("2. Web 플랫폼 등록 (도메인: localhost)")
    print("3. 동의항목에서 '위치 정보 수집' 추가")
    print("4. REST API 키를 환경변수에 설정")

if __name__ == "__main__":
    check_kakao_api_status() 