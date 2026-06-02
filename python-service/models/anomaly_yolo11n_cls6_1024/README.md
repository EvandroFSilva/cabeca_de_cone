# Modelo treinado YOLO11-cls

Esta pasta contem os artefatos do melhor treino feito para o classificador de falhas.

## Uso na API

O `python-service/app/model_loader.py` carrega por padrao:

`python-service/models/anomaly_yolo11n_cls6_1024/best.pt`

## Resumo do treino

- Base: `yolo11n-cls.pt`
- Tamanho de imagem: `1024`
- Melhor epoca: `18`
- Melhor `accuracy_top1`: `0.98333`
- `val/loss` na melhor epoca: `0.10938`

## Arquivos

- `best.pt`: peso recomendado para inferencia
- `last.pt`: ultimo peso salvo
- `results.csv`: historico completo do treino
- `results.png`: curva de treino
- `confusion_matrix.png`: matriz de confusao
- `confusion_matrix_normalized.png`: matriz normalizada
- `args.yaml`: parametros usados no treino
