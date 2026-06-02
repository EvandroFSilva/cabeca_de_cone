## Dependencias

Instale os pacotes em `python-service/requirements.txt`.

## Passos

1. Gerar o dataset organizado:

```bash
python python-service/yolo/prepare_dataset.py --overwrite
```

2. Treinar o modelo:

```bash
python python-service/yolo/train.py --weights yolo11n-cls.pt
```

O `train.py` usa por padrao a pasta `dataset/yolo_cls` como entrada.

3. Gerar o CSV para as imagens de teste:

```bash
python python-service/yolo/predict_test.py
```

## Observacao importante

Use `yolo11n-cls.pt`, que e o checkpoint de classificacao do YOLO11. Este dataset nao usa caixas delimitadoras; ele usa rotulos por imagem vindos do `train.csv`.
