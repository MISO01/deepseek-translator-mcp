import os
import requests
from dotenv import load_dotenv

class DeepSeekTranslator:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY 환경 변수가 설정되지 않았습니다.")
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def translate(self, text, source_lang="korean", target_lang="chinese"):
        """
        한국어 텍스트를 중국어로 번역합니다.
        
        Args:
            text (str): 번역할 텍스트
            source_lang (str): 원본 언어 (기본값: korean)
            target_lang (str): 목표 언어 (기본값: chinese)
            
        Returns:
            str: 번역된 텍스트
        """
        prompt = f"""
        다음 {source_lang} 텍스트를 {target_lang}로 번역해주세요.
        원본 텍스트:
        {text}
        
        번역:
        """
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": f"You are a professional translator from {source_lang} to {target_lang}. Translate the text accurately without adding explanations."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 4000
        }
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"번역 오류: {str(e)}"

# 테스트 함수
def test_translation():
    translator = DeepSeekTranslator()
    test_text = "안녕하세요, 반갑습니다. 오늘 날씨가 정말 좋네요."
    translated = translator.translate(test_text)
    print(f"원본: {test_text}")
    print(f"번역: {translated}")

if __name__ == "__main__":
    test_translation() 