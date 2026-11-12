# Conectar o GitHub ao Claude

Mostre este guia ao usuário quando a skill não conseguir ler o repositório `Agencia-LIVEIDEA/id-liveidea`
(script com código 2 e nenhum conector GitHub disponível na conversa). Fale em linguagem simples,
sem termos técnicos, e passe os links exatamente como estão aqui.

## Mensagem para o usuário (adapte o tom, mantenha os passos)

Para aplicar a marca LIVEIDEA, eu preciso ler a versão mais recente do design system no repositório
`id-liveidea` do GitHub da agência. Ele é privado, então o Claude precisa estar conectado ao GitHub.
Recomendo fazer isso uma vez só, em cinco minutos:

1. **Conecte sua conta do GitHub ao Claude.** Abra https://claude.ai/customize/connectors, encontre o
   **GitHub** e clique em conectar. Entre com a conta do GitHub que tem acesso à organização
   **Agencia-LIVEIDEA** e autorize.
2. **Libere o repositório.** Se o GitHub pedir para escolher organizações ou repositórios, marque
   **Agencia-LIVEIDEA** e o repositório **id-liveidea**. Se o acesso não aparecer ou estiver bloqueado,
   instale o app do Claude no repositório em https://github.com/apps/claude/installations/select_target.
   Só o dono da organização no GitHub pode liberar esse acesso; se não for você, peça a ele.
3. **Se o GitHub não aparecer na lista de conectores**, o administrador da conta da agência no Claude
   precisa habilitar o conector GitHub para a organização. Peça a ele.
4. **Abra uma conversa nova.** Os conectores são carregados quando a conversa começa. Na conversa nova,
   confira no menu de ferramentas da conversa que o GitHub está ativado.
5. **Peça de novo.** Na primeira resposta eu informo a versão aplicada (ex.: "v1.2.0, main @ ce5a99f").
   Se aparecer a versão com o commit, a conexão está funcionando.

Se não der para conectar agora, há duas alternativas, nesta ordem:
- **Enviar o ZIP da `main`:** no GitHub, botão **Code** > **Download ZIP**, e me envie aqui. Funciona, mas eu
  não consigo garantir que é a última versão, e vai ser preciso repetir isso a cada mudança do design system.
- **Último caso, seguir com a cópia que vem na skill:** a skill traz uma cópia do design system da versão
  <versão e data de snapshot/VERSION>. Posso fazer a peça com ela, mas, se o design system mudou depois disso,
  a peça sai na versão antiga. Quer seguir assim?

## Regras para o Claude

- Recomende o conector como caminho principal. O ZIP é o plano B. A cópia do pacote é o último caso e só
  entra com o "sim" explícito do usuário, depois de ele saber a versão e a data da cópia.
- Não peça senha, token ou código de autorização na conversa. A conexão é feita pelo próprio usuário
  nos links acima.
- Não continue com a peça usando valores de memória. Enquanto o usuário decide, pode adiantar o texto e a
  estrutura do conteúdo, deixando claro que a marca será aplicada depois.
- Se o conector existe mas a leitura falha (erro de permissão ou "não encontrado"), o problema
  costuma ser o passo 2 (repositório não liberado). Diga isso ao usuário.
