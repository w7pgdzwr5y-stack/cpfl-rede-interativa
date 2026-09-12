#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Importador de dados EPE
Baixa e processa dados da Empresa de Pesquisa Energética
"""

import json
import argparse
from datetime import datetime

class ImportadorEPE:
    """
    Importador de dados da EPE
    
    Dados podem ser obtidos em: https://webmap.epe.gov.br
    Formatos suportados: GeoJSON, Shapefile, KML
    """
    
    def __init__(self):
        self.url_webmap = "https://webmap.epe.gov.br"
        print(f"\n📍 Acesse {self.url_webmap} para baixar dados")
        print("   Formatos disponíveis:")
        print("   - GeoJSON (recomendado)")
        print("   - Shapefile")
        print("   - KML")
    
    def processar_geojson_epe(self, arquivo_entrada: str) -> dict:
        """
        Processa arquivo GeoJSON da EPE
        """
        print(f"📂 Carregando arquivo: {arquivo_entrada}")
        
        try:
            with open(arquivo_entrada, 'r', encoding='utf-8') as f:
                geojson = json.load(f)
            
            # Adicionar metadados
            geojson['metadata'] = {
                'fonte': 'EPE',
                'data_sincronizacao': datetime.now().isoformat(),
                'total_features': len(geojson.get('features', []))
            }
            
            print(f"✅ {len(geojson.get('features', []))} features carregadas")
            return geojson
        except Exception as e:
            print(f"❌ Erro ao carregar arquivo: {str(e)}")
            return None
    
    def salvar_geojson(self, geojson: dict, arquivo_saida: str):
        """
        Salva GeoJSON processado
        """
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            json.dump(geojson, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Dados salvos em {arquivo_saida}")
    
    def executar(self, arquivo_entrada: str = None, arquivo_saida: str = "data/features_epe.json"):
        """
        Executa o importador
        """
        print("🔄 Importador EPE iniciado")
        
        if not arquivo_entrada:
            print("\n⚠️  Instruções:")
            print("1. Acesse https://webmap.epe.gov.br")
            print("2. Baixe os dados em formato GeoJSON")
            print(f"3. Execute: python3 tools/importador_epe.py --input seu_arquivo.geojson --output {arquivo_saida}")
            return
        
        geojson = self.processar_geojson_epe(arquivo_entrada)
        if geojson:
            self.salvar_geojson(geojson, arquivo_saida)
            print("\n✅ Importação concluída!")
        else:
            print("\n❌ Importação falhou")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Importador de dados EPE")
    parser.add_argument('--input', help='Arquivo GeoJSON de entrada (obtido em webmap.epe.gov.br)')
    parser.add_argument('--output', default='data/features_epe.json', help='Arquivo de saída')
    args = parser.parse_args()
    
    importador = ImportadorEPE()
    importador.executar(args.input, args.output)
