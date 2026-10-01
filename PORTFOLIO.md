# Apresentação do projeto no portfólio

**Nome:** Sentinela Logs — análise defensiva de autenticação.

**Objetivo:** facilitar a identificação de padrões suspeitos em logs e organizar evidências para investigação.

**Tecnologias:** Python, JSON Lines, unittest, Git e GitHub Actions.

**Conhecimentos demonstrados:** validação de entradas, tratamento de exceções, análise de eventos em janelas temporais, regras de detecção, documentação e testes automatizados.

**Demonstração:** executar o arquivo de exemplo e explicar os dois alertas. Alterar o limiar e a janela para observar como as regras afetam o resultado.

**Resultado verificável do exemplo:** sete eventos válidos, nenhuma linha rejeitada e dois alertas. Os testes incluem eventos fora de ordem, expiração da janela, separação por IP e sucesso de outra conta.

**Impacto esperado:** apoiar a triagem e reduzir o esforço de revisão manual. O projeto ainda não foi validado em um ambiente real; não há métricas de economia de tempo ou incidentes evitados.

**Como apresentar sua participação:** este material foi preparado com auxílio de IA. Antes de apresentá-lo como experiência própria, execute, estude e adapte o código. Registre no README as alterações que você realmente realizou e os aprendizados que consegue explicar.

**Exercício para personalizar:** crie novos dados fictícios, escreva um teste para IPv6 e implemente exportação CSV. Documente o problema, a decisão e o resultado de cada alteração.
