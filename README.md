# Configuração de Servidor Web com Monitoramento

🚀 **Sobre o Projeto**  
Este projeto faz parte do programa de bolsas da Compass UOL, com foco em **Linux, AWS e automação de processos**. O objetivo é configurar um **servidor web** dentro de uma instância **EC2 na AWS**, garantindo sua **disponibilidade** e implementando um **sistema de monitoramento** para detectar possíveis falhas.

---
## 📌 Tecnologias Utilizadas
### ☁️ Infraestrutura em Nuvem (AWS)
- **Amazon VPC** → Rede isolada com sub-redes públicas e privadas.
- **Amazon EC2** → Instância de máquina virtual para o servidor web.
- **Internet Gateway** → Permite acesso externo às instâncias EC2.
- **Security Groups** → Regras de firewall para controle de tráfego HTTP e SSH.

### 🖥️ Sistema Operacional e Acesso
- **SO da Instância**: Amazon Linux (AMI escolhida).
- **Acesso SSH**: Feito pelo VS Code via *Remote - SSH* ou via terminal local com:
  ```bash
  ssh -i "chave.pem" usuario@ip-da-instancia
  ```
- **Alternativa**: Cliente SSH como PuTTY.

### 🌐 Servidor Web
- **Nginx** → Servidor HTTP para hospedar a página HTML.
- **Systemd** → Configura o Nginx para reiniciar automaticamente.

### 🔍 Monitoramento e Automação
- **Bash ou Python** → Script de monitoramento.
- **Curl (Bash) ou Requests (Python)** → Verifica a disponibilidade do site.
- **Logging** → Logs em `/var/log/monitoramento.log`.
- **Cron/Systemd Timers** → Agendamento a cada minuto.

### 📢 Notificações e Alertas
- **Telegram Bot** → Envia alertas quando o servidor cai.
- **Alternativas**: Discord Webhook ou Slack Webhook.

### 🛠️ Automação e Testes
- **Testes Manuais** → Acessar o site via navegador.
- **Simulação de Falhas** → Parar o Nginx e verificar resposta do monitoramento.

---
## ⚙️ Etapa 1: Configuração do Ambiente na AWS
### 1️⃣ Criar uma VPC com:
✅ 2 sub-redes públicas *(para acesso externo)*.  
✅ 2 sub-redes privadas *(para futuras expansões)*.  
✅ Um Internet Gateway conectado às sub-redes públicas.  

No console da AWS, acesse **VPC** > **Suas VPCs** e configure conforme indicado.

![Painel da vpc](img/painel%20da%20vpc.png)


### 🌍 Criação da Internet Gateway
1. No console da AWS, vá até **Internet Gateways**.
2. Clique em **Create Internet Gateway** e forneça um nome.
3. Após a criação, selecione o Internet Gateway.
4. Vá até **Actions** → **Attach to VPC**.
5. Associe o Internet Gateway à VPC criada.

### 2️⃣ Criação de Security Group
1. No console da AWS, vá até **EC2** > **Security Groups**.
2. Clique em **Create Security Group** e forneça um nome.
3. Configure as **Regras de Entrada (Inbound Rules)**:
   | Porta  | Protocolo | Descrição                      |
   |--------|-----------|--------------------------------|
   | 80     | HTTP      | Permitir acesso à web         |
   | 22     | SSH       | Permitir conexões remotas     |
   *🔹 Dica: Restrinja o acesso SSH ao seu IP para maior segurança.*
4. Configure as **Regras de Saída (Outbound Rules)**:
   - **All Traffic** → Permitir saída para qualquer destino (`0.0.0.0/0`).
5. Clique em **Create Security Group** para finalizar.

![Grupo de segurança](img/grupo%20de%20segurança.png)
![Grupo de segurança](img/grupo%20de%20segurança%202.png)
---
💡 *Pronto! Agora sua VPC e regras básicas de segurança estão configuradas. Vamos para a próxima etapa!* 🚀

### 3️⃣ Provisionamento da Instância EC2

#### Implantação da Instância
1. Acesse o console da AWS e vá até **EC2 > Instances**.  
2. Clique em **Launch Instances** para iniciar o provisionamento.  
3. Selecione a **Amazon Linux 2023 AMI** como sistema operacional da instância.  
4. Defina as tags necessárias e vincule a instância à **VPC configurada anteriormente**, garantindo que ela esteja em uma **sub-rede pública**.  

![Instancia](img/instancia.png)

#### Configuração de Acesso
1. **Gere e associe uma chave SSH (.pem)** para permitir conexões remotas seguras.  
2. Vincule a instância ao **Security Group definido previamente**, assegurando o controle adequado do tráfego de rede.  
3. Finalize a criação da instância clicando em **Launch Instance**.  
### 4️⃣ Conectando-se à Instância EC2 via SSH  

