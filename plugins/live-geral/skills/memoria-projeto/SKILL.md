---
name: memoria-projeto
description: Memória comum da LIVEIDEA (repositório live-memoria), em três níveis — agência, cliente e projeto. Use no começo de qualquer trabalho num job de cliente, para carregar o que já se sabe. Use também ao fechar uma etapa, tomar uma decisão, sair de uma reunião, receber aprovação ou veto do cliente ou encerrar um job, para registrar. Dispara com frases como "registra isso", "anota na memória", "o que já decidimos nesse job", "como esse cliente costuma aprovar", "abre um job novo na memória", "fecha a retrospectiva".
---

# Memória da LIVEIDEA

Você mantém a memória comum da agência. Ela vive no repositório `live-memoria`, em Markdown, e é compartilhada por todo o time. Fale sempre em português.

## Onde fica

Procure o repositório nesta ordem:

1. A variável de ambiente `LIVE_MEMORIA_DIR`, se existir.
2. Uma pasta `live-memoria` que seja repositório git, nos lugares de costume (`~/dev/liveidea/live-memoria`, `C:\dev\liveidea\live-memoria`).
3. Se não achar, pergunte o caminho uma vez. Se a pessoa não tiver o repositório, explique que ela precisa cloná-lo (ou pedir acesso ao Martech) e siga em **modo sem repositório** (fim deste arquivo).

O `README.md` do repositório descreve a estrutura e onde registrar cada coisa. Leia-o na primeira vez que usar a memória numa conversa.

```
agencia/resumo.md                       ← sempre lido
clientes/<cliente>/perfil.md            ← sempre lido
clientes/<cliente>/preferencias.md      ← sempre lido
clientes/<cliente>/<projeto>/resumo.md  ← sempre lido
(todo o resto)                          ← lido sob demanda
```

## 1. Ler — no começo do trabalho

1. Identifique cliente e projeto pelo pedido ou pela pasta em que a pessoa está. Na dúvida, pergunte.
2. Rode `git pull` para pegar a versão mais nova.
3. Leia **só os quatro arquivos "sempre lido"** acima.
4. Diga em 2 ou 3 linhas o que importa para a tarefa de agora (ex.: "o cliente vetou tom informal em 04/11; aprovação leva duas rodadas"). Não despeje o conteúdo.
5. Abra os outros arquivos **só quando a tarefa pedir**: o histórico de decisões em `decisoes.md`, o retorno de uma rodada em `feedbacks/`, uma reunião em `reunioes/`. Para achar algo específico, procure por palavra (grep) antes de abrir arquivos inteiros.

Se o cliente ou o projeto ainda não existir na memória, ofereça abrir (passo 3).

## 2. Registrar — ao fechar uma etapa

Fique atento a decisões, aprovações, vetos, reuniões e aprendizados durante a conversa. Ao fim de uma etapa, ou quando a pessoa pedir:

1. **Decida o lugar de cada coisa**, pela tabela "Onde registrar cada coisa" do README:
   - decisão do job → `decisoes.md`;
   - reunião → `reunioes/AAAA-MM-DD-tema.md`;
   - retorno do cliente → `feedbacks/AAAA-MM-DD-rodada-N.md`;
   - entrega → `entregas.md`;
   - padrão do cliente → `preferencias.md` ou `perfil.md`;
   - lição para qualquer job → `agencia/aprendizados.md`.
2. **Mostre exatamente o que vai gravar e onde, e espere o ok.** Nunca grave sem confirmação.
3. Com o ok: `git pull`; grave; **atualize o `resumo.md` do projeto** (estado atual, próximos passos, últimas 5 decisões); faça o commit e o push.
4. Mensagem de commit: `memoria(<cliente>/<projeto>): <resumo curto>`.
5. Confirme em uma linha o que foi gravado.

Regras de escrita:

- Em `decisoes.md` e `aprendizados.md`, **acrescente no fim e nunca apague**. Se algo mudou, registre a nova decisão.
- Formato de linha: `- AAAA-MM-DD · texto · por: <nome ou papel>`.
- O `resumo.md` é o único arquivo que você reescreve. Mantenha-o com no máximo 1 página.
- Se o push falhar por conflito, rode `git pull --rebase` e tente de novo. Como os logs só crescem no fim, o conflito costuma se resolver mantendo as duas linhas.

## 3. Abrir cliente ou projeto novo

1. Cliente novo: copie `_modelo/cliente/` para `clientes/<cliente>/`.
2. Projeto novo: copie `_modelo/projeto/` para `clientes/<cliente>/<projeto>/` (sem os arquivos `_modelo-*`).
3. Nomes em `kebab-case` minúsculo, sem acentos.
4. Preencha `contexto.md` e `resumo.md` com o que já se sabe do briefing. O que não se sabe vira pergunta aberta.
5. Mostre o resultado, peça o ok e faça o commit.

## 4. Encerrar um job

1. Proponha a retrospectiva em `agencia/retrospectivas/AAAA-<cliente>-<projeto>.md`, a partir de `_modelo/retrospectiva.md`, usando o que está na memória do projeto.
2. Proponha quais aprendizados sobem para `preferencias.md` do cliente e quais sobem para `agencia/aprendizados.md`.
3. Se algum aprendizado for importante o bastante, proponha levá-lo para `agencia/resumo.md`.
4. Grave só com o ok.

## Modo sem repositório

Quando a pessoa não tem o repositório local (por exemplo, no app do Claude):

- Para **ler**, use o conector do GitHub, se estiver ligado.
- Para **registrar**, entregue o texto pronto e diga em qual arquivo colar. A pessoa cola pelo site do GitHub ou envia para o Martech.

## O que nunca registrar

- Dados pessoais e contatos (telefone, e-mail, CPF).
- Valores financeiros, orçamentos e cachês.
- Senhas, tokens e chaves de API.
- Opiniões sobre pessoas com nome. O perfil descreve a empresa e os papéis.
- Conteúdo de cliente com NDA neste repositório (ele tem repositório próprio).

Na dúvida, pergunte antes de gravar.
