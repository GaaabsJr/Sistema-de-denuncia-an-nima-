# Justificativa de Decisões de Modelagem

**Disciplina:** Engenharia de Software (CC0116) — Prof. Adolfo Colares — UNIFAP 2026.1  
**Projeto:** Sistema de Denúncia Anônima  
**Equipe:** Cauan Miranda · Eric Fernandes · Gabriel Lima · Johan Natividade · João Lucas Farias De Sena

---

## 1. Por que escolhemos essas classes? Como derivamos das User Stories?

As classes foram extraídas diretamente das User Stories e dos Requisitos Funcionais. A classe **Denuncia** é o coração do sistema — ela aparece em praticamente todas as histórias de usuário (US-01, US-04, US-08). A classe **Administrador** surgiu das histórias US-05 a US-10, que descrevem todo o fluxo de gestão dos casos. **Evidencia** veio da US-03 (anexar arquivos), **Protocolo** veio da US-04 (acompanhamento por código), e **ComentarioInterno** e **HistoricoStatus** foram derivados dos requisitos RF-11 (comentários internos) e RF-14 (histórico de alterações). A classe abstrata **Usuario** foi criada pensando em evolução futura (RNF-06): hoje existe apenas o perfil Administrador, mas o diagrama já permite adicionar novos perfis sem reescrever o código.

---

## 2. Qual relacionamento foi mais difícil de decidir?

O relacionamento entre **Denuncia** e **HistoricoStatus** foi o mais debatido. A dúvida foi entre associação simples e composição. Optamos por **composição (◆)** porque, conforme RN-06, o histórico deve ser preservado mas só existe em função de uma denúncia — se a denúncia for removida do sistema, seus registros de histórico perdem totalmente o sentido. O mesmo raciocínio se aplicou a **ComentarioInterno** e **Evidencia**: são partes que compõem a denúncia e não têm existência independente. Já o relacionamento entre **Administrador** e **Denuncia** ficou como **associação simples (0..*)** porque o administrador é uma entidade independente que pode existir sem gerenciar nenhuma denúncia (quando recém cadastrado, por exemplo).

---

## 3. Se o sistema crescer, que novas classes precisariam ser adicionadas? O design atual permite isso?

Sim, o design atual permite evolução com baixo impacto. A herança de **Usuario** permitiria adicionar facilmente um perfil **Supervisor** com acesso amplo ou um perfil **Auditor** com permissão somente leitura, sem alterar as classes existentes. Um módulo de **Notificação** poderia ser adicionado como uma classe independente que observa mudanças de status, sem modificar **Denuncia** ou **Administrador**. A separação das enumerações (**StatusDenuncia**, **CategoriaDenuncia**) facilita adicionar novos estados e categorias sem alterar a estrutura das classes. O único ponto de atenção é que, se surgirem múltiplos tipos de denunciante com atributos próprios (por exemplo, denunciante organizacional vs. individual), seria necessário criar uma hierarquia similar à de **Usuario** para o lado do cidadão — o que exigiria revisão do diagrama atual.