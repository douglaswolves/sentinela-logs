# Sentinela Logs 🛡️

Analisador defensivo de logs de autenticação em Python, com regras transparentes para identificar atividades que merecem investigação.

## Problema e objetivo

Falhas de login isoladas são comuns. Sequências de falhas em um intervalo curto podem indicar tentativas de adivinhar credenciais. Este projeto organiza eventos e gera alertas para apoiar a triagem de segurança.

## Funcionalidades

- Identifica cinco ou mais falhas do mesmo IP em uma janela de cinco minutos, por padrão.
- Destaca autenticação bem-sucedida após cinco falhas da mesma conta e IP na janela.
- Ordena eventos pelo horário e normaliza fusos para UTC.
- Valida IPs IPv4/IPv6, status, usuário e timestamp; informa linhas rejeitadas.
- Exporta relatório JSON e permite configurar limiar e janela.
- Inclui testes automatizados e configuração de CI para GitHub Actions.

## Executar

Requisito: Python 3.10 ou superior. Sem dependências externas.

Extraia o projeto e abra o terminal na pasta `sentinela-logs`:

```bash
python sentinela.py examples/demo.jsonl
python sentinela.py examples/demo.jsonl --threshold 5 --window 300 --output relatorio.json
python -m unittest discover -s tests -v
```

No Windows, se necessário, substitua `python` por `py`.

O exemplo contém sete eventos fictícios e produz dois alertas: `repeated_failures` e `success_after_failures`. O relatório esperado está em `examples/expected-report.json`.

## Formato de entrada

Um objeto JSON por linha, com todos os campos abaixo:

```json
{"timestamp":"2026-09-30T12:00:00Z","ip":"192.0.2.10","user":"admin","status":"failure"}
```

`timestamp` usa ISO 8601 com fuso (`Z` ou offset); `status` aceita `failure` ou `success`. Linhas vazias são ignoradas. Os IPs do exemplo são destinados à documentação.

Logs nativos do Windows, Linux, roteadores ou câmeras precisam ser convertidos para este formato antes da análise. O projeto não coleta logs automaticamente.

## Como as regras funcionam

A janela é inclusiva: um evento exatamente no limite ainda conta. Um alerta de falhas é emitido quando o IP atinge o limiar. Novos alertas para o mesmo IP ficam suprimidos enquanto a sequência permanece acima do limiar. Após sucesso suspeito, a sequência de falhas daquela conta é encerrada. Falhas distribuídas entre várias contas também podem gerar o alerta por IP, mas o alerta de sucesso exige falhas da mesma conta.

## Estrutura

- `sentinela.py`: leitura, validação, detecção e CLI.
- `tests/test_sentinela.py`: cenários de janela temporal, isolamento por IP, dados inválidos e regras.
- `examples/`: dados sintéticos e resultado esperado.
- `.github/workflows/tests.yml`: testes em três versões do Python.
- `PORTFOLIO.md`: roteiro para documentar e apresentar o trabalho.

## Limitações e interpretação

Os alertas são indícios, não confirmação de invasão. Erros de senha e usuários atrás de um mesmo IP podem causar falsos positivos. A regra de sucesso não prova comprometimento. A ferramenta analisa um arquivo completo em memória; para grandes volumes, uma evolução seria processamento incremental. Não detecta todos os ataques nem bloqueia acessos. Não substitui um SIEM.

## Publicar no GitHub

1. Crie um repositório vazio chamado `sentinela-logs` em sua conta, sem adicionar README ou licença pelo site.
2. Extraia o ZIP e abra um terminal na pasta do projeto.
3. Execute os testes e, com Git instalado, rode:

```bash
git init
git add .
git commit -m "Adiciona analisador defensivo de logs"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/sentinela-logs.git
git push -u origin main
```

Substitua `SEU-USUARIO` pelo seu usuário. A autenticação é feita pelo Git conforme sua configuração. Alternativamente, use **Add file → Upload files** no repositório; para incluir o workflow e outros arquivos ocultos, prefira Git.

Descrição sugerida para o repositório: “Analisador de logs de autenticação em Python para detectar falhas repetidas e sucessos suspeitos, com testes automatizados.”

Antes de publicar dados reais, remova informações pessoais e credenciais. O material de exemplo já é sintético.

## Próximas melhorias

- Adaptadores para logs de SSH e eventos do Windows.
- Exportação CSV e painel de visualização.
- Processamento incremental e métricas de falsos positivos.

## Licença

MIT. Veja `LICENSE`.
