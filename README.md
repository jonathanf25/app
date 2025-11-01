# Omnichannel Support Platform

Este repositório contém um protótipo de plataforma omnichannel para atendimento humano, automações com bots/IA e integrações (ex.: WhatsApp). O foco é oferecer um ponto de partida para evoluir os requisitos descritos no backlog inicial.

## Estrutura

```
backend/
  app/
    routers/       # Endpoints organizados por domínio (departamentos, tickets, bots, etc.)
    schemas/       # Modelos Pydantic utilizados pela API
    services/      # Serviços de domínio (distribuição, bots, observabilidade...)
    utils/         # Utilitários de persistência em memória
    main.py        # Inicialização FastAPI
```

## Executando localmente

1. Crie um ambiente virtual (Python >= 3.11).
2. Instale as dependências:

   ```bash
   pip install -e .[dev]
   ```

3. Execute a aplicação com Uvicorn:

   ```bash
   uvicorn backend.app.main:app --reload
   ```

4. A documentação interativa estará disponível em `http://127.0.0.1:8000/docs`.

## Testes

Para executar a suíte de testes:

```bash
pytest
```

## Próximos passos sugeridos

- Substituir o armazenamento em memória por um banco persistente.
- Implementar autenticação, controle de permissões e auditoria completos.
- Integrar com provedores reais (WhatsApp Business Platform, motores NLP/LLM, CRMs).
- Evoluir dashboards e exportações para refletir métricas reais de operação.
- Acrescentar monitoramento e alertas integrados com ferramentas de observabilidade.
