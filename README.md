# 📊 Modelo de Propensão à Inadimplência com Dashboard Analítico

## 📝 Sobre o Projeto

Este projeto implementa um modelo de Machine Learning (Random Forest) para prever a propensão à inadimplência de clientes, complementado por um dashboard interativo para análise dos resultados. O modelo foi treinado com dados históricos e utiliza diversas features para fazer previsões precisas sobre a probabilidade de inadimplência.

## 🚀 Tecnologias Utilizadas

### Modelo de Machine Learning
- **Python 3.7+**
- **Scikit-learn**: 
  - RandomForestClassifier
  - train_test_split
  - MinMaxScaler
  - Métricas (precision_score, recall_score, f1_score, accuracy_score, roc_auc_score)
- **Pandas**: Manipulação e análise de dados
- **NumPy**: Computação numérica
- **Matplotlib**: Visualizações básicas
- **Seaborn**: Visualizações estatísticas
- **Imbalanced-learn**: 
  - SMOTE para balanceamento de dados
  - Under/Over sampling
- **Joblib**: Salvamento e carregamento do modelo
- **PyODBC**: Conexão com SQL Server

### Dashboard e Visualização
- **Dash**: Framework para criação de dashboards interativos
- **Plotly**: 
  - Express para gráficos rápidos
  - Graph Objects para gráficos personalizados
- **Dash Bootstrap Components**: Componentes de UI responsivos
- **Dash DataTable**: Tabelas interativas e ordenáveis
- **Flask**: Servidor web base

### Processamento e Análise
- **Openpyxl**: Leitura de arquivos Excel
- **Pandas**: 
  - Manipulação de dados
  - Agregações
  - Transformações
  - Análise exploratória

### Desenvolvimento e Qualidade
- **Git**: Controle de versão
- **Python warnings**: Tratamento de avisos
- **Try/Except**: Tratamento de erros

### Ambiente e Deploy
- **Flask**: Servidor web
- **Dash**: Servidor de desenvolvimento
- **Porta 8050**: Porta padrão do servidor

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/GabrielHenriqueCA/loan-default-prediction.git
cd default_prone_model/src
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🎯 Funcionalidades Implementadas

### 1. Modelo de Propensão
- Treinamento com Random Forest
- Features importantes:
  - Histórico de atrasos
  - Valor do financiamento
  - Idade do cliente
  - Localização
  - Outros fatores relevantes
- Métricas de avaliação:
  - Acurácia

### 2. Dashboard Analítico
#### Métricas Principais
- Probabilidade média de inadimplência
- Valor total em risco
- Média de dias em atraso

#### Visualizações
- Gráfico de barras por estado com:
  - Probabilidade de inadimplência
  - Valor médio de financiamento (normalizado)
  - Dias médios de atraso (normalizado)
- Gráfico de pizza para distribuição de risco
- Mapa de calor por região
- Gráfico de tendência temporal

#### Tabela de Contratos
- Lista dos 10 contratos com maior risco
- Ordenação por qualquer coluna
- Formatação automática de valores monetários e percentuais


## 🎨 Personalização

O dashboard utiliza uma paleta de cores personalizada que pode ser facilmente modificada no arquivo `app.py`:

```python
CORES = {
    'fundo': '#F8F9FA',
    'card': '#FFFFFF',
    'texto': '#2C3E50',
    'primaria': '#3498DB',
    'secundaria': '#E74C3C',
    'terciaria': '#2ECC71',
    'destaque': '#F1C40F'
}
```

## 🚀 Como Executar

1. Certifique-se de que o arquivo Excel está no diretório correto
2. Execute o servidor:
```bash
python app.py
```
3. Acesse o dashboard em: `http://localhost:8050`

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📧 Contato

Para sugestões, dúvidas ou contribuições, entre em contato através de:
- Email: gabrielhcacontato@gmail.com
- LinkedIn: https://www.linkedin.com/in/gabrielhenri/