Após o lançamento da instância, é necessário estabelecer uma conexão SSH para realizar as configurações iniciais.  

#### Acesso pelo Visual Studio Code  
1. Acesse o **console da AWS** e vá até **EC2 > Instâncias**.  
2. Selecione a instância desejada e clique em **Connect**.  
3. Copie o comando exibido na seção **SSH Client**.  
4. No **Visual Studio Code**, abra o terminal e cole o comando copiado.  
5. Substitua `"nome_da_chave"` pelo caminho correto do arquivo `.pem`, geralmente localizado em:  
   ```bash
   C:\Users\seu_usuario\.ssh\nome_da_chave.pem

## Etapa 2: Configuração do Servidor Web (Nginx)

### 📌 1. Instalando o Nginx
Para configurar o servidor web, primeiro instale o **Nginx** utilizando o gerenciador de pacotes do **Amazon Linux**:

```bash
sudo yum install nginx -y
```

Após a instalação, verifique se o **Nginx** foi instalado corretamente:

```bash
nginx -v
```
![Versão do Servidor](img/versão%20do%20servidor.png)


---

### ⚙️ 2. Configurando o Nginx
Agora, inicie o serviço **Nginx** e configure-o para iniciar automaticamente sempre que a instância EC2 for ligada:

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```
![comando de inicio automatico](img/comando%20de%20inicio%20automatico.png)


Para garantir que o **Nginx** está em execução, verifique seu status com:

```bash
sudo systemctl status nginx
```
![status do servidor](img/status%20servidor.png)

Se tudo estiver correto, ele deve estar **ativo e rodando**. ✅

---

### 🖥️ 3. Criando uma Página Web Simples
Agora, vamos criar uma página HTML básica para testar o servidor.

Abra o arquivo de **index** no editor de texto:

```bash
sudo nano /usr/share/nginx/html/index.html
```

Edite o conteúdo conforme necessário, salve e saia do editor (**CTRL+X → Y → ENTER**).

🔗 **Dica**: A página utilizada neste projeto pode ser encontrada neste repositório.

Para testar, acesse o **IP público** da instância EC2 no navegador. Se tudo estiver certo, a página será exibida corretamente! 🎉

![pagina html](img/pagina%20html.png)

---

### 🔄 4. Configuração para Reinício Automático do Nginx
Caso o **Nginx** falhe ou pare de funcionar, podemos garantir que ele será reiniciado automaticamente.

Abra o arquivo de serviço do **Nginx**:

```bash
sudo nano /lib/systemd/system/nginx.service
```

Adicione as seguintes linhas dentro da seção `[Service]`:

```ini
Restart=always
RestartSec=30s
```

📌 **Explicação:**  
- `Restart=always`: Faz com que o **Nginx** reinicie sempre que ocorrer uma falha.
- `RestartSec=30s`: Aguarda **30 segundos** antes de tentar reiniciar.

Após adicionar as configurações, salve e saia do editor.

Para aplicar as mudanças, recarregue o **systemd**:

```bash
sudo systemctl daemon-reload
```

Agora, teste se a reinicialização automática está funcionando simulando uma falha.

![config](img/config.png)

### 1️⃣ Obtenha o **PID** (**Process ID**) do **Nginx**:

```bash
ps aux | grep nginx
```

### 2️⃣ O **PID** do processo mestre será o número exibido antes de `nginx: master process`.

Agora seu servidor **Nginx** está pronto e mais resiliente! 🚀

### 5. Simulação de Falha e Reinicialização Automática
Para testar a resiliência do Nginx, vamos simular uma falha matando o processo manualmente:

```bash
sudo kill -9 <PID>
```

> **Nota:** Substitua `<PID>` pelo ID do processo principal do Nginx.

Agora, verifique se o serviço foi reiniciado automaticamente:

```bash
sudo systemctl status nginx
```
![auto restart](img/auto%20restart.png)

Se tudo estiver correto, o systemd detectará a falha e reiniciará o Nginx automaticamente. Durante esse processo, sua página HTML ficará temporariamente fora do ar, mas assim que a reinicialização for concluída, o site voltará a funcionar normalmente.

![reinicio](img/reinicio.png)


## 🚀 Etapa 3: Monitoramento e Notificações  

### 📌 1. Criando o Script de Monitoramento  

Desenvolvemos um script em Python para verificar se o seu site está online.  
Você pode encontrar o código completo neste repositório.  

### 🛠 Como utilizar:  

### 1️⃣ Abra o terminal e crie o arquivo do script na pasta `/home/ec2-user` executando:  

```bash
sudo nano /home/ec2-user/monitoramento.py
```

