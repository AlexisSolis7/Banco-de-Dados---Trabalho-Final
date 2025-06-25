#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste da funcionalidade de IA do Sistema SiCoPluE
"""

import google.generativeai as genai
import json

# Configurar API
GEMINI_API_KEY = "AIzaSyA83Xy_avI2LjPBISqoBdhrMPdgyzNCNxU"
genai.configure(api_key=GEMINI_API_KEY)

def teste_ia():
    """Testa a funcionalidade de IA"""
    
    print("TESTE DA IA GEMINI")
    print("=" * 50)
    
    observacao_teste = "Chuva muito forte com granizo e vento, vi alguns alagamentos começando na rua da frente."
    
    prompt = f"""
Você é um assistente de análise de dados meteorológicos para um projeto escolar.

A observação a ser analisada é:
"{observacao_teste}"

Retorne suas conclusões estritamente no formato JSON:

{{
    "resumo": "Resuma tecnicamente em uma frase",
    "sentimento": "Normal, Preocupante, ou Severo",
    "palavras_chave": ["lista", "de", "fenômenos"],
    "impacto_observado": "Descreva os impactos",
    "fenomenos_identificados": ["fenômenos", "meteorológicos"],
    "nivel_confianca": "Alto, Médio, ou Baixo"
}}

Retorne apenas a estrutura JSON.
"""
    
    try:
        print(f"📝 Observação teste:")
        print(f'"{observacao_teste}"')
        print("\n🔄 Processando com IA...")
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        if response and response.text:
            print("\nResposta da IA:")
            print(response.text)
            
            # Limpar resposta removendo markdown
            texto_resposta = response.text.strip()
            
            if "```json" in texto_resposta:
                inicio = texto_resposta.find("```json") + 7
                fim = texto_resposta.find("```", inicio)
                if fim != -1:
                    texto_resposta = texto_resposta[inicio:fim].strip()
            elif "```" in texto_resposta:
                inicio = texto_resposta.find("```") + 3
                fim = texto_resposta.find("```", inicio)
                if fim != -1:
                    texto_resposta = texto_resposta[inicio:fim].strip()
            
            # Tentar parse JSON
            resultado = json.loads(texto_resposta)
            
            print("\nRESULTADO ESTRUTURADO:")
            print("-" * 30)
            print(f"Resumo: {resultado.get('resumo')}")
            print(f"Severidade: {resultado.get('sentimento')}")
            print(f"Palavras-chave: {resultado.get('palavras_chave')}")
            print(f"Impacto: {resultado.get('impacto_observado')}")
            print(f"Fenômenos: {resultado.get('fenomenos_identificados')}")
            print(f"Confiança: {resultado.get('nivel_confianca')}")
            
            print("\nTESTE CONCLUÍDO COM SUCESSO!")
            
        else:
            print("❌ Resposta vazia da IA")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    teste_ia()