### 2️⃣ Copie e cole o conteúdo do script no arquivo.
### 3️⃣ Substitua a seguinte linha pelo endereço do seu site:
```bash
url = "http://seu_site_aqui"
```
### 4️⃣ Salve o arquivo e saia do editor pressionando Ctrl + X, Y e Enter.

#### ✅ Pronto! Agora o seu script de monitoramento está configurado. 🎉

![monitoramento](img/monitoramento.png)

### 📊 2. Verificando o Funcionamento do Script  

Para garantir que o script está registrando as mensagens de disponibilidade do site corretamente, siga estes passos:  

### 1️⃣ Execute o script manualmente para testar:  

   ```bash
   python3 /home/ec2-user/monitoramento.py
   ```
### 2️⃣ Verifique o log em tempo real para acompanhar as mensagens registradas:
 ```bash
   tail -f /home/ec2-user/monitoramento.log
   ```
O script exibirá mensagens informando se o site está disponível ou indisponível, juntamente com a data e hora da verificação.

✅ Se tudo estiver funcionando corretamente, o monitoramento está ativo! 

![comando tail](img/comando%20tail.png)

### ⚙️ 3. Configuração do Script para Execução Automática  

Para que o script seja executado automaticamente a cada minuto, utilizaremos o **cron**.  

#### 📌 Instalando o Cron (caso ainda não esteja instalado)  

```bash
sudo yum install cronie -y
```
### ▶️ Iniciando e habilitando o serviço do cron
Após a instalação, inicie o serviço e configure-o para iniciar automaticamente junto com o sistema:
```bash
sudo systemctl start crond
sudo systemctl enable crond
```
### 🔎 Verificando se o serviço do cron está ativo
Para confirmar se tudo está funcionando corretamente, execute:
```bash
sudo systemctl status crond
```
Se o serviço estiver ativo, você verá uma saída indicando que o crond está em execução.

### 🕒 Agendando a execução automática do script
Agora, edite o arquivo crontab para definir a execução do script a cada minuto:
```bash
crontab -e
```
No editor aberto, adicione a seguinte linha ao final do arquivo:
```bash
* * * * * /usr/bin/python3 /home/ec2-user/monitoramento.py
```
![crontab](img/crontab.png)

Salve e feche o editor. Agora, o script será executado automaticamente a cada minuto.

Para testar, verifique os logs do script em tempo real:
```bash
tail -f /home/ec2-user/monitoramento.log
```
 - A cada minuto, um novo log será registrado, informando se o site está "disponível" ou "indisponível".
- Se quiser testar manualmente, altere o estado do Nginx entre ativo e inativo.
- Como o script roda a cada minuto, aguarde um momento para ver a atualização nos logs.
 - Se os logs estiverem sendo atualizados corretamente, a configuração foi concluída com sucesso!

### 📢 4. Envio de Notificação no Discord em Caso de Indisponibilidade  
Para receber alertas no Discord quando o site estiver indisponível, precisamos configurar um Webhook.

#### Criando um Webhook no Discord:
- Acesse o seu servidor no Discord.
- Clique no nome do servidor no topo e selecione "Configurações do servidor".
- Escolha um canal onde deseja receber as notificações e clique no ícone de configurações ⚙️ desse canal.
- Vá até a aba "Integrações" e clique em "Webhooks".
- Clique no botão "Criar Webhook".
- Defina um nome para o Webhook e copie a URL gerada.
- Agora, edite o script de monitoramento para adicionar o Webhook:
```bash
sudo nano /home/ec2-user/monitoramento.py
```
Dentro do script, encontre a variável `webhook_url` e substitua pelo seu Webhook do Discord:
webhook_url = 
```bash
"https://discord.com/api/webhooks/SEU_WEBHOOK_AQUI"
```
Salve e feche o arquivo.
![webhooks](img/webhooks.png)
#### 🚨 Com a notificação configurada, aguarde a execução do script.
Para testar, interrompa o serviço do Nginx (simulando uma falha) e veja se a notificação aparece no canal do Discord escolhido.
![teste monitor](img/teste%20monitor.png)

## Conclusão

Este projeto abordou a configuração de um servidor web utilizando Nginx na AWS, com o objetivo de automatizar o monitoramento da disponibilidade do site e implementar um sistema de alertas via Discord para notificar sobre falhas.

Ao integrar ferramentas como Amazon EC2, Amazon VPC, Nginx, Python e o cron, foi possível estabelecer um ambiente robusto e confiável para monitoramento contínuo, garantindo uma resposta rápida em caso de problemas.

Com esta abordagem, conseguimos não apenas assegurar que o servidor esteja sempre operante, mas também otimizar o processo de monitoramento e notificações, tornando-o mais eficiente e automatizado. Isso permite que as equipes responsáveis possam agir de forma proativa, minimizando o impacto de possíveis interrupções no serviço.